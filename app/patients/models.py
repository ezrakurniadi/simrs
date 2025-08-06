import uuid
from sqlalchemy.dialects.postgresql import JSONB
from flask_sqlalchemy import SQLAlchemy
from app.auth.models import User, Patient

db = SQLAlchemy()

class Vitals(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    recorded_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    bp_systolic = db.Column(db.Integer)
    bp_diastolic = db.Column(db.Integer)
    heart_rate = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    patient = db.relationship('Patient', backref=db.backref('vitals', lazy=True))
    recorder = db.relationship('User', backref=db.backref('recorded_vitals', lazy=True))

class Allergy(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    allergen = db.Column(db.String(100), nullable=False)
    reaction = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # Mild, Moderate, Severe
    recorded_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    recorded_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    patient = db.relationship('Patient', backref=db.backref('allergies', lazy=True))
    recorder = db.relationship('User', backref=db.backref('recorded_allergies', lazy=True))

class Medication(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    prescribed_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    drug_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Active')  # Active, Completed, Discontinued
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    patient = db.relationship('Patient', backref=db.backref('medications', lazy=True))
    prescriber = db.relationship('User', backref=db.backref('prescribed_medications', lazy=True))

from flask_login import UserMixin
import bcrypt
from app.hospital.models import Admission
def is_patient_admitted(patient_id):
    """Check if a patient is currently admitted"""
    admission = Admission.query.filter_by(patient_id=patient_id, status='Admitted').first()
    return admission is not None

from app.hospital.models import Admission

class PatientUser(UserMixin, db.Model):
    __tablename__ = 'patient_user'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationship with Patient model
    patient = db.relationship('Patient', backref=db.backref('user_account', lazy=True, uselist=False))
    
    def set_password(self, password):
        # Hash a password with bcrypt
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        # Check a hashed password
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))