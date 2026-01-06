# LLM client for content generation

import logging
import os
from typing import Optional
from config import LLM_CONFIG

logger = logging.getLogger(__name__)

class LLMClient:
    """Client for LLM-based content generation."""
    
    def __init__(self, provider: str = None):
        """Initialize LLM client."""
        self.provider = provider or LLM_CONFIG['provider']
        self.api_key = None
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize the appropriate LLM client."""
        if self.provider == 'google':
            try:
                import google.generativeai as genai
                api_key = os.getenv('GOOGLE_API_KEY')
                if api_key:
                    genai.configure(api_key=api_key)
                    self.client = genai
                    logger.info("Google Generative AI client initialized")
                else:
                    logger.warning("GOOGLE_API_KEY not set, LLM generation disabled")
            except ImportError:
                logger.warning("google-generativeai not installed")
        
        elif self.provider == 'openai':
            try:
                from openai import OpenAI
                api_key = os.getenv('OPENAI_API_KEY')
                if api_key:
                    self.client = OpenAI(api_key=api_key)
                    logger.info("OpenAI client initialized")
                else:
                    logger.warning("OPENAI_API_KEY not set, LLM generation disabled")
            except ImportError:
                logger.warning("openai not installed")
    
    def generate_task_name(self, project_type: str, context: str = "") -> Optional[str]:
        """Generate realistic task name using LLM."""
        if not self.client or not LLM_CONFIG['use_llm']:
            return None
        
        try:
            prompt = f"""Generate a realistic Asana task name for a {project_type} project.
Project context: {context}
Requirements:
- Keep it concise (max 10 words)
- Use action verbs
- Be specific and measurable
Just return the task name, nothing else."""
            
            if self.provider == 'google':
                response = self.client.generate_content(prompt)
                return response.text.strip()
            elif self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=50,
                    temperature=LLM_CONFIG['temperature']
                )
                return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.warning(f"LLM generation failed: {e}")
            return None
    
    def generate_task_description(self, task_name: str) -> Optional[str]:
        """Generate task description using LLM."""
        if not self.client or not LLM_CONFIG['use_llm']:
            return None
        
        try:
            prompt = f"""Write a brief task description for an Asana task.
Task: {task_name}
Requirements:
- Keep it 2-3 sentences max
- Include acceptance criteria
- Be professional
Return only the description."""
            
            if self.provider == 'google':
                response = self.client.generate_content(prompt)
                return response.text.strip()
            elif self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100,
                    temperature=LLM_CONFIG['temperature']
                )
                return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.warning(f"LLM generation failed: {e}")
            return None
    
    def generate_comment(self, task_name: str) -> Optional[str]:
        """Generate realistic task comment using LLM."""
        if not self.client or not LLM_CONFIG['use_llm']:
            return None
        
        try:
            prompt = f"""Generate a realistic Asana comment/discussion on this task:
Task: {task_name}
Requirements:
- Keep it 1-2 sentences
- Sound like a team member's comment
- Be helpful and professional
Return only the comment."""
            
            if self.provider == 'google':
                response = self.client.generate_content(prompt)
                return response.text.strip()
            elif self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100,
                    temperature=LLM_CONFIG['temperature']
                )
                return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.warning(f"LLM generation failed: {e}")
            return None
