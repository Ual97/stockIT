from flask import Blueprint, render_template, request, flash
from . import db

# This file is a blueprint, it has urls in it
# We can have url routes in different files because of this
auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('fname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(email) < 4:
            flash("Invalid email", category='error')
        elif len(fname) < 3:
            flash("Invalid name", category='error')
        elif password1 != password2:
            flash("passwords dont match", category='error')
        elif len(password1) < 7:
            flash("password too short", category='error')
        else:
            flash("account created", category='success')
            pass
    return render_template("sign_up.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>logout</>"

@auth.route('/inventario')
def inv():
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM inventory')
    data = cur.fetchall()
    return render_template('inventario.html', products=data)

@auth.route('/inventario/add')
def add():
    return render_template('add.html')