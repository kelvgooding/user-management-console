# CONTACTS

## Description

Repository: https://github.com/kelvgooding/user-management-console

UMC (User Management Console) is a small web application designed to show the log in screen of an application, before gaining access to the main features. There is a feature to create an account if the user does not have login credentials.

## System Requirements

- Linux

## Prerequisites

Run the following command to install the requirements.txt file:

```
pip3 install -r requirements.txt
```

A .config.ini file needs to be created in the home directory. The values placed within this file are used within the /modules/auth.py file:

```
touch ~/.config.ini
vi ~/.config.ini
```

Add the following contents into the files, whislt updating the values for each line:

```
[SMTP]
SMTP_SERVER = 
SMTP_PORT = 
SMTP_EMAIL = 
SMTP_PASSWORD = 
```

## Dependencies

### Software:

- Python

### Modules:

- from flask import Flask, render_template, flash, request, session, url_for, redirect
- from modules import smtp_mail
- from modules import db_check
- import sqlite3
- import random
- import string
- import os
- import getpass

## Stakeholders

PM: Kelvin Gooding | kelv.gooding@outlook.com<br>
Design: Kelvin Gooding | kelv.gooding@outlook.com<br>
Dev: Kelvin Gooding | kelv.gooding@outlook.com<br>
QA: Kelvin Gooding | kelv.gooding@outlook.com<br>
Support: Kelvin Gooding | kelv.gooding@outlook.com

## Contribution

Issue Tracker: https://github.com/kelvgooding/user-management-console/issues<br>
Contact: Kelvin Gooding | kelv.gooding@outlook.com
