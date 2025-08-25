from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
import uuid
# Remove the direct import of Nationality to avoid circular import

# Import choice constants from forms for reference
from app.patients.forms import ETHNICITY_CHOICES, PREFERRED_LANGUAGE_CHOICES

class Patient(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    id_type = db.Column(db.String(50), nullable=True)
    id_card_number = db.Column(db.String(50), nullable=True)
    blood_type = db.Column(db.String(5), nullable=True)
    birthplace = db.Column(db.String(100), nullable=True)
    marriage_status = db.Column(db.String(20), nullable=True)
    nationality_id = db.Column(db.String(36), db.ForeignKey('nationality.id'), nullable=True)
    vip_status = db.Column(db.Boolean, default=False)
    problematic_patient = db.Column(db.Boolean, default=False)
    problematic_patient_reason = db.Column(db.Text, nullable=True)
    loyalty_member = db.Column(db.Boolean, default=False)
    loyalty_member_number = db.Column(db.String(50), nullable=True)
    ihs_number = db.Column(db.String(50), nullable=True)
    mrn = db.Column(db.String(11), nullable=True, unique=True)  # Format: 00-00-00-00
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'), nullable=True)
    ethnicity = db.Column(db.String(50), nullable=True)
    # Relationship
    race = db.relationship('Race', backref=db.backref('patients', lazy=True))
    chronic_condition = db.Column(db.Boolean, default=False)
    chronic_condition_details = db.Column(db.Text, nullable=True)
    allergy_alert = db.Column(db.Boolean, default=False)
    allergy_alert_details = db.Column(db.Text, nullable=True)
    preferred_communication = db.Column(db.String(50), nullable=True)
    preferred_language = db.Column(db.String(50), nullable=True)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_phone = db.Column(db.String(20), nullable=True)
    emergency_contact_relationship = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(50), nullable=True)
    payor_type = db.Column(db.String(50), nullable=True)  # Insurance, Company, Stakeholder
    payor_detail = db.Column(db.String(100), nullable=True)  # Specific insurance company, company name, or stakeholder name
    insurance_policy_id = db.Column(db.String(50), nullable=True)
    insurance_group_number = db.Column(db.String(50), nullable=True)
    guarantor_name = db.Column(db.String(100), nullable=True)
    guarantor_relationship = db.Column(db.String(50), nullable=True)
    guarantor_phone = db.Column(db.String(20), nullable=True)
    guarantor_address = db.Column(db.String(255), nullable=True)
    is_deceased = db.Column(db.Boolean, default=False)
    consent_to_treat = db.Column(db.Boolean, nullable=True)
    privacy_practices_acknowledged = db.Column(db.Boolean, nullable=True)

    # Use string reference for the relationship to avoid circular import
    nationality = db.relationship('Nationality', backref=db.backref('patients', lazy=True))

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def get_valid_ethnicities():
        """Return list of valid ethnicity choices (excluding empty choice)"""
        return [choice[0] for choice in ETHNICITY_CHOICES if choice[0]]

    @staticmethod
    def get_valid_preferred_languages():
        """Return list of valid preferred language choices (excluding empty choice)"""
        return [choice[0] for choice in PREFERRED_LANGUAGE_CHOICES if choice[0]]

    def is_valid_ethnicity(self):
        """Check if the patient's ethnicity is valid"""
        return self.ethnicity in self.get_valid_ethnicities() if self.ethnicity else True

    def is_valid_preferred_language(self):
        """Check if the patient's preferred language is valid"""
        return self.preferred_language in self.get_valid_preferred_languages() if self.preferred_language else True
        
class Nationality(db.Model):
    __tablename__ = 'nationality'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Nationality {self.name}>'

class Vitals(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    recorded_by = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    bp_systolic = db.Column(db.Integer, nullable=False)
    bp_diastolic = db.Column(db.Integer, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Vitals for Patient {self.patient_id} recorded on {self.date}>'

class Allergy(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    allergen = db.Column(db.String(100), nullable=False)
    reaction = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    recorded_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    recorded_by = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Allergy for Patient {self.patient_id}: {self.allergen}>'

class Medication(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    prescribed_by = db.Column(db.String(50), nullable=False)
    drug_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Medication for Patient {self.patient_id}: {self.drug_name}>'

class PatientUser(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    patient = db.relationship('Patient', backref=db.backref('patient_users', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<PatientUser {self.username}>'

# Import the get_all_nationalities function from system_params.models
from app.system_params.models import get_all_nationalities
from sqlalchemy import func


def generate_mrn():
    """
    Generate a new MRN in the format "00-00-00-00".
    The MRN is generated by incrementing the last used MRN stored in system parameters.
    """
    # Get the last used MRN from system parameters
    # Import SystemParameter inside the function to avoid circular import
    from app.system_params.models import SystemParameter
    last_mrn_param = SystemParameter.query.filter_by(name='last_mrn').first()
    
    if last_mrn_param:
        # Parse the last MRN
        last_mrn = last_mrn_param.value  # Format: "00-00-00-00"
        parts = last_mrn.split('-')  # Split into parts
        # Convert to integers and increment the last part
        numbers = [int(part) for part in parts]
        
        # Increment the MRN (handling carry-over)
        carry = 1
        for i in range(len(numbers) - 1, -1, -1):
            numbers[i] += carry
            if numbers[i] > 99:
                numbers[i] = 0
                carry = 1
            else:
                carry = 0
                break
        
        # Format the new MRN
        new_mrn = '-'.join(f"{num:02d}" for num in numbers)
    else:
        # If no last MRN exists, start with "00-00-00-01"
        new_mrn = "00-00-00-01"
    
    # Update the system parameter with the new MRN
    if last_mrn_param:
        last_mrn_param.value = new_mrn
    else:
        # Create a new system parameter if it doesn't exist
        last_mrn_param = SystemParameter(
            name='last_mrn',
            value=new_mrn,
            description='Last used Medical Record Number for patient registration'
        )
        db.session.add(last_mrn_param)
    
    # Commit the changes to the database
    db.session.commit()
    
    return new_mrn