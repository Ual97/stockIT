from flask import Blueprint, render_template

# This file is a blueprint, it has urls in it
# We can have url routes in different files because of this
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")