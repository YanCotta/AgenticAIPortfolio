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
        self.max_attempts = 3  # Maximum attempts before escalation
        self.confidence_threshold = 70  # Minimum confidence level before escalation

    def handle_inquiry(self, customer_info: Dict[str, Any], inquiry: str) -> Dict[str, Any]:
        attempts = 0
        while attempts < self.max_attempts:
            try:
                tasks = self._create_support_tasks(customer_info, inquiry)
                crew = Crew(
                    agents=[self.support_agent, self.qa_agent],
                    tasks=tasks,
                    verbose=2,
                    memory=True
                )
                logger.info(f"Initiating CrewAI for handling inquiry (Attempt {attempts + 1}).")
                result = crew.kickoff()

                # Check confidence level (assuming result contains a confidence score)
                if result.get("confidence_score", 0) >= self.confidence_threshold:
                    return result
                else:
                    logger.warning(f"Low confidence score: {result.get('confidence_score', 0)}. Retrying...")
                    attempts += 1

            except Exception as e:
                logger.error(f"Error handling inquiry: {str(e)}")
                attempts += 1

        # Escalation logic
        logger.warning("Escalating to human operator or advanced QA pipeline.")
        return self._escalate_inquiry(customer_info, inquiry)

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

    def _escalate_inquiry(self, customer_info: Dict[str, Any], inquiry: str) -> Dict[str, Any]:
        # Placeholder for escalation logic
        logger.info(f"Escalating inquiry from {customer_info['name']}: {inquiry}")
        return {"status": "escalated", "message": "Inquiry has been escalated to a human operator."}

if __name__ == "__main__":
    support_system = CustomerSupportSystem()
    result = support_system.handle_inquiry(
        customer_info={"name": "Test Customer"},
        inquiry="How do I implement memory in CrewAI?"
    )
    print(result)
