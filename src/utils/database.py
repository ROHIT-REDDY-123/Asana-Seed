# Database utility functions

import sqlite3
import logging
from contextlib import contextmanager
from typing import List, Dict, Any, Tuple
from config import DATABASE_PATH

logger = logging.getLogger(__name__)

class AsanaDatabase:
    """Database connection and operation handler for Asana simulation."""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            # Enable foreign keys
            self.cursor.execute('PRAGMA foreign_keys = ON')
            logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def disconnect(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    @contextmanager
    def get_cursor(self):
        """Context manager for cursor operations."""
        try:
            yield self.cursor
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            self.conn.rollback()
            raise
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a query and return cursor."""
        try:
            if params:
                return self.cursor.execute(query, params)
            else:
                return self.cursor.execute(query)
        except sqlite3.Error as e:
            logger.error(f"Query execution failed: {query} | Error: {e}")
            raise
    
    def executemany(self, query: str, params_list: List[tuple]):
        """Execute multiple queries."""
        try:
            self.cursor.executemany(query, params_list)
            logger.debug(f"Executed {len(params_list)} rows")
        except sqlite3.Error as e:
            logger.error(f"Batch execution failed: {e}")
            raise
    
    def commit(self):
        """Commit transaction."""
        try:
            self.conn.commit()
            logger.debug("Transaction committed")
        except sqlite3.Error as e:
            logger.error(f"Commit failed: {e}")
            raise
    
    def rollback(self):
        """Rollback transaction."""
        try:
            self.conn.rollback()
            logger.info("Transaction rolled back")
        except sqlite3.Error as e:
            logger.error(f"Rollback failed: {e}")
            raise
    
    def insert_organization(self, **kwargs) -> str:
        """Insert organization record."""
        query = '''
            INSERT INTO organizations 
            (organization_id, name, domain, created_at, description, employee_count, industry, website)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute(query, (
            kwargs['organization_id'],
            kwargs['name'],
            kwargs['domain'],
            kwargs['created_at'],
            kwargs.get('description'),
            kwargs.get('employee_count'),
            kwargs.get('industry'),
            kwargs.get('website'),
        ))
        return kwargs['organization_id']
    
    def insert_team(self, **kwargs) -> str:
        """Insert team record."""
        query = '''
            INSERT INTO teams (team_id, organization_id, name, description, color, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.execute(query, (
            kwargs['team_id'],
            kwargs['organization_id'],
            kwargs['name'],
            kwargs.get('description'),
            kwargs.get('color'),
            kwargs['created_at'],
        ))
        return kwargs['team_id']
    
    def insert_user(self, **kwargs) -> str:
        """Insert user record."""
        query = '''
            INSERT INTO users 
            (user_id, organization_id, name, email, first_name, last_name, 
             profile_photo_url, phone_number, timezone, role, department, created_at, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute(query, (
            kwargs['user_id'],
            kwargs['organization_id'],
            kwargs['name'],
            kwargs['email'],
            kwargs.get('first_name'),
            kwargs.get('last_name'),
            kwargs.get('profile_photo_url'),
            kwargs.get('phone_number'),
            kwargs.get('timezone', 'UTC'),
            kwargs.get('role'),
            kwargs.get('department'),
            kwargs['created_at'],
            kwargs.get('active', True),
        ))
        return kwargs['user_id']
    
    def insert_project(self, **kwargs) -> str:
        """Insert project record."""
        query = '''
            INSERT INTO projects 
            (project_id, organization_id, team_id, name, description, 
             created_at, updated_at, archived, color, project_type, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute(query, (
            kwargs['project_id'],
            kwargs['organization_id'],
            kwargs.get('team_id'),
            kwargs['name'],
            kwargs.get('description'),
            kwargs['created_at'],
            kwargs.get('updated_at'),
            kwargs.get('archived', False),
            kwargs.get('color'),
            kwargs.get('project_type'),
            kwargs.get('status', 'active'),
        ))
        return kwargs['project_id']
    
    def insert_task(self, **kwargs) -> str:
        """Insert task record."""
        query = '''
            INSERT INTO tasks 
            (task_id, project_id, section_id, name, description, 
             created_at, updated_at, due_date, start_date, completed, completed_at,
             priority, status, parent_task_id, created_by_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute(query, (
            kwargs['task_id'],
            kwargs['project_id'],
            kwargs['section_id'],
            kwargs['name'],
            kwargs.get('description'),
            kwargs['created_at'],
            kwargs.get('updated_at'),
            kwargs.get('due_date'),
            kwargs.get('start_date'),
            kwargs.get('completed', False),
            kwargs.get('completed_at'),
            kwargs.get('priority'),
            kwargs.get('status', 'not_started'),
            kwargs.get('parent_task_id'),
            kwargs.get('created_by_id'),
        ))
        return kwargs['task_id']
    
    def get_tables_row_count(self) -> Dict[str, int]:
        """Get row count for all tables."""
        tables = [
            'organizations', 'teams', 'users', 'team_memberships',
            'projects', 'sections', 'tasks', 'subtasks', 'task_assignees',
            'comments', 'custom_field_definitions', 'custom_field_values',
            'tags', 'task_tags'
        ]
        counts = {}
        for table in tables:
            try:
                count = self.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
                counts[table] = count
            except sqlite3.Error:
                counts[table] = 0
        return counts
    
    def print_summary(self):
        """Print database summary."""
        counts = self.get_tables_row_count()
        logger.info("Database Summary:")
        for table, count in counts.items():
            logger.info(f"  {table}: {count} records")
