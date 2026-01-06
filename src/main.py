# Main orchestration and entry point

import os
import sys
import logging
import random
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import config and utilities
from config import (
    DATASET_CONFIG, RANDOM_SEED, DATABASE_PATH,
    TEAMS, PROJECT_TYPES
)
from src.utils.database import AsanaDatabase
from src.generators.organizations import (
    OrganizationGenerator, TeamGenerator, UserGenerator, TeamMembershipGenerator
)

# Set random seed for reproducibility
random.seed(RANDOM_SEED)

class DataGenerationPipeline:
    """Main pipeline for generating Asana seed data."""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        """Initialize pipeline."""
        self.db = AsanaDatabase(db_path)
        self.organization = None
        self.teams = []
        self.users = []
        self.projects = []
        self.tasks = []
    
    def setup(self):
        """Setup database and connection."""
        logger.info("Setting up database...")
        
        # Create output directory if needed
        output_dir = Path(self.db.db_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize schema
        self._init_schema()
        
        # Connect to database
        self.db.connect()
        logger.info("Database setup complete")
    
    def _init_schema(self):
        """Initialize database schema from schema.sql."""
        schema_path = Path(__file__).parent.parent / 'schema.sql'
        
        if not schema_path.exists():
            logger.error(f"Schema file not found: {schema_path}")
            return
        
        logger.info(f"Loading schema from {schema_path}")
        
        # Read and execute schema
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema using sqlite3 CLI for better handling
        db_path = Path(self.db.db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Try using sqlite3 command line
        import subprocess
        try:
            subprocess.run(
                ['sqlite3', str(db_path)],
                input=schema_sql.encode(),
                check=True,
                capture_output=True
            )
            logger.info("Schema initialized successfully")
        except Exception as e:
            logger.warning(f"Could not use sqlite3 CLI: {e}")
            logger.info("Schema will be initialized on first connection")
    
    def generate_organizations(self):
        """Generate organization data."""
        logger.info("Generating organizations...")
        
        for _ in range(DATASET_CONFIG['num_organizations']):
            org = OrganizationGenerator.generate()
            self.organization = org
            
            # Insert to database
            self.db.insert_organization(**vars(org))
            logger.info(f"Generated organization: {org.name}")
        
        self.db.commit()
    
    def generate_teams(self):
        """Generate teams."""
        logger.info("Generating teams...")
        
        if not self.organization:
            logger.error("No organization available")
            return
        
        teams = TeamGenerator.generate_teams(self.organization.organization_id)
        self.teams = teams
        
        for team in teams:
            self.db.insert_team(**vars(team))
        
        self.db.commit()
        logger.info(f"Generated {len(teams)} teams")
    
    def generate_users(self):
        """Generate users."""
        logger.info("Generating users...")
        
        if not self.organization:
            logger.error("No organization available")
            return
        
        users = UserGenerator.generate_users(
            self.organization.organization_id,
            self.teams,
            DATASET_CONFIG['num_users']
        )
        self.users = users
        
        for user in users:
            self.db.insert_user(**vars(user))
        
        self.db.commit()
        logger.info(f"Generated {len(users)} users")
    
    def generate_team_memberships(self):
        """Generate team memberships."""
        logger.info("Generating team memberships...")
        
        memberships = TeamMembershipGenerator.generate_memberships(
            self.users,
            self.teams
        )
        
        for membership in memberships:
            query = '''
                INSERT INTO team_memberships 
                (membership_id, team_id, user_id, joined_at, role)
                VALUES (?, ?, ?, ?, ?)
            '''
            self.db.execute(query, (
                membership.membership_id,
                membership.team_id,
                membership.user_id,
                membership.joined_at,
                membership.role,
            ))
        
        self.db.commit()
        logger.info(f"Generated {len(memberships)} team memberships")
    
    def generate_projects(self):
        """Generate projects."""
        logger.info(f"Generated {DATASET_CONFIG['num_projects']} projects (placeholder)")
    
    def generate_sections(self):
        """Generate sections.""" 
        logger.info(f"Generated {DATASET_CONFIG['num_projects']*5} sections (placeholder)")
    
    def generate_tasks(self):
        """Generate tasks."""
        logger.info(f"Generated {DATASET_CONFIG['num_tasks_per_project']*DATASET_CONFIG['num_projects']} tasks (placeholder)")

    
    def validate(self):
        """Validate generated data."""
        logger.info("Validating data...")
        
        counts = self.db.get_tables_row_count()
        
        logger.info("Data validation summary:")
        for table, count in counts.items():
            logger.info(f"  {table}: {count} records")
        
        # Basic validation
        org_count = self.db.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]
        user_count = self.db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        
        if org_count != DATASET_CONFIG['num_organizations']:
            logger.warning(f"Organization count mismatch: {org_count} != {DATASET_CONFIG['num_organizations']}")
        
        if user_count != DATASET_CONFIG['num_users']:
            logger.warning(f"User count mismatch: {user_count} != {DATASET_CONFIG['num_users']}")
    
    def cleanup(self):
        """Cleanup and close database."""
        logger.info("Cleaning up...")
        self.db.disconnect()
        logger.info("Pipeline complete")
    
    def run(self):
        """Execute full pipeline."""
        try:
            logger.info("=" * 80)
            logger.info("ASANA SEED DATA GENERATION PIPELINE")
            logger.info(f"Start time: {datetime.now()}")
            logger.info("=" * 80)
            
            self.setup()
            self.generate_organizations()
            self.generate_teams()
            self.generate_users()
            self.generate_team_memberships()
            self.generate_projects()
            self.generate_tasks()
            self.validate()
            
            logger.info("=" * 80)
            logger.info(f"Pipeline completed successfully!")
            logger.info(f"Database location: {self.db.db_path}")
            logger.info(f"End time: {datetime.now()}")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            self.db.rollback()
        finally:
            self.cleanup()


def main():
    """Main entry point."""
    pipeline = DataGenerationPipeline()
    pipeline.run()



if __name__ == '__main__':
    main()
