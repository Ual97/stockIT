from os import abort
import os
from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort, url_for
from website import db, limiter
from website.models.product import Product
from website.models.branch import Branch
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from sqlalchemy import and_, or_, desc, asc
import requests

product = Blueprint('product', __name__)

@product.route('/product', methods=['GET', 'POST'])
@limiter.limit("20/minute")
@login_required
def prod():
    """products available in the inventory and in their entries"""

    #if user is not confirmed, block access and send to home
    #if current_user.confirmed is False:
    #    flash('Please confirm your account, check your email (and spam folder)', 'error')
    #    return redirect(url_for('views.home'))

    # if user presses Search
    if request.method == 'POST' and "btn-srch" in request.form:
        search = request.form.get("search")

        #checks that products are from user
        userprod = Product.query.filter(Product.owner == current_user.email)

        # search input section
        data = userprod.filter(or_(Product.id.like(search),
                                    Product.name.like('%' + search + '%'), 
                                    Product.qr_barcode.like(search)))

        return render_template('product.html', user=current_user, products=data)

    if request.method == 'POST' and "btn-add" in request.form:
        prodDict = request.form.to_dict()
        name = prodDict.get('name')    
        qr_barcode = prodDict.get('qr_barcode')
        description = prodDict.get('description')


        if name:
            name = name.strip()
            currentName = Product.query.filter((Product.name==name) & (Product.owner==current_user.email)).first()
            if currentName and name.lower() == currentName.name.lower():
                flash('Product already exists', 'error')
                return redirect(url_for('product.prod'))

            prodDict['name'] = name
            # adding new product instance to database
            prodDict['owner'] = current_user.email
            if description == '' or description is None:
                prodDict['description'] = 'No description'
            new_prod = Product(**prodDict)
            db.session.add(new_prod)
            db.session.commit()
            if qr_barcode == 'qr':
                generate_qr(new_prod.id)
            elif qr_barcode == 'barcode':
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

    data = Product.query.filter_by(owner=current_user.email).paginate(per_page=10)
    return render_template('product.html', user=current_user,
                           branches=branches, nextid=nextid, products=data)


@product.route('/product/<id>', methods=['POST','GET'], strict_slashes=False)
@limiter.limit("20/minute")
@login_required
def prodUpdate(id):
    """updating or consulting item from product"""
    print(f'\n\n\n{request.method}\n\n')
    item = Product.query.filter_by(id=id).first()
    if request.method == 'POST':
        prodDict = request.form.to_dict()
        print(f'donde teniaq entrar, entré lpm keys:{prodDict.keys()}')

        if prodDict is None:
            abort(404)

        #updating description if exists

        description = prodDict.get('descriptionUpdate')
        print(f'\n\ndescription del primer get {description}\n')
        if description is None:
            print(f'\n\nentre al if q no debía xd\n')

            description = prodDict.get('descriptionBarcodeUpdate')

        print(f'antes de setear descripción qr_barcodeUpdate{prodDict.get("qr_barcodeUpdate")}\n\n{item.description}\n')
        if description:
            print(f"\n\nentré a setear nueva descripción item.description {item.description} description {description}\n")
            item.description = description
            db.session.commit()
            print(f"\n\ndespués de setear nueva descripción item.description {item.description} description {description}\n")


        print(f'\n\nitem descrption en obj{item.description}\n')

        qr_barcode = prodDict.get('qr_barcodeUpdate')
        if qr_barcode is None:
            qr_barcode = prodDict.get('qr_barcodeBarcodeUpdate')
        print(f'\n\nllegué acá. form dict:{prodDict}\n\n')
        if qr_barcode:


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
        toDict['branches'] = [branch.name for branch in branches]
        return jsonify(toDict)
    except Exception:
        abort(404)

def generate_qr(id):
    """consulting API which generates a qr"""
    url = "https://qrickit-qr-code-qreator.p.rapidapi.com/api/qrickit.php"

    querystring = {"d":f'{id}'}

    headers = {
	            "X-RapidAPI-Key": "1f2d50fbf4mshdcf01c7289d62e9p1f5cf7jsn978bc35e8d2d",
	            "X-RapidAPI-Host": "qrickit-qr-code-qreator.p.rapidapi.com"
                }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(f'\n\n\n{response._content}\n\n')
    #taking the content's bytes to write the PNG img
    image_data = response._content
    path = f'./../static/images/qr.{id}.png'
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
        path = f'./../static/images/barcode.{id}.png'
        print(f'\n\n\n{path}\n\n')
        with open(os.path.join(os.path.dirname(__file__), path), 'wb+') as out_file:
            out_file.write(image_data)
        return response.json().get('barcode')
    except:
        pass