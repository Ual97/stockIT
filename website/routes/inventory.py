from website.models.product import Product
from website.models.movements import Movements
from website.models.branch import Branch
from website.models.inventory import Inventory
from flask_login import login_required
from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort, url_for
from flask_login import login_required, current_user
from sqlalchemy import and_, asc
from website import limiter

inventory = Blueprint('inventory', __name__)

@login_required
@limiter.limit("10/minute")
@inventory.route('/inventory', methods=['GET', 'POST'], strict_slashes=False)
def inventory_page():
    """inventory page"""

    #if user is not confirmed, block access and send to home
    #if current_user.confirmed is False:
    #    flash('Please confirm your account, check your email (and spam folder)', 'error')
    #    return redirect(url_for('views.home'))

    graph_data = {'Task' : 'Products per branch'}

    formDict = request.form.to_dict()

    # store some  product name if some product is searched
    search = formDict.get('search')
    search = search.lower().strip() if search else None

    border_case = False

    # consulting stock from all branches
    stockQuery = Inventory.query.filter_by(owner=current_user.email).all()
    stock = []
    # filling stock dictionary with prod name, quantity, description and product id
    for item in stockQuery:
        stockItem = {}
        product = Product.query.filter_by(owner=current_user.email).filter_by(id=item.prod_id).first()
        # if search not in product name then its not listed
        if search and search not in product.name.lower():
            continue
        stockItem['name'] = product.name
        stockItem['quantity'] = item.quantity
        stockItem['branch'] = "All Branches"
        stockItem['description'] = product.description
        stockItem['id'] = item.prod_id
        stockItem['qr_barcode'] = product.qr_barcode

        stock.append(stockItem)
        
        graph_data[product.name] = item.quantity
    if search and not stock:
        flash("No items with that name", "error")
        return redirect('/inventory')

    # if user presses Search
    if request.method == 'POST' and "btn-srch" in request.form:

        selectedBranch = formDict.get('selectBranch')

        # filtering by branch
        if selectedBranch != 'All Branches (default)':
            selectedBranch = Branch.query.filter_by(owner=current_user.email).filter_by(name=selectedBranch).first()
            item_no_quantity = []
            for item in stock:
                # calculating the current stock for specific branch
                currentStock = 0
                for mov in Movements.query.filter_by(owner=current_user.email).filter(and_(
                                                                                      Movements.prod_id == item['id'],
                                                                                      Movements.branch_id == selectedBranch.id)).all():
                    if mov.in_out is True:
                        currentStock += mov.quantity
                    elif mov.in_out is False:
                        currentStock -= mov.quantity
                item['quantity'] = currentStock
                item['branch'] = selectedBranch.name
                graph_data[item['name']] = item['quantity']
                print(item)

                if item['quantity'] == 0:
                    item_no_quantity.append(item)    
            for item2 in item_no_quantity:
                stock.remove(item2)

        selectedBranch = formDict.get('selectBranch')

        if selectedBranch != 'All Branches (default)' and search:
            prod_id = Product.query.filter_by(name=search).first().id
            branch_id = Branch.query.filter_by(name=selectedBranch).first().id
            print(f'\n\n\nbranch_id {prod_id}\n\n')
            prodMovements = Movements.query.filter((Movements.branch_id==branch_id) & (Movements.prod_id==prod_id) & (Movements.owner==current_user.email)).order_by(asc(Movements.date)).all()
            graph_data = [['Date', 'Entries', 'Outs']]

            print(f'\n\n\nprodMovements antes del for: {prodMovements}\n\n')
            prev = None
            prodMovementsLen = len(prodMovements)
            for i in range(prodMovementsLen):
                print(f'\n\n\n{prodMovements[i].__dict__}\n\n')
                print(f'\n\nmov date : {str(prodMovements[i].date.date())} prev: {prev}\n')
                if not prev:
                    new_data = [0, 0, 0]
                    new_data[0] = str(prodMovements[i].date.date())
                    if prodMovements[i].in_out == True:
                        new_data[1] += prodMovements[i].quantity
                    elif prodMovements[i].in_out == False:
                        new_data[2] += prodMovements[i].quantity
                    prev = str(prodMovements[i].date.date())
                    if i == prodMovementsLen -1:
                        graph_data.append(new_data)
                    print(f'\n\nentre al primer if new data: {new_data} prev: {prev}\n')
                elif prev and str(prodMovements[i].date.date()) == prev:
                    new_data[0] = str(prodMovements[i].date.date())
                    if prodMovements[i].in_out == True:
                        new_data[1] += prodMovements[i].quantity
                    elif prodMovements[i].in_out == False:
                        new_data[2] += prodMovements[i].quantity
                    prev = str(prodMovements[i].date.date())
                    print(f'\n\nentre al segundo if new data: {new_data} prev: {prev}\n')
                    if i == prodMovementsLen -1:
                        graph_data.append(new_data)
                elif prev and str(prodMovements[i].date.date()) != prev:
                    graph_data.append(new_data)
                    new_data = [0, 0, 0]
                    new_data[0] = str(prodMovements[i].date.date())
                    if prodMovements[i].in_out == True:
                        new_data[1] += prodMovements[i].quantity
                    elif prodMovements[i].in_out == False:
                        new_data[2] += prodMovements[i].quantity
                    prev = str(prodMovements[i].date.date())
                    if i == prodMovementsLen -1:
                        graph_data.append(new_data)
            border_case = True

        if selectedBranch == 'All Branches (default)' and search:
            for selectedBranch in Branch.query.filter_by(owner=current_user.email).all():
                for item in stock:
                    # calculating the current stock for all branches
                    currentStock = 0
                    for mov in Movements.query.filter_by(owner=current_user.email).filter(and_(Movements.prod_id == item['id'],
                                                        Movements.branch_id == selectedBranch.id)).all():
                        if mov.in_out is True:
                            currentStock += mov.quantity
                        elif mov.in_out is False:
                            currentStock -= mov.quantity
                    if item['name'] == search:
                        graph_data[item['name'] + " " + "On(" + selectedBranch.name + ")"] = currentStock
                        if item['name'] in graph_data:
                            graph_data.pop(item['name'])
                        print(graph_data)
                    print(item)

    # branches from user to pass to jinja
    branches = Branch.query.filter_by(owner=current_user.email).all()
    branchesList = ["All Branches (default)"]
    for branch in branches:
        branchesList.append(branch.name)

    print(f'\n\n\nla data: {graph_data}\n\n')
    return render_template('inventory.html', stock=stock, user=current_user, branches=branchesList, data=graph_data, border_case=border_case)


@login_required
@limiter.limit("10/minute")
@inventory.route('/inventory/<id>', methods=['GET'], strict_slashes=False)
def inventory_product(id):
    """Api Endpoint for inventory product"""

    # if user is not confirmed, block access and send to home
    #if current_user.confirmed is False:
    #    flash('Please confirm your account, check your email (and spam folder)', 'error')
    #    return redirect(url_for('views.home'))
    
    # consulting stock from all branches
    stockQuery = Inventory.query.filter_by(owner=current_user.email).filter_by(prod_id=id).first()


    #filling stock dictionary with prod name, quantity, description and product id
    stockItem = {}

    product = Product.query.filter_by(owner=current_user.email).filter_by(id=id).first()
        
    # if is searched a particular product only that product is gonna be listed

    stockItem['name'] = product.name
    stockItem['quantity'] = stockQuery.quantity
    stockItem['branch'] = "All Branches"
    stockItem['description'] = product.description
    stockItem['id'] = stockQuery.prod_id
    stockItem['qr_barcode'] = product.qr_barcode

    if not stockItem:
        return None

    return jsonify(stockItem)