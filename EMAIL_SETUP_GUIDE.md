# 📧 Email Setup Guide

## Quick Setup (Recommended)

Run the setup script:
```bash
python setup_email.py
```

This will guide you through configuring your email settings.

---

## Manual Setup

### Step 1: Install Dependencies
```bash
pip install python-dotenv
```

### Step 2: Create `.env` File

Create a file named `.env` in the project root with your email credentials:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

---

## Email Provider Setup Instructions

### 🔵 Gmail (Recommended)

1. **Enable 2-Factor Authentication**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password

3. **Configure .env**
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=xxxx-xxxx-xxxx-xxxx
   ```

### 🔷 Office 365 / Outlook

1. **Enable SMTP Authentication**
   - Go to Microsoft 365 Admin Center
   - Users → Active Users → Select your mailbox
   - Mail tab → "Manage email apps"
   - Enable "Authenticated SMTP (SMTP AUTH)"

2. **Configure .env**
   ```env
   SMTP_SERVER=smtp.office365.com
   SMTP_PORT=587
   SENDER_EMAIL=your-email@outlook.com
   SENDER_PASSWORD=your-password
   ```

### 🟣 Yahoo Mail

1. **Generate App Password**
   - Go to Yahoo Account Security
   - Generate App Password for "Mail"

2. **Configure .env**
   ```env
   SMTP_SERVER=smtp.mail.yahoo.com
   SMTP_PORT=587
   SENDER_EMAIL=your-email@yahoo.com
   SENDER_PASSWORD=your-app-password
   ```

---

## Testing Your Configuration

### Method 1: Using Setup Script
```bash
python setup_email.py
```
Follow the prompts to test email sending.

### Method 2: Using Python
```python
from email_sender import EmailSender
import os
from dotenv import load_dotenv

load_dotenv()

email_sender = EmailSender(
    smtp_server=os.getenv('SMTP_SERVER'),
    smtp_port=int(os.getenv('SMTP_PORT')),
    sender_email=os.getenv('SENDER_EMAIL'),
    sender_password=os.getenv('SENDER_PASSWORD')
)

success = email_sender.send_email(
    recipient_email="test@example.com",
    name="Test User",
    role="Test Role",
    match_percentage=85.0
)

print("✅ Success!" if success else "❌ Failed!")
```

### Method 3: Using Web Interface
1. Start the application: `python app.py`
2. Open browser: http://localhost:5000
3. Use the "Test Email" feature in the UI

---

## Common Issues & Solutions

### ❌ Authentication Failed

**Problem:** `SMTPAuthenticationError: Username and Password not accepted`

**Solutions:**
- **Gmail:** Use App Password, not regular password
- **Office 365:** Enable SMTP AUTH in admin center
- **Yahoo:** Use App Password
- Check email and password are correct
- Ensure no extra spaces in credentials

### ❌ Connection Timeout

**Problem:** `TimeoutError: Connection timed out`

**Solutions:**
- Check firewall settings
- Verify SMTP server and port
- Try port 465 (SSL) instead of 587 (TLS)
- Check internet connection

### ❌ Recipient Refused

**Problem:** `SMTPRecipientsRefused: Recipient address rejected`

**Solutions:**
- Verify recipient email is valid
- Check for typos in email address
- Ensure email domain exists

### ❌ SSL/TLS Errors

**Problem:** SSL certificate verification failed

**Solutions:**
- Update Python SSL certificates
- Try different port (587 vs 465)
- Check system date/time is correct

---

## Security Best Practices

1. **Never commit .env file to Git**
   - Already in .gitignore
   - Use .env.example for templates

2. **Use App Passwords**
   - Never use your main account password
   - Generate app-specific passwords

3. **Rotate Credentials**
   - Change passwords regularly
   - Revoke unused app passwords

4. **Limit Permissions**
   - Use dedicated email account for sending
   - Don't use personal email for production

---

## Troubleshooting Checklist

- [ ] .env file exists in project root
- [ ] python-dotenv is installed
- [ ] Email credentials are correct
- [ ] No extra spaces in .env values
- [ ] 2FA enabled (for Gmail)
- [ ] App Password generated (for Gmail/Yahoo)
- [ ] SMTP AUTH enabled (for Office 365)
- [ ] Firewall allows SMTP connections
- [ ] Internet connection is working
- [ ] Tested with setup_email.py script

---

## Getting Help

If you're still having issues:

1. Check the logs in `logs/app.log`
2. Run with debug mode: `FLASK_DEBUG=True python app.py`
3. Look for detailed error messages in console
4. Verify email provider's SMTP documentation

---

## Example Working Configurations

### Gmail
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=myapp@gmail.com
SENDER_PASSWORD=abcd-efgh-ijkl-mnop
```

### Office 365
```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SENDER_EMAIL=myapp@company.com
SENDER_PASSWORD=MySecurePassword123!
```

### Custom Domain (Google Workspace)
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=noreply@mycompany.com
SENDER_PASSWORD=abcd-efgh-ijkl-mnop
```
