-- =============================================================================
-- Asana Seed Data Generator - Database Schema (SQLite)
-- =============================================================================
-- This schema represents a complete Asana-like project management platform
-- with support for organizations, teams, users, projects, tasks, and more.
-- =============================================================================

-- Drop existing tables (for fresh start)
DROP TABLE IF EXISTS task_tags;
DROP TABLE IF EXISTS task_assignees;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS custom_field_values;
DROP TABLE IF EXISTS custom_field_definitions;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS subtasks;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS sections;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS team_memberships;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS organizations;

-- =============================================================================
-- ORGANIZATION / WORKSPACE
-- =============================================================================
CREATE TABLE organizations (
    organization_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL,
    description TEXT,
    employee_count INTEGER,
    industry TEXT,
    website TEXT
);

-- =============================================================================
-- TEAMS
-- =============================================================================
CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    color TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id) ON DELETE CASCADE
);

CREATE INDEX idx_teams_organization_id ON teams(organization_id);

-- =============================================================================
-- USERS
-- =============================================================================
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    first_name TEXT,
    last_name TEXT,
    profile_photo_url TEXT,
    phone_number TEXT,
    timezone TEXT DEFAULT 'UTC',
    role TEXT,  -- e.g., 'Engineer', 'Product Manager', 'Designer'
    department TEXT,
    created_at TIMESTAMP NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id) ON DELETE CASCADE
);

CREATE INDEX idx_users_organization_id ON users(organization_id);
CREATE INDEX idx_users_email ON users(email);

-- =============================================================================
-- TEAM MEMBERSHIPS
-- =============================================================================
CREATE TABLE team_memberships (
    membership_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    joined_at TIMESTAMP NOT NULL,
    role TEXT,  -- 'member', 'admin', 'lead'
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(team_id, user_id)
);

CREATE INDEX idx_team_memberships_team_id ON team_memberships(team_id);
CREATE INDEX idx_team_memberships_user_id ON team_memberships(user_id);

-- =============================================================================
-- PROJECTS
-- =============================================================================
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    team_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    archived BOOLEAN DEFAULT FALSE,
    color TEXT,
    project_type TEXT,  -- 'engineering', 'marketing', 'operations', 'product'
    status TEXT DEFAULT 'active',  -- 'active', 'on-hold', 'completed'
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL
);

CREATE INDEX idx_projects_organization_id ON projects(organization_id);
CREATE INDEX idx_projects_team_id ON projects(team_id);
CREATE INDEX idx_projects_status ON projects(status);

-- =============================================================================
-- SECTIONS (Project subdivisions: "To Do", "In Progress", "Done", etc.)
-- =============================================================================
CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    position INTEGER,  -- Order within project
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE INDEX idx_sections_project_id ON sections(project_id);
CREATE INDEX idx_sections_position ON sections(project_id, position);

-- =============================================================================
-- TASKS (Core unit of work)
-- =============================================================================
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    due_date DATE,
    start_date DATE,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    priority TEXT,  -- 'low', 'medium', 'high', 'urgent'
    status TEXT DEFAULT 'not_started',  -- 'not_started', 'in_progress', 'completed'
    parent_task_id TEXT,  -- For task hierarchy
    created_by_id TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id) ON DELETE SET NULL,
    FOREIGN KEY (created_by_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_section_id ON tasks(section_id);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
CREATE INDEX idx_tasks_parent_task_id ON tasks(parent_task_id);

-- =============================================================================
-- TASK ASSIGNEES (Many-to-many: tasks can have multiple assignees)
-- =============================================================================
CREATE TABLE task_assignees (
    assignment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    assigned_at TIMESTAMP NOT NULL,
    assigned_by_id TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by_id) REFERENCES users(user_id) ON DELETE SET NULL,
    UNIQUE(task_id, user_id)
);

CREATE INDEX idx_task_assignees_task_id ON task_assignees(task_id);
CREATE INDEX idx_task_assignees_user_id ON task_assignees(user_id);
CREATE INDEX idx_task_assignees_assigned_at ON task_assignees(assigned_at);

-- =============================================================================
-- SUBTASKS
-- =============================================================================
CREATE TABLE subtasks (
    subtask_id TEXT PRIMARY KEY,
    parent_task_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    position INTEGER,  -- Order within parent task
    assigned_to_id TEXT,
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE INDEX idx_subtasks_parent_task_id ON subtasks(parent_task_id);
CREATE INDEX idx_subtasks_assigned_to_id ON subtasks(assigned_to_id);
CREATE INDEX idx_subtasks_completed ON subtasks(completed);

-- =============================================================================
-- COMMENTS / ACTIVITY FEED
-- =============================================================================
CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    is_edited BOOLEAN DEFAULT FALSE,
    parent_comment_id TEXT,  -- For nested comments/replies
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_comment_id) REFERENCES comments(comment_id) ON DELETE SET NULL
);

