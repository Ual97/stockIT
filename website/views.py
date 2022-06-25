from flask import Blueprint, render_template
from flask_login import current_user
from website import limiter

# This file is a blueprint, it has urls in it
# We can have url routes in different files because of this
views = Blueprint('views', __name__)

@views.route('/')
@limiter.limit("10/minute")
def home():
    if current_user.is_authenticated:
        return render_template("home.html", user=current_user)
    else:
        return render_template("landingpage.html")