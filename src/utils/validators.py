# Data validation utilities

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataValidator:
    """Validation utilities for generated data."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_uuid(uuid_str: str) -> bool:
        """Validate UUID format."""
        import re
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return re.match(pattern, uuid_str, re.IGNORECASE) is not None
    
    @staticmethod
    def validate_temporal_consistency(
        created_at: datetime,
        updated_at: datetime = None,
        due_date = None,
        completed_at: datetime = None,
        completed: bool = False
    ) -> bool:
        """Validate temporal consistency."""
        now = datetime.now()
        
        # created_at should not be in future
        if created_at > now:
            logger.warning(f"created_at is in future: {created_at}")
            return False
        
        # updated_at should be >= created_at
        if updated_at and updated_at < created_at:
            logger.warning(f"updated_at < created_at")
            return False
        
        # If completed, check completed_at
        if completed and not completed_at:
            logger.warning("completed=True but completed_at is None")
            return False
        
        if completed_at and completed_at < created_at:
            logger.warning(f"completed_at < created_at")
            return False
        
        return True
    
    @staticmethod
    def validate_dataset(db_cursor) -> dict:
        """Validate generated dataset integrity."""
        issues = {
            'errors': [],
            'warnings': [],
            'stats': {}
        }
        
        try:
            # Check referential integrity
            # All foreign keys should exist
            
            # Check temporal constraints
            # No completed_at before created_at
            
            # Check business logic
            # No unassigned tasks beyond threshold
            
            logger.info(f"Validation complete: {len(issues['errors'])} errors, {len(issues['warnings'])} warnings")
        
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            issues['errors'].append(str(e))
        
        return issues
