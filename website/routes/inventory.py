from website import db
from website.models.product import Product
from website.models.movements import Movements
from website.models.branch import Branch
from flask_login import login_required
from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from sqlalchemy import and_, or_, desc, asc
import requests

inventory = Blueprint('inventory', __name__)

@login_required
@inventory.route('/inventory', methods=['GET', 'POST'])
def inventory_page():
    """inventory page"""

    #if user is not confirmed, block access and send to home
    if current_user.confirmed is False:
        flash('Please confirm your account, check your email (and spam folder)', 'error')
        return redirect(url_for('views.home'))
    
    # consulting products and movements to get the quantity of each product in inventory
    products = Product.query.filter(Product.owner == current_user.email)
    branches = Branch.query.filter(Branch.owner == current_user.email)
    movements = Movements.query.filter(Movements.owner == current_user.email)

    prodList = []
    for product in products:
        prodList.append(product.id)
    
    branchesList = []
    for branch in branches:
        branchesList.append(branch.id)
    
    inventoryDict = {}

    for branch in branchesList:
        for product in prodList:
            

    

    # if user presses Search
    if request.method == 'POST' and "btn-srch" in request.form:
        search = request.form.get("search")

        #checks that products are from user
        userprod = Product.query.filter(Product.owner == current_user.email)