# Quick stub files for remaining generators

# subtasks.py
import uuid
import random
import logging
from src.models.data_models import Subtask

logger = logging.getLogger(__name__)

class SubtaskGenerator:
    @staticmethod
    def generate_subtasks(tasks: list, probability=0.20):
        subtasks = []
        for task in tasks:
            if random.random() < probability:
                num_subtasks = random.randint(1, 4)
                for i in range(num_subtasks):
                    subtask = Subtask(
                        subtask_id=str(uuid.uuid4()),
                        parent_task_id=task.task_id,
                        name=f"Subtask {i+1} for {task.name[:20]}...",
                        created_at=task.created_at,
                        position=i,
                    )
                    subtasks.append(subtask)
        logger.info(f"Generated {len(subtasks)} subtasks")
        return subtasks

# comments.py
import uuid
import random
import logging
from datetime import timedelta
from src.models.data_models import Comment

logger = logging.getLogger(__name__)

class CommentGenerator:
    COMMENT_TEMPLATES = [
        "This looks good, let's move forward.",
        "Can you provide more details on this?",
        "I've reviewed the changes, approved.",
        "Let's schedule a sync to discuss.",
        "Great progress! Keep it up.",
        "Need clarification on requirements.",
        "Ready for testing phase.",
        "Please address the feedback.",
    ]
    
    @staticmethod
    def generate_comments(tasks: list, users: list, probability=0.50):
        comments = []
        for task in tasks:
            if random.random() < probability and users:
                num_comments = random.randint(1, 3)
                for i in range(num_comments):
                    comment_time = task.created_at + timedelta(hours=random.randint(1, 48))
                    comment = Comment(
                        comment_id=str(uuid.uuid4()),
                        task_id=task.task_id,
                        user_id=random.choice(users).user_id,
                        content=random.choice(CommentGenerator.COMMENT_TEMPLATES),
                        created_at=comment_time,
                    )
                    comments.append(comment)
        logger.info(f"Generated {len(comments)} comments")
        return comments

# custom_fields.py
import uuid
import json
import logging
from src.models.data_models import CustomFieldDefinition, CustomFieldValue

logger = logging.getLogger(__name__)

class CustomFieldGenerator:
    FIELD_TEMPLATES = {
        'engineering': [
            {'name': 'Priority', 'type': 'dropdown', 'options': ['Low', 'Medium', 'High', 'Critical']},
            {'name': 'Story Points', 'type': 'number'},
            {'name': 'Sprint', 'type': 'text'},
        ],
        'marketing': [
            {'name': 'Campaign', 'type': 'dropdown', 'options': ['Q1', 'Q2', 'Q3', 'Q4']},
            {'name': 'Budget', 'type': 'number'},
        ],
    }
    
    @staticmethod
    def generate_custom_fields(projects: list):
        definitions = []
        for project in projects:
            project_type = project.project_type or 'engineering'
            templates = CustomFieldGenerator.FIELD_TEMPLATES.get(project_type, [])
            
            for template in templates:
                field_def = CustomFieldDefinition(
                    custom_field_id=str(uuid.uuid4()),
                    project_id=project.project_id,
                    name=template['name'],
                    field_type=template['type'],
                    options=json.dumps(template.get('options', [])) if 'options' in template else None,
                    created_at=project.created_at,
                )
                definitions.append(field_def)
        
        logger.info(f"Generated {len(definitions)} custom field definitions")
        return definitions

# tags.py
import uuid
import logging
from config import DEFAULT_TAGS
from src.models.data_models import Tag, TaskTag

logger = logging.getLogger(__name__)

class TagGenerator:
    @staticmethod
    def generate_tags(organization_id: str):
        from datetime import datetime
        tags = []
        for tag_name in DEFAULT_TAGS:
            tag = Tag(
                tag_id=str(uuid.uuid4()),
                organization_id=organization_id,
                name=tag_name,
                created_at=datetime.now(),
            )
            tags.append(tag)
        logger.info(f"Generated {len(tags)} tags")
        return tags
    
    @staticmethod
    def generate_task_tags(tasks: list, tags: list):
        import random
        task_tags = []
        for task in tasks:
            if random.random() < 0.40 and tags:  # 40% of tasks get tags
                num_tags = random.randint(1, 3)
                assigned_tags = random.sample(tags, min(num_tags, len(tags)))
                for tag in assigned_tags:
                    task_tag = TaskTag(
                        task_tag_id=str(uuid.uuid4()),
                        task_id=task.task_id,
                        tag_id=tag.tag_id,
                        added_at=task.created_at,
                    )
                    task_tags.append(task_tag)
        logger.info(f"Generated {len(task_tags)} task-tag associations")
        return task_tags
