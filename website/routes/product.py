from os import abort
import os
from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort, url_for
from website import db
from website.models.product import Product
from website.models.branch import Branch
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from sqlalchemy import and_, or_, desc, asc
import requests

product = Blueprint('product', __name__)

@product.route('/product', methods=['GET', 'POST'])
@login_required
def prod():
    """products available in the inventory and in their entries"""

    #if user is not confirmed, block access and send to home
    if current_user.confirmed is False:
        flash('Please confirm your account, check your email (and spam folder)', 'error')
        return redirect(url_for('views.home'))

    # if user presses Search
    if request.method == 'POST' and "btn-srch" in request.form:
        search = request.form.get("search")
        orderby = request.form.get("orderby")
        
        #checks that products are from user
        userprod = Product.query.filter(Product.owner == current_user.email)

        # search input section
        srch = userprod.filter(or_(Product.id.like(search),
                                    Product.name.like('%' + search + '%'), 
                                    Product.branch.like('%' + search + '%'), 
                                    Product.qr_barcode.like(search)))

        # Order By select section
        if orderby == 'higherprice':
            data = srch.order_by(desc(Product.price)).paginate(per_page=10)
        elif orderby == 'lowerprice':
            data = srch.order_by(asc(Product.price)).paginate(per_page=10)
        elif orderby == 'highercost':
            data = srch.order_by(desc(Product.cost)).paginate(per_page=10)
        elif orderby == 'lowercost':
            data = srch.order_by(asc(Product.cost)).paginate(per_page=10)
        else:
            data = srch.paginate(per_page=10)

        # show branches and next prod id for add product row
        branches = Branch.query.filter_by(owner=current_user.email)
        nextid = db.session.query(func.max(Product.id)).scalar()
        if nextid is None:
            nextid = 1
        else:
            nextid += 1

        return render_template('product.html', user=current_user,
                            branches=branches, nextid=nextid, products=data)

    if request.method == 'POST' and "btn-add" in request.form:
        prodDict = request.form.to_dict()
        name = prodDict.get('name')    
        branch = prodDict.get('branch')
        qty = prodDict.get('quantity')
        cost = prodDict.get('cost')
        price = prodDict.get('price')
        qr_barcode = prodDict.get('qr_barcode')
        
        if cost == '' or cost == 'None':
            prodDict['cost'] = None
        elif cost: 
            if cost.isnumeric() is False:
                flash("Quantity, cost, price and reserved have to be numbers.", category='error')
                return redirect('/product') 
        if price == '' or price == 'None':
            prodDict['price'] = None
        elif price:
            if price.isnumeric() is False:
                flash("Quantity, cost, price and reserved have to be numbers.", category='error')
                return redirect('/product') 
         
    
        if name and branch:
            # adding new product instance to database
            prodDict['owner'] = current_user.email
            new_prod = Product(**prodDict)
            db.session.add(new_prod)
            db.session.commit()
            if prodDict.get('qr_barcode') == 'qr':
                generate_qr(new_prod.id)
            elif prodDict.get('qr_barcode') == 'barcode':
                generate_barcode(new_prod.id)
            db.session.commit()
            #print(f'\n\n\n{new_prod.qr_barcode}\n\n')
            flash("Poduct added", category='success')
            return redirect('/product')
        else:
            flash('Name, Branch and Quantity are mandatory fields', category='error')
    # branches to display as options in add product table
    branches = Branch.query.filter_by(owner=current_user.email)
    # hardprint next id for new product
    nextid = db.session.query(func.max(Product.id)).scalar()
    if nextid is None:
        nextid = 1
    else:
        nextid += 1
    data = Product.query.filter_by(owner=current_user.email).paginate(per_page=10)
    return render_template('product.html', user=current_user,
                           branches=branches, nextid=nextid, products=data)

@product.route('/product/<id>', methods=['POST','GET'], strict_slashes=False)
@login_required
def prodUpdate(id):
    """updating or consulting item from product"""
    print(f'\n\n\n{request.method}\n\n')
    item = Product.query.filter(and_(Product.owner==current_user.email, Product.id==id)).first()
    if request.method == 'POST':
        prodDict = request.form.to_dict()
        print(f'donde teniaq entrar, entré lpm keys:{prodDict.keys()}')

        if prodDict is None:
            abort(404)

        name = prodDict.get('nameUpdate')
        if name is None:
            name = prodDict.get('nameBarcodeUpdate')
        
        branch = prodDict.get('branchesUpdate')
        if branch is None:
            branch = prodDict.get('branchesBarcodeUpdate')
        
        cost = prodDict.get('costUpdate')
        if cost is None:
            cost = prodDict.get('costBarcodeUpdate')
        
        price = prodDict.get('priceUpdate')
        if price is None:
            price = prodDict.get('priceBarcodeUpdate')

        
        qr_barcode = prodDict.get('qr_barcodeUpdate')
        if qr_barcode is None:
            qr_barcode = prodDict.get('qr_barcodeBarcodeUpdate')
        print(f'\n\nllegué acá. form dict:{prodDict}\n\n')
        if name and branch:
            if type(name) is str:
                item.name = name
            else:
                flash("Name has to be a string", category='error')
                return redirect('/product')
            if type(branch) is str:
                item.branch = branch
            else:
                flash("Branch has to be a string", category='error')
                return redirect('/product')
            if cost and cost.isnumeric():
                item.cost = cost
            elif cost != '':
                flash("Cost has to be a number", category='error')
                return redirect('/product')
            if price and price.isnumeric():
                item.price = price
            elif price != '':
                flash("Price has to be a number", category='error')
                return redirect('/product')
            
            print(f'\n\n\nque mierda soy? qr_barcode {qr_barcode} item.qr_barcode: {item.qr_barcode}\n\n')
            if qr_barcode == 'qr' and item.qr_barcode != qr_barcode:
                print(f'\n\n\nentre lpm al qr\n\n')
                generate_qr(item.id)
            elif qr_barcode == 'barcode' and item.qr_barcode != qr_barcode:
                print(f'\n\n\nentre lpm al barcode\n\n')
                generate_barcode(item.id)

            item.qr_barcode = qr_barcode

            db.session.commit()
            flash("Item updated successfully!", category='success')
            return redirect('/product')
        else:
            flash('Name, Branch and Quantity are mandatory fields', category='error')
        
    try:
        # filter query by logged user and id
        product = Product.query.filter(and_(Product.owner==current_user.email, Product.id==id)).first()
        print(f'\n\n\n{product}\n\n')
        # making a diccionary to use the GET method as API
        toDict = product.__dict__
        toDict.pop('_sa_instance_state')
        branches = Branch.query.filter_by(owner=current_user.email).all()
        listBranches = []
        for branch in branches:
            listBranches.append(branch.name)
        print(f'a ver el diccionariode las sucursales: {listBranches}\n\n')
        toDict['ownerBranches'] = listBranches
        print(f'a ver el diccionario: {toDict}\n\n')
        return jsonify(toDict)
    except Exception:
        abort(404)

@product.route('/product/delete/<id>', strict_slashes=False)
@login_required
def Delete(id):
    """product page"""
    product = Product.query.get(id)
    path = f'./../static/images/{id}.png'
    path =  os.path.join(os.path.dirname(__file__), path)
    if os.path.exists(path):
        os.remove(path)
    db.session.delete(product)
    db.session.commit()
    flash('Item deleted successfully!')
    print(f'\n\n\naaaaaaaaaaaa{request.url_rule}\n\n\n')
    return redirect('/product')

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

