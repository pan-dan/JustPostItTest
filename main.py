from flask import Flask, render_template, url_for, request, redirect, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'data.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'data.db')))


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/login', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute(('''SELECT password FROM passwords
                                               WHERE login = '{}';
                                               ''').format(Login))
        pas = cursor_db.fetchall()

        cursor_db.close()
        try:
            if pas[0][0] != Password:
                return render_template('auth_bad.html')
        except:
            return render_template('auth_bad.html')

        db_lp.close()
        return render_template('successauth.html')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        sql_insert = '''INSERT OR IGNORE INTO passwords VALUES('{}','{}');'''.format(Login, Password)

        cursor_db.execute(sql_insert)

        cursor_db.close()

        db_lp.commit()
        db_lp.close()

        return render_template('successregis.html')
    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)
