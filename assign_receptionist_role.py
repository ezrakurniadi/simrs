#!/usr/bin/env python
"""Script to assign the receptionist role to the existing receptionist user."""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.auth.models import db, User, Role

def assign_receptionist_role():
    """Assign the receptionist role to the existing receptionist user."""
    app = create_app()
    
    with app.app_context():
        # Check if receptionist user exists
        user = User.query.filter_by(username='receptionist').first()
        if not user:
            print("User 'receptionist' not found.")
            return
        
        # Check if receptionist role exists
        role = Role.query.filter_by(name='Receptionist').first()
        if not role:
            print("Receptionist role not found.")
            return
        
        # Check if user already has the role
        if user.has_role('Receptionist'):
            print("User 'receptionist' already has the Receptionist role.")
            return
        
        # Assign role to user
        user.roles.append(role)
        
        try:
            db.session.commit()
            print("Receptionist role assigned to user 'receptionist' successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to assign role: {str(e)}")

if __name__ == '__main__':
    assign_receptionist_role()