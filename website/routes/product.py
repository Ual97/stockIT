from os import abort
from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort, url_for
from website import db
from website.models.product import Product
from website.models.branch import Branch
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from sqlalchemy import and_


inventory = Blueprint('inventory', __name__)

@inventory.route('/inventory', methods=['GET', 'POST'])
@login_required
def inv():
    #if user is not confirmed, block access and send to home
    if current_user.confirmed is False:
        flash('Please confirm your account, check your email (and spam folder)', 'error')
        return redirect(url_for('views.home'))

    """main page of inventory"""
    if request.method == 'POST':
        prodDict = request.form.to_dict()
        name = prodDict.get('name')    
        branch = prodDict.get('branch')
        qty = prodDict.get('quantity')
        cost = prodDict.get('cost')
        price = prodDict.get('price')
        expiry = prodDict.get('expiry')
        reserved = prodDict.get('qty_reserved')
        cbarras = prodDict.get('qr_barcode')
        
        if cost == '' or cost == 'None':
            prodDict['cost'] = None
        if price == '' or price == 'None':
            prodDict['price'] = None
        if expiry == '' or expiry == 'None':
            prodDict['expiry'] = None
        if reserved == '' or reserved == 'None':
            prodDict['qty_reserved'] = None
        if cbarras == '' or cbarras == 'None':
            prodDict['qr_barcode'] = None
    
        if name and branch and qty:
            prodDict['owner'] = current_user.email
            new_prod = Product(**prodDict)
            db.session.add(new_prod)
            db.session.commit()
            flash("Poduct added", category='success')
            return redirect('/inventory')
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
    return render_template('inventory.html', user=current_user,
                           branches=branches, nextid=nextid, products=data)

@inventory.route('/inventory/<id>', methods=['POST','GET'], strict_slashes=False)
@login_required
def Put(id):
    """updating or consulting item from inventory"""
    item = Product.query.get(id)

    if request.method == 'POST':
        prodDict = request.form.to_dict()
        if prodDict is None:
            abort(404)
        debugKeys = prodDict.keys()

        keys = ('nameUpdate', 'branchesUpdate', 'quantityUpdate', 'costUpdate', 'priceUpdate', 'expiryUpdate', 'qty_reservedUpdate', 'qr_barcodeUpdate')

        print(f'\n\nlas keys del form: {debugKeys} \n\n keys set: {keys}\n\n diccionario antes de update: {item.__dict__}\n\n datos nuevos: {prodDict}')
        pos = 0
        for pos in range(len(keys)):
            if pos == 0:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if type(prodDict[keys[pos]]) is str:
                        item.name = prodDict[keys[pos]]
            if pos == 1:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if type(prodDict[keys[pos]]) is str:
                        item.branch = prodDict[keys[pos]]
            if pos == 2:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    print(f'\n\n\ntype de esta mierda{type(prodDict[keys[pos]])}\n\n')
                    if prodDict[keys[pos]].isdigit() is True:
                        item.quantity = prodDict[keys[pos]]
            if pos == 3:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if prodDict[keys[pos]].isdigit() is True:
                        item.cost = prodDict[keys[pos]]
            if pos == 4:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if prodDict[keys[pos]].isdigit() is True:
                        item.price = prodDict[keys[pos]]
            if pos == 5:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    item.expiry = prodDict[keys[pos]]
            if pos == 6:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if prodDict[keys[pos]].isdigit() is True:
                        item.qty_reserved = prodDict[keys[pos]]
            if pos == 7:
                if prodDict[keys[pos]] != '' and prodDict[keys[pos]] != 'None':
                    if prodDict[keys[pos]].isdigit() is True:
                        item.qr_barcode = prodDict[keys[pos]]
        print(f'diccionario desp {item.__dict__}')
        
        db.session.commit()

        flash('Item updated successfully!')
        
        return redirect('/inventory')
    try:
        # filter query by logged user and id
        product = Product.query.filter(and_(Product.owner==current_user.email, Product.id==id)).first()
        
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

@inventory.route('/inventory/delete/<id>', strict_slashes=False)
@login_required
def Delete(id):
    """inventory page"""
    db.session.delete(Product.query.get(id))
    db.session.commit()
    flash('Item deleted successfully!')
    print(f'\n\n\naaaaaaaaaaaa{request.url_rule}\n\n\n')
    return redirect('/inventory')