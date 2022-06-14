from os import abort 
from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort, url_for 
from website import db 
from website.models.product import Product 
from website.models.branch import Branch 
from website.models.csv import UploadFileForm 
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
        with open(os.path.abspath(os.path.dirname(__file__)) + '/files/' + file.filename, 'r') as data:
            for line in csv.DictReader(data):
                print(line)
                name = line.get('name')    
                branch = line.get('branch')
                qty = line.get('quantity')
                cost = line.get('cost')
                price = line.get('price')
                expiry = line.get('expiry')
                reserved = line.get('qty_reserved')
                cbarras = line.get('qr_barcode')
                
                if cost == '' or cost == 'None':
                    line['cost'] = None
                if price == '' or price == 'None':
                    line['price'] = None
                if expiry == '' or expiry == 'None':
                    line['expiry'] = None
                else:
                    line['expiry'] = datetime.strptime(line.get('expiry'), "%Y-%m-%d")
                if reserved == '' or reserved == 'None':
                    line['qty_reserved'] = None
                if cbarras == '' or cbarras == 'None':
                    line['qr_barcode'] = None
            
                if name and branch and qty:
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
            flash("Poduct added", category='success')
            return redirect('/inventory')
            #db.session.commit()
            #print(f'\n\n\n{new_prod.qr_barcode}\n\n')
        return "File has been uploaded." 
    return render_template('csv.html', user=current_user, form=form)