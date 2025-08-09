from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, TextAreaField, SubmitField, IntegerField, FloatField, DateTimeField
from wtforms.validators import DataRequired, Email, Optional, NumberRange
import requests
import json
from flask import current_app
from app.system_params.models import SystemParameter

def get_id_types(db):
    with db.engine.connect() as connection:
        id_types = db.session.execute(
            db.select(SystemParameter).filter_by(name='id_types')
        ).scalar()
        if id_types and id_types.value:
            try:
                # Parse the JSON value and create choices with string keys
                id_types_dict = json.loads(id_types.value)
                return [(str(key), name) for key, name in id_types_dict.items()]
            except (ValueError, TypeError):
                return []
    return []

class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    address = TextAreaField('Address')
    phone = StringField('Phone')
    email = StringField('Email', validators=[Email()])
    id_type = SelectField(
        'ID Type',
        coerce=str,
        validators=[DataRequired()]
    )
    id_card_number = StringField(
        'ID Card Number',
        validators=[DataRequired()]
    )
    blood_type = SelectField(
        'Blood Type',
        choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                 ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        validators=[DataRequired()]
    )
    birthplace = StringField('Birthplace')
    marriage_status = SelectField('Marriage Status', choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')])
    nationality_id = SelectField('Nationality', coerce=str, choices=[])
    vip_status = SelectField('VIP Status', choices=[(True, 'Yes'), (False, 'No')], default=False)
    problematic_patient = SelectField('Problematic Patient', choices=[(True, 'Yes'), (False, 'No')], default=False)
    problematic_patient_reason = TextAreaField('Problematic Patient Reason', validators=[Optional()])
    loyalty_member = SelectField('Loyalty Member', choices=[(True, 'Yes'), (False, 'No')], default=False)
    loyalty_member_number = StringField('Loyalty Member Number', validators=[Optional()])
    ihs_number = StringField('IHS Number')
    chronic_condition = SelectField('Chronic Condition', choices=[(True, 'Yes'), (False, 'No')], default=False)
    chronic_condition_details = TextAreaField('Chronic Condition Details', validators=[Optional()])
    allergy_alert = SelectField('Allergy Alert', choices=[(True, 'Yes'), (False, 'No')], default=False)
    allergy_alert_details = TextAreaField('Allergy Alert Details', validators=[Optional()])
    preferred_communication = StringField('Preferred Communication Method')
    preferred_language = StringField('Preferred Language')
    emergency_contact_name = StringField('Emergency Contact Name')
    emergency_contact_phone = StringField('Emergency Contact Phone')
    emergency_contact_relationship = StringField('Emergency Contact Relationship')
    submit = SubmitField('Save Patient')

    def __init__(self, *args, db=None, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        # Fetch nationalities from the API
        try:
            response = requests.get(f"{current_app.config['API_BASE_URL']}/api/nationalities")
            if response.status_code == 200:
                nationalities = response.json()
                self.nationality_id.choices = [(str(n['id']), n['name']) for n in nationalities]
            else:
                self.nationality_id.choices = []
        except Exception as e:
            self.nationality_id.choices = []
            print(f"Error fetching nationalities: {e}")

        # Set ID types
        if db:
            self.id_type.choices = get_id_types(db)

class PatientSearchForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    gender = SelectField('Gender', choices=[('', 'Any'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[Optional()], default='')
    phone = StringField('Phone', validators=[Optional()])
    submit = SubmitField('Search Patients')

class VitalsForm(FlaskForm):
    date = DateTimeField('Date', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    bp_systolic = IntegerField('Systolic Blood Pressure', validators=[Optional(), NumberRange(min=0)])
    bp_diastolic = IntegerField('Diastolic Blood Pressure', validators=[Optional(), NumberRange(min=0)])
    heart_rate = IntegerField('Heart Rate (bpm)', validators=[Optional(), NumberRange(min=0)])
    temperature = FloatField('Temperature (°C)', validators=[Optional(), NumberRange(min=0)])
    weight = FloatField('Weight (kg)', validators=[Optional(), NumberRange(min=0)])
    height = FloatField('Height (cm)', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Save Vitals')

class AllergyForm(FlaskForm):
    allergen = StringField('Allergen', validators=[DataRequired()])
    reaction = TextAreaField('Reaction', validators=[DataRequired()])
    severity = SelectField('Severity', choices=[('Mild', 'Mild'), ('Moderate', 'Moderate'), ('Severe', 'Severe')], validators=[DataRequired()])
    recorded_date = DateTimeField('Recorded Date', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Save Allergy')

class PatientRegistrationForm(PatientForm):
    # Personal Information
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    id_type = SelectField(
        'ID Type',
        coerce=str,
        validators=[DataRequired()]
    )
    id_card_number = StringField(
        'ID Card Number',
        validators=[DataRequired()]
    )
    blood_type = SelectField(
        'Blood Type',
        choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                 ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        validators=[DataRequired()]
    )
    birthplace = StringField('Birthplace')
    marriage_status = SelectField('Marriage Status', choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')])

    # Contact Information
    address = TextAreaField('Address')
    phone = StringField('Phone')
    email = StringField('Email', validators=[Email()])
    preferred_communication = StringField('Preferred Communication Method')
    preferred_language = StringField('Preferred Language')

    # Emergency Contact
    emergency_contact_name = StringField('Emergency Contact Name')
    emergency_contact_phone = StringField('Emergency Contact Phone')
    emergency_contact_relationship = StringField('Emergency Contact Relationship')

    # Insurance Information
    insurance_provider = StringField('Insurance Provider')

    # Status
    is_deceased = SelectField('Status', choices=[(True, 'Deceased'), (False, 'Alive')], default=False)
    vip_status = SelectField('VIP Status', choices=[(True, 'Yes'), (False, 'No')], default=False)
    problematic_patient = SelectField('Problematic Patient', choices=[(True, 'Yes'), (False, 'No')], default=False)
    problematic_patient_reason = TextAreaField('Problematic Patient Reason', validators=[Optional()])
    loyalty_member = SelectField('Loyalty Member', choices=[(True, 'Yes'), (False, 'No')], default=False)
    loyalty_member_number = StringField('Loyalty Member Number', validators=[Optional()])
    chronic_condition = SelectField('Chronic Condition', choices=[(True, 'Yes'), (False, 'No')], default=False)
    chronic_condition_details = TextAreaField('Chronic Condition Details', validators=[Optional()])
    allergy_alert = SelectField('Allergy Alert', choices=[(True, 'Yes'), (False, 'No')], default=False)
    allergy_alert_details = TextAreaField('Allergy Alert Details', validators=[Optional()])

    submit = SubmitField('Register Patient')

class MedicationForm(FlaskForm):
    drug_name = StringField('Drug Name', validators=[DataRequired()])
    dosage = StringField('Dosage', validators=[DataRequired()])
    frequency = SelectField('Frequency', choices=[
        ('Once daily', 'Once daily'),
        ('Twice daily', 'Twice daily'),
        ('Three times daily', 'Three times daily'),
        ('Four times daily', 'Four times daily'),
        ('Every 4 hours', 'Every 4 hours'),
        ('Every 6 hours', 'Every 6 hours'),
        ('Every 8 hours', 'Every 8 hours'),
        ('As needed', 'As needed'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Discontinued', 'Discontinued')
    ], default='Active', validators=[DataRequired()])
    submit = SubmitField('Prescribe Medication')