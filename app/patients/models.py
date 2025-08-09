from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
import uuid
from app.system_params.models import Nationality

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
    insurance_provider = db.Column(db.String(100), nullable=True)
    is_deceased = db.Column(db.Boolean, default=False)

    nationality = db.relationship('Nationality', backref=db.backref('patients', lazy=True))

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'

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