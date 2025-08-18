from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz
from app import db

# Remove the user_roles table definition since it's defined in auth/models.py

class SystemParameter(db.Model):
    __tablename__ = 'system_parameters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255))
    # Remove parameter_type as it doesn't exist in the existing table
    # Remove is_active as it doesn't exist in the existing table
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # Remove created_by and updated_by as they don't exist in the existing table

    def __repr__(self):
        return f'<SystemParameter {self.parameter_name}>'

class PayorType(db.Model):
    __tablename__ = 'payor_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<PayorType {self.name}>'

class PayorDetail(db.Model):
    __tablename__ = 'payor_details'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    payor_type_id = db.Column(db.Integer, db.ForeignKey('payor_types.id'), nullable=False)
    is_active = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Relationship
    payor_type = db.relationship('PayorType', backref=db.backref('details', lazy=True))

    def __repr__(self):
        return f'<PayorDetail {self.name}>'

class IDType(db.Model):
    __tablename__ = 'id_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<IDType {self.name}>'

class Ethnicity(db.Model):
    __tablename__ = 'ethnicities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Ethnicity {self.name}>'

class Language(db.Model):
    __tablename__ = 'languages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    iso_code = db.Column(db.String(10), unique=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Language {self.name}>'

# Helper functions for use in routes
def get_all_nationalities():
    """Get all nationalities from the database"""
    from app.patients.models import Nationality
    return Nationality.query.all()

def get_nationalities_count():
    """Get count of all nationalities"""
    from app.patients.models import Nationality
    return Nationality.query.count()

def get_active_settings_count():
    """Get count of active system parameters"""
    # Since is_active doesn't exist in the system_parameters table, count all
    return SystemParameter.query.count()

def get_system_updates_count():
    """Get count of system parameters"""
    return SystemParameter.query.count()

def get_last_updated():
    """Get the most recent update timestamp"""
    last_update = SystemParameter.query.order_by(SystemParameter.updated_at.desc()).first()
    return last_update.updated_at if last_update else None
