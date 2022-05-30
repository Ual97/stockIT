from flask import Blueprint, render_template, request, flash, redirect, url_for
from website import views
from . import db
from .models import Product, Sucursal, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.sql.expression import func

# This file is a blueprint, it has urls in it
# We can have url routes in different files because of this
auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # get info submitted on form
        email = request.form.get('email')
        usrname = request.form.get('usrname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
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
            new_user = User(email=email, usrname=usrname, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created", category='success')
            login_user(new_user, remember=True )
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
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

@auth.route('/logout')
@login_required # only allows access to route if user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/inventario')
@login_required
def inv():
    """ returns prduct list of current user with pagination"""
    data = Product.query.filter_by(owner=current_user.email).paginate(per_page=10)
    return render_template('inventario.html', user=current_user, products=data )

@auth.route('/inventario/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('pname')
        sucursal = request.form.get('sucursal')
        qty = request.form.get('cant')
        cost = request.form.get('cost')
        price = request.form.get('price')
        expiry = request.form.get('expiry')
        reserved = request.form.get('reserved')
        cbarras = request.form.get('cbarras')
        
        if cost == '':
            cost = None
        if price == '':
            price = None
        if expiry == '':
            expiry = None
        if reserved == '':
            reserved = None
        if cbarras == '':
            cbarras = None
    
        if name and sucursal and qty:
            new_prod = Product(owner=current_user.email, name=name, sucursal=sucursal, quantity=qty, cost=cost,
                               price=price, expiry=expiry, qty_reserved=reserved, qr_barcode=cbarras)
            db.session.add(new_prod)
            db.session.commit()
            flash("Poduct added", category='success')
        else:
            flash('Name, Sucursal and Quantity are mandatory fields', category='error')

    # sucursales to display as options in add product table
    sucs = Sucursal.query.filter_by(owner=current_user.email)
    # hardprint next id for new product
    nextid = db.session.query(func.max(Product.id)).scalar()
    if nextid is None:
        nextid = 1
    else:
        nextid += 1
    return render_template('add.html', user=current_user, sucursales=sucs, nextid=nextid)