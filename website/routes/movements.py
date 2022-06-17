import os
from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort, url_for
from website import db
from website.models.movements import Movements
from website.models.branch import Branch
from website.models.product import Product
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from sqlalchemy import and_, or_, desc, asc
import requests

movements = Blueprint('movements', __name__)

@movements.route('/movements', methods=['GET', 'POST'])
@login_required
def move():
    """movements of products"""

    #if user is not confirmed, block access and send to home
    if current_user.confirmed is False:
        flash('Please confirm your account, check your email (and spam folder)', 'error')
        return redirect(url_for('views.home'))

    # if user presses Search
    if request.method == 'POST' and "btn-srch" in request.form:
        search = request.form.get("search")
        orderby = request.form.get("orderby")
        
        #checks that products are from user
        userprod = Movements.query.filter(Movements.owner == current_user.email)

        # search input section
        srch = userprod.filter(or_(Movements.id.like(search),
                                    Movements.name.like('%' + search + '%'), 
                                    Movements.branch.like('%' + search + '%')))

        # Order By select section
        if orderby == 'higherprice':
            data = srch.order_by(desc(Movements.price)).paginate(per_page=10)
        elif orderby == 'lowerprice':
            data = srch.order_by(asc(Movements.price)).paginate(per_page=10)
        elif orderby == 'highercost':
            data = srch.order_by(desc(Movements.cost)).paginate(per_page=10)
        elif orderby == 'lowercost':
            data = srch.order_by(asc(Movements.cost)).paginate(per_page=10)
        elif orderby == 'higherdate':
            data = srch.order_by(desc(Movements.date)).paginate(per_page=10)
        elif orderby == 'lowerdate':
            data = srch.order_by(asc(Movements.date)).paginate(per_page=10)

        else:
            data = srch.paginate(per_page=10)

        # show branches and next prod id for add entry row
        branches = Branch.query.filter_by(owner=current_user.email)
        products = Product.query.filter_by(owner=current_user.email)
        nextid = db.session.query(func.max(Movements.id)).scalar()

        if nextid is None:
            nextid = 1
        else:
            nextid += 1

        return render_template('movements.html', user=current_user,
                            branches=branches, products=products, nextid=nextid, movements=data)

    if request.method == 'POST' and "btn-add" in request.form:
        prodDict = request.form.to_dict()
        name = prodDict.get('name')    
        branch = prodDict.get('branch')
        qty = prodDict.get('quantity')
        in_out = prodDict.get('movement')
        date = prodDict.get('date')
        
        if name and branch and qty:
            print("EEEEEEEEEEEEEEOOOOOOOOOOOOOOOOOO")
            if qty.isnumeric() is False:
                flash("Quantity has to be a number.", category='error')
                return redirect('/movements')
            prodDict['owner'] = current_user.email
            branch2 = Branch.query.filter_by(name=branch).first()
            prodDict['branch_id'] = branch2.id
            prod = Product.query.filter_by(name=name).first()
            prodDict['prod_name'] = name
            prodDict['branch_name'] = branch
            prodDict['prod_id'] = prod.id
            new_prod = Movements(**prodDict)
            db.session.add(new_prod)
            db.session.commit()
            #print(f'\n\n\n{new_prod.qr_barcode}\n\n')
            flash("Poduct added", category='success')
            return redirect('/movements')
        else:
            flash('Name, Branch and Quantity are mandatory fields', category='error')
    # branches and products to display as options in add entry table
    branches = Branch.query.filter_by(owner=current_user.email)
    products = Product.query.filter_by(owner=current_user.email)
    # hardprint next id for new product
    nextid = db.session.query(func.max(Movements.id)).scalar()
    if nextid is None:
        nextid = 1
    else:
        nextid += 1
    data = Movements.query.filter_by(owner=current_user.email).paginate(per_page=10)
    return render_template('movements.html', user=current_user,
                           branches=branches, products=products, nextid=nextid, movements=data)