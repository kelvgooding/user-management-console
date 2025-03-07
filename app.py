"""
Author: Kelvin Gooding
Created: 2022-12-12
Updated: 2025-03-07
Version: 1.3
"""

# Modules

from flask import Flask, render_template, flash, request, session, url_for, redirect
from modules import db_check
from modules import smtp_mail
import os
import random
import sqlite3
import string

# Variables

base_path = os.path.dirname(os.path.abspath(__file__))
app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
db_filename = 'user_management_console.db'
sql_script = os.path.join(base_path, 'scripts/sql/create_tables.sql')

# SQLite3 Variables

db_check.check_db(f'/data', f'{db_filename}', f'{sql_script}')
conn = db_check.sqlite3.connect(os.path.join('/data', db_filename), check_same_thread=False)
c = conn.cursor()

# Flask Variables

app = Flask(__name__)
app.secret_key = os.urandom(26)

# Script

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
            if not session.get('name'):
                print(session.get('name'))
                return render_template("login.html")
        else:
            session["name"] = request.form.get('login-username')
            print(session.get('name'))
            return redirect(url_for("umc"))
    else:
        return render_template("login.html")

@app.route("/login_pw_reset", methods=["POST", "GET"])
def login_pw_reset():
    if request.method == "POST":

        list1 = []

        for i in c.execute("SELECT loginid FROM users;"):
            list1.append(i[-1])

        if request.form.get("pwreset-username") in list1:
            c.execute(f"UPDATE users SET password=(?), lastpasschange=(CURRENT_TIMESTAMP) WHERE loginid=(?)", (
            f'{"".join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=20))}',
            request.form.get("pwreset-username"),))
            conn.commit()

            c.execute("SELECT password FROM users where loginid=(?);", (
            f'{request.form.get("pwreset-username")[0:5].lower().strip()}{request.form.get("pwreset-username")[0:3].lower().strip()}',))
            passwd = c.fetchone()

            smtp_mail.send_email(f"", f"{request.form.get('pwreset-username')} - UMC Password Reset", f"Hi {request.form.get('pwreset-username')}\n\n"
                             f"Your password is: {passwd}\n\n")

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
                conn.commit()

                smtp_mail.send_email(f"{request.form.get('cu-email').lower().strip()}", f'{first_name} {last_name} - UMC Username', 'Hi,\n\n'
                                 f'Your username is: {request.form.get("cu-lastname")[0:5].lower().strip()}{request.form.get("cu-firstname")[0:3].lower().strip()}\n\n'
                                 f'Your password will be send in a separate email.')

                c.execute("SELECT password FROM users where loginid=(?);", (
                f'{request.form.get("cu-lastname")[0:5].lower().strip()}{request.form.get("cu-firstname")[0:3].lower().strip()}',))

                passwd = c.fetchone()[-1]

                smtp_mail.send_email(f"{request.form.get('cu-email').lower().strip()}", f'{first_name} {last_name} - UMC Password', "Hi,\n\n"
                                 f"Your password is: {passwd}\n\n")

                flash('Your account has been created.')
                flash(f'An email has been sent to {request.form.get("cu-email").lower().strip()}')

                return render_template("create_user.html")

        except sqlite3.IntegrityError:
            flash('This username already exists.')
            return render_template("create_user.html")

    else:
        return render_template("create_user.html")

@app.route("/umc", methods=["POST", "GET"])
def umc():
    if session.get('name') is None:
        return redirect("/")
    return render_template("umc.html", session=session.get('name'))

@app.route("/logout")
def logout():
    session['name'] = None
    return redirect("/")

@app.route("/view_users", methods=["POST", "GET"])
def view_users():
    headings = ("Full Name", "UID", "Created Date")

    data = []

    for i in c.execute("SELECT first_name || ' ' || last_name AS full_name, loginid, SUBSTRING(accountcreation,1,10) FROM users ORDER BY loginid ASC"):
        data.append(i)

    if 'buttontest' in request.form:
        c.execute('DELETE FROM users where loginid is not "goodikel";')
        conn.commit()

    return render_template("view_users.html", data=data, headings=headings)

@app.route("/add_users", methods=["POST", "GET"])
def add_users():
    first_name = request.form.get("au-firstname")
    last_name = request.form.get("au-lastname")

    if request.method == "POST":

        c.execute('SELECT loginid FROM users WHERE loginid=(?);', (
        f'{request.form.get("au-lastname")[0:5].lower().strip()}{request.form.get("au-firstname")[0:3].lower().strip()}',))

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
                conn.commit()

                smtp_mail.send_email('livelifeautomate@gmail.com', f'{first_name} {last_name} - UMC Username', 'Hi,\n\n'
                                 f'Your username is: {request.form.get("au-lastname")[0:5].lower().strip()}{request.form.get("au-firstname")[0:3].lower().strip()}\n\n'
                                 f'Your password will be send in a separate email.')

                c.execute("SELECT password FROM users where loginid=(?);", (
                f'{request.form.get("au-lastname")[0:5].lower().strip()}{request.form.get("au-firstname")[0:3].lower().strip()}',))

                passwd = c.fetchone()[-1]

                smtp_mail.send_email('livelifeautomate@gmail.com', f'{first_name} {last_name} - UMC Password', 'Hi,\n\n'
                                 f'Your password is: {passwd}\n\n')

                flash('A new account has been created!')
                return render_template("add_users.html")

        except sqlite3.IntegrityError:
            flash('This username already exists.')
    return render_template("add_users.html")

@app.route("/delete_user", methods=["POST", "GET"])
def delete_user():
    username = request.form.get("delete-dropdownbox")

    list1 = []

    for i in c.execute("SELECT loginid FROM users;"):
        list1.append(i[-1])

    if request.method == "POST":
        c.execute(f"SELECT loginid FROM users WHERE loginid=(?)", (username,))
        result = c.fetchone()[-1]

        if result == username:
            c.execute(f"DELETE FROM users WHERE loginid=(?)", (username,))
            conn.commit()
            flash("User has been deleted!")
        else:
            flash("User does not exist. Please try again.")

    return render_template("delete_user.html", list1=list1)

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
                c.execute(f"UPDATE users SET password=(?), lastpasschange=(CURRENT_TIMESTAMP) WHERE loginid=(?)",
                          (password1, username,))
                conn.commit()
                flash("Password has been changed!")
            else:
                flash("Password does not match. Please try again.")
        else:
            flash("Password is incorrect. Please try again")
    return render_template("password_reset.html", list1=list1)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3002)
