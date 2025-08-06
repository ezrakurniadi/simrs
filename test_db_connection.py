#!/usr/bin/env python
"""Script to test the database connection."""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.auth.models import db, User, Role

def test_db_connection():
    """Test the database connection."""
    app = create_app()
    
    with app.app_context():
        try:
            # Try to query the database
            user_count = User.query.count()
            role_count = Role.query.count()
            
            print("Database connection successful!")
            print(f"Number of users: {user_count}")
            print(f"Number of roles: {role_count}")
            
            # Try to get all roles
            roles = Role.query.all()
            print("Roles in database:")
            for role in roles:
                print(f"  - {role.name}: {role.description}")
                
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    return True

if __name__ == '__main__':
    test_db_connection()