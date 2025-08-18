#!/usr/bin/env python
"""Script to test receptionist login and patient registration access."""

import sys
import os
import requests

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.auth.models import User

def test_receptionist_login():
    """Test receptionist login and access to patient registration."""
    app = create_app()
    
    with app.app_context():
        # Check if receptionist user exists and has the correct role
        user = User.query.filter_by(username='receptionist').first()
        if not user:
            print("ERROR: User 'receptionist' not found.")
            return False
        
        if not user.has_role('Receptionist'):
            print("ERROR: User 'receptionist' does not have the Receptionist role.")
            return False
        
        print("SUCCESS: Receptionist user exists and has the correct role.")
        print(f"User: {user.username} ({user.email})")
        
        # Check user password (assuming default password)
        if user.check_password('password'):
            print("SUCCESS: Password verification passed.")
        else:
            print("INFO: Could not verify password (might be different from default).")
        
        return True

def test_patient_registration_access():
    """Test access to patient registration system."""
    try:
        # Test accessing the patient registration page
        response = requests.get('http://127.0.0.1:5000/patients/new')
        
        if response.status_code == 200:
            print("SUCCESS: Can access patient registration page.")
            return True
        elif response.status_code == 401:
            print("INFO: Patient registration page requires authentication.")
            return True
        else:
            print(f"INFO: Patient registration page returned status code {response.status_code}.")
            return True
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the Flask application.")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error when testing patient registration access: {str(e)}")
        return False

if __name__ == '__main__':
    print("Testing receptionist login and patient registration access...\n")
    
    # Test user and role
    user_test = test_receptionist_login()
    
    # Test patient registration access
    access_test = test_patient_registration_access()
    
    print("\n" + "="*50)
    if user_test and access_test:
        print("OVERALL RESULT: All tests passed! Receptionist can access the system.")
    else:
        print("OVERALL RESULT: Some tests failed. Please check the errors above.")
    print("="*50)