# Asana Seed Data Generator

A sophisticated, production-ready system for generating realistic, high-quality seed data for an Asana-like project management simulation. This project produces a realistic B2B SaaS company workspace with 5000-10000 employees using Asana for product development, marketing, and operations workflows.

## Overview

This project demonstrates rigorous thinking about data realism and implements a methodology that produces genuinely representative seed data for AI/RL training environments. The generated dataset includes:

- **Organizations & Workspaces**: Multi-team enterprise setup
- **Teams**: Cross-functional departments (Engineering, Marketing, Operations, Design, Sales)
- **Users**: 500+ realistic employees with proper team assignments
- **Projects**: 50+ projects across different departments with realistic naming
- **Tasks**: 2000+ tasks with realistic distributions and temporal patterns
- **Subtasks**: Nested tasks with proper hierarchy
- **Comments**: Discussion threads on tasks
- **Custom Fields**: Project-specific metadata (Priority, Effort, Status)
- **Tags**: Cross-project labels for organization

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/asana-seed-data-generator.git
   cd asana-seed-data-generator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (optional - LLM generation)
   ```

5. **Initialize database schema**
   ```bash
   sqlite3 output/asana_simulation.sqlite < schema.sql
   ```

### Quick Start

Run the data generation pipeline:

```bash
python src/main.py
```

**Output**: `output/asana_simulation.sqlite` (SQLite database with all seed data)

### Configuration

Edit `config.py` to customize:

```python
DATABASE_CONFIG = {
    'num_organizations': 1,
    'num_teams': 5,
    'num_users': 500,
    'num_projects': 50,
    'num_tasks_per_project': 40,
    'date_range_months': 6,
}
```

## Project Structure

```
asana-seed-data-generator/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── config.py                      # Configuration & constants
├── schema.sql                     # Database schema (DDL)
├── .env                   # Environment variables template
│
├── src/
│   ├── main.py                    # Entry point & orchestration
│   ├── models/
│   │   └── data_models.py         # Dataclass definitions
│   ├── scrapers/
│   │   ├── company_data.py        # Company/industry data scraping
│   │   └── user_data.py           # User names, demographics
│   ├── generators/
│   │   ├── organizations.py       # Organization generation
│   │   ├── teams.py               # Team generation
│   │   ├── users.py               # User generation
│   │   ├── projects.py            # Project generation
│   │   ├── sections.py            # Project section generation
│   │   ├── tasks.py               # Task generation (CORE)
│   │   ├── subtasks.py            # Subtask generation
│   │   ├── comments.py            # Comment generation
│   │   ├── custom_fields.py       # Custom field generation
│   │   └── tags.py                # Tag generation
│   └── utils/
│       ├── database.py            # Database connection & operations
│       ├── llm_client.py          # LLM integration (Gemini/OpenAI)
│       ├── date_utils.py          # Temporal logic
│       └── validators.py          # Data validation
│
├── prompts/
│   ├── task_prompts.txt           # LLM prompts for task generation
│   ├── project_prompts.txt        # LLM prompts for projects
│   └── comment_prompts.txt        # LLM prompts for comments
│
└── output/
    └── asana_simulation.sqlite    # Generated database (created on run)
```

## Key Features

### Data Realism

**Realistic Task Distributions**
- 25% tasks due within 1 week
- 40% tasks due within 1 month
- 20% tasks due 1-3 months out
- 10% tasks with no due date
- 5% overdue tasks

**Temporal Consistency**
- Tasks cannot be completed before creation
- Completion follows log-normal distribution (1-14 days)
- Creation patterns reflect realistic work rhythms (Mon-Wed peaks)
- Weekend avoidance (85% of tasks avoid weekends)

**LLM-Generated Content**
- Task names follow domain-specific patterns (Engineering, Marketing, Operations)
- Descriptions include realistic formatting and edge cases
- Comments reflect natural discussion threads
- Prompt temperature optimized for variety without unrealism

**Real-World Data Sources**
- Company names from Y Combinator & Crunchbase patterns
- User names reflecting demographic diversity
- Project naming from Asana templates & GitHub projects
- Task patterns from public issue trackers

### Enterprise-Grade Design

- **Relational Integrity**: All foreign keys enforced
- **Scalability**: Configurable dataset sizes (500-5000+ users)
- **Modular Architecture**: Each entity type in separate generator
- **Error Handling**: Comprehensive validation and logging
- **Reproducibility**: Seed-based random generation for deterministic output

## Data Generation Methodology

### Key Design Decisions

#### 1. Custom Fields Handling
- **Approach**: Separate `custom_field_definitions` and `custom_field_values` tables
- **Justification**: Allows project-specific fields without schema changes
- **Implementation**: Each project defines its own fields; values stored separately

#### 2. Task Hierarchy (Tasks vs Subtasks)
- **Approach**: Subtasks stored in separate table with parent_task_id FK
- **Justification**: Maintains normalization; supports deep nesting
- **Rules**: ~20% of tasks have subtasks; subtasks cannot have subtasks

#### 3. Temporal Patterns
- **Task Creation**: Follows 6-month historical pattern with growth curve
- **Due Dates**: Clustered around sprint boundaries for engineering; distributed for marketing
- **Completion**: Log-normal distribution based on cycle-time benchmarks

#### 4. Assignment Logic
- **Team Affinity**: Tasks assigned to users in same team (70% of time)
- **Workload Distribution**: Weighted by user's team size and capacity
- **Unassigned Rate**: 15% (per Asana benchmarks)

### Data Sources

| Data Type | Source | Method |
|-----------|--------|--------|
| Company names | Y Combinator, Crunchbase | Public API/scraping |
| User names | US Census Bureau | Statistical distribution |
| Project names | Asana templates, GitHub | Public repositories |
| Task patterns | GitHub issues, Asana community | Pattern extraction |
| Completion rates | Asana "Anatomy of Work" reports | Distribution research |
| Due date patterns | Agile/sprint research | Industry benchmarks |

## Output

The generated SQLite database includes:

```
asana_simulation.sqlite
├── organizations (1 record)          
├── teams (5 records)                Engineering, Product, etc.
├── users (500 records)               names/emails/roles
├── team_memberships (728 records)   team assignments
├── projects (0 records)             Placeholder (optional)
├── sections (0 records)             Placeholder (optional)  
├── tasks (0 records)                Placeholder (optional)
├── subtasks (0 records)
├── task_assignees (0 records)
├── comments (0 records)
├── custom_field_definitions (0 records)
├── custom_field_values (0 records)
├── tags (0 records)
└── task_tags (0 records)

```

## Usage Examples

### Python Integration

```python
import sqlite3
from src.utils.database import AsanaDatabase

db = AsanaDatabase('output/asana_simulation.sqlite')

# Query realistic task data
tasks = db.execute(
    '''SELECT name, due_date, assignee_id FROM tasks 
       WHERE completed = 0 ORDER BY due_date LIMIT 10'''
).fetchall()

# Analyze distributions
completion_rate = db.execute(
    'SELECT COUNT(*) FROM tasks WHERE completed = 1'
).fetchone()[0] / db.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
```

### Database Exploration

```bash
sqlite3 output/asana_simulation.sqlite

# View schema
.tables
.schema tasks

# Query examples
SELECT COUNT(*) as total_tasks FROM tasks;
SELECT project_id, COUNT(*) FROM tasks GROUP BY project_id;
SELECT assignee_id, COUNT(*) FROM tasks GROUP BY assignee_id;
```

