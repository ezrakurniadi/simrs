#!/usr/bin/env python
"""Script to create a user with a specific role."""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.auth.models import db, User, Role
from app.patients.models import Patient

def create_user():
    """Create a user with a specific role."""
    app = create_app()
    
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username='admin').first()
        if existing_user:
            print("User 'admin' already exists.")
            return
        
        # Create user
        user = User(
            username='admin',
            email='admin@example.com',
            first_name='Admin',
            last_name='User'
        )
        user.set_password('password')
        
        # Assign role
        role = Role.query.filter_by(name='Admin').first()
        if role:
            user.roles.append(role)
        else:
            print("Admin role not found. Please run seed_roles.py first.")
            return
        
        db.session.add(user)
        db.session.commit()
        print("User 'admin' created successfully with Admin role!")

if __name__ == '__main__':
    create_user()