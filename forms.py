from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])

class noaaDataForm(FlaskForm):
    zipCode = StringField('zipCode', validators=[DataRequired()])
    startDate = StringField('startDate', validators=[DataRequired()])
    endDate = StringField('endDate', validators=[DataRequired()])
    # dataSet = StringField('setName', validators=[DataRequired()])
