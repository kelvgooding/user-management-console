# USER MANAGEMENT CONSOLE

## Description

UMC (User Management Console) is a simple web application designed to show the log in process, before gaining access to the main features, such as create users, deleting, and resetting password for user accounts.

## Running app locally

Clone the repository:

```
cd ~
git clone https://github.com/kelvgooding/user-management-console.git
cd ~/user-management-console
```

A ```config.ini``` file needs to be created. The values placed within this file are used in ```modules/auth.py```:

```
touch ~/.config.ini
vi ~/.config.ini
```
Add the below into ```.config.ini``` and update the values accordingly:

```
[SMTP]
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
SMTP_EMAIL = username@gmail.com
SMTP_PASSWORD = password
```

Install any dependices required:

```
pip install -r requirements.txt
```

The log file will contain the URL for the application, along with each request that is made.

```
python3 ~/user-management-console/app.py >> ~/user-management-console/user-management-console_`date +\%Y\%m\%d`.log 2>&1 &
```
```
cat ~/user-management-console/user-management-console_`date +\%Y\%m\%d`.log 2>&1 &
```

This can now be accessed via web browser - http://localhost:3002

## Running app using Docker

Clone the repository:

```
cd ~
git clone https://github.com/kelvgooding/user-management-console.git
cd ~/user-management-console
```

A ```config.ini``` file needs to be created. The values placed within this file are used in ```modules/auth.py```:

```
touch ~/.config.ini
vi ~/.config.ini
```
Add the below into ```.config.ini``` and update the values accordingly:

```
[SMTP]
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
SMTP_EMAIL = username@gmail.com
SMTP_PASSWORD = password
```

Run the following command to build the Docker image

```
sudo docker build -t user-management-console .
```

Run the following command to create and start the container:

```
sudo docker run -itd -p 3002:3002 user-management-console
```

This can now be accessed via web browser - http://localhost:3002