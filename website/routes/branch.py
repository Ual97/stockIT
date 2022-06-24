from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from website import views
from website import db
from website.models.branch import Branch
from website.models.user import User
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func

subsidiary = Blueprint('subsidiary', __name__)

@subsidiary.route('/branch', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def subsidiary_view():
    """
    Branch main page
    """
    #if user is not confirmed, block access and send to home
    #if current_user.confirmed is False:
    #    flash('Please confirm your account, check your email (and spam folder)', 'error')
    #    return redirect(url_for('views.home'))

    if request.method == 'POST':
        branch_dict = request.form.to_dict()
        name = branch_dict.get('name')
        print(f'\n\n\n{branch_dict}\n\n')
        if not name:
            flash('Name is mandatory', category='error')
            return redirect(url_for('subsidiary.subsidiary_view'))

        if type(name) != str:
            flash('Name must be a string', category='error')
            return redirect(url_for('subsidiary.subsidiary_view'))

        name = name.strip()

        branch_dict['name'] = name

        currentBranch = currentBranch = Branch.query.filter((Branch.name==name) & (Branch.owner==current_user.email)).first()
        if currentBranch:
            currentBranchName = currentBranch.name.strip()
            print(f"\n\n\nnew {name.lower()} current {currentBranchName.lower()}\n\n")
            if name.lower() == currentBranchName.lower():
                flash('This branch already exists', category='error')
                return redirect(url_for('subsidiary.subsidiary_view'))

        branch_dict['owner'] = current_user.email
        new_branch = Branch(**branch_dict)
        db.session.add(new_branch)
        db.session.commit()
        flash('Branch added', category='success')
        return redirect(url_for('subsidiary.subsidiary_view'))
    subsidiarys = Branch.query.filter_by(owner=current_user.email).paginate(per_page=10)

    return render_template('branches.html', subsidiarys=subsidiarys,
                           user=current_user)

@subsidiary.route('/branch/<id>', methods=['GET', 'POST'],
                  strict_slashes=False)
@login_required

def update_subsidiary(id):
    """
    updates a subsidiary
    """
    currentSubsidiary = Branch.query.filter_by(id=id).first()
    if request.method == 'POST':
        subsidiary_dict = request.form.to_dict()
        name = subsidiary_dict.get('nameUpdate')
        if name is None:
            flash('Name is mandatory', category='error')
            return redirect(url_for('subsidiary.subsidiary_view'))
        if type(name) != str:
            flash('Name must be a string', category='error')
            return redirect(url_for('subsidiary.subsidiary_view'))
        currentBranch = Branch.query.filter((Branch.name==name) & (Branch.owner==current_user.email)).first()
        if currentBranch:
            currentBranchName = currentBranch.name.strip()
            print(f"\n\n\nnew {name.lower()} current {currentBranchName.lower()}\n\n")
            if name.lower() == currentBranchName.lower():
                flash('This branch already exists', category='error')
                return redirect(url_for('subsidiary.subsidiary_view'))

        currentSubsidiary.name = name
        db.session.commit()
        flash('Branch updated', category='success')
        return redirect(url_for('subsidiary.subsidiary_view'))
    try:
        currentSubsidiaryDict = currentSubsidiary.__dict__
        currentSubsidiaryDict.pop('_sa_instance_state')
        print(f'\n\n\ndiccionario tas? {currentSubsidiaryDict}\n\n')
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