from crewai import Agent
from ..config.settings import OPENAI_MODEL
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class QAAgent:
    def __init__(self, company_info):
        self.company_info = company_info
        
    def create(self) -> Agent:
        try:
            return Agent(
                role="Quality Assurance Specialist",
                goal="Verify accuracy and completeness of support responses, incorporating relevance scoring and user feedback",
                backstory=self._generate_backstory(),
                allow_delegation=False,
                verbose=True,
                llm=OPENAI_MODEL,
                tools=[self.relevance_score, self.feedback_tool]
            )
        except Exception as e:
            logger.error(f"Error creating QA agent: {str(e)}")
            raise

    def _generate_backstory(self) -> str:
        return f"""
        As a QA specialist at {self.company_info['name']}, you ensure:
        - Technical accuracy of all responses
        - Compliance with company guidelines
        - Completeness of problem resolution
        - Professional communication standards
        - High relevance scores based on user needs
        - Continuous improvement through user feedback analysis
        """

    def relevance_score(self, query: str, response: str) -> int:
        # Dummy implementation for relevance scoring
        # Replace with actual relevance scoring logic
        if "implement" in query and "implement" in response:
            return 90
        else:
            return 60

    def feedback_tool(self, feedback: str) -> str:
        # Dummy implementation for feedback processing
        # Replace with actual feedback processing and retraining logic
        logger.info(f"Received feedback: {feedback}")
        return "Feedback processed. Thank you!"
