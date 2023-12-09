#!/bin/usr/python3

"""
Author: Kelvin Gooding
Created: 2022-10-11
Updated: 2023-10-16
Version: 1.1
"""

# Modules

import smtplib
from email.message import EmailMessage
from . import auth

# Variables

server = smtplib.SMTP(auth.smtp_auth['server'], auth.smtp_auth['port'])
server.starttls()

# Script

server.login(auth.smtp_auth['email'], auth.smtp_auth['password'])

def send_email(recipient, subject, body):

    msg = EmailMessage()

    msg["Subject"] = f"{subject}"
    msg["From"] = auth.smtp_auth['email']
    msg["To"] = recipient
    msg.set_content(body)
    server.send_message(msg)

    print(f'Email has been sent successfully to {recipient}')
