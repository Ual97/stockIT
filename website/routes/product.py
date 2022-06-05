from operator import or_
from os import abort
from re import X
from urllib import response
from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort
from website import db
from website.models.product import Product
from website.models.sucursal import Sucursal
from website.models.user import User
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from sqlalchemy import and_
from datetime import datetime

inventory = Blueprint('inventory', __name__)

@inventory.route('/inventario', methods=['GET', 'POST'])
@login_required
def inv():
    print(f'\n\nentre donde pense q entraba chinchulin {request.method}\n\n\n')
    if request.method == 'POST':
        prodDict = request.form.to_dict()
        name = prodDict.get('pname')    
        sucursal = prodDict.get('sucursal')
        qty = prodDict.get('cant')
        cost = prodDict.get('cost')
        price = prodDict.get('price')
        expiry = prodDict.get('expiry')
        reserved = prodDict.get('reserved')
        cbarras = prodDict.get('cbarras')
        
        if cost == '' or cost == 'None':
            prodDict['cost'] = None
        if price == '' or price == 'None':
            prodDict['price'] = None
        if expiry == '' or expiry == 'None':
            prodDict['expiry'] = None
        if reserved == '' or reserved == 'None':
            prodDict['reserved'] = None
        if cbarras == '' or cbarras == 'None':
            prodDict['cbarras'] = None
    
        if name and sucursal and qty:
            prodDict['owner'] = current_user.email
            new_prod = Product(**prodDict)
            db.session.add(new_prod)
            db.session.commit()
            flash("Poduct added", category='success')
            return redirect('/inventario')
        else:
            flash('Name, Sucursal and Quantity are mandatory fields', category='error')
    # sucursales to display as options in add product table
    sucs = Sucursal.query.filter_by(owner=current_user.email)
    # hardprint next id for new product
    nextid = db.session.query(func.max(Product.id)).scalar()
    if nextid is None:
        nextid = 1
    else:
        nextid += 1
    data = Product.query.filter_by(owner=current_user.email).paginate(per_page=10)
    return render_template('inventario.html', user=current_user,
                           sucursales=sucs, nextid=nextid, products=data)

@inventory.route('/inventario/update/<id>', methods=['POST','GET'], strict_slashes=False)
@login_required
def Put(id):
    """updating or consulting item from inventory"""
    item = Product.query.get(id)

    if request.method == 'POST':
        prodDict = request.form.to_dict()
        if prodDict is None:
            abort(404)
        debugKeys = prodDict.keys()

        keys = ('name', 'sucursal', 'quantity', 'cost', 'price', 'expiry', 'qty_reserved', 'qr_barcode')

        print(f'debug keys: {debugKeys} \n\n keys set: {keys}\n\n diccionario antes de update: {item.__dict__}\n\n datos nuevos: {prodDict}')
        pos = 0
        for pos in range(len(keys)):
            if pos == 0:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if type(prodDict[keys[pos]]) is str:
                        item.name = prodDict[keys[pos]]
            if pos == 1:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if type(prodDict[keys[pos]]) is str:
                        item.sucursal = prodDict[keys[pos]]
            if pos == 2:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if type(prodDict[keys[pos]]) is int:
                        item.quantity = prodDict[keys[pos]]
            if pos == 3:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if type(prodDict[keys[pos]]) is int:
                        item.cost = prodDict[keys[pos]]
            if pos == 4:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if type(prodDict[keys[pos]]) is int:
                        item.price = prodDict[keys[pos]]
            if pos == 5:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    item.expiry = prodDict[keys[pos]]
            if pos == 6:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if type(prodDict[keys[pos]]) is int:
                        item.qty_reserved = prodDict[keys[pos]]
            if pos == 7:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if type(prodDict[keys[pos]]) is int:
                        item.qr_barcode = prodDict[keys[pos]]
        print(f'diccionario desp {item.__dict__}')
        
        db.session.commit()

        flash('Item updated successfully!')
        
        return redirect('/inventario')
    try:
        # filter query by logged user and id
        product = Product.query.filter(and_(Product.owner==current_user.email, Product.id==id)).first()
        
        # making a diccionary to use the GET method as API
        toDict = product.__dict__
        toDict.pop('_sa_instance_state')
        return jsonify(toDict)
    except Exception:
        abort(404)

@inventory.route('/inventario/delete/<id>', strict_slashes=False)
@inventory.route('/inventario/add/delete/<id>', strict_slashes=False)
@login_required
def Delete(id):
    """inventory page"""
    db.session.delete(Product.query.get(id))
    db.session.commit()
    flash('Item deleted successfully!')
    print(f'\n\n\naaaaaaaaaaaa{request.url_rule}\n\n\n')
    if request.url_rule == '/inventario/add/delete/<id>':
        return redirect('/inventario/add/delete/<id>')
    else:
        return redirect('/inventario')