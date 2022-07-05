from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort, url_for
from website import db, limiter
from website.models.cost_qty import Cost_qty
from website.models.movements import Movements
from website.models.branch import Branch
from website.models.product import Product
from website.models.inventory import Inventory
from website.models.profits import Profits
from flask_login import login_required, current_user
from sqlalchemy import and_, or_, desc, asc
import requests


movements = Blueprint('movements', __name__)

@movements.route('/movements', methods=['GET', 'POST'], strict_slashes=False)
@limiter.limit("20/minute")
@login_required
def move():
    """movements of products"""

    #if user is not confirmed, block access and send to home
    #if current_user.confirmed is False:
    #    flash('Please confirm your account, check your email (and spam folder)', 'error')
    #    return redirect(url_for('views.home'))

    graph_data = {'Task' : 'Hours per Day'}
    graph_data2 = {'Task' : 'Hours per Day'}
    graph_data3 = {'Task' : 'Hours per Day'}
    graph_data4 = {'Task' : 'Hours per Day'}

    # branches and products to display as options in add entry table
    branches = Branch.query.filter_by(owner=current_user.email)
    products = Product.query.filter_by(owner=current_user.email)

    # getting all current user's movements from db (more recent movements first)
    data = Movements.query.filter_by(owner=current_user.email).order_by(desc(Movements.date)).all()
    # filling a list of movements to paass them to jinja. Each movement is a dict
    movementsList = []
    for item in data:
        movementDict = {}
        movementDict['id'] = item.id
        movementDict['product'] = Product.query.filter_by(id=item.prod_id).first().name
        movementDict['branch'] = Branch.query.filter_by(id=item.branch_id).first().name
        movementDict['quantity'] = item.quantity
        movementDict['price_cost'] = item.price_cost
        movementDict['date'] = item.date
        movementDict['in_out'] = "Entry" if item.in_out is True else "Exit"
        movementDict['currency'] = "USD" if item.currency is True else "UYU"
        movementsList.append(movementDict)
        
        # filling movement data for pie charts
        if movementDict['in_out'] == 'Entry':
            if movementDict['product'] in graph_data:
                graph_data[movementDict['product']] += movementDict['quantity']
            else: 
                graph_data[movementDict['product']] = movementDict['quantity']

        if movementDict['in_out'] == 'Exit':
            if movementDict['product'] in graph_data2:
                graph_data2[movementDict['product']] += movementDict['quantity']
            else: 
                graph_data2[movementDict['product']] = movementDict['quantity']

        for selectedBranch2 in Branch.query.filter_by(owner=current_user.email).all():
            print(selectedBranch2.name)
            if movementDict['in_out'] == 'Entry' and selectedBranch2.name == movementDict['branch']:
                if movementDict['product'] + " On(" + movementDict['branch'] + ")" in graph_data3:
                    graph_data3[movementDict['product'] + " On (" + movementDict['branch'] + ")"] += movementDict['quantity']
                else: 
                    graph_data3[movementDict['product'] + " On (" + movementDict['branch'] + ")"] = movementDict['quantity']
            if movementDict['in_out'] == 'Exit' and selectedBranch2.name == movementDict['branch']:
                if movementDict['product'] + " On(" + movementDict['branch'] + ")" in graph_data4:
                    graph_data4[movementDict['product'] + " On (" + movementDict['branch'] + ")"] += movementDict['quantity']
                else: 
                    graph_data4[movementDict['product'] + " On (" + movementDict['branch'] + ")"] = movementDict['quantity']

    # if user presses Search button
    if request.method == 'POST' and "btn-srch" in request.form:
        # show branches and products for add movement row
        branches = Branch.query.filter_by(owner=current_user.email)
        products = Product.query.filter_by(owner=current_user.email)
        
        search = request.form.get("search")
        if search:
            search = search.strip()
        orderby = request.form.get("orderby")
        
        #checks that movements are from user
        userprod = Movements.query.filter(Movements.owner == current_user.email)

        searchProduct = Product.query.filter_by(name=search).first()
        searchProduct = "None" if not searchProduct else str(searchProduct.id)

        searchBranch = Branch.query.filter_by(name=search).first()
        searchBranch = "None" if not searchBranch else str(searchBranch.id)

        # search input section
        srch = userprod.filter(or_(Movements.date.like(search),
                                   Movements.prod_id.like(searchProduct),
                                   Movements.branch_id.like(searchBranch)))
 
        # Order By select section
        if orderby == 'newest' and search:
            data = srch.order_by(asc(Movements.date)).all()
        elif orderby == 'newest' and not search:
            print(f"\n\n\n{srch}\n\n")
            data = userprod.order_by(desc(Movements.date)).all()
        elif orderby == 'oldest' and search:
            data = srch.order_by(desc(Movements.date)).all()
        elif orderby == 'oldest' and not search:
            data = userprod.order_by(asc(Movements.date)).all()
        else:
            data = srch
        movementsList = []
        # filling movements history to be displayed by jinja
        for item in data:
            movementDict = {}
            movementDict['id'] = item.id
            movementDict['product'] = Product.query.filter_by(id=item.prod_id).first().name
            movementDict['branch'] = Branch.query.filter_by(id=item.branch_id).first().name
            movementDict['quantity'] = item.quantity
            movementDict['date'] = item.date
            movementDict['in_out'] = "Entry" if item.in_out is True else "Exit"
            movementDict['currency'] = "USD" if item.currency is True else "UYU"
            movementsList.append(movementDict)
        if not movementsList and not orderby:
            flash('No results found', 'error')
            return redirect('/movements')
        print(f'\n{movementDict}')

        return render_template('movements.html', user=current_user,
                            branches=branches, products=products, movements=movementsList, data=graph_data, data2=graph_data2, data3=graph_data3, data4=graph_data4)

    if request.method == 'POST' and "btn-add" in request.form:
        prodDict = request.form.to_dict()
        name = prodDict.get('name')    
        branch = prodDict.get('branch')
        qty = prodDict.get('quantity')
        if (qty.replace('-', '', 1).isnumeric()):
            qty = int(qty)
        else:
            flash("Quantity has to be a number.", category='error')
            return redirect('/movements')

        currency = prodDict.get('currency')
        if currency == 'USD':
            currency = True
            prodDict['currency'] = True
        else:
            currency = False
            prodDict['currency'] = False

        in_out = prodDict.get('in_out')
        if in_out == 'in':
            in_out = True
            prodDict['in_out'] = True
        else:
            in_out = False
            prodDict['in_out'] = False


        price_cost = prodDict.get('price_cost')
        if (price_cost.replace('-', '', 1).replace('.', '', 1).isnumeric()):
            price_cost = float(price_cost)
        else:
            if in_out is True:
                flash("Cost has to be a number.", category='error')
            else:
                flash("Price has to be a number.", category='error')

            return redirect('/movements')

        
        if name and branch and qty and price_cost:
            prodDict['owner'] = current_user.email
            branch2 = Branch.query.filter_by(name=branch).first()
            prodDict['branch_id'] = branch2.id
            prod = Product.query.filter_by(name=name).first()
            prodDict['prod_id'] = prod.id
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
                if item.in_out is True:
                    itemQuantity += item.quantity
                else:
                    itemQuantity -= item.quantity
            if itemQuantity < qty and in_out is False:
                flash('Error. Cannot make outs of products greather than branch stock', category='error')
                return redirect('/movements')
            print(f'\n\n\nlargo: {len(prodMov)} movement: {in_out} pelado: {prodMov}\n\n')
            if qty < 1:
                flash('Error. Cannot make movements of numbers lower than 1', category='error')
                return redirect('/movements')
            if not prodMov and in_out == False:
                print("\n\nbolas\n")
                flash('Error. Cannot make outs of products without stock', category='error')
                return redirect('/movements')
            new_prod = Movements(**prodDict)
            db.session.add(new_prod)
            db.session.commit()

            item2 = Movements.query.filter_by(prod_id=prod.id).order_by(desc(Movements.date)).all()
            for item in item2:
                print("aaaaaaasheeee")
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
                db.session.commit()

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

                item = Inventory.query.filter_by(prod_id=prod.id).first()
                if in_out is True:
                    """quantity addition of the product in inventory"""
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
                    """quantity substraction of the product in inventory"""
                    print(f'\n\n\nle restamos al producto :3\n\n')
                    item.quantity -= qty

                    """adding new item to price-cant json if not exists is
                       created and if the item exists make an addition
                    """
                    profit = 0
                    cost_qty = Cost_qty.query.filter((Cost_qty.prod_id==prod.id) & (Cost_qty.sold == False) & (Cost_qty.branch_id == branch2.id)).order_by(Cost_qty.date.asc()).all()
                    i = 1
                    dollar = None
                    for _ in range(qty, 0, -1):
                        flag = True
                        if cost_qty[-i].qty_sold == cost_qty[-i].quantity - 1:
                            cost_qty[-i].qty_sold += 1                            
                            cost_qty[-i].sold = True
                            flag = False
                        if cost_qty[-i].currency is True and prodMov[0].currency is False:
                            if not dollar:
                                dollar = requests.get(f'https://cotizaciones-brou.herokuapp.com/api/currency/{str(prodMov[0].date.date())}')
                                dollar = dollar.json()['rates']['USD']['sell']
                            profit += price_cost - (cost_qty[-i].cost * dollar)
                        if cost_qty[-i].currency is False and prodMov[0].currency is True:
                            if not dollar:
                                dollar = requests.get(f'https://cotizaciones-brou.herokuapp.com/api/currency/{str(prodMov[0].date.date())}')
                                dollar = dollar.json()['rates']['USD']['sell']
                            print(f'\nde dolares a pesos pesos{price_cost} pesos convertidos{(price_cost / dollar)} dolares {cost_qty[-i].cost}')
                            profit += price_cost  - (cost_qty[-i].cost / dollar)
                        else:
                            profit += price_cost - cost_qty[-i].cost
                        if flag:
                            cost_qty[-i].qty_sold += 1
                        else:
                            i += 1
                            dollar = None


                    profitDict = {}
                    profitDict['prod_id'] = prod.id
                    profitDict['owner'] = current_user.email
                    profitDict['profit'] = profit
                    profitDict['date'] = prodMov[0].date
                    profitDict['quantity'] = qty
                    profitDict['branch_id'] = prodMov[0].branch_id
                    profitDict['currency'] = prodMov[0].currency
                    newItem = Profits(**profitDict)
                    db.session.add(newItem)



                db.session.commit()
            return redirect('/movements')
        else:
            flash('Name, Branch and Quantity are mandatory fields', category='error')
    
    return render_template('movements.html', user=current_user,
                           movements=movementsList,
                           branches=branches, products=products, data=graph_data, data2=graph_data2, data3=graph_data3, data4=graph_data4)