from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import validators
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField
from wtforms.validators import DataRequired


class ImageForm(FlaskForm):
    
    picture = FileField('Update Picture', validators=[FileAllowed(['jpg', 'png'])])

class ResumeForm(FlaskForm):
    
    resume = FileField('Update Resume', validators=[FileAllowed(['pdf', 'docx'])])

class InterviewForm(FlaskForm):

    entryDate = DateField('Interview Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    entryTime = TimeField('Interview Time', validators=(validators.DataRequired(),))