CREATE INDEX idx_comments_task_id ON comments(task_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_created_at ON comments(created_at);
CREATE INDEX idx_comments_parent_comment_id ON comments(parent_comment_id);

-- =============================================================================
-- CUSTOM FIELD DEFINITIONS (Project-specific metadata)
-- =============================================================================
CREATE TABLE custom_field_definitions (
    custom_field_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    field_type TEXT NOT NULL,  -- 'text', 'number', 'dropdown', 'date', 'checkbox'
    description TEXT,
    required BOOLEAN DEFAULT FALSE,
    options TEXT,  -- JSON array of options for dropdown types
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    UNIQUE(project_id, name)
);

CREATE INDEX idx_custom_field_definitions_project_id ON custom_field_definitions(project_id);

-- =============================================================================
-- CUSTOM FIELD VALUES
-- =============================================================================
CREATE TABLE custom_field_values (
    custom_field_value_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    custom_field_id TEXT NOT NULL,
    value TEXT,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (custom_field_id) REFERENCES custom_field_definitions(custom_field_id) ON DELETE CASCADE,
    UNIQUE(task_id, custom_field_id)
);

CREATE INDEX idx_custom_field_values_task_id ON custom_field_values(task_id);
CREATE INDEX idx_custom_field_values_custom_field_id ON custom_field_values(custom_field_id);

-- =============================================================================
-- TAGS (Cross-project labels)
-- =============================================================================
CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id) ON DELETE CASCADE,
    UNIQUE(organization_id, name)
);

CREATE INDEX idx_tags_organization_id ON tags(organization_id);

-- =============================================================================
-- TASK-TAG ASSOCIATIONS (Many-to-many)
-- =============================================================================
CREATE TABLE task_tags (
    task_tag_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    added_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE,
    UNIQUE(task_id, tag_id)
);

CREATE INDEX idx_task_tags_task_id ON task_tags(task_id);
CREATE INDEX idx_task_tags_tag_id ON task_tags(tag_id);

-- =============================================================================
-- VIEWS FOR COMMON QUERIES
-- =============================================================================

-- Overview of all tasks with assignee and project info
CREATE VIEW task_overview AS
SELECT 
    t.task_id,
    t.name as task_name,
    p.name as project_name,
    sec.name as section_name,
    u.name as assignee_name,
    t.due_date,
    t.status,
    t.completed,
    t.created_at
FROM tasks t
LEFT JOIN projects p ON t.project_id = p.project_id
LEFT JOIN sections sec ON t.section_id = sec.section_id
LEFT JOIN task_assignees ta ON t.task_id = ta.task_id
LEFT JOIN users u ON ta.user_id = u.user_id;

-- Team workload analysis
CREATE VIEW team_workload AS
SELECT 
    tm.team_id,
    t.name as team_name,
    COUNT(DISTINCT ta.user_id) as num_team_members,
    COUNT(DISTINCT ta.task_id) as total_assigned_tasks,
    SUM(CASE WHEN tsk.completed = 0 THEN 1 ELSE 0 END) as open_tasks,
    SUM(CASE WHEN tsk.completed = 1 THEN 1 ELSE 0 END) as completed_tasks
FROM team_memberships tm
JOIN teams t ON tm.team_id = t.team_id
LEFT JOIN task_assignees ta ON tm.user_id = ta.user_id
LEFT JOIN tasks tsk ON ta.task_id = tsk.task_id
GROUP BY tm.team_id, t.name;

-- User productivity metrics
CREATE VIEW user_productivity AS
SELECT 
    u.user_id,
    u.name,
    COUNT(DISTINCT ta.task_id) as total_assigned_tasks,
    SUM(CASE WHEN t.completed = 1 THEN 1 ELSE 0 END) as completed_tasks,
    ROUND(
        CAST(SUM(CASE WHEN t.completed = 1 THEN 1 ELSE 0 END) AS FLOAT) / 
        NULLIF(COUNT(DISTINCT ta.task_id), 0) * 100, 2
    ) as completion_percentage,
    COUNT(DISTINCT ta.task_id) FILTER (WHERE t.due_date < DATE('now') AND t.completed = 0) as overdue_tasks
FROM users u
LEFT JOIN task_assignees ta ON u.user_id = ta.user_id
LEFT JOIN tasks t ON ta.task_id = t.task_id
GROUP BY u.user_id, u.name;

-- =============================================================================
-- CONSTRAINTS & TRIGGERS (Optional but recommended)
-- =============================================================================

-- Ensure completed_at is only set when completed = TRUE
CREATE TRIGGER validate_completed_at_on_insert
BEFORE INSERT ON tasks
WHEN NEW.completed = FALSE AND NEW.completed_at IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'completed_at can only be set when completed is TRUE');
END;

CREATE TRIGGER validate_completed_at_on_update
BEFORE UPDATE ON tasks
WHEN NEW.completed = FALSE AND NEW.completed_at IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'completed_at can only be set when completed is TRUE');
END;

-- Ensure completion timestamp is after creation timestamp
CREATE TRIGGER validate_completion_date
BEFORE INSERT ON tasks
WHEN NEW.completed_at IS NOT NULL AND NEW.completed_at < NEW.created_at
BEGIN
    SELECT RAISE(ABORT, 'completed_at cannot be before created_at');
END;

-- =============================================================================
-- SEED DATA INTEGRITY NOTES
-- =============================================================================
-- All tables should maintain referential integrity:
-- - Tasks must belong to existing projects and sections
-- - Assignments must reference existing users
-- - Comments must reference existing tasks and users
-- - Custom fields must belong to existing projects
-- - Task-tag associations must use existing tags
--
-- Temporal consistency:
-- - created_at <= updated_at
-- - created_at <= completed_at
-- - Task creation should occur before any associated comments
-- - Assignments should occur after task creation
-- =============================================================================
