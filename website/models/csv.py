from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField 
from wtforms.validators import InputRequired 

class UploadFileForm(FlaskForm): 
    file = FileField("File", validators=[InputRequired()]) 
    submit = SubmitField("Upload File") 
class UploadFileForm2(FlaskForm): 
    file2 = FileField("File 2", validators=[InputRequired()]) 
    submit2 = SubmitField("Upload File") 
class UploadFileForm3(FlaskForm): 
    file3 = FileField("File 3", validators=[InputRequired()]) 
    submit3 = SubmitField("Upload File")