import uuid
from sqlalchemy.dialects.postgresql import JSONB
from app.auth.models import Patient, User, db
from app.hospital.models import Room

class Appointment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.String(36), db.ForeignKey('room.id'))
    scheduled_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, default=30)  # Duration in minutes
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Completed, Cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases
    
    # Relationships
    patient = db.relationship('Patient', backref=db.backref('appointments', lazy=True))
    doctor = db.relationship('User', backref=db.backref('appointments', lazy=True))
    room = db.relationship('Room', backref=db.backref('appointments', lazy=True))