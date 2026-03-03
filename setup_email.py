"""
Email Configuration Setup Script
Run this to configure your email settings
"""

import os
import getpass

def setup_email_config():
    print("=" * 60)
    print("📧 Email Configuration Setup")
    print("=" * 60)
    print()
    
    print("Choose your email provider:")
    print("1. Gmail (Recommended)")
    print("2. Office 365 / Outlook")
    print("3. Yahoo Mail")
    print("4. Custom SMTP Server")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        smtp_server = "smtp.gmail.com"
        smtp_port = "587"
        print("\n📌 Gmail Setup Instructions:")
        print("1. Enable 2-Factor Authentication: https://myaccount.google.com/security")
        print("2. Generate App Password: https://myaccount.google.com/apppasswords")
        print("3. Use the 16-character App Password (not your regular password)")
        print()
    elif choice == "2":
        smtp_server = "smtp.office365.com"
        smtp_port = "587"
        print("\n📌 Office 365 Setup Instructions:")
        print("1. Go to Microsoft 365 Admin Center")
        print("2. Users → Active Users → Select your mailbox")
        print("3. Mail tab → 'Manage email apps'")
        print("4. Enable 'Authenticated SMTP (SMTP AUTH)'")
        print()
    elif choice == "3":
        smtp_server = "smtp.mail.yahoo.com"
        smtp_port = "587"
        print("\n📌 Yahoo Mail Setup Instructions:")
        print("1. Generate App Password in Yahoo Account Security")
        print("2. Use the App Password (not your regular password)")
        print()
    elif choice == "4":
        smtp_server = input("Enter SMTP server (e.g., smtp.example.com): ").strip()
        smtp_port = input("Enter SMTP port (usually 587 or 465): ").strip()
    else:
        print("❌ Invalid choice!")
        return
    
    print()
    sender_email = input("Enter your email address: ").strip()
    sender_password = getpass.getpass("Enter your password/app password: ").strip()
    
    # Create .env file
    env_content = f"""# Flask Configuration
SECRET_KEY={os.urandom(24).hex()}
FLASK_DEBUG=True

# Email Configuration
SMTP_SERVER={smtp_server}
SMTP_PORT={smtp_port}
SENDER_EMAIL={sender_email}
SENDER_PASSWORD={sender_password}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print()
    print("=" * 60)
    print("✅ Email configuration saved to .env file")
    print("=" * 60)
    print()
    print("🧪 Testing email configuration...")
    print()
    
    # Test email
    test_choice = input("Do you want to send a test email? (y/n): ").strip().lower()
    if test_choice == 'y':
        test_email = input("Enter test recipient email: ").strip()
        
        from email_sender import EmailSender
        
        email_sender = EmailSender(
            smtp_server=smtp_server,
            smtp_port=int(smtp_port),
            sender_email=sender_email,
            sender_password=sender_password
        )
        
        print(f"\n📤 Sending test email to {test_email}...")
        success = email_sender.send_email(
            recipient_email=test_email,
            name="Test User",
            role="Test Position",
            match_percentage=85.0
        )
        
        if success:
            print("✅ Test email sent successfully!")
            print(f"📬 Check {test_email} inbox")
        else:
            print("❌ Test email failed!")
            print("Check the error messages above for troubleshooting")
    
    print()
    print("=" * 60)
    print("🚀 Setup complete! You can now run: python app.py")
    print("=" * 60)

if __name__ == "__main__":
    try:
        setup_email_config()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
