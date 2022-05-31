from flask import Blueprint, render_template, request, flash, redirect, url_for
from website import views
from website import db
from models.user import User
from models.product import Product
from models.sucursal import Sucursal
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.sql.expression import func

