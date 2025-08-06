from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.patients.models import PatientUser, Patient

class PatientLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PatientRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = PatientUser.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        # Check if patient exists with this email
        patient = Patient.query.filter_by(email=email.data).first()
        if not patient:
            raise ValidationError('No patient record found with this email address.')
        
        # Check if user account already exists for this patient
        existing_user = PatientUser.query.filter_by(patient_id=patient.id).first()
        if existing_user:
            raise ValidationError('An account already exists for this patient.')