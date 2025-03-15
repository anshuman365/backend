from flask import Blueprint, render_template, request, redirect, url_for, session
from database.db import cursor, bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM admin WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user[2], password):
            session['admin'] = user[1]
            return redirect(url_for('dashboard'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))