from flask import Blueprint, render_template, request, flash, redirect, url_for
from website import db
from website.models.product import Product
from website.models.sucursal import Sucursal
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from datetime import datetime

inventory = Blueprint('inventory', __name__)

@inventory.route('/inventario')
@login_required
def inv():
    """ returns prduct list of current user with pagination"""
    data = Product.query.filter_by(owner=current_user.email).paginate(per_page=10)
    print(f'\n\n\ndata pal render: {data.query.values()}\n\n')
    return render_template('inventario.html', user=current_user, products=data)

@inventory.route('/inventario/add', methods=['GET', 'POST'])
@login_required
def InvAdd():
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
            return redirect('/inventario/add')
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
    return render_template('add.html', user=current_user,
                           sucursales=sucs, nextid=nextid, products=data)

@inventory.route('/inventario/update/<id>', methods=['POST','GET'], strict_slashes=False)
@login_required
def Put(id):
    """updating or consulting item from inventory"""
    item = Product.query.get(id)

    if request.method == 'POST':

        item.name = request.form.get('pname') if request.form.get('pname\
') != 'None' else item.name

        item.sucursal = request.form.get('sucursal') if request.form.get('\
sucursal') != 'None' else item.sucursal

        item.quantity = request.form.get('cant') if request.form.get('\
cant') != 'None' else item.quantity
        
        item.cost = request.form.get('cost') if request.form.get('cost') != '\
None' else item.cost
        
        item.price = request.form.get('price') if request.form.get('price') != '\
None' and request.form.get('price') != '' else item.price
        
        item.expiry = datetime.strptime(request.form.get('expiry'), '%d/%m/%Y').date() if request.form.get('expiry\
') != 'None' and request.form.get('expiry').replace('/', '\
').isnumeric() != False and request.form.get('expiry') != '' else item.expiry
        
        item.qty_reserved = request.form.get('qty_reserved') if request.form.\
get('qty_reserved') != 'None' and request.form.get('qty_reserved') != '' else item.qty_reserved
        
        item.qr_barcode = request.form.get('qr_barcode') if request.form.get(\
'qr_barcode') != 'None' else item.qr_barcode
        
        db.session.commit()

        flash('Item updated successfully!')
        
        return redirect('/inventario')
    # sucursales to display as options in add product table
    sucs = Sucursal.query.filter_by(owner=current_user.email)
    data = Product.query.filter_by(owner=current_user.email).paginate(per_page=10)    
    return render_template('update.html', user=current_user, item=item,
                           sucursales=sucs, products=data)

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