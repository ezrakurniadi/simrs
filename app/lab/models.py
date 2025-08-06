import uuid
from app.auth.models import db, User, Patient

class LabOrder(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    ordered_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    test_type = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    status = db.Column(db.String(20), default='Ordered')  # Ordered, Completed, Cancelled
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    patient = db.relationship('Patient', backref=db.backref('lab_orders', lazy=True))
    orderer = db.relationship('User', backref=db.backref('ordered_labs', lazy=True))


class LabResult(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('lab_order.id'), nullable=False)
    performed_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    result_data = db.Column(db.Text, nullable=False)
    result_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    released = db.Column(db.Boolean, default=False, nullable=False)  # Whether the result has been released to the patient
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    order = db.relationship('LabOrder', backref=db.backref('lab_results', lazy=True))
    performer = db.relationship('User', backref=db.backref('performed_labs', lazy=True))