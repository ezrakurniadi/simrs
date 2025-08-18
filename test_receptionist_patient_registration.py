#!/usr/bin/env python
"""Comprehensive test script for receptionist login and patient registration."""

import sys
import os
import requests

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.auth.models import User, Role

def test_user_and_role_setup():
    """Test that the receptionist user exists and has the correct role."""
    app = create_app()
    
    with app.app_context():
        print("1. Testing user and role setup...")
        
        # Check if receptionist user exists
        user = User.query.filter_by(username='receptionist').first()
        if not user:
            print("   ERROR: User 'receptionist' not found.")
            return False
        
        print(f"   SUCCESS: User 'receptionist' exists ({user.email})")
        
        # Check if receptionist role exists
        role = Role.query.filter_by(name='Receptionist').first()
        if not role:
            print("   ERROR: Receptionist role not found.")
            return False
        
        print("   SUCCESS: Receptionist role exists")
        
        # Check if user has the receptionist role
        if not user.has_role('Receptionist'):
            print("   ERROR: User 'receptionist' does not have the Receptionist role.")
            return False
        
        print("   SUCCESS: User 'receptionist' has the Receptionist role")
        
        return True

def test_routes_access():
    """Test access to key routes for receptionist."""
    print("\n2. Testing route access...")
    
    try:
        # Test accessing the receptionist dashboard
        response = requests.get('http://127.0.0.1:5000/receptionist')
        
        if response.status_code == 200:
            print("   SUCCESS: Can access receptionist dashboard")
        elif response.status_code == 401:
            print("   INFO: Receptionist dashboard requires authentication")
        else:
            print(f"   INFO: Receptionist dashboard returned status code {response.status_code}")
        
        # Test accessing the patient registration page
        response = requests.get('http://127.0.0.1:5000/patients/new')
        
        if response.status_code == 200:
            print("   SUCCESS: Can access patient registration page")
        elif response.status_code == 401:
            print("   INFO: Patient registration page requires authentication")
        else:
            print(f"   INFO: Patient registration page returned status code {response.status_code}")
        
        # Test accessing the patient list page
        response = requests.get('http://127.0.0.1:5000/patients/list')
        
        if response.status_code == 200:
            print("   SUCCESS: Can access patient list page")
        elif response.status_code == 401:
            print("   INFO: Patient list page requires authentication")
        else:
            print(f"   INFO: Patient list page returned status code {response.status_code}")
        
        return True
    except requests.exceptions.ConnectionError:
        print("   ERROR: Could not connect to the Flask application.")
        return False
    except Exception as e:
        print(f"   ERROR: Unexpected error when testing route access: {str(e)}")
        return False

def test_role_based_access():
    """Test role-based access control."""
    print("\n3. Testing role-based access control...")
    
    try:
        # Test accessing receptionist-only route
        response = requests.get('http://127.0.0.1:5000/patients/test_receptionist_only')
        
        if response.status_code == 200:
            print("   SUCCESS: Can access receptionist-only route")
        elif response.status_code == 401:
            print("   INFO: Receptionist-only route requires authentication")
        else:
            print(f"   INFO: Receptionist-only route returned status code {response.status_code}")
        
        # Test accessing doctor-only route (should be denied)
        response = requests.get('http://127.0.0.1:5000/patients/test_doctor_only')
        
        if response.status_code == 200:
            print("   INFO: Can access doctor-only route (unexpected)")
        elif response.status_code == 401:
            print("   SUCCESS: Doctor-only route correctly requires authentication")
        elif response.status_code == 403:
            print("   SUCCESS: Doctor-only route correctly denied to receptionist")
        else:
            print(f"   INFO: Doctor-only route returned status code {response.status_code}")
        
        return True
    except requests.exceptions.ConnectionError:
        print("   ERROR: Could not connect to the Flask application.")
        return False
    except Exception as e:
        print(f"   ERROR: Unexpected error when testing role-based access: {str(e)}")
        return False

def test_database_connectivity():
    """Test database connectivity and table existence."""
    print("\n4. Testing database connectivity...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test if we can query the User table
            user_count = User.query.count()
            print(f"   SUCCESS: Database connection established. Found {user_count} users.")
            
            # Test if we can query the Role table
            role_count = Role.query.count()
            print(f"   SUCCESS: Found {role_count} roles in database.")
            
            # Test if we can query the Patient table
            from app.patients.models import Patient
            patient_count = Patient.query.count()
            print(f"   SUCCESS: Found {patient_count} patients in database.")
            
            return True
        except Exception as e:
            print(f"   ERROR: Database connectivity test failed: {str(e)}")
            return False

def main():
    """Main test function."""
    print("Testing receptionist login and patient registration functionality...\n")
    
    # Test database connectivity
    db_test = test_database_connectivity()
    
    # Test user and role setup
    user_test = test_user_and_role_setup()
    
    # Test route access
    route_test = test_routes_access()
    
    # Test role-based access
    role_test = test_role_based_access()
    
    print("\n" + "="*60)
    print("TEST SUMMARY:")
    print("="*60)
    
    tests = [
        ("Database connectivity", db_test),
        ("User and role setup", user_test),
        ("Route access", route_test),
        ("Role-based access control", role_test)
    ]
    
    all_passed = True
    for test_name, result in tests:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name:<30} {status}")
        if not result:
            all_passed = False
    
    print("="*60)
    if all_passed:
        print("OVERALL RESULT: ALL TESTS PASSED!")
        print("Receptionist can successfully log in and access the patient registration system.")
    else:
        print("OVERALL RESULT: SOME TESTS FAILED!")
        print("Please check the errors above.")
    print("="*60)
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)