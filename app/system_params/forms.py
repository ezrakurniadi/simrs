from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NationalityForm(FlaskForm):
    name = StringField('Nationality Name', validators=[DataRequired()])
    submit = SubmitField('Add Nationality')