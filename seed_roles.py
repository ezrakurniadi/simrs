#!/usr/bin/env python
"""Script to seed the database with initial roles."""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.auth.models import db, Role

def seed_roles():
    """Seed the database with initial roles."""
    app = create_app()
    
    with app.app_context():
        # Check if roles already exist
        existing_roles = Role.query.all()
        if existing_roles:
            print("Roles already exist in the database. Skipping seeding.")
            return
        
        # Create initial roles
        roles_data = [
            {'name': 'Admin', 'description': 'System administrator with full access'},
            {'name': 'Doctor', 'description': 'Medical doctor with patient access'},
            {'name': 'Receptionist', 'description': 'Receptionist with patient registration access'},
            {'name': 'Lab Technician', 'description': 'Laboratory technician with test result access'},
            {'name': 'Nurse', 'description': 'Nurse with patient care access'}
        ]
        
        for role_data in roles_data:
            role = Role(name=role_data['name'], description=role_data['description'])
            db.session.add(role)
        
        db.session.commit()
        print("Roles seeded successfully!")

if __name__ == '__main__':
    seed_roles()