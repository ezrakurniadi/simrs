from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email

class RoleForm(FlaskForm):
    name = StringField('Role Name', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description', validators=[Length(max=200)])
    submit = SubmitField('Save Role')

class UserRoleForm(FlaskForm):
    role_id = SelectField('Role', validators=[DataRequired()], coerce=str)
    submit = SubmitField('Assign Role')

class RemoveRoleForm(FlaskForm):
    role_id = SelectField('Role to Remove', validators=[DataRequired()], coerce=str)
    submit = SubmitField('Remove Role')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Save User')