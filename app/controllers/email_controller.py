import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

def send_email(to_email, subject, body):
    try:
        email_user = os.getenv("EMAIL_SENDER")
        email_pass = os.getenv("EMAIL_PASSWORD")

        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = email_user
        msg["To"] = to_email

        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)
            print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
