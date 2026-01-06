# Organization and team generation

import uuid
import random
import logging
from datetime import datetime
from config import DATASET_CONFIG, TEAMS
from src.models.data_models import Organization, Team, User, TeamMembership

logger = logging.getLogger(__name__)

class OrganizationGenerator:
    """Generate realistic organization data."""
    
    COMPANY_NAMES = [
        'Stripe', 'Figma', 'Vercel', 'Notion', 'Datadog', 'PagerDuty',
        'HashiCorp', 'Twilio', 'Slack', 'Shopify', 'Airbnb', 'Uber',
        'Plaid', 'TransferWise', 'Robinhood', 'Revolut', 'OpenAI', 'Anthropic',
        'Stable Diffusion', 'Hugging Face', 'Snyk', 'CloudFlare', 'Auth0',
    ]
    
    INDUSTRIES = [
        'SaaS', 'FinTech', 'Enterprise Software', 'AI/ML', 'DevTools',
        'Cloud Infrastructure', 'Productivity', 'Analytics', 'Security',
    ]
    
    @staticmethod
    def generate(org_id: str = None) -> Organization:
        """Generate single organization."""
        if org_id is None:
            org_id = str(uuid.uuid4())
        
        name = random.choice(OrganizationGenerator.COMPANY_NAMES)
        domain = name.lower().replace(' ', '') + '.com'
        
        return Organization(
            organization_id=org_id,
            name=name,
            domain=domain,
            created_at=datetime.now(),
            description=f"{name} is a leading {random.choice(OrganizationGenerator.INDUSTRIES)} company.",
            employee_count=random.randint(5000, 10000),
            industry=random.choice(OrganizationGenerator.INDUSTRIES),
            website=f"https://{domain}"
        )


class TeamGenerator:
    """Generate team data."""
    
    @staticmethod
    def generate_teams(organization_id: str) -> list:
        """Generate all teams for organization."""
        teams = []
        
        for team_config in TEAMS:
            team = Team(
                team_id=str(uuid.uuid4()),
                organization_id=organization_id,
                name=team_config['name'],
                created_at=datetime.now(),
                description=f"{team_config['name']} team responsible for core functions.",
                color=team_config.get('color', '#3B82F6')
            )
            teams.append(team)
            logger.debug(f"Generated team: {team.name}")
        
        return teams


class UserGenerator:
    """Generate realistic user data."""
    
    FIRST_NAMES = [
        'John', 'Jane', 'Michael', 'Sarah', 'David', 'Emma', 'Robert', 'Lisa',
        'James', 'Mary', 'Richard', 'Jennifer', 'Charles', 'Patricia', 'Christopher', 'Linda',
        'Daniel', 'Barbara', 'Matthew', 'Elizabeth', 'Mark', 'Susan', 'Donald', 'Jessica',
        'Steven', 'Sarah', 'Paul', 'Karen', 'Andrew', 'Nancy', 'Joshua', 'Donna',
        'Kevin', 'Carol', 'Brian', 'Pamela', 'George', 'Debra', 'Edward', 'Deborah',
        'Ronald', 'Kathleen', 'Anthony', 'Cathleen', 'Frank', 'Teresa', 'Ryan', 'Theresa',
        'Gary', 'Nora', 'Nicholas', 'Norma', 'Eric', 'Nellie', 'Jonathan', 'Naomi',
        'Stephen', 'Nicole', 'Larry', 'Nicola', 'Justin', 'Nina', 'Scott', 'Natalie',
        'Brandon', 'Natasha', 'Benjamin', 'Natalia', 'Samuel', 'Nahuatl', 'Raymond', 'Nadine',
    ]
    
    LAST_NAMES = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzales', 'Wilson', 'Anderson', 'Thomas',
        'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White',
        'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Young', 'Allen',
        'King', 'Wright', 'Scott', 'Torres', 'Peterson', 'Phillips', 'Campbell', 'Parker',
        'Evans', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris', 'Morales', 'Murphy',
        'Rogers', 'Cook', 'Morgan', 'Peterson', 'Cooper', 'Reed', 'Bell', 'Gomez',
    ]
    
    ROLES = [
        'Software Engineer', 'Senior Engineer', 'Product Manager', 'Designer',
        'Data Scientist', 'DevOps Engineer', 'QA Engineer', 'Product Owner',
        'Operations Manager', 'Marketing Manager', 'Sales Manager', 'HR Manager',
        'Business Analyst', 'Solutions Architect', 'Tech Lead', 'Scrum Master',
    ]
    
    @staticmethod
    def generate_users(
        organization_id: str,
        teams: list,
        num_users: int = None
    ) -> list:
        """Generate users and assign to teams."""
        if num_users is None:
            num_users = DATASET_CONFIG['num_users']
        
        users = []
        team_sizes = {team.team_id: 0 for team in teams}
        target_per_team = num_users // len(teams)
        
        for i in range(num_users):
            first_name = random.choice(UserGenerator.FIRST_NAMES)
            last_name = random.choice(UserGenerator.LAST_NAMES)
            
            user = User(
                user_id=str(uuid.uuid4()),
                organization_id=organization_id,
                name=f"{first_name} {last_name}",
                email=f"{first_name.lower()}.{last_name.lower()}_{i}@example.com",
                first_name=first_name,
                last_name=last_name,
                created_at=datetime.now(),
                timezone=random.choice(['UTC', 'EST', 'CST', 'PST']),
                role=random.choice(UserGenerator.ROLES),
                active=random.random() < 0.95,  # 5% inactive
            )
            users.append(user)
        
        logger.info(f"Generated {num_users} users")
        return users


class TeamMembershipGenerator:
    """Generate team membership assignments."""
    
    @staticmethod
    def generate_memberships(
        users: list,
        teams: list
    ) -> list:
        """Assign users to teams."""
        memberships = []
        team_list = list(teams)
        
        # Distribute users across teams
        for user in users:
            # Random team assignment (some users in multiple teams)
            num_teams = 1 if random.random() < 0.7 else random.randint(2, 3)
            assigned_teams = random.sample(team_list, min(num_teams, len(team_list)))
            
            for team in assigned_teams:
                membership = TeamMembership(
                    membership_id=str(uuid.uuid4()),
                    team_id=team.team_id,
                    user_id=user.user_id,
                    joined_at=datetime.now(),
                    role=random.choice(['member', 'lead']) if random.random() < 0.1 else 'member'
                )
                memberships.append(membership)
        
        logger.info(f"Generated {len(memberships)} team memberships")
        return memberships
