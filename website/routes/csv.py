from flask import Blueprint, render_template, flash, redirect, send_file, url_for 
from website import db, limiter
from website.models.movements import Movements
from website.models.inventory import Inventory
from website.models.branch import Branch 
from website.models.csv import UploadFileForm, UploadFileForm2, UploadFileForm3 
from website.models.product import Product
from website.models.cost_qty import Cost_qty
from website.models.profits import Profits
from website.routes.product import generate_qr, generate_barcode
from flask_login import login_required, current_user 
from sqlalchemy.sql.expression import func 
from sqlalchemy import and_ 
from flask import Flask, render_template  
from werkzeug.utils import secure_filename 
from sqlalchemy import and_, desc
import requests
import os 
import csv
import math
from datetime import datetime

csv_v = Blueprint('csv', __name__) 
 
@csv_v.route('/csv', methods=['GET', 'POST'], strict_slashes=False) 
@limiter.limit("20/minute")
@login_required
def dic_csv():  
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
                    date = line.get('date')
                    name = line.get('product')
                    names2 = Product.query.filter_by(owner=current_user.email).all()
                    listNames = []
                    for name2 in names2:
                        listNames.append(name2.name)
                    if name not in listNames:
                        flash("The product must already be created", category='error')
                        return redirect('/movements') 
                    branch = line.get('branch')
                    branches = Branch.query.filter_by(owner=current_user.email).all()
                    listBranches = []
                    for branch2 in branches:
                        listBranches.append(branch2.name)
                    if branch not in listBranches:
                        flash("The branch must already be created", category='error')
                        return redirect('/movements') 
                    qty = line.get('quantity')

                    if (qty.replace('-', '', 1).isnumeric()):
                        qty = int(qty)
                    else:
                        flash("Quantity has to be a number.", category='error')
                        return redirect('/movements')
                    price_cost =  line.get('cost/price')
                    if (price_cost.replace('-', '', 1).isnumeric()):
                        price_cost = float(price_cost)
                        line['price_cost'] = price_cost
                    else:
                        flash("Cost/Price has to be a number.", category='error')
                        return redirect('/movements')
                    print("xddddddd", price_cost)
                    
                    currency = line.get('UYU/USD')
                    if currency and currency.upper() == 'UYU' or currency.upper() == 'USD':
                        line['currency'] = True if currency.upper() == 'USD' else False 
                    else:
                        flash("Currency has to be USD or UYU")                     
                    print("kakaka")
                    print(f'tiṕo ***{type(date)}*** largo ***{len(date)}***')
                    print("kakaka")
                    if len(date) > 0 and date != 'None' and date != '':
                        print("entre a la chucha del if")
                        try:
                            print(str(line.get('date')) + ' 00:00:00')
                            line['date'] = datetime.strptime(str(line.get('date')) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
                        except:
                            flash("Date need the format '%Y-%m-%d'", category='error')
                            return redirect('/movements')

                    in_out = line.get('action')
                    if in_out == 'in':
                        in_out = True
                        line['in_out'] = True
                    elif in_out == 'out':
                        in_out = False
                        line['in_out'] = False
                    else:
                        flash("Action must be 'in' or 'out'", category='error')
                        return redirect('/movements')

                    if name and branch and qty:
                        line['owner'] = current_user.email
                        branch2 = Branch.query.filter_by(name=branch).first()
                        line['branch_id'] = branch2.id
                        prod = Product.query.filter_by(name=name).first()
                        print(prod)
                        line['prod_id'] = prod.id
                        # checking if exists prevs entries of this new entrie in all branches
                        prodMov = Movements.query.filter_by(prod_id=prod.id).order_by(desc(Movements.date)).all()
                        # checking if exists prevs entries of this new entry in their respective branch
                        branchStock = Movements.query.filter(and_(Movements.prod_id == prod.id, Movements.branch_id == branch2.id)).order_by(desc(Movements.date)).all()

                        if not branchStock and in_out == False:
                            flash('Error. Cannot make outs of products on branch without stock', category='error')
                            return redirect('/movements')
                        # checking if branch has stock before make outs of products
                        itemQuantity = 0
                        for item in branchStock:
                            print((item.quantity))
                            if item.in_out is True:
                                print(item.quantity)
                                itemQuantity += int(item.quantity)
                            else:
                                itemQuantity -= int(item.quantity)
                        if itemQuantity < qty and in_out is False:
                            flash('Error. Cannot make outs of products greather than branch stock', category='error')
                            return redirect('/movements')
                        if qty < 0:
                            flash('Error. Cannot make movements of numbers lower than 0', category='error')
                            return redirect('/movements')
                        if not prodMov and in_out == False:
                            flash('Error. Cannot make outs of products without stock', category='error')
                            return redirect('/movements')
                        new_prod = Movements(**line)
                        db.session.add(new_prod)

                        item2 = Movements.query.filter_by(prod_id=prod.id).order_by(desc(Movements.date)).all()
                        for item in item2:
                            print(item.date)
                        prodMov = Movements.query.filter_by(prod_id=prod.id).order_by(desc(Movements.date)).all()
                        if len(prodMov) == 1:
                            """new product to the inventory"""
                            print(f'\n\n\nvamos a hacer un nuevo producto :3\n\n')
                            newItemInv = {}
                            newItemInv['owner'] = current_user.email
                            newItemInv['prod_id'] = prod.id
                            newItemInv['quantity'] = qty
                            newItem = Inventory(**newItemInv)
                            db.session.add(newItem)
                            
                            """adding item to cost_cant table"""
                
                            dict = {}
                            
                            dict['owner'] = current_user.email
                            dict['prod_id'] = prod.id
                            dict['branch_id'] = branch2.id
                            dict['date'] = prodMov[0].date
                            dict['cost'] = price_cost
                            dict['quantity'] = qty
                            dict['qty_sold'] = 0
                            dict['sold'] = False
                            dict['currency'] = prodMov[0].currency
                            newItem = Cost_qty(**dict)
                            db.session.add(newItem)
                            db.session.commit()
                        else:
                            """quantity addition of the product"""
                            item = Inventory.query.filter_by(prod_id=prod.id).first()
                            if in_out is True:
                                print(f'\n\n\nle sumamos al producto :3\n\n')
                                item.quantity += qty
                                
                                """adding item to cost_qty table"""

                                dict = {}

                                dict['owner'] = current_user.email
                                dict['prod_id'] = prod.id
                                dict['branch_id'] = branch2.id
                                dict['date'] = prodMov[0].date
                                dict['cost'] = price_cost
                                dict['quantity'] = qty
                                dict['qty_sold'] = 0
                                dict['sold'] = False
                                dict['currency'] = prodMov[0].currency
                                newItem = Cost_qty(**dict)
                                db.session.add(newItem)
                                
                            elif in_out is False and qty > item.quantity or item.quantity is None:
                                print(f'\n\n\nflasheaste :3\n\n')
                                flash('Error. Cannot make outs of products without stock', category='error')
                                redirect('/movements')
                            else:
                                print(f'\n\n\nle restamos el producto :3\n\n')
                                item.quantity -= qty
                                """adding new item to price-cant json if not exists is
                                created and if the item exists make an addition
                                """

                                cost_qty = Cost_qty.query.filter((Cost_qty.prod_id==prod.id) & (Cost_qty.sold == False) & (Cost_qty.branch_id == branch2.id)).order_by(Cost_qty.date.asc()).all()
                                i = 1
                                dollar = None
                                profitList = []
                                for j in range(qty, 0, -1):
                                    flag = True
                                    if cost_qty[-i].qty_sold == cost_qty[-i].quantity - 1:
                                        cost_qty[-i].qty_sold += 1                            
                                        cost_qty[-i].sold = True
                                        flag = False
                                    if cost_qty[-i].currency is True and prodMov[0].currency is False:
                                        if not dollar:
                                            dollar = requests.get(f'https://cotizaciones-brou.herokuapp.com/api/currency/{str(prodMov[0].date.date())}')
                                            dollar = dollar.json()['rates']['USD']['sell']
                                        unitprofit = (price_cost - (cost_qty[-i].cost * dollar))
                                        print(f'\nunit profit {unitprofit} iteracion {j}')
                                        profitList.append(unitprofit)
                                    elif cost_qty[-i].currency is False and prodMov[0].currency is True:
                                        if not dollar:
                                            dollar = requests.get(f'https://cotizaciones-brou.herokuapp.com/api/currency/{str(prodMov[0].date.date())}')
                                            dollar = dollar.json()['rates']['USD']['sell']
                                        unitprofit = (price_cost  - (cost_qty[-i].cost / dollar))
                                        profitList.append(unitprofit)
                                    else:
                                        unitprofit = price_cost - cost_qty[-i].cost
                                        profitList.append(unitprofit)
                                    if flag:
                                        cost_qty[-i].qty_sold += 1
                                    else:
                                        i += 1
                                        dollar = None

                                print(f"\n profitlist {profitList} suma de los profits {math.fsum(profitList)}")
                                profitDict = {}
                                profitDict['prod_id'] = prod.id
                                profitDict['owner'] = current_user.email
                                profitDict['profit'] = math.fsum(profitList)
                                profitDict['date'] = prodMov[0].date
                                profitDict['quantity'] = qty
                                profitDict['branch_id'] = prodMov[0].branch_id
                                profitDict['currency'] = prodMov[0].currency
                                newItem = Profits(**profitDict)
                                db.session.add(newItem)

                            db.session.commit()
                    else:
                        flash('Name, Branch, Quantity and Action are mandatory fields', category='error')
                        return redirect('/movements')
                db.session.commit()
                flash("Movement/s added", category='success')
                return redirect('/movements')
        else:
            flash("Your file must have extension '.csv'", category='error')
    #### Add Branches via CSV ####
    form2 = UploadFileForm2() 
    if form2.validate_on_submit(): 
        from main import app     
        file = form2.file2.data 
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        filename, file_extension = os.path.splitext(file.filename)
        print(file_extension)
        branches = Branch.query.filter_by(owner=current_user.email)
        print(branches)
        if file_extension == '.csv':
            with open(os.path.abspath(os.path.dirname(__file__)) + '/files/' + file.filename, 'r') as data:
                for line in csv.DictReader(data):
                    branch_name = line.get('branch')
                    print(f'\n\n\n{line}\n\n')
                    if not branch_name:
                        flash('Branch is mandatory', category='error')
                        return redirect(url_for('subsidiary.subsidiary_view'))

                    if type(branch_name) != str:
                        flash('Branch must be a string', category='error')
                        return redirect(url_for('subsidiary.subsidiary_view'))

                    branch_name = branch_name.strip()

                    line['name'] = branch_name

                    currentBranch = currentBranch = Branch.query.filter((Branch.name==branch_name) & (Branch.owner==current_user.email)).first()
                    if currentBranch:
                        currentBranchName = currentBranch.name.strip()
                        print(f"\n\n\nnew {branch_name.lower()} current {currentBranchName.lower()}\n\n")
                        if branch_name.lower() == currentBranchName.lower():
                            flash('This branch already exists "' + str(branch_name) + '"', category='error')
                            return redirect(url_for('subsidiary.subsidiary_view'))

                    line['owner'] = current_user.email
                    new_branch = Branch(**line)
                    db.session.add(new_branch)
                    db.session.commit()
                flash('Branches added', category='success')
                return redirect(url_for('subsidiary.subsidiary_view'))
    #### Add Products via CSV ####
    form3 = UploadFileForm3() 
    if form3.validate_on_submit(): 
        from main import app     
        file = form3.file3.data 
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        filename, file_extension = os.path.splitext(file.filename)
        print(file_extension)
        branches = Branch.query.filter_by(owner=current_user.email)
        print(branches)
        if file_extension == '.csv':
            with open(os.path.abspath(os.path.dirname(__file__)) + '/files/' + file.filename, 'r') as data:
                for line in csv.DictReader(data):
                    name = line.get('product')    
                    qr_barcode = line.get('qr_barcode')
                    description = line.get('description')


                    if name:
                        name = name.strip()
                        currentName = Product.query.filter((Product.name==name) & (Product.owner==current_user.email)).first()
                        if currentName and name.lower() == currentName.name.lower():
                            flash('Product already exists "' + str(name)  + '"', 'error')
                            return redirect(url_for('product.prod'))

                        line['name'] = name
                        # adding new product instance to database
                        line['owner'] = current_user.email
                        if description == '' or description is None:
                            line['description'] = 'No description'
                        new_prod = Product(**line)
                        db.session.add(new_prod)
                        db.session.commit()
                        if qr_barcode == 'qr':
                            generate_qr(new_prod.id)
                        elif qr_barcode == 'barcode':
                            generate_barcode(new_prod.id)
                        else:
                            generate_qr(new_prod.id)
                        db.session.commit()
                        #print(f'\n\n\n{new_prod.qr_barcode}\n\n')
                    else:
                        print("HELLOOWEWE")
                        flash('Product is a mandatory field', category='error')
                        return redirect(url_for('product.prod'))
                flash("Poducts added", category='success')
                return redirect('/product')
    return render_template('csv.html', user=current_user, form3=form3, form2=form2, form=form)
@csv_v.route('/csv/download', methods=['GET', 'POST'], strict_slashes=False) 
@limiter.limit("20/minute")
@login_required
def download_file_movement():
    print("downloaaaad")
    return send_file("routes/files/csv_templates/movement_template.csv", as_attachment=True)
@csv_v.route('/csv/download2', methods=['GET', 'POST'], strict_slashes=False) 
@limiter.limit("20/minute")
@login_required
def download_file_product():
    print("downloaaaad")
    return send_file("routes/files/csv_templates/product_template.csv", as_attachment=True)
@csv_v.route('/csv/download3', methods=['GET', 'POST'], strict_slashes=False) 
@limiter.limit("20/minute")
@login_required
def download_file_branch():
    print("downloaaaad")
    return send_file("routes/files/csv_templates/branch_template.csv", as_attachment=True)