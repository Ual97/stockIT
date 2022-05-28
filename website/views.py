from flask import Blueprint, render_template
from flask_login import current_user

# This file is a blueprint, it has urls in it
# We can have url routes in different files because of this
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)
