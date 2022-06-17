import os
from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort, url_for
from website import db
from website.models.entries import Entries
from website.models.branch import Branch
from website.models.product import Product
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from sqlalchemy import and_, or_, desc, asc
import requests

entries = Blueprint('entries', __name__)

@entries.route('/entries', methods=['GET', 'POST'])
@login_required
def entr():
    """entries of products"""

    #if user is not confirmed, block access and send to home
    if current_user.confirmed is False:
        flash('Please confirm your account, check your email (and spam folder)', 'error')
        return redirect(url_for('views.home'))

    # if user presses Search
    if request.method == 'POST' and "btn-srch" in request.form:
        search = request.form.get("search")
        orderby = request.form.get("orderby")
        
        #checks that products are from user
        userprod = Entries.query.filter(Entries.owner == current_user.email)

        # search input section
        srch = userprod.filter(or_(Entries.id.like(search),
                                    Entries.name.like('%' + search + '%'), 
                                    Entries.branch.like('%' + search + '%'), 
                                    Entries.qr_barcode.like(search)))

        # Order By select section
        if orderby == 'higherprice':
            data = srch.order_by(desc(Entries.price)).paginate(per_page=10)
        elif orderby == 'lowerprice':
            data = srch.order_by(asc(Entries.price)).paginate(per_page=10)
        elif orderby == 'highercost':
            data = srch.order_by(desc(Entries.cost)).paginate(per_page=10)
        elif orderby == 'lowercost':
            data = srch.order_by(asc(Entries.cost)).paginate(per_page=10)
        elif orderby == 'higherdate':
            data = srch.order_by(desc(Entries.date)).paginate(per_page=10)
        elif orderby == 'lowerdate':
            data = srch.order_by(asc(Entries.date)).paginate(per_page=10)

        else:
            data = srch.paginate(per_page=10)

        # show branches and next prod id for add entry row
        branches = Branch.query.filter_by(owner=current_user.email)
        products = Product.query.filter_by(owner=current_user.email)
        nextid = db.session.query(func.max(Entries.id)).scalar()

        if nextid is None:
            nextid = 1
        else:
            nextid += 1

        return render_template('entries.html', user=current_user,
                            branches=branches, products=products, nextid=nextid, entries=data)

    if request.method == 'POST' and "btn-add" in request.form:
        prodDict = request.form.to_dict()
        name = prodDict.get('name')    
        branch = prodDict.get('branch')
        qty = prodDict.get('quantity')
        cost = prodDict.get('cost')
        price = prodDict.get('price')
        expiry = prodDict.get('expiry')
        reserved = prodDict.get('qty_reserved')
        qr_barcode = prodDict.get('qr_barcode')
        
        if cost == '' or cost == 'None':
            prodDict['cost'] = None
        elif cost: 
            if cost.isnumeric() is False:
                flash("Quantity, cost, price and reserved have to be numbers.", category='error')
                return redirect('/entries') 
        if price == '' or price == 'None':
            prodDict['price'] = None
        elif price:
            if price.isnumeric() is False:
                flash("Quantity, cost, price and reserved have to be numbers.", category='error')
                return redirect('/entries') 
        if expiry == '' or expiry == 'None':
            prodDict['expiry'] = None
        if reserved == '' or reserved == 'None':
            prodDict['qty_reserved'] = None
        elif reserved:
            if reserved.isnumeric() is False:
                flash("Quantity, cost, price and reserved have to be numbers.", category='error')
                return redirect('/entries')         
    
        if name and branch and qty:
            if qty.isnumeric() is False:
                flash("Quantity, cost, price and reserved have to be numbers.", category='error')
                return redirect('/entries')
            prodDict['owner'] = current_user.email
            new_prod = Entries(**prodDict)
            db.session.add(new_prod)
            db.session.commit()
            if qr_barcode == 'qr':
                generate_qr(new_prod.id)
            elif qr_barcode == 'barcode':
                generate_barcode(new_prod.id)
            new_prod.qr_barcode = qr_barcode
            db.session.commit()
            #print(f'\n\n\n{new_prod.qr_barcode}\n\n')
            flash("Poduct added", category='success')
            return redirect('/entries')
        else:
            flash('Name, Branch and Quantity are mandatory fields', category='error')
    # branches and products to display as options in add entry table
    branches = Branch.query.filter_by(owner=current_user.email)
    products = Product.query.filter_by(owner=current_user.email)
    # hardprint next id for new product
    nextid = db.session.query(func.max(Entries.id)).scalar()
    if nextid is None:
        nextid = 1
    else:
        nextid += 1
    data = Entries.query.filter_by(owner=current_user.email).paginate(per_page=10)
    return render_template('entries.html', user=current_user,
                           branches=branches, products=products, nextid=nextid, entries=data)

def generate_qr(id):
    """consulting API which generates a qr"""
    url = "https://qrickit-qr-code-qreator.p.rapidapi.com/api/qrickit.php"

    querystring = {"d":f'{id}'}

    headers = {
	            "X-RapidAPI-Key": "71760ccf2fmshaa151dcb49bd23cp1ad4b7jsn1d74bdc7fa4e",
	            "X-RapidAPI-Host": "qrickit-qr-code-qreator.p.rapidapi.com"
                }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(f'\n\n\n{response._content}\n\n')
    #taking the content's bytes to write the PNG img
    image_data = response._content
    path = f'./../static/images/{id}.png'
    with open(os.path.join(os.path.dirname(__file__), path), 'wb+') as out_file:
        out_file.write(image_data)

def generate_barcode(id):
    """consulting API which generates a barcode"""
    
    url = "https://barcode-generator4.p.rapidapi.com/"

    querystring = {"text":f'{id}',"barcodeType":"C128","imageType":"PNG"}

    headers = {
    	"X-RapidAPI-Key": "71760ccf2fmshaa151dcb49bd23cp1ad4b7jsn1d74bdc7fa4e",
    	"X-RapidAPI-Host": "barcode-generator4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    image_data = response.json().get('barcode')
    import base64
    try:
        #encoding string to bytes to then write a file with the PNG img
        image_data = base64.b64decode(image_data.replace('data:image/PNG;base64,', '').encode())
        path = f'./../static/images/{id}.png'
        print(f'\n\n\n{path}\n\n')
        with open(os.path.join(os.path.dirname(__file__), path), 'wb+') as out_file:
            out_file.write(image_data)
        return response.json().get('barcode')
    except:
        pass