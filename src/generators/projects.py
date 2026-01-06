# Projects generation module

import uuid
import random
import logging
from datetime import datetime
from config import DATASET_CONFIG, PROJECT_TYPES
from src.models.data_models import Project

logger = logging.getLogger(__name__)

class ProjectGenerator:
    """Generate realistic project data."""
    
    @staticmethod
    def generate_projects(
        organization_id: str,
        teams: list,
        num_projects: int = None
    ) -> list:
        """Generate projects across different teams."""
        if num_projects is None:
            num_projects = DATASET_CONFIG['num_projects']
        
        projects = []
        project_types = list(PROJECT_TYPES.keys())
        
        for i in range(num_projects):
            project_type = random.choice(project_types)
            type_config = PROJECT_TYPES[project_type]
            
            # Find team matching project type
            team = None
            for t in teams:
                if t.name == type_config['team']:
                    team = t
                    break
            
            project = Project(
                project_id=str(uuid.uuid4()),
                organization_id=organization_id,
                name=f"{random.choice(type_config['names'])} #{i+1}",
                created_at=datetime.now(),
                team_id=team.team_id if team else None,
                description=f"Project for {type_config['team']} team",
                color=random.choice(['#3B82F6', '#EC4899', '#8B5CF6', '#F59E0B']),
                project_type=project_type,
                status='active'
            )
            projects.append(project)
        
        logger.info(f"Generated {len(projects)} projects")
        return projects
