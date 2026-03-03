"""Mock email sender for testing - logs emails instead of sending"""
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockEmailSender:
    """Mock email sender that logs emails to a file instead of sending"""

    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sent_emails = []

    def send_email(self, recipient_email, name, role, match_percentage):
        """Log email instead of sending"""
        if not recipient_email or str(recipient_email).strip() in ("", "N/A"):
            logger.warning("No valid recipient email — skipping.")
            return False

        recipient_email = str(recipient_email).strip()
        
        email_record = {
            'timestamp': datetime.now().isoformat(),
            'to': recipient_email,
            'name': name,
            'role': role,
            'score': match_percentage,
            'from': self.sender_email
        }
        
        self.sent_emails.append(email_record)
        
        # Log to file
        try:
            with open('logs/emails_sent.log', 'a') as f:
                f.write(f"[{email_record['timestamp']}] To: {recipient_email} | Name: {name} | Role: {role} | Score: {match_percentage:.2f}%\n")
        except:
            pass
        
        logger.info(f"✅ Email logged (MOCK) to {recipient_email} - {name} ({role}, {match_percentage:.2f}%)")
        return True
