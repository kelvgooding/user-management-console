from flask import Flask
from flask import render_template
from flask import request
from flask import flash
import sqlite3
import random
import string
import smtplib
from email.message import EmailMessage

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
app.secret_key = "abcde"


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

                #c.execute("SELECT password FROM users where loginid=?;", f'{request.form.get("cu-lastname")[0:5].lower().strip()}{request.form.get("cu-firstname")[0:3].lower().strip()},')
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
    return render_template("view_users.html")


@app.route("/add_users", methods=["POST", "GET"])
def add_users():
    return render_template("add_users.html")


@app.route("/delete_users", methods=["POST", "GET"])
def delete_users():
    return render_template("delete_users.html")


@app.route("/password_reset", methods=["POST", "GET"])
def password_reset():
    return render_template("password_reset.html")
