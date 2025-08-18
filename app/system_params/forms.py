from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional

class SystemParameterForm(FlaskForm):
    parameter_name = StringField('Parameter Name', validators=[DataRequired()])
    parameter_value = StringField('Parameter Value', validators=[DataRequired()])
    description = TextAreaField('Description')
    parameter_type = SelectField('Parameter Type', choices=[
        ('string', 'String'),
        ('integer', 'Integer'),
        ('boolean', 'Boolean'),
        ('json', 'JSON')
    ])
    submit = SubmitField('Save Parameter')

class PayorTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save Payor Type')

class PayorDetailForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    payor_type_id = SelectField('Payor Type', coerce=int)
    submit = SubmitField('Save Payor Detail')


class IDTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save ID Type')

class EthnicityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save Ethnicity')

class LanguageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    iso_code = StringField('ISO Code', validators=[Optional()])
    submit = SubmitField('Save Language')