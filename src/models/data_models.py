# Data model definitions

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List

@dataclass
class Organization:
    """Organization/Workspace model."""
    organization_id: str
    name: str
    domain: str
    created_at: datetime
    description: Optional[str] = None
    employee_count: Optional[int] = None
    industry: Optional[str] = None
    website: Optional[str] = None

@dataclass
class Team:
    """Team model."""
    team_id: str
    organization_id: str
    name: str
    created_at: datetime
    description: Optional[str] = None
    color: Optional[str] = None

@dataclass
class User:
    """User model."""
    user_id: str
    organization_id: str
    name: str
    email: str
    created_at: datetime
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_photo_url: Optional[str] = None
    phone_number: Optional[str] = None
    timezone: str = 'UTC'
    role: Optional[str] = None
    department: Optional[str] = None
    active: bool = True

@dataclass
class TeamMembership:
    """Team membership model."""
    membership_id: str
    team_id: str
    user_id: str
    joined_at: datetime
    role: Optional[str] = None

@dataclass
class Project:
    """Project model."""
    project_id: str
    organization_id: str
    name: str
    created_at: datetime
    team_id: Optional[str] = None
    description: Optional[str] = None
    updated_at: Optional[datetime] = None
    archived: bool = False
    color: Optional[str] = None
    project_type: Optional[str] = None
    status: str = 'active'

@dataclass
class Section:
    """Project section model."""
    section_id: str
    project_id: str
    name: str
    created_at: datetime
    description: Optional[str] = None
    position: int = 0

@dataclass
class Task:
    """Task model."""
    task_id: str
    project_id: str
    section_id: str
    name: str
    created_at: datetime
    description: Optional[str] = None
    updated_at: Optional[datetime] = None
    due_date: Optional[date] = None
    start_date: Optional[date] = None
    completed: bool = False
    completed_at: Optional[datetime] = None
    priority: Optional[str] = None
    status: str = 'not_started'
    parent_task_id: Optional[str] = None
    created_by_id: Optional[str] = None

@dataclass
class TaskAssignee:
    """Task assignee model."""
    assignment_id: str
    task_id: str
    user_id: str
    assigned_at: datetime
    assigned_by_id: Optional[str] = None

@dataclass
class Subtask:
    """Subtask model."""
    subtask_id: str
    parent_task_id: str
    name: str
    created_at: datetime
    description: Optional[str] = None
    completed: bool = False
    completed_at: Optional[datetime] = None
    position: int = 0
    assigned_to_id: Optional[str] = None

@dataclass
class Comment:
    """Comment model."""
    comment_id: str
    task_id: str
    user_id: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_edited: bool = False
    parent_comment_id: Optional[str] = None

@dataclass
class CustomFieldDefinition:
    """Custom field definition model."""
    custom_field_id: str
    project_id: str
    name: str
    field_type: str  # 'text', 'number', 'dropdown', 'date', 'checkbox'
    created_at: datetime
    description: Optional[str] = None
    required: bool = False
    options: Optional[str] = None  # JSON for dropdown

@dataclass
class CustomFieldValue:
    """Custom field value model."""
    custom_field_value_id: str
    task_id: str
    custom_field_id: str
    value: str
    updated_at: datetime

@dataclass
class Tag:
    """Tag model."""
    tag_id: str
    organization_id: str
    name: str
    created_at: datetime
    color: Optional[str] = None

@dataclass
class TaskTag:
    """Task-tag association model."""
    task_tag_id: str
    task_id: str
    tag_id: str
    added_at: datetime
