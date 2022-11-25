from flask import Flask
from flask import render_template
from flask import request
from flask import flash
import sqlite3
import random
import string
import smtplib
from email.message import EmailMessage
import os

# SQLite3 DB Connection

connection = sqlite3.connect("db/umc-users.db", check_same_thread=False)
c = connection.cursor()

# Mailbox

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
sender = "kelvingooding25@gmail.com"
passwd = "ioswjokbvpxifias"
server.login(sender, passwd)

# Flask

app = Flask(__name__)
app.secret_key = os.urandom(26)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        c.execute(f"SELECT loginid, password FROM users WHERE loginid=(?) and password=(?);", (
            f"{request.form.get('login-username')}",
            f"{request.form.get('login-password')}",))

        result = c.fetchone()
        if result != (f"{request.form.get('login-username')}", f"{request.form.get('login-password')}"):
            flash("Login failed. Please try again.")
            return render_template("login.html")
        else:
            return render_template("umc.html")
    else:
        return render_template("login.html")

@app.route("/login_pw_reset", methods=["POST", "GET"])
def login_pw_reset():

    if request.method == "POST":

        list1 = []

        for i in c.execute("SELECT loginid FROM users;"):
            list1.append(i[-1])

        if request.form.get("pwreset-username") in list1:
            c.execute(f"UPDATE users SET password=(?), lastpasschange=(CURRENT_TIMESTAMP) WHERE loginid=(?)", (f'{"".join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=20))}', request.form.get("pwreset-username"),))
            connection.commit()

            c.execute("SELECT password FROM users where loginid=(?);", (f'{request.form.get("pwreset-username")[0:5].lower().strip()}{request.form.get("pwreset-username")[0:3].lower().strip()}',))
            passwd = c.fetchone()


            msg2 = EmailMessage()
            msg2["Subject"] = f"{request.form.get('pwreset-username')} - UMC Password Reset"
            msg2["From"] = sender
            msg2["To"] = "kelv.gooding@outlook.com"
            msg2.set_content(f"Hi {request.form.get('pwreset-username')}\n\n"
                             f"Your password is: {passwd}\n\n")
            server.send_message(msg2)

            flash("Password Reset email has been sent.")
            return render_template("login_pw_reset.html")
        else:
            flash("Username does not exist. Please create a user.")
            return render_template("login_pw_reset.html")
    else:
        return render_template("login_pw_reset.html")

@app.route("/create_user", methods=["POST", "GET"])
def create_user():
    first_name = request.form.get("cu-firstname")
    last_name = request.form.get("cu-lastname")

    if request.method == "POST":

        c.execute('SELECT loginid FROM users WHERE loginid=(?);', (
            f'{request.form.get("cu-lastname")[0:5].lower().strip()}{request.form.get("cu-firstname")[0:3].lower().strip()}',))

        result = c.fetchone()
        try:
            if result == f'{request.form.get("cu-lastname")[0:5].lower().strip()}{request.form.get("cu-firstname")[0:3].lower().strip()}':
                flash('This username already exists.')
                return render_template("create_user.html")
            elif result != f'{request.form.get("cu-lastname")[0:5].lower().strip()}{request.form.get("cu-firstname")[0:3].lower().strip()}':
                c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, NULL)", (
                    f'{request.form.get("cu-firstname").title().strip()}',
                    f'{request.form.get("cu-lastname").title().strip()}',
                    f'{request.form.get("cu-lastname")[0:5].lower()}{request.form.get("cu-firstname")[0:3].lower()}',
                    f'{"".join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=20))}',
                    f'{request.form.get("cu-email").lower().strip()}'
                ))
                connection.commit()

                msg1 = EmailMessage()
                msg1["Subject"] = f'{first_name} {last_name} - UMC Username'
                msg1["From"] = sender
                msg1["To"] = "kelv.gooding@outlook.com"
                msg1.set_content('Hi,\n\n'
                                 f'Your username is: {request.form.get("cu-lastname")[0:5].lower().strip()}{request.form.get("cu-firstname")[0:3].lower().strip()}\n\n'
                                 f'Your password will be send in a separate email.')
                server.send_message(msg1)

                c.execute("SELECT password FROM users where loginid=(?);", (f'{request.form.get("cu-lastname")[0:5].lower().strip()}{request.form.get("cu-firstname")[0:3].lower().strip()}',))

                passwd = c.fetchone()[-1]

                msg2 = EmailMessage()
                msg2["Subject"] = f'{first_name} {last_name} - UMC Password'
                msg2["From"] = sender
                msg2["To"] = "kelv.gooding@outlook.com"
                msg2.set_content("Hi,\n\n"
                                 f"Your password is: {passwd}\n\n")
                server.send_message(msg2)

                flash('Your account has been created.')
                return render_template("create_user.html")

        except sqlite3.IntegrityError:
            flash('This username already exists.')
            return render_template("create_user.html")

    else:
        return render_template("create_user.html")


