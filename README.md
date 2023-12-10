# USER MANAGEMENT CONSOLE

## Description

Repository: https://github.com/kelvgooding/user-management-console

UMC (User Management Console) is a small web application designed to show the log in screen of an application, before gaining access to the main features. There is a feature to create an account if the user does not have login credentials.

## OS Compatibility

- Linux

## Dependencies

### Linux Packages

- python3
- python3-pip

### Python Modules

- from flask import Flask, render_template, flash, request, session, url_for, redirect
- from modules import smtp_mail
- from modules import db_check
- import sqlite3
- import random
- import string
- import os
- import getpass

## Installation

To download this web application, run the following commands on your linux environment:

Downloading the repository from GitHub:

```
cd ~
git clone https://github.com/kelvgooding/user-management-console.git
```

Installating the requirements.txt file to ensure the correct packages are available and installed:

```
cd ~/user-management-console
pip3 install -r requirements.txt
```

The log file will contain the URL for the application, along with each request that is made.

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

Running the application:

```
cd ~/user-management-console
python3 ~/user-management-console/app.py >> ~/app_user-management-console_`date +\%Y\%m\%d`.log 2>&1 &
```
## Stakeholders

PM: Kelvin Gooding | kelv.gooding@outlook.com<br>
Design: Kelvin Gooding | kelv.gooding@outlook.com<br>
Dev: Kelvin Gooding | kelv.gooding@outlook.com<br>
QA: Kelvin Gooding | kelv.gooding@outlook.com<br>
Support: Kelvin Gooding | kelv.gooding@outlook.com

## Contribution

Issue Tracker: https://github.com/kelvgooding/user-management-console/issues<br>
Contact: Kelvin Gooding | kelv.gooding@outlook.com
