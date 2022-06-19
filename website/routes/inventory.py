from codecs import strict_errors
from website import db
from website.models.product import Product
from website.models.movements import Movements
from website.models.branch import Branch
from website.models.inventory import Inventory
from flask_login import login_required
from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from sqlalchemy import and_, or_, desc, asc
import requests

inventory = Blueprint('inventory', __name__)

@login_required
@inventory.route('/inventory', methods=['GET', 'POST'], strict_slashes=False)
def inventory_page():
    """inventory page"""

    formDict = request.form.to_dict()

    #if user is not confirmed, block access and send to home
    if current_user.confirmed is False:
        flash('Please confirm your account, check your email (and spam folder)', 'error')
        return redirect(url_for('views.home'))
    
    # consulting stock from all branches
    stockQuery = Inventory.query.filter_by(owner=current_user.email).all()

    # store some  product name if some product is searched
    search = formDict.get('search')
    search = search.lower().strip() if search else None

    stock = []

    #filling stock dictionary with prod name, quantity, description and product id
    for item in stockQuery:
        stockItem = {}

        product = Product.query.filter_by(owner=current_user.email).filter_by(id=item.prod_id).first()
        
        # if is searched a particular product only that product is gonna be listed
        if search and search not in product.name.lower():
            continue
        stockItem['name'] = product.name
        stockItem['quantity'] = item.quantity
        stockItem['description'] = product.description
        stockItem['id'] = item.prod_id

        stock.append(stockItem)

    print(f'\n\n\nlista final:{stockItem}\n\n')

    # if user presses Search
    if request.method == 'POST' and "btn-srch" in request.form:

        print(f'\n\n\nformDict: {formDict}\n\n')

        selectedBranch = formDict.get('selectBranch')

        # filtering by branch
        if selectedBranch != 'All Branches (default)':
            selectedBranch = Branch.query.filter_by(owner=current_user.email).filter_by(name=selectedBranch).first()

            for item in stock:
                # calculating the current stock for
                # each branch distinct from the selected
                currentStock = 0
                for mov in Movements.query.filter_by(owner=current_user.email).filter(and_(Movements.prod_id == item['id'],
                                                     Movements.branch_id == selectedBranch.id)).all():
                    if mov.in_out is True:
                        currentStock += mov.quantity
                    elif mov.in_out is False:
                        currentStock -= mov.quantity
                item['quantity'] = currentStock

        
    # branches from user
    branches = Branch.query.filter_by(owner=current_user.email).all()
    branchesList = ["All Branches (default)"]
    for branch in branches:
        branchesList.append(branch.name)

    return render_template('inventory.html', stock=stock, user=current_user, branches=branchesList)