@app.route("/umc", methods=["POST", "GET"])
def umc():
    return render_template("umc.html")


@app.route("/view_users", methods=["POST", "GET"])
def view_users():

    headings = ("Full Name", "UID", "Email", "Created Date")

    data = []

    for i in c.execute("SELECT first_name || ' ' || last_name AS full_name, loginid, email, accountcreation FROM users ORDER BY loginid ASC"):
        data.append(i)

    return render_template("view_users.html", data=data, headings=headings)


@app.route("/add_users", methods=["POST", "GET"])
def add_users():
    first_name = request.form.get("au-firstname")
    last_name = request.form.get("au-lastname")

    if request.method == "POST":

        c.execute('SELECT loginid FROM users WHERE loginid=(?);', (f'{request.form.get("au-lastname")[0:5].lower().strip()}{request.form.get("au-firstname")[0:3].lower().strip()}',))

        result = c.fetchone()
        try:
            if result == f'{request.form.get("au-lastname")[0:5].lower().strip()}{request.form.get("au-firstname")[0:3].lower().strip()}':
                flash('This username already exists.')
                return render_template("create_user.html")
            elif result != f'{request.form.get("au-lastname")[0:5].lower().strip()}{request.form.get("au-firstname")[0:3].lower().strip()}':
                c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, NULL)", (
                    f'{request.form.get("au-firstname").title().strip()}',
                    f'{request.form.get("au-lastname").title().strip()}',
                    f'{request.form.get("au-lastname")[0:5].lower()}{request.form.get("au-firstname")[0:3].lower()}',
                    f'{"".join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=20))}',
                    f'{request.form.get("au-email").lower().strip()}'
                ))
                connection.commit()

                msg1 = EmailMessage()
                msg1["Subject"] = f'{first_name} {last_name} - UMC Username'
                msg1["From"] = sender
                msg1["To"] = "kelv.gooding@outlook.com"
                msg1.set_content('Hi,\n\n'
                                 f'Your username is: {request.form.get("au-lastname")[0:5].lower().strip()}{request.form.get("au-firstname")[0:3].lower().strip()}\n\n'
                                 f'Your password will be send in a separate email.')
                server.send_message(msg1)

                c.execute("SELECT password FROM users where loginid=(?);", (f'{request.form.get("au-lastname")[0:5].lower().strip()}{request.form.get("au-firstname")[0:3].lower().strip()}',))

                passwd = c.fetchone()[-1]

                msg2 = EmailMessage()
                msg2["Subject"] = f'{first_name} {last_name} - UMC Password'
                msg2["From"] = sender
                msg2["To"] = "kelv.gooding@outlook.com"
                msg2.set_content("Hi,\n\n"
                                 f"Your password is: {passwd}\n\n")
                server.send_message(msg2)

                flash('A new account has been created!')
                return render_template("add_users.html")

        except sqlite3.IntegrityError:
            flash('This username already exists.')
    return render_template("add_users.html")


@app.route("/delete_users", methods=["POST", "GET"])
def delete_users():

    username = request.form.get("delete-dropdownbox")

    list1 = []

    for i in c.execute("SELECT loginid FROM users;"):
        list1.append(i[-1])

    if request.method == "POST":
        c.execute(f"SELECT loginid FROM users WHERE loginid=(?)", (username,))
        result = c.fetchone()[-1]

        if result == username:
            c.execute(f"DELETE FROM users WHERE loginid=(?)", (username,))
            connection.commit()
            flash("User has been deleted!")
        else:
            flash("User does not exist. Please try again.")

    return render_template("delete_users.html", list1=list1)


@app.route("/password_reset", methods=["POST", "GET"])
def password_reset():

    username = request.form.get("dropdownbox")
    c_password = request.form.get("password-input")
    password1 = request.form.get("password-input1")
    password2 = request.form.get("password-input2")

    list1 = []

    for i in c.execute("SELECT loginid FROM users;"):
        list1.append(i[-1])

    if request.method == "POST":
        c.execute("SELECT password FROM users WHERE loginid=(?)", (username,))
        result = c.fetchone()[-1]
        if result == c_password:
            if password1 == password2:
                c.execute(f"UPDATE users SET password=(?), lastpasschange=(CURRENT_TIMESTAMP) WHERE loginid=(?)", (password1, username,))
                connection.commit()
                flash("Password has been changed!")
            else:
                flash("Password does not match. Please try again.")
        else:
            flash("Password is incorrect. Please try again")
    return render_template("password_reset.html", list1=list1)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)