from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, TextAreaField, SubmitField, IntegerField, FloatField, DateTimeField
from wtforms.validators import DataRequired, Email, Optional, NumberRange
import requests
import json
from flask import current_app
from app.system_params.models import SystemParameter, PayorType, PayorDetail, IDType, Race, Ethnicity

# Choice constants for better organization and reusability
ETHNICITY_CHOICES = [
    ('', 'Select Ethnicity'),
    ('Asian', 'Asian'),
    ('Black or African American', 'Black or African American'),
    ('Hispanic or Latino', 'Hispanic or Latino'),
    ('White', 'White'),
    ('Native American or Alaska Native', 'Native American or Alaska Native'),
    ('Native Hawaiian or Other Pacific Islander', 'Native Hawaiian or Other Pacific Islander'),
    ('Other', 'Other')
]

PREFERRED_LANGUAGE_CHOICES = [
    ('', 'Select Preferred Language'),
    ('English', 'English'),
    ('Spanish', 'Spanish'),
    ('French', 'French'),
    ('German', 'German'),
    ('Chinese', 'Chinese'),
    ('Japanese', 'Japanese'),
    ('Korean', 'Korean'),
    ('Vietnamese', 'Vietnamese'),
    ('Other', 'Other')
]



# def get_id_types(db):
#     # Get ID types from the id_types table
#     id_types = db.session.query(IDType).filter_by(is_active=True).all()
#     return [('', 'Select ID Type')] + [(it.name, it.name) for it in id_types]

# def get_races(db):
#     # Get races from the races table
#     races = db.session.query(Race).all()
#     return [('', 'Select Race')] + [(r.name, r.name) for r in races]

