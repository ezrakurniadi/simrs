#!/usr/bin/env python
"""Script to test admin functionality."""

import requests
from app import create_app
from app.auth.models import User

def test_admin():
    """Test admin functionality."""
    app = create_app()
    
    with app.app_context():
        # Get the admin user
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("Admin user not found")
            return
        
        print(f"Found user: {user.username}, ID: {user.id}")
        print(f"User roles: {[role.name for role in user.roles]}")
        
        # Test login via requests
        session = requests.Session()
        
        # Get login page to retrieve CSRF token
        login_page = session.get('http://127.0.0.1:5000/login')
        print(f"Login page status: {login_page.status_code}")
        
        # Try to login
        login_data = {
            'username': 'admin',
            'password': 'password',
            'submit': 'Sign In'
        }
        
        response = session.post('http://127.0.0.1:5000/login', data=login_data)
        print(f"Login response status: {response.status_code}")
        print(f"Login response URL: {response.url}")
        
        # Try to access admin users page
        admin_users = session.get('http://127.0.0.1:5000/admin/users')
        print(f"Admin users page status: {admin_users.status_code}")
        print(f"Admin users page URL: {admin_users.url}")

if __name__ == '__main__':
    test_admin()