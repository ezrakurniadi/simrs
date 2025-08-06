#!/usr/bin/env python
"""Script to test all admin functionality."""

import requests
from bs4 import BeautifulSoup

def test_admin_functionality():
    """Test all admin functionality."""
    session = requests.Session()
    
    # Get login page to retrieve CSRF token
    print("Getting login page...")
    login_page = session.get('http://127.0.0.1:5000/login')
    print(f"Login page status: {login_page.status_code}")
    
    # Parse the login page to extract CSRF token
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    print(f"CSRF token: {csrf_token}")
    
    # Login with correct CSRF token
    login_data = {
        'username': 'admin',
        'password': 'password',
        'submit': 'Sign In',
        'csrf_token': csrf_token
    }
    
    print("Attempting login...")
    response = session.post('http://127.0.0.1:5000/login', data=login_data)
    print(f"Login response status: {response.status_code}")
    
    # Check if login was successful
    if response.status_code == 302 or 'patients' in response.url or 'admin' in response.url:
        print("Login successful!")
        
        # Test 1: Admin dashboard
        print("\n=== Testing Admin Dashboard ===")
        admin_dashboard = session.get('http://127.0.0.1:5000/admin')
        print(f"Admin dashboard status: {admin_dashboard.status_code}")
        if admin_dashboard.status_code == 200:
            print("✓ Admin dashboard loads successfully")
        else:
            print("✗ Failed to load admin dashboard")
            return False
        
        # Test 2: Admin users list
        print("\n=== Testing Admin Users List ===")
        admin_users = session.get('http://127.0.0.1:5000/admin/users')
        print(f"Admin users page status: {admin_users.status_code}")
        if admin_users.status_code == 200:
            print("✓ Admin users list loads successfully")
        else:
            print("✗ Failed to load admin users list")
            return False
        
        # Test 3: User view page
        print("\n=== Testing User View Page ===")
        user_view = session.get('http://127.0.0.1:5000/admin/users/c98854cd-e686-4390-ba43-2f50b960e9df')
        print(f"User view page status: {user_view.status_code}")
        if user_view.status_code == 200:
            print("✓ User view page loads successfully")
        else:
            print("✗ Failed to load user view page")
            return False
        
        # Test 4: Admin roles list
        print("\n=== Testing Admin Roles List ===")
        admin_roles = session.get('http://127.0.0.1:5000/admin/roles')
        print(f"Admin roles page status: {admin_roles.status_code}")
        if admin_roles.status_code == 200:
            print("✓ Admin roles list loads successfully")
        else:
            print("✗ Failed to load admin roles list")
            return False
        
        # Test 5: Admin role creation page (GET request)
        print("\n=== Testing Admin Role Creation Page ===")
        create_role = session.get('http://127.0.0.1:5000/admin/roles/new')
        print(f"Create role page status: {create_role.status_code}")
        if create_role.status_code == 200:
            print("✓ Admin role creation page loads successfully")
        else:
            print("✗ Failed to load admin role creation page")
            return False
        
        print("\n=== All Admin Functionality Tests Passed ===")
        return True
        
    else:
        print("Login failed!")
        return False

if __name__ == '__main__':
    success = test_admin_functionality()
    if success:
        print("\n🎉 All admin functionality is working correctly!")
    else:
        print("\n❌ Some admin functionality is not working.")