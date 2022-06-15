from os import abort 
from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort, url_for 
from website import db 
from website.models.product import Product 
from website.models.branch import Branch 
from website.models.csv import UploadFileForm 
from website.routes.product import generate_qr, generate_barcode
from flask_login import login_required, current_user 
from sqlalchemy.sql.expression import func 
from sqlalchemy import and_ 
from flask import Flask, render_template  
from werkzeug.utils import secure_filename 
import os 
from wtforms.validators import InputRequired 
import csv
from datetime import datetime

csv_v = Blueprint('csv', __name__) 
 
@csv_v.route('/csv', methods=['GET', 'POST'], strict_slashes=False) 
@login_required 
def dic_csv(): 
    #if user is not confirmed, block access and send to home 
    if current_user.confirmed is False: 
        flash('Please confirm your account, check your email (and spam folder)', 'error') 
        return redirect(url_for('views.home')) 
    form = UploadFileForm() 
    if form.validate_on_submit(): 
        from main import app     
        file = form.file.data 
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        filename, file_extension = os.path.splitext(file.filename)
        print(file_extension)
        branches = Branch.query.filter_by(owner=current_user.email)
        print(branches)
        if file_extension == '.csv':
            with open(os.path.abspath(os.path.dirname(__file__)) + '/files/' + file.filename, 'r') as data:
                for line in csv.DictReader(data):
                    name = line.get('name')
                    branch = line.get('branch')
                    qty = line.get('quantity')
                    cost = line.get('cost')
                    price = line.get('price')
                    expiry = line.get('expiry')
                    reserved = line.get('qty_reserved')
                    cbarras = line.get('qr_barcode')
                    
                    branches = Branch.query.filter_by(owner=current_user.email).all()
                    listBranches = []
                    for branch2 in branches:
                        listBranches.append(branch2.name)
                    if branch not in listBranches:
                        flash("The branch must be created", category='error')
                        return redirect('/inventory') 

                    if cost == '' or cost == 'None':
                        line['cost'] = None
                    elif cost.isnumeric() is False:
                        flash("Quantity, cost, price and reserved have to be numbers.", category='error')
                        return redirect('/inventory') 
                    if price == '' or price == 'None':
                        line['price'] = None
                    elif price.isnumeric() is False:
                        flash("Quantity, cost, price and reserved have to be numbers.", category='error')
                        return redirect('/inventory') 
                    if expiry == '' or expiry == 'None':
                        line['expiry'] = None
                    else:
                        try:
                            line['expiry'] = datetime.strptime(line.get('expiry'), "%Y-%m-%d")
                        except:
                            flash("Expiry need the format '%Y-%m-%d'", category='error')
                            return redirect('/inventory')
                    if reserved == '' or reserved == 'None':
                        line['qty_reserved'] = None
                    elif reserved.isnumeric() is False:
                        flash("Quantity, cost, price and reserved have to be numbers.", category='error')
                        return redirect('/inventory') 

                    if name and branch and qty:
                        if qty.isnumeric() is False:
                            flash("Quantity, cost, price and reserved have to be numbers.", category='error')
                            return redirect('/inventory')
                        line['owner'] = current_user.email
                        new_prod = Product(**line)
                        db.session.add(new_prod)
                        db.session.commit()
                        if line.get('qr_barcode') == 'qr':
                            generate_qr(new_prod.id)
                        elif line.get('qr_barcode') == 'barcode':
                            new_prod.qr_barcode = generate_barcode(new_prod.id)
                            db.session.commit()
                        #print(f'\n\n\n{new_prod.qr_barcode}\n\n')
                    else:
                        flash('Name, Branch and Quantity are mandatory fields', category='error')
                        return redirect('/inventory')
                flash("Poducts added", category='success')
                return redirect('/inventory')
                #db.session.commit()
                #print(f'\n\n\n{new_prod.qr_barcode}\n\n')
        else:
            flash("Your file must have extension '.csv'", category='error')
    return render_template('csv.html', user=current_user, form=form)