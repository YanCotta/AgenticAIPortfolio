from crewai import Agent
from ..config.settings import OPENAI_MODEL
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class QAAgent:
    def __init__(self, company_info):
        self.company_info = company_info
        
    def create(self):
        try:
            return Agent(
                role="Quality Assurance Specialist",
                goal="Verify accuracy and completeness of support responses",
                backstory=self._generate_backstory(),
                allow_delegation=False,
                verbose=True,
                llm=OPENAI_MODEL
            )
        except Exception as e:
            logger.error(f"Error creating QA agent: {str(e)}")
            raise

    def _generate_backstory(self):
        return f"""
        As a QA specialist at {self.company_info['name']}, you ensure:
        - Technical accuracy of all responses
        - Compliance with company guidelines
        - Completeness of problem resolution
        - Professional communication standards
        """
