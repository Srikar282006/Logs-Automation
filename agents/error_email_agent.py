import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


@tool
def handle_error(error_summary: str) -> str:
    """Send an EV charger error summary to the network owner by email."""

    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("OWNER_EMAIL")

    if not sender or not password or not receiver:
        return "Email credentials are missing."

    message = EmailMessage()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = "EV Charger Failure Detected"
    message.set_content(error_summary)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(message)

        return "Email sent successfully"

    except Exception as e:
        return f"Email failed: {e}"