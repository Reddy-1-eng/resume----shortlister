import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSender:
    """
    Sends emails via Office 365.
    Tries port 465 (SSL) first, falls back to port 587 (STARTTLS).
    """

    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server   = smtp_server
        self.smtp_port     = smtp_port
        self.sender_email  = sender_email
        self.sender_password = sender_password

    def _build_message(self, recipient_email, name, role, match_percentage):
        """Construct the MIME email message."""
        subject = f"Congratulations {name}! You have been shortlisted for the {role} role"
        body = (
            f"Dear {name},\n\n"
            f"We are pleased to inform you that your resume has been shortlisted "
            f"for the {role} role with a match score of {match_percentage:.2f}%.\n\n"
            f"Our recruitment team will reach out to you shortly with the next steps "
            f"in the selection process.\n\n"
            f"Best regards,\n"
            f"HR Team\n"
            f"Woxsen University"
        )
        msg = MIMEMultipart()
        msg["From"]    = self.sender_email
        msg["To"]      = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))
        return msg

    def _try_send_ssl(self, recipient_email, msg):
        """
        Attempt delivery via SMTP_SSL on port 465.
        This is the most reliable method for Office 365.
        """
        context = ssl.create_default_context()
        logger.info(f"Trying SSL (port 465) to {self.smtp_server}...")
        with smtplib.SMTP_SSL(self.smtp_server, 465, context=context, timeout=30) as server:
            server.login(self.sender_email, self.sender_password)
            refused = server.sendmail(self.sender_email, recipient_email, msg.as_string())
            if refused:
                logger.warning(f"Recipient refused: {refused}")
                return False
            return True

    def _try_send_starttls(self, recipient_email, msg):
        """
        Attempt delivery via STARTTLS on port 587.
        Fallback when port 465 is unavailable.
        """
        logger.info(f"Trying STARTTLS (port 587) to {self.smtp_server}...")
        server = None
        try:
            server = smtplib.SMTP(self.smtp_server, 587, timeout=30)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.sender_email, self.sender_password)
            refused = server.sendmail(self.sender_email, recipient_email, msg.as_string())
            if refused:
                logger.warning(f"Recipient refused: {refused}")
                return False
            return True
        finally:
            if server:
                try:
                    server.quit()
                except Exception:
                    pass

    def send_email(self, recipient_email, name, role, match_percentage):
        """
        Send a shortlist notification email.
        Tries SSL/465 first, then STARTTLS/587.
        Returns True on success, False on failure.
        """
        if not recipient_email or str(recipient_email).strip() in ("", "N/A"):
            logger.warning("No valid recipient email — skipping.")
            return False

        recipient_email = str(recipient_email).strip()
        logger.info(f"Sending shortlist email to: {recipient_email} (role={role}, score={match_percentage:.2f}%)")
        logger.info(f"Using SMTP: {self.smtp_server}:{self.smtp_port} from {self.sender_email}")

        msg = self._build_message(recipient_email, name, role, match_percentage)

        # --- Attempt 1: SSL on port 465 ---
        try:
            success = self._try_send_ssl(recipient_email, msg)
            if success:
                logger.info(f"✅ Email delivered (SSL/465) to {recipient_email}")
                return True
        except smtplib.SMTPAuthenticationError as auth_err:
            logger.error(
                f"❌ SMTP Authentication failed on SSL/465: {auth_err}\n"
                "SOLUTION:\n"
                "  For Gmail: Use App Password (not regular password)\n"
                "    1. Enable 2FA: https://myaccount.google.com/security\n"
                "    2. Generate App Password: https://myaccount.google.com/apppasswords\n"
                "    3. Use the 16-character password in SENDER_PASSWORD\n"
                "  For Office 365: Enable SMTP AUTH in Microsoft 365 Admin Centre\n"
                "    Users → Active Users → select mailbox → Mail → 'Manage email apps' → enable 'Authenticated SMTP'"
            )
            return False
        except Exception as e1:
            logger.warning(f"SSL/465 attempt failed ({type(e1).__name__}: {e1}), trying STARTTLS/587...")

        # --- Attempt 2: STARTTLS on port 587 ---
        try:
            success = self._try_send_starttls(recipient_email, msg)
            if success:
                logger.info(f"✅ Email delivered (STARTTLS/587) to {recipient_email}")
                return True
            return False
        except smtplib.SMTPAuthenticationError as auth_err:
            logger.error(
                f"❌ SMTP Authentication failed on STARTTLS/587: {auth_err}\n"
                "SOLUTION:\n"
                "  For Gmail: Use App Password (not regular password)\n"
                "    1. Enable 2FA: https://myaccount.google.com/security\n"
                "    2. Generate App Password: https://myaccount.google.com/apppasswords\n"
                "    3. Use the 16-character password in SENDER_PASSWORD\n"
                "  For Office 365: Enable SMTP AUTH in Microsoft 365 Admin Centre or use App Password\n"
                "  Check your email provider's SMTP settings and authentication requirements"
            )
            return False
        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"❌ Recipient refused by server: {e}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"❌ SMTP error: {type(e).__name__}: {e}")
            return False
        except TimeoutError:
            logger.error(f"❌ Connection to {self.smtp_server} timed out (30s). Check firewall/network.")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error: {type(e).__name__}: {e}")
            return False