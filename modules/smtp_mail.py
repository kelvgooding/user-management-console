"""
Author: Kelvin Gooding
Created: 2022-10-11
Updated: 2025-02-11
Version: 1.2
"""

# Modules

import smtplib
from email.message import EmailMessage
from . import auth

try:
    server = smtplib.SMTP(auth.smtp_auth['server'], auth.smtp_auth['port'])
    server.starttls()
    server.login(auth.smtp_auth['email'], auth.smtp_auth['password'])
    print("SMTP login successful!")
except Exception as e:
    print("Failed to connect:", e)
    server = None

def send_email(recipient, subject, body):
    if server is None:
        print("SMTP connection not established. Email not sent.")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = auth.smtp_auth['email']
    msg["To"] = recipient
    msg.set_content(body)

    try:
        server.send_message(msg)
        print(f"Email successfully sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {e}")