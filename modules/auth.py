"""
Author: Kelvin Gooding
Created: 2022-10-11
Updated: 2025-01-05
Version: 1.2
"""

# Modules

from configparser import ConfigParser
import os
import getpass

config = ConfigParser()

current_dir = os.path.dirname(os.path.abspath(__file__))
previous_dir = os.path.dirname(current_dir)
config.read(os.path.join(previous_dir, 'config.ini'))

smtp_auth = {
    'server': config.get('SMTP', 'SMTP_SERVER'),
    'port': config.get('SMTP', 'SMTP_PORT'),
    'email': config.get('SMTP', 'SMTP_EMAIL'),
    'password': config.get('SMTP', 'SMTP_PASSWORD'),
}
