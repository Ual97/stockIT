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
 
csv = Blueprint('csv', __name__) 
 
@csv.route('/csv', methods=['GET', 'POST'], strict_slashes=False) 
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
        return "File has been uploaded." 
    return render_template('csv.html', user=current_user, form=form)