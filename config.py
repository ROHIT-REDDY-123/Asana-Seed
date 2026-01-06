# Configuration constants and parameters

# Database configuration
DATABASE_PATH = 'output/asana_simulation.sqlite'

# Dataset sizing
DATASET_CONFIG = {
    'num_organizations': 1,
    'num_teams': 5,
    'num_users': 500,
    'num_projects': 50,
    'num_tasks_per_project': 40,  # Total tasks ≈ 2000
    'num_comments_per_task': 0.5,  # Average comments per task
    'date_range_months': 6,
}

# Team definitions
TEAMS = [
    {'name': 'Engineering', 'color': '#1F2937'},
    {'name': 'Product', 'color': '#3B82F6'},
    {'name': 'Marketing', 'color': '#EC4899'},
    {'name': 'Operations', 'color': '#F59E0B'},
    {'name': 'Design', 'color': '#8B5CF6'},
]

# Project types and their characteristics
PROJECT_TYPES = {
    'engineering': {
        'names': ['Backend API', 'Frontend Dashboard', 'Mobile App', 'Infrastructure', 'DevOps', 'Data Pipeline'],
        'team': 'Engineering',
        'completion_rate': 0.75,
        'task_name_template': '[Component] - [Action] - [Detail]',
    },
    'marketing': {
        'names': ['Q1 Campaign', 'Social Media', 'Content Calendar', 'Product Launch', 'SEO Strategy'],
        'team': 'Marketing',
        'completion_rate': 0.60,
        'task_name_template': '[Campaign] - [Deliverable]',
    },
    'operations': {
        'names': ['Budget Planning', 'Process Improvement', 'HR Onboarding', 'Finance Audit'],
        'team': 'Operations',
        'completion_rate': 0.55,
        'task_name_template': '[Process] - [Action]',
    },
    'product': {
        'names': ['Feature Request', 'User Research', 'Roadmap Planning', 'Analytics'],
        'team': 'Product',
        'completion_rate': 0.65,
        'task_name_template': '[Feature] - [Activity]',
    },
}

# LLM Configuration
LLM_CONFIG = {
    'provider': 'google',  # 'google' or 'openai'
    'temperature': 0.7,  # For variety with consistency
    'max_tokens': 150,
    'use_llm': True,  # Set to False for template-based generation
}

# Task distribution parameters (based on Asana benchmarks)
TASK_DISTRIBUTIONS = {
    'due_date': {
        'within_1_week': 0.25,
        'within_1_month': 0.40,
        'within_3_months': 0.20,
        'no_due_date': 0.10,
        'overdue': 0.05,
    },
    'weekend_avoidance': 0.85,
    'unassigned_rate': 0.15,
    'completion_time_mean_days': 5.0,  # Log-normal mean
    'completion_time_std_days': 3.0,   # Log-normal std
}

# Custom field types
CUSTOM_FIELD_TYPES = {
    'engineering': ['Priority', 'Story Points', 'Sprint', 'Status'],
    'marketing': ['Campaign', 'Channel', 'Budget', 'Status'],
    'operations': ['Department', 'Budget Category', 'Status'],
    'product': ['Feature Area', 'Impact', 'Effort', 'Status'],
}

# Comment generation probability
COMMENT_PROBABILITY = 0.50  # 50% of tasks have comments

# Subtask probability
SUBTASK_PROBABILITY = 0.20  # 20% of tasks have subtasks
MAX_SUBTASKS_PER_TASK = 4

# Attachment probability
ATTACHMENT_PROBABILITY = 0.30

# Tag definitions
DEFAULT_TAGS = [
    'bug', 'feature', 'enhancement', 'documentation',
    'high-priority', 'low-priority', 'urgent', 'blocked',
    'review', 'testing', 'deployment', 'research',
    'design', 'backend', 'frontend', 'database',
]

# Date/Time patterns
WORKDAYS = [0, 1, 2, 3, 4]  # Monday to Friday
PEAK_CREATION_DAYS = [0, 1, 2]  # Mon, Tue, Wed

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Seed for reproducibility
RANDOM_SEED = 42
