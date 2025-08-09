from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

# Import db from the app factory
from app import db

# System parameter model for managing application settings
class SystemParameter(db.Model):
    __tablename__ = 'system_parameters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)

    def __repr__(self):
        return f'<SystemParameter {self.name}>'

# Nationality model for patient registration
class Nationality(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Nationality {self.name}>'

# Function to get all nationalities
def get_all_nationalities():
    return Nationality.query.all()

# Helper functions for dashboard statistics
def get_nationalities_count():
    """Get the total count of nationalities in the system."""
    return Nationality.query.count()

def get_active_settings_count():
    """Get the count of active system settings."""
    # This would query the actual settings table in a real implementation
    return 15  # Placeholder value

def get_system_updates_count():
    """Get the count of available system updates."""
    # This would query the actual updates table in a real implementation
    return 3  # Placeholder value

def get_last_updated():
    """Get the timestamp of the last system update."""
    # This would query the actual updates table in a real implementation
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Placeholder value
