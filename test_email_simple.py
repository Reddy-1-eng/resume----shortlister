"""
Simple Email Test Script
Run this to quickly test if your email configuration works
"""

import os
import sys

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded .env file")
except ImportError:
    print("⚠️  Installing python-dotenv...")
    os.system("pip install python-dotenv")
    from dotenv import load_dotenv
    load_dotenv()

from email_sender import EmailSender

def test_email():
    print("\n" + "="*60)
    print("📧 Email Configuration Test")
    print("="*60 + "\n")
    
    # Get configuration
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL', '')
    sender_password = os.getenv('SENDER_PASSWORD', '')
    
    print(f"SMTP Server: {smtp_server}")
    print(f"SMTP Port: {smtp_port}")
    print(f"Sender Email: {sender_email}")
    print(f"Password: {'*' * len(sender_password) if sender_password else '(not set)'}")
    print()
    
    # Check if credentials are set
    if not sender_email or sender_email == 'your-email@gmail.com':
        print("❌ ERROR: Email credentials not configured!")
        print()
        print("Please run: python setup_email.py")
        print("Or manually create a .env file with your credentials")
        print()
        print("See EMAIL_SETUP_GUIDE.md for detailed instructions")
        return False
    
    # Get test recipient
    test_recipient = input("Enter test recipient email address: ").strip()
    
    if not test_recipient or '@' not in test_recipient:
        print("❌ Invalid email address!")
        return False
    
    print(f"\n📤 Sending test email to: {test_recipient}")
    print("Please wait...\n")
    
    # Initialize email sender
    email_sender = EmailSender(
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        sender_email=sender_email,
        sender_password=sender_password
    )
    
    # Send test email
    try:
        success = email_sender.send_email(
            recipient_email=test_recipient,
            name="Test User",
            role="Software Engineer",
            match_percentage=85.5
        )
        
        print()
        print("="*60)
        if success:
            print("✅ SUCCESS! Test email sent successfully!")
            print(f"📬 Check the inbox of: {test_recipient}")
            print("="*60)
            return True
        else:
            print("❌ FAILED! Email was not sent.")
            print("Check the error messages above for details.")
            print("="*60)
            print("\n💡 Common Solutions:")
            print("  • Gmail: Use App Password (not regular password)")
            print("  • Office 365: Enable SMTP AUTH in admin center")
            print("  • Check firewall/antivirus settings")
            print("  • Verify credentials in .env file")
            print("\nSee EMAIL_SETUP_GUIDE.md for detailed help")
            return False
            
    except Exception as e:
        print()
        print("="*60)
        print(f"❌ ERROR: {e}")
        print("="*60)
        print("\n💡 Troubleshooting:")
        print("  1. Check your .env file exists and has correct values")
        print("  2. Verify email and password are correct")
        print("  3. For Gmail, use App Password (not regular password)")
        print("  4. Check internet connection")
        print("\nRun: python setup_email.py for guided setup")
        return False

if __name__ == "__main__":
    try:
        test_email()
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
