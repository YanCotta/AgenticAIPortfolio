import re
from .base_agent import BaseAgent

class EmailAgent(BaseAgent):
    def __init__(self):
        super().__init__("EmailAgent")
        self.signature = "Best Regards,\nBrim AI"  # customizable signature

    def tone_analysis(self, text):
        # Simple tone analysis: returns "urgent" if urgency keywords found, else "normal"
        urgency_keywords = ["urgent", "immediately", "asap", "now"]
        if any(word in text.lower() for word in urgency_keywords):
            return "urgent"
        return "normal"

    def validate_email(self, email):
        # Basic email validation regex
        pattern = r"(^[\w\.-]+@[\w\.-]+\.\w+$)"
        return re.match(pattern, email) is not None

    def process(self, data):
        summary = data["summary"]
        metadata = data.get("metadata", {})
        recipient = metadata.get("recipient", "")
        file_name = metadata.get("file_name", "Document")
        attachments = data.get("attachments", [])

        # Validate recipient email
        if not self.validate_email(recipient):
            self.logger.error("Invalid recipient email address.")
            return None

        # Tone analysis and adjust subject if urgent
        tone = self.tone_analysis(summary)
        subject_prefix = "[URGENT] " if tone == "urgent" else ""
        subject = f"{subject_prefix}Summary: {file_name}"

        # Select email template based on HTML flag
        if data.get("html", False):
            email_body = (
                f"<html><body>"
                f"<p>Dear Team,</p>"
                f"<p>Here is the summary of the document <strong>{file_name}</strong>:</p>"
                f"<p>{summary}</p>"
                f"<p>{self.signature.replace(chr(10), '<br>')}</p>"
                f"</body></html>"
            )
        else:
            email_body = (
                f"Dear Team,\n\n"
                f"Here is the summary of the document '{file_name}':\n\n"
                f"{summary}\n\n"
                f"{self.signature}"
            )
        
        return {
            "subject": subject,
            "body": email_body,
            "attachments": attachments  # includes attachments if any
        }
