import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv 
load_dotenv()
from langchain_core.tools import tool

@tool
def send_mail(subject, body, receiver):
    """
    Send an email notification.
    """
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender or not password:
        return "Email credentials are missing"

    message = EmailMessage()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(message)

        return "Email sent successfully"

    except Exception as e:
        return f"Email failed: {e}"