from agents.doc_ingest_agent import DocumentIngestionAgent
from agents.summarizer_agent import SummarizerAgent
from agents.email_agent import EmailAgent

class TaskManager:
    def __init__(self):
        self.ingestion_agent = DocumentIngestionAgent()
        self.summarizer_agent = SummarizerAgent()
        self.email_agent = EmailAgent()

    def execute_pipeline(self, file_path):
        print("📂 Extracting document...")
        doc_data = self.ingestion_agent.process(file_path)

        print("📝 Summarizing content...")
        summary_data = self.summarizer_agent.process(doc_data)

        print("📧 Drafting email...")
        email_data = self.email_agent.process(summary_data)

        print("\n✅ Generated Email:")
        print(f"Subject: {email_data['subject']}")
        print(f"Body:\n{email_data['body']}")
