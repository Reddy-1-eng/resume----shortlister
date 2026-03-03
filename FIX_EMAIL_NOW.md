# 🔧 Fix Email Sending - Quick Guide

## The Problem
Emails show as "sent" but recipients don't receive them. This is due to incorrect email configuration.

## The Solution (3 Steps)

### Step 1: Run Setup Script
```bash
python setup_email.py
```

Follow the prompts to configure your email. Choose Gmail for easiest setup.

### Step 2: Test Email
```bash
python test_email_simple.py
```

Enter a test email address to verify it works.

### Step 3: Run Application
```bash
python app.py
```

Your emails will now be sent successfully!

---

## Quick Gmail Setup (Recommended)

### 1. Enable 2-Factor Authentication
- Go to: https://myaccount.google.com/security
- Turn on 2-Step Verification

### 2. Generate App Password
- Go to: https://myaccount.google.com/apppasswords
- Select "Mail" and your device
- Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### 3. Create .env File
Create a file named `.env` in your project folder:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=abcdefghijklmnop
```

Replace with your actual email and the 16-character app password (remove spaces).

### 4. Test It
```bash
python test_email_simple.py
```

---

## Alternative: Office 365 Setup

### 1. Enable SMTP Authentication
- Go to Microsoft 365 Admin Center
- Users → Active Users → Select your mailbox
- Mail → "Manage email apps"
- Enable "Authenticated SMTP"

### 2. Create .env File
```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SENDER_EMAIL=your-email@outlook.com
SENDER_PASSWORD=your-password
```

### 3. Test It
```bash
python test_email_simple.py
```

---

## Verify It's Working

After setup, you should see:
```
✅ SUCCESS! Test email sent successfully!
📬 Check the inbox of: test@example.com
```

If you see errors, check:
- ❌ Wrong password → Use App Password for Gmail
- ❌ Authentication failed → Enable SMTP AUTH for Office 365
- ❌ Connection timeout → Check firewall/internet

---

## Still Not Working?

1. Check `logs/app.log` for detailed errors
2. Read `EMAIL_SETUP_GUIDE.md` for comprehensive help
3. Make sure `.env` file is in the project root folder
4. Verify no extra spaces in email/password

---

## What Changed?

✅ Email credentials now loaded from `.env` file (secure)  
✅ Better error messages with solutions  
✅ Support for Gmail, Office 365, Yahoo  
✅ Test scripts to verify configuration  
✅ Detailed logging for troubleshooting  

---

## Files Created

- `setup_email.py` - Interactive setup wizard
- `test_email_simple.py` - Quick email test
- `EMAIL_SETUP_GUIDE.md` - Comprehensive guide
- `.env.example` - Template for credentials
- `FIX_EMAIL_NOW.md` - This file

---

## Next Steps

1. Run: `python setup_email.py`
2. Test: `python test_email_simple.py`
3. Start app: `python app.py`
4. Send emails from the web interface

✅ Done! Emails will now be delivered successfully.
