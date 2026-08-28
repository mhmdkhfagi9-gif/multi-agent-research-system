"""
Email delivery tool for the Action Agent.

Runs in DRY-RUN mode by default (config.EMAIL_DRY_RUN = True), so the whole
pipeline can be tested end-to-end without real SMTP credentials -- it just
prints what WOULD be sent. Set EMAIL_DRY_RUN = False and provide real
SMTP_* values (in config.py or as environment variables) to actually send.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config


def send_email(subject: str, body: str, recipient: str = None) -> dict:
    recipient = recipient or config.EMAIL_RECIPIENT

    if config.EMAIL_DRY_RUN:
        print("\n[EMAIL - DRY RUN, nothing actually sent]")
        print(f"To: {recipient}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}\n")
        return {"success": True, "dry_run": True}

    try:
        msg = MIMEMultipart()
        msg["From"] = config.SMTP_USERNAME
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            server.send_message(msg)

        return {"success": True, "dry_run": False}
    except Exception as e:
        return {"success": False, "error": str(e)}
