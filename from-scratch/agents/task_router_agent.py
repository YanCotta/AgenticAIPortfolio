from agents.base_agent import BaseAgent
from agents.doc_ingest_agent import DocumentIngestionAgent
from agents.summarizer_agent import SummarizerAgent
from agents.email_agent import EmailAgent
import asyncio

class TaskRouterAgent(BaseAgent):
    def __init__(self):
        super().__init__("TaskRouterAgent")
        self.doc_agent = DocumentIngestionAgent()
        self.summarizer = SummarizerAgent()
        self.email_agent = EmailAgent()

    async def process(self, file_path):
        try:
            # Ingest document
            doc_result = self.doc_agent.execute(file_path)
            if not doc_result:
                self.logger.error("Document ingestion failed.")
                return None

            # Generate summary asynchronously
            summary_result = await self.summarizer.process(doc_result)
            if not summary_result:
                self.logger.error("Summarization failed.")
                return None

            # Merge metadata from ingestion into summary data
            summary_result["metadata"] = doc_result.get("metadata", {})

            # If metadata provides a recipient email, send an email
            recipient = summary_result["metadata"].get("recipient")
            email_result = None
            if recipient:
                email_result = self.email_agent.process(summary_result)

            # Return combined results
            return {
                "document": doc_result,
                "summary": summary_result,
                "email": email_result
            }
        except Exception as e:
            self.logger.error(f"Task routing failed: {str(e)}")
            return None

    # Synchronous wrapper for compatibility
    def process_sync(self, file_path):
        return asyncio.run(self.process(file_path))
