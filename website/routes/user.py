from flask import Blueprint, render_template, request, flash, redirect, url_for
#from website import views
from website import db
from website.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.sql.expression import func

# This file is a blueprint, it has urls in it
# We can have url routes in different files because of this
usr = Blueprint('usr', __name__)

@usr.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # get info submitted on form
        usrDict = request.form.to_dict()
        email = usrDict.get('email')
        usrname = usrDict.get('usrname')
        password1 = usrDict.get('password1')
        password2 = usrDict.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists', category='error')
        elif len(email) < 4:
            flash("Invalid email", category='error')
        elif len(usrname) < 3:
            flash("Username too short", category='error')
        elif password1 != password2:
            flash("Passwords dont match", category='error')
        elif len(password1) < 7:
            flash("Password >= 8 characters", category='error')
        else:
            usrDict['password1'] = generate_password_hash(password1, method='sha256')
            usrDict.pop('password2')
            new_user = User(**usrDict)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created", category='success')
            login_user(new_user, remember=True )
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@usr.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form.get('email')
        pswd = request.form.get('password')
        # if email in form is in teh db..
        user = User.query.filter_by(email=mail).first()
        if user:
            if check_password_hash(user.password, pswd):
                flash('Log-in successful', category='success')
                # method of flask-login, takes db user
                login_user(user, remember=True )
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Incorrect email', category='error')

    return render_template("login.html", user=current_user)

@usr.route('/logout')
@login_required # only allows access to route if user is logged in
def logout():
    logout_user()
    return redirect(url_for('usr.login'))