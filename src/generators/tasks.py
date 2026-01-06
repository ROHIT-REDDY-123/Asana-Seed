# Tasks generation module - CORE MODULE

import uuid
import random
import logging
from datetime import datetime
from config import DATASET_CONFIG, TASK_DISTRIBUTIONS, DEFAULT_TAGS
from src.models.data_models import Task, TaskAssignee, Comment, TaskTag
from src.utils.date_utils import DateGenerator

logger = logging.getLogger(__name__)

class TaskGenerator:
    """Generate realistic task data."""
    
    TASK_ACTIONS = {
        'engineering': [
            'Implement', 'Fix', 'Refactor', 'Optimize', 'Document',
            'Review', 'Test', 'Deploy', 'Debug', 'Design'
        ],
        'marketing': [
            'Create', 'Launch', 'Analyze', 'Plan', 'Execute',
            'Review', 'Update', 'Draft', 'Publish', 'Promote'
        ],
        'operations': [
            'Process', 'Audit', 'Plan', 'Execute', 'Report',
            'Monitor', 'Improve', 'Document', 'Schedule', 'Assign'
        ],
    }
    
    @staticmethod
    def generate_tasks(
        projects: list,
        users: list,
        sections: list
    ) -> list:
        """Generate tasks for all projects."""
        tasks = []
        num_tasks_per_project = DATASET_CONFIG['num_tasks_per_project']
        
        for project in projects:
            # Get sections for this project
            project_sections = [s for s in sections if s.project_id == project.project_id]
            
            for i in range(num_tasks_per_project):
                created_at = DateGenerator.generate_creation_timestamp()
                
                # Determine if task should be completed
                completion_rate = 0.65  # Default
                if project.project_type:
                    completion_rate = {
                        'engineering': 0.75,
                        'marketing': 0.60,
                        'operations': 0.55,
                        'product': 0.65,
                    }.get(project.project_type, 0.65)
                
                completed = random.random() < completion_rate
                completed_at = None
                if completed:
                    completed_at = DateGenerator.generate_completion_timestamp(created_at)
                
                due_date = DateGenerator.generate_due_date(created_at)
                
                task = Task(
                    task_id=str(uuid.uuid4()),
                    project_id=project.project_id,
                    section_id=random.choice(project_sections).section_id if project_sections else None,
                    name=TaskGenerator.generate_task_name(project.project_type),
                    description=TaskGenerator.generate_task_description(),
                    created_at=created_at,
                    updated_at=DateGenerator.generate_updated_at(created_at, completed_at),
                    due_date=due_date,
                    completed=completed,
                    completed_at=completed_at,
                    priority=random.choice(['low', 'medium', 'high', 'urgent']),
                    status='completed' if completed else random.choice(['not_started', 'in_progress']),
                    created_by_id=random.choice(users).user_id if users else None,
                )
                tasks.append(task)
        
        logger.info(f"Generated {len(tasks)} tasks")
        return tasks
    
    @staticmethod
    def generate_task_name(project_type: str = None) -> str:
        """Generate realistic task name based on project type."""
        if project_type == 'engineering':
            components = ['API', 'Database', 'Frontend', 'Backend', 'Cache', 'Queue']
            actions = TaskGenerator.TASK_ACTIONS['engineering']
            details = ['for performance', 'for security', 'for scalability', 'for reliability']
            return f"{random.choice(components)} - {random.choice(actions)} - {random.choice(details)}"
        
        elif project_type == 'marketing':
            campaigns = ['Q1 Campaign', 'Social Media', 'Email Marketing', 'Content']
            deliverables = ['Design', 'Copy', 'Analytics Report', 'Strategy']
            return f"{random.choice(campaigns)} - {random.choice(deliverables)}"
        
        elif project_type == 'operations':
            processes = ['Onboarding', 'Budget', 'Procurement', 'Compliance']
            actions = ['Planning', 'Review', 'Audit', 'Update']
            return f"{random.choice(processes)} - {random.choice(actions)}"
        
        else:
            # Default generic naming
            templates = ['Task for {}', '{} needs review', 'Complete {} task']
            return random.choice(templates).format(random.choice(['feature', 'bug fix', 'enhancement']))
    
    @staticmethod
    def generate_task_description() -> str:
        """Generate task description with realistic variations."""
        rand = random.random()
        
        if rand < 0.20:
            return None  # 20% no description
        
        elif rand < 0.50:
            # 30% 1-3 sentences
            sentences = [
                "This task requires implementation of the specified feature.",
                "Please complete this work according to the acceptance criteria.",
                "Review the requirements and provide updates.",
            ]
            return " ".join(random.sample(sentences, random.randint(1, 3)))
        
        else:
            # 50% detailed with bullet points
            details = [
                "Requirements:\n• Implement feature\n• Add unit tests\n• Document code",
                "Tasks:\n• Research the topic\n• Create design spec\n• Get stakeholder approval",
                "Checklist:\n- Review existing code\n- Design new approach\n- Implement solution\n- Test thoroughly",
            ]
            return random.choice(details)
    
    @staticmethod
    def generate_task_assignments(
        tasks: list,
        users: list,
        teams: list
    ) -> list:
        """Generate task assignments."""
        assignments = []
        unassigned_rate = TASK_DISTRIBUTIONS['unassigned_rate']
        
        for task in tasks:
            # 15% unassigned
            if random.random() < unassigned_rate:
                continue
            
            # Assign to random user(s)
            num_assignees = 1 if random.random() < 0.8 else random.randint(2, 3)
            assigned_users = random.sample(users, min(num_assignees, len(users)))
            
            for user in assigned_users:
                assignment = TaskAssignee(
                    assignment_id=str(uuid.uuid4()),
                    task_id=task.task_id,
                    user_id=user.user_id,
                    assigned_at=task.created_at,
                    assigned_by_id=random.choice(users).user_id if users else None,
                )
                assignments.append(assignment)
        
        logger.info(f"Generated {len(assignments)} task assignments")
        return assignments
