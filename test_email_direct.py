"""Direct email test"""
import os
from dotenv import load_dotenv
from email_sender import EmailSender
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

# Get credentials from .env
smtp_server = os.getenv('SMTP_SERVER', 'smtp.office365.com')
smtp_port = int(os.getenv('SMTP_PORT', '587'))
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')

print(f"SMTP Server: {smtp_server}")
print(f"SMTP Port: {smtp_port}")
print(f"Sender Email: {sender_email}")
print(f"Password Set: {bool(sender_password)}")
print()

# Create email sender
email_sender = EmailSender(
    smtp_server=smtp_server,
    smtp_port=smtp_port,
    sender_email=sender_email,
    sender_password=sender_password
)

# Test email
test_recipient = sender_email  # Send to yourself
print(f"Sending test email to: {test_recipient}")
print()

try:
    success = email_sender.send_email(
        recipient_email=test_recipient,
        name="Test User",
        role="Software Engineer",
        match_percentage=85.5
    )
    
    if success:
        print("✅ Email sent successfully!")
    else:
        print("❌ Email sending returned False")
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()
