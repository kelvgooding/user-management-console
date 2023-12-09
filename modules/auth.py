"""
Author: Kelvin Gooding
Created: 2022-10-11
Updated: 2023-10-16
Version: 1.1.0
"""

# Modules

from configparser import ConfigParser
import getpass

config = ConfigParser()
config.read(f'/home/{getpass.getuser()}/.config.ini')

smtp_auth = {
    'server' : config.get('SMTP', 'SMTP_SERVER'),
    'port' : config.get('SMTP', 'SMTP_PORT'),
    'email' : config.get('SMTP', 'SMTP_EMAIL'),
    'password' : config.get('SMTP', 'SMTP_PASSWORD'),
    }