# def get_ethnicities(db):
#     # Get ethnicities from the ethnicities table
#     ethnicities = db.session.query(Ethnicity).all()    
#     return [('', 'Select Ethnicity')] + [(e.name, e.name) for e in ethnicities]

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
    preferred_language = SelectField('Preferred Language', choices=PREFERRED_LANGUAGE_CHOICES, validators=[Optional()], default='')
    emergency_contact_name = StringField('Emergency Contact Name')
    emergency_contact_phone = StringField('Emergency Contact Phone')
    emergency_contact_relationship = StringField('Emergency Contact Relationship')
    payor_type = SelectField('Payor Type', choices=[('', 'Select Payor Type')], validators=[Optional()], default='')
    payor_detail = SelectField('Payor Detail', choices=[('', 'Select Payor Type First')], validators=[Optional()], default='')
    insurance_policy_id = StringField('Insurance Policy/ID Number')
    insurance_group_number = StringField('Insurance Group Number')
    guarantor_name = StringField('Guarantor Name')
    guarantor_relationship = StringField('Guarantor Relationship to Patient')
    guarantor_phone = StringField('Guarantor Phone')
    guarantor_address = TextAreaField('Guarantor Address')
    ethnicity = SelectField('Ethnicity', choices=ETHNICITY_CHOICES, validators=[Optional()], default='')
    mrn = StringField('Medical Record Number (MRN)', render_kw={'readonly': True})
    is_deceased = SelectField('Status', choices=[(True, 'Deceased'), (False, 'Alive')], default=False)
    consent_to_treat = SelectField('Consent to Treat', choices=[(True, 'Yes'), (False, 'No')], default=False)
    privacy_practices_acknowledged = SelectField('Privacy Practices Acknowledged', choices=[(True, 'Yes'), (False, 'No')], default=False)
    submit = SubmitField('Save Patient')

    def __init__(self, *args, db=None, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        # Fetch nationalities from the API
        # try:
        #     response = requests.get(f"{current_app.config['API_BASE_URL']}/api/nationalities")
        #     if response.status_code == 200:
        #         nationalities = response.json()
        #         self.nationality_id.choices = [(str(n['id']), n['name']) for n in nationalities]
        #     else:
        #         self.nationality_id.choices = []
        # except Exception as e:
        #     self.nationality_id.choices = []
        #     print(f"Error fetching nationalities: {e}")

        # Set ID types
        # if db:
            # self.id_type.choices = get_id_types(db)
            # self.race.choices = get_races(db)
            # self.ethnicity.choices = get_ethnicities(db)

        
        # Set payor type choices
        if db:
            payor_types = db.session.query(PayorType).filter_by(is_active=True).all()
            self.payor_type.choices = [('', 'Select Payor Type')] + [(pt.name, pt.name) for pt in payor_types]
        else:
            self.payor_type.choices = [('', 'Select Payor Type')]
        
        # Set payor detail choices based on payor type
        payor_type = kwargs.get('obj', None) and getattr(kwargs['obj'], 'payor_type', None)
        if payor_type and db:
            payor_details = db.session.query(PayorDetail).join(PayorType).filter(
                PayorType.name == payor_type,
                PayorDetail.is_active == True
            ).all()
            self.payor_detail.choices = [('', f'Select {payor_type} Detail')] + [(pd.name, pd.name) for pd in payor_details]
        else:
            self.payor_detail.choices = [('', 'Select Payor Type First')]

    def get_payor_detail_choices(self, payor_type):
        """Return payor detail choices based on payor type"""
        # This method is kept for backward compatibility but will be replaced with database queries
        payor_details = {
            'Insurance': [('', 'Select Insurance Company'), ('BPJS', 'BPJS'), ('AdMedika', 'AdMedika'), ('Aetna', 'Aetna'), ('Allianz', 'Allianz'), ('Cigna', 'Cigna'), ('Prudential', 'Prudential')],
            'Company': [('', 'Select Company'), ('PT. Medistra Hospital', 'PT. Medistra Hospital'), ('PT. Healthcare Corp', 'PT. Healthcare Corp'), ('PT. Medical Solutions', 'PT. Medical Solutions'), ('PT. Wellness Group', 'PT. Wellness Group')],
            'Stakeholder': [('', 'Select Stakeholder'), ('Government', 'Government'), ('NGO', 'NGO'), ('Private Donor', 'Private Donor'), ('International Aid', 'International Aid')]
        }
        return payor_details.get(payor_type, [('', 'Select Payor Type First')])

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

    # Emergency Contact
    emergency_contact_name = StringField('Emergency Contact Name')
    emergency_contact_phone = StringField('Emergency Contact Phone')
    emergency_contact_relationship = StringField('Emergency Contact Relationship')

    # Payor Information
    payor_type = SelectField('Payor Type', choices=[('', 'Select Payor Type')], validators=[Optional()], default='')
    payor_detail = SelectField('Payor Detail', choices=[('', 'Select Payor Type First')], validators=[Optional()], default='')
    insurance_policy_id = StringField('Insurance Policy/ID Number')
    insurance_group_number = StringField('Insurance Group Number')
    guarantor_name = StringField('Guarantor Name')
    guarantor_relationship = StringField('Guarantor Relationship to Patient')
    guarantor_phone = StringField('Guarantor Phone')
    guarantor_address = TextAreaField('Guarantor Address')
    mrn = StringField('Medical Record Number (MRN)', render_kw={'readonly': True})

    # Demographics
    nationality_id = SelectField('Nationality',
        validators=[Optional()],
        coerce=str,
        default='')
    ethnicity = SelectField('Ethnicity',
        choices=ETHNICITY_CHOICES,
        validators=[Optional()],
        coerce=str,
        default='')

    # Status
    is_deceased = SelectField('Status', choices=[('True', 'Deceased'), ('False', 'Alive')], coerce=str, default='False')
    vip_status = SelectField('VIP Status', choices=[('True', 'Yes'), ('False', 'No')], coerce=str, default='False')
    problematic_patient = SelectField('Problematic Patient', choices=[('True', 'Yes'), ('False', 'No')], coerce=str, default='False')
    problematic_patient_reason = TextAreaField('Problematic Patient Reason', validators=[Optional()])
    loyalty_member = SelectField('Loyalty Member', choices=[('True', 'Yes'), ('False', 'No')], coerce=str, default='False')
    loyalty_member_number = StringField('Loyalty Member Number', validators=[Optional()])
    chronic_condition = SelectField('Chronic Condition', choices=[('True', 'Yes'), ('False', 'No')], coerce=str, default='False')
    chronic_condition_details = TextAreaField('Chronic Condition Details', validators=[Optional()])
    allergy_alert = SelectField('Allergy Alert', choices=[('True', 'Yes'), ('False', 'No')], coerce=str, default='False')
    allergy_alert_details = TextAreaField('Allergy Alert Details', validators=[Optional()])
    
    submit = SubmitField('Register Patient')

    def __init__(self, *args, **kwargs):
        super(PatientRegistrationForm, self).__init__(*args, **kwargs)
        # Set payor type choices
        if hasattr(self, 'db') and self.db:
            payor_types = self.db.session.query(PayorType).filter_by(is_active=True).all()
            self.payor_type.choices = [('', 'Select Payor Type')] + [(pt.name, pt.name) for pt in payor_types]
        else:
            self.payor_type.choices = [('', 'Select Payor Type')]
        
        # Set payor detail choices based on payor type
        payor_type = kwargs.get('obj', None) and getattr(kwargs['obj'], 'payor_type', None)
        if payor_type and hasattr(self, 'db') and self.db:
            payor_details = self.db.session.query(PayorDetail).join(PayorType).filter(
                PayorType.name == payor_type,
                PayorDetail.is_active == True
            ).all()
            self.payor_detail.choices = [('', f'Select {payor_type} Detail')] + [(pd.name, pd.name) for pd in payor_details]
        else:
            self.payor_detail.choices = [('', 'Select Payor Type First')]
            
        # Set nationality choices from database
        if hasattr(self, 'db') and self.db:
            nationalities = self.db.session.query(Nationality).all()
            self.nationality_id.choices = [('', 'Select Nationality')] + [(n.id, n.name) for n in nationalities]
        else:
            self.nationality_id.choices = [('', 'Select Nationality')]

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