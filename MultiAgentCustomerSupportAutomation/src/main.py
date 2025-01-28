from agents.support_agent import SupportAgent
from agents.qa_agent import QAAgent
from tools.scraping import DocumentScraper
from config.settings import COMPANY_INFO
from utils.logger import setup_logger
from crewai import Crew, Task
from typing import Dict, Any

logger = setup_logger(__name__)

class CustomerSupportSystem:
    def __init__(self):
        self.support_agent = SupportAgent(COMPANY_INFO).create()
        self.qa_agent = QAAgent(COMPANY_INFO).create()
        self.docs_scraper = DocumentScraper()

    def handle_inquiry(self, customer_info: Dict[str, Any], inquiry: str) -> Dict[str, Any]:
        try:
            tasks = self._create_support_tasks(customer_info, inquiry)
            crew = Crew(
                agents=[self.support_agent, self.qa_agent],
                tasks=tasks,
                verbose=2,
                memory=True
            )
            logger.info("Initiating CrewAI for handling inquiry.")
            return crew.kickoff()
        except Exception as e:
            logger.error(f"Error handling inquiry: {str(e)}")
            return {"error": "Failed to process inquiry", "details": str(e)}

    def _create_support_tasks(self, customer_info: Dict[str, Any], inquiry: str) -> list:
        # Task creation logic here
        return [
            Task(
                description=self._format_inquiry_task(customer_info, inquiry),
                agent=self.support_agent,
                tools=[self.docs_scraper]
            ),
            # Additional tasks...
        ]

    @staticmethod
    def _format_inquiry_task(customer_info: Dict[str, Any], inquiry: str) -> str:
        return f"""
        Priority customer inquiry from {customer_info['name']}:
        {inquiry}
        
        Requirements:
        - Provide detailed, accurate response
        - Include relevant documentation references
        - Maintain professional yet friendly tone
        - Ensure complete problem resolution
        """

if __name__ == "__main__":
    support_system = CustomerSupportSystem()
    result = support_system.handle_inquiry(
        customer_info={"name": "Test Customer"},
        inquiry="How do I implement memory in CrewAI?"
    )
    print(result)
