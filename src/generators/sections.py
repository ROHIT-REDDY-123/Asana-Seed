# Sections generation module

import uuid
import logging
from datetime import datetime
from src.models.data_models import Section

logger = logging.getLogger(__name__)

class SectionGenerator:
    """Generate project sections."""
    
    SECTION_NAMES = {
        'engineering': ['Backlog', 'To Do', 'In Progress', 'In Review', 'Done'],
        'marketing': ['Planned', 'To Do', 'In Progress', 'Review', 'Published'],
        'operations': ['Queue', 'In Progress', 'Pending Approval', 'Completed'],
        'product': ['Ideation', 'Backlog', 'In Progress', 'Testing', 'Launched'],
    }
    
    @staticmethod
    def generate_sections(projects: list) -> list:
        """Generate sections for all projects."""
        sections = []
        
        for project in projects:
            project_type = project.project_type or 'product'
            section_names = SectionGenerator.SECTION_NAMES.get(project_type, ['To Do', 'In Progress', 'Done'])
            
            for position, section_name in enumerate(section_names):
                section = Section(
                    section_id=str(uuid.uuid4()),
                    project_id=project.project_id,
                    name=section_name,
                    created_at=project.created_at,
                    position=position
                )
                sections.append(section)
        
        logger.info(f"Generated {len(sections)} sections")
        return sections
