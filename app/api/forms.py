from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DateTimeField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email

# API forms can be defined here if needed
# For API endpoints, validation is often handled differently than in web forms