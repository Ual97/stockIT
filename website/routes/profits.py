from ast import operator
from hashlib import new
from website.models.product import Product
from website.models.movements import Movements
from website.models.branch import Branch
from website.models.inventory import Inventory
from website.models.profits import Profits
from website.models.cost_qty import Cost_qty
from flask_login import login_required
from flask import Blueprint, render_template, request, flash, redirect, jsonify, abort, url_for
from flask_login import login_required, current_user
from sqlalchemy import and_, asc, desc
from website import limiter
from operator import itemgetter
import requests
import math

profits = Blueprint('profits', __name__)

@login_required
@limiter.limit("20/minute")
@profits.route('/profits', methods=['GET', 'POST'], strict_slashes=False)
def inventory_page():
    """profits page"""

    #if user is not confirmed, block access and send to home
    #if current_user.confirmed is False:
    #    flash('Please confirm your account, check your email (and spam folder)', 'error')
    #    return redirect(url_for('views.home'))

    formDict = request.form.to_dict()

    # store some  product name if some product is searched
    search = formDict.get('search')
    search = search.lower().strip() if search else None
    selectedBranch = formDict.get('selectBranch')
    orderBy = formDict.get('orderBy')
    print(f'\nlas weas:{formDict}')


    # consulting profits from all branches
    if orderBy == 'Lower Profit':
        stockQuery = Profits.query.filter_by(owner=current_user.email).order_by(asc(Profits.profit)).all()
    elif orderBy == 'Higher Profit':
        stockQuery = Profits.query.filter_by(owner=current_user.email).order_by(desc(Profits.profit)).all()
    elif orderBy == 'Lower Quantity':
        stockQuery = Profits.query.filter_by(owner=current_user.email).order_by(asc(Profits.quantity)).all()
    elif orderBy == 'Higher Quantity':
        stockQuery = Profits.query.filter_by(owner=current_user.email).order_by(desc(Profits.quantity)).all()
    else:
        stockQuery = Profits.query.filter_by(owner=current_user.email).order_by(desc(Profits.date)).all()

    profits = []
    # filling profits dictionary with prod name, quantity, description and product id
    for item in stockQuery:
        profitItem = {}
        product = Product.query.filter_by(id=item.prod_id).first()
        # if search not in product name then its not listed
        if search and search not in product.name.lower():
            continue
        # if selected branch not in product name then its not listed
        if selectedBranch and selectedBranch != 'All Branches (default)' and Branch.query.filter_by(name=selectedBranch).first().id != item.branch_id:
            continue
        profitItem['name'] = product.name
        profitItem['profit'] = item.profit
        profitItem['quantity'] = item.quantity
        profitItem['branch'] = Branch.query.filter_by(id=item.branch_id).first().name
        profitItem['date'] = item.date
        profitItem['description'] = product.description
        profitItem['id'] = item.prod_id
        profitItem['qr_barcode'] = product.qr_barcode
        profitItem['currency'] = "USD" if item.currency is True else "UYU"


        profits.append(profitItem)
        
    if search and not profits:
        flash("No items with that name", "error")
        return redirect('/profits')


    # branches from user to pass to jinja
    branches = Branch.query.filter_by(owner=current_user.email).all()
    branchesList = ["All Branches (default)"]
    for branch in branches:
        branchesList.append(branch.name)

    # making graph throghout the time
    graphQuery = Profits.query.filter_by(owner=current_user.email).order_by(asc(Profits.date)).all()
    graphList = []
    dollar = None
    for item in graphQuery:
        graphItem = {}
        product = Product.query.filter_by(id=item.prod_id).first()
        # if search not in product name then its not listed
        if search and search not in product.name.lower():
            continue
        # if selected branch not in product name then its not listed
        if selectedBranch and selectedBranch != 'All Branches (default)' and Branch.query.filter_by(name=selectedBranch).first().id != item.branch_id:
            continue
        graphItem['name'] = product.name
        if item.currency is False:
            if not dollar:
                dollar = requests.get('https://cotizaciones-brou.herokuapp.com/api/currency/latest')
                print(f"\n\n{dollar.json()}")
                dollar = dollar.json()['rates']['USD']['sell']
            graphItem['profit'] = item.profit / dollar
        else:    
            graphItem['profit'] = item.profit
        graphItem['date'] = str(item.date.date())

        graphList.append(graphItem)

    to_sort = []
    for item in graphList:
        if not to_sort:
            to_sort.append([item])
        elif to_sort[-1][0]['date'] == item['date']:
            to_sort[-1].append(item)
        else:
            to_sort.append([item])
        print(f"\nitems de la query {item}")

    print(f'estaran separadas? {to_sort}')
    uniqueValues = []
    for item in to_sort:
        unique = []
        item.sort(key=itemgetter('name'))
        prev = None
        i = 0
        for dict in item:
            if prev is None:
                dictUnique = {}
                prev = dict['name']
                dictUnique['name'] = dict['name']
                dictUnique['profit'] = dict['profit']
                dictUnique['date'] = dict['date']
            elif prev != dict['name']:
                unique.append(dictUnique)
                dictUnique = {}
                prev = dict['name']
                dictUnique['name'] = dict['name']
                dictUnique['profit'] = dict['profit']
                dictUnique['date'] = dict['date']
            else:
                dictUnique['profit'] += dict['profit']
            i += 1
            if i == len(item):
                unique.append(dictUnique)
        uniqueValues.append(unique)
    

    print(f'\nestá ordenada? {to_sort}\n\n valores unicos {uniqueValues} \n')

    invProd = Inventory.query.filter_by(owner=current_user.email).all()
    prodList = []
    for item in invProd:
        prodList.append(Product.query.filter_by(id=item.prod_id).first().name)
    prodList.sort()
    prodLen = len(prodList)
    print(f'\nproductos {prodList}')
    to_graph = [["Product names"] + prodList]
    if search:
        to_graph = [["Product name", search]]
        for item in uniqueValues:
            newEntry = [item[0]['date']]
            for dict in item:
                print(f"\ndict['name'].lower() {dict['name'].lower()} == prodList[0].lower() {prodList[0].lower()}")
                if search in dict['name'].lower():
                    if len(newEntry) == 2:
                        newEntry[1] += dict['profit']
                    else:
                        newEntry.append(dict['profit'])
            to_graph.append(newEntry)
                
    if not search:
        for item in uniqueValues:
            newEntry = [item[0]['date']]
            lenItem = len(item)
            flag = False
            for i in range(prodLen):
                if i < lenItem and item[i]['name'] == prodList[i]:
                    newEntry.append(item[i]['profit'])
                elif i < lenItem and item[i]['name'] != prodList[i]:
                    newEntry.append(0)
                    flag = True
                    checkpoint = i
                else:
                    if flag == True and prodList[i] == item[checkpoint]['name']:
                        newEntry.append(item[checkpoint]['profit'])
                        flag = False
                    else:
                        newEntry.append(0)
            to_graph.append(newEntry)
    print(f'\nestará para graficar? {to_graph}')
    
    branchesChart = [['Branch', 'Profit']]
    for item in Branch.query.filter_by(owner=current_user.email).all():
        branchProfit = Profits.query.filter_by(branch_id=item.id).all()
        if branchProfit:
            list = [item.name]
            sum = []
            for value in branchProfit:
                print(f"\n\n{branchProfit}\n")
                if value.currency is False:
                    if not dollar:
                        dollar = requests.get('https://cotizaciones-brou.herokuapp.com/api/currency/latest')
                        print(f"\n\n{dollar.json()}")
                        dollar = dollar.json()['rates']['USD']['sell']
                    sum.append(value.profit / dollar)
                else:
                    print(f"\n\nesta en dolares {value.profit}")
                    sum.append(value.profit)
            print(f"\n\nsumas {sum}\n")
            list.append(math.fsum(sum))
            branchesChart.append(list)

    productsChart = [['Product', 'Profit']]


    for item in Product.query.filter_by(owner=current_user.email).all():
        if selectedBranch and selectedBranch != 'All Branches (default)':
            branchId = Branch.query.filter_by(name=selectedBranch).first().id
            prodProfit = Profits.query.filter((Profits.prod_id==item.id) & (Profits.branch_id==branchId)).all()
        else:
            prodProfit = Profits.query.filter_by(prod_id=item.id).all()
        if prodProfit:
            list = [item.name]
            sum = []
            for value in prodProfit:
                if value.currency is False:
                    if not dollar:
                        dollar = requests.get('https://cotizaciones-brou.herokuapp.com/api/currency/latest')
                        print(f"\n\n{dollar.json()}")
                        dollar = dollar.json()['rates']['USD']['sell']
                    sum.append(value.profit / dollar)
                else:    
                    sum.append(value.profit)
            print(f"\n\nsumas {sum}\n")
            list.append(math.fsum(sum))
            productsChart.append(list)

    print(f"\nbranches chart {branchesChart}")

    print(f'\n\n{to_graph}\n')        
    
    return render_template('profits.html', profits=profits, user=current_user,
                           branches=branchesList, graph0=to_graph, graph1=branchesChart)

@login_required
@limiter.limit("20/minute")
@profits.route('/profits/<id>', methods=['GET'], strict_slashes=False)
def profits_product(id):
    """Api Endpoint for profits of products"""

    # if user is not confirmed, block access and send to home
    #if current_user.confirmed is False:
    #    flash('Please confirm your account, check your email (and spam folder)', 'error')
    #    return redirect(url_for('views.home'))
    
    # consulting profits from all branches
    profitsQuery = Profits.query.filter_by(owner=current_user.email).filter_by(prod_id=id).all()


    #filling profits dictionary with prod name, quantity, description and product id
    profitsList = []

    product = Product.query.filter_by(owner=current_user.email).filter_by(id=id).first()
        
    # if is searched a particular product only that product is gonna be listed
    for item in profitsQuery:
        profitItem = {}

        profitItem['name'] = product.name
        profitItem['quantity'] = item.quantity
        profitItem['branch'] = Branch.query.filter_by(id=item.branch_id).first().name
        profitItem['description'] = product.description
        profitItem['id'] = item.prod_id
        profitItem['qr_barcode'] = product.qr_barcode
        profitsList.append(profitItem)

    if not profitsList:
        return None

    return jsonify(profitsList)