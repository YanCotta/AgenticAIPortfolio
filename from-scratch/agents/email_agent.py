from .base_agent import BaseAgent

class EmailAgent(BaseAgent):
    def __init__(self):
        super().__init__("EmailAgent")

    def process(self, data):
        summary = data["summary"]
        subject = f"Summary: {data['metadata']['file_name']}"
        email_body = (
            f"Dear Team,\n\n"
            f"Here is the summary of the document '{data['metadata']['file_name']}':\n\n"
            f"{summary}\n\n"
            f"Best Regards,\nBrim AI"
        )
        return {"subject": subject, "body": email_body}
