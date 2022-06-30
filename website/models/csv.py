from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField 
from wtforms.validators import InputRequired 

class UploadFileForm(FlaskForm): 
    file = FileField("File", validators=[InputRequired()]) 
    submit = SubmitField("Upload File") 