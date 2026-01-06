# Date and time generation utilities

import random
import logging
from datetime import datetime, timedelta, date
from numpy.random import lognormal
from config import TASK_DISTRIBUTIONS, WORKDAYS, PEAK_CREATION_DAYS

logger = logging.getLogger(__name__)

class DateGenerator:
    """Generate realistic date/time values for task management."""
    
    @staticmethod
    def get_base_date():
        """Get base date (6 months ago from now)."""
        return datetime.now() - timedelta(days=180)
    
    @staticmethod
    def generate_creation_timestamp(base_date=None) -> datetime:
        """
        Generate realistic task creation timestamp.
        
        Patterns:
        - Higher creation rates Mon-Wed (peak_creation_days)
        - Lower creation rates Thu-Fri
        - Distributed over last 6 months
        - Follows realistic growth curve
        """
        if base_date is None:
            base_date = DateGenerator.get_base_date()
        
        # Random number of days from base date to now
        now = datetime.now()
        days_delta = (now - base_date).days
        random_days = random.randint(0, days_delta)
        
        # Create timestamp
        creation_date = base_date + timedelta(days=random_days)
        
        # Add time component (weighted toward peak creation days)
        weekday = creation_date.weekday()
        if weekday not in PEAK_CREATION_DAYS:
            # Lower probability for Thu-Fri, but still possible
            if random.random() < 0.3:
                # Skip this one and try again
                return DateGenerator.generate_creation_timestamp(base_date)
        
        # Add random time
        hour = random.randint(8, 18)  # Business hours
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        creation_date = creation_date.replace(hour=hour, minute=minute, second=second)
        return creation_date
    
    @staticmethod
    def generate_due_date(created_at: datetime) -> date:
        """
        Generate realistic due date distribution.
        
        Distribution (based on Asana research):
        - 25% within 1 week (1-7 days)
        - 40% within 1 month (8-30 days)
        - 20% within 3 months (31-90 days)
        - 10% no due date (None)
        - 5% overdue (before creation)
        
        Avoidance of weekends: 85% of tasks
        Clustering around sprint boundaries for engineering
        """
        rand = random.random()
        
        # 10% no due date
        if rand < 0.10:
            return None
        
        # Determine days in future
        elif rand < 0.35:  # 25% within 1 week
            days_out = random.randint(1, 7)
        elif rand < 0.75:  # 40% within 1 month
            days_out = random.randint(8, 30)
        elif rand < 0.95:  # 20% within 3 months
            days_out = random.randint(31, 90)
        else:  # 5% overdue
            days_out = random.randint(-30, -1)
        
        due_date = created_at + timedelta(days=days_out)
        due_date = due_date.date()
        
        # 85% avoid weekends
        if random.random() < 0.85:
            # Adjust to next workday if weekend
            while due_date.weekday() > 4:  # 5 = Saturday
                due_date = due_date + timedelta(days=1)
        
        return due_date
    
    @staticmethod
    def generate_completion_timestamp(
        created_at: datetime,
        due_date: date = None
    ) -> datetime:
        """
        Generate realistic completion timestamp.
        
        Rules:
        - Cannot be before creation
        - Follows log-normal distribution (mean ~5 days)
        - Always after creation
        - Never in future
        - Respects due date if present
        """
        # Generate days-to-completion from log-normal
        mean = TASK_DISTRIBUTIONS['completion_time_mean_days']
        std = TASK_DISTRIBUTIONS['completion_time_std_days']
        
        # Convert to log-normal parameters
        # lognormal takes mu and sigma (log-space)
        mu = (mean ** 2) / ((std ** 2 + mean ** 2) ** 0.5)
        sigma = ((std ** 2) / (mean ** 2) + 1) ** 0.5
        
        days_to_complete = max(1, int(lognormal(mu, sigma)))
        
        # Completion is 1-14 days after creation
        days_to_complete = min(days_to_complete, 14)
        
        completion_at = created_at + timedelta(days=days_to_complete)
        
        # Never complete in the future
        now = datetime.now()
        if completion_at > now:
            completion_at = now - timedelta(hours=1)
        
        # If due date exists, try to respect it
        if due_date and completion_at.date() > due_date:
            # 70% of tasks complete before due date
            if random.random() < 0.70:
                days_before_due = random.randint(0, 3)
                completion_at = datetime.combine(
                    due_date - timedelta(days=days_before_due),
                    datetime.min.time()
                ) + timedelta(hours=random.randint(8, 18))
        
        return completion_at
    
    @staticmethod
    def generate_updated_at(created_at: datetime, completed_at: datetime = None) -> datetime:
        """
        Generate update timestamp.
        Usually last updated is around creation or completion.
        """
        if completed_at and random.random() < 0.7:
            # Often last updated at completion
            return completed_at
        else:
            # Or shortly after creation
            return created_at + timedelta(hours=random.randint(1, 24))
    
    @staticmethod
    def validate_temporal_consistency(
        created_at: datetime,
        updated_at: datetime = None,
        due_date: date = None,
        completed_at: datetime = None,
        completed: bool = False
    ) -> bool:
        """
        Validate temporal consistency of task dates.
        
        Rules:
        - created_at must be earliest
        - updated_at >= created_at
        - due_date should be >= created_at.date()
        - If completed=True, completed_at must exist and be >= created_at
        - completed_at <= now
        """
        now = datetime.now()
        
        # Check created_at is not in future
        if created_at > now:
            logger.warning(f"created_at is in future: {created_at}")
            return False
        
        # Check updated_at >= created_at
        if updated_at and updated_at < created_at:
            logger.warning(f"updated_at ({updated_at}) < created_at ({created_at})")
            return False
        
        # Check due_date >= created_at
        if due_date and due_date < created_at.date():
            logger.warning(f"due_date ({due_date}) < created_at.date ({created_at.date()})")
            return False
        
        # Check completed_at validity
        if completed:
            if not completed_at:
                logger.warning("completed=True but completed_at is None")
                return False
            if completed_at < created_at:
                logger.warning(f"completed_at ({completed_at}) < created_at ({created_at})")
                return False
            if completed_at > now:
                logger.warning(f"completed_at ({completed_at}) is in future")
                return False
        
        return True
    
    @staticmethod
    def get_sprint_boundary_dates() -> list:
        """
        Get sprint boundary dates (2-week sprints, starting on Mondays).
        Useful for clustering engineering task due dates.
        """
        base_date = DateGenerator.get_base_date()
        boundaries = []
        current = base_date
        end = datetime.now()
        
        while current < end:
            # Move to next Monday if not already
            if current.weekday() != 0:
                current = current + timedelta(days=7 - current.weekday())
            boundaries.append(current.date())
            current = current + timedelta(days=14)  # 2-week sprints
        
        return boundaries
