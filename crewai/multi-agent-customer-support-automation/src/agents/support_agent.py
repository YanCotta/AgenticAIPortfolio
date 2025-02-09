from crewai import Agent
from ..config.settings import OPENAI_MODEL
from ..utils.logger import setup_logger
from ..conversation_memory import ConversationMemory

logger = setup_logger(__name__)

class SupportAgent:
    def __init__(self, company_info):
        self.company_info = company_info
        self.memory = ConversationMemory()
        
    def create(self) -> Agent:
        try:
            return Agent(
                role="Senior Support Representative",
                goal="Provide exceptional, accurate, and friendly customer support",
                backstory=self._generate_backstory(),
                allow_delegation=True,
                verbose=True,
                llm=OPENAI_MODEL,
                memory=True,
            )
        except Exception as e:
            logger.error(f"Error creating support agent: {str(e)}")
            raise

    def _generate_backstory(self) -> str:
        return f"""
        As a senior support representative at {self.company_info['name']}, 
        you excel at:
        - Deep technical understanding of our products
        - Clear and friendly communication
        - Problem-solving with creative solutions
        - Following up until issues are fully resolved
        
        You have access to our documentation at {self.company_info['docs_url']}
        and maintain our company's reputation for excellent support.
        
        Here's a summary of recent conversation history: {self.memory.get_history()}
        """
