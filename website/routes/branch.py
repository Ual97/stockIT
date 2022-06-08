from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from website import views
from website import db
from website.models.user import User
from website.models.product import Product
from website.models.branch import Branch
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.sql.expression import func

subsidiary = Blueprint('subsidiary', __name__)

@subsidiary.route('/branch', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def subsidiary_view():
    """
    Branch main page
    """
    if request.method == 'POST':
        sucursal_dict = request.form.to_dict()
        print(f'\n\n\n{sucursal_dict}\n\n')
        if sucursal_dict.get('name') is None:
            flash('Name is mandatory', category='error')
            return redirect(url_for('subsidiary.subsidiary_view'))
        if type(sucursal_dict.get('name')) != str:
            flash('Name must be a string', category='error')
            return redirect(url_for('subsidiary.subsidiary_view'))
        sucursal_dict['owner'] = current_user.email
        new_sucursal = Branch(**sucursal_dict)
        db.session.add(new_sucursal)
        db.session.commit()
        flash('Branch added', category='success')
        return redirect(url_for('subsidiary.subsidiary_view'))
    subsidiarys = Branch.query.filter_by(owner=current_user.email).paginate(per_page=10)
    nextid = db.session.query(func.max(Branch.id)).scalar()
    if nextid is None:
        nextid = 1
    else:
        nextid += 1
    return render_template('branches.html', subsidiarys=subsidiarys,
                           user=current_user, nextid=nextid)

@subsidiary.route('/branch/<int:id>', methods=['GET', 'POST'],
                  strict_slashes=False)
@login_required

def update_subsidiary(id):
    """
    updates a subsidiary
    """
    currentSubsidiary = Branch.query.filter_by(id=id).first()
    if request.method == 'POST':
        subsidiary_dict = request.form.to_dict()
        if subsidiary_dict.get('name') is None:
            flash('Name is mandatory', category='error')
            return redirect(url_for('subsidiary.subsidiary_view'))
        if type(subsidiary_dict.get('name')) != str:
            flash('Name must be a string', category='error')
            return redirect(url_for('subsidiary.subsidiary_view'))
        currentSubsidiary.name = subsidiary_dict.get('name')
        db.session.commit()
        flash('Sucursal updated', category='success')
        return redirect(url_for('subsidiary.subsidiary_view'))
    try:
        currentSubsidiaryDict = currentSubsidiary.__dict__
        currentSubsidiaryDict.pop('_sa_instance_state')
        return jsonify(currentSubsidiaryDict)
    except:
        pass

@subsidiary.route('/branch/delete/<id>', strict_slashes=False)
@login_required
def Delete(id):
    """inventory page"""
    db.session.delete(Branch.query.get(id))
    db.session.commit()
    flash('Branch deleted successfully!')
    print(f'\n\n\naaaaaaaaaaaa{request.url_rule}\n\n\n')
    return redirect('/branch')