import uuid
from app.auth.models import db, User, Patient

class ClinicalNote(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    written_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    note_type = db.Column(db.String(50), nullable=False)  # e.g., 'Progress Note', 'Consultation Note', etc.
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    patient = db.relationship('Patient', backref=db.backref('clinical_notes', lazy=True))
    author = db.relationship('User', backref=db.backref('written_clinical_notes', lazy=True))