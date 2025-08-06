#!/usr/bin/env python
"""Script to test login functionality."""

import requests
from bs4 import BeautifulSoup

def test_login():
    """Test login functionality with proper CSRF handling."""
    session = requests.Session()
    
    # Get login page to retrieve CSRF token
    print("Getting login page...")
    login_page = session.get('http://127.0.0.1:5000/login')
    print(f"Login page status: {login_page.status_code}")
    
    # Parse the login page to extract CSRF token
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    print(f"CSRF token: {csrf_token}")
    
    # Try to login with correct CSRF token
    login_data = {
        'username': 'admin',
        'password': 'password',
        'submit': 'Sign In',
        'csrf_token': csrf_token
    }
    
    print("Attempting login...")
    response = session.post('http://127.0.0.1:5000/login', data=login_data)
    print(f"Login response status: {response.status_code}")
    print(f"Login response URL: {response.url}")
    
    # Check if login was successful
    if 'patients' in response.url or 'admin' in response.url:
        print("Login successful!")
        
        # Try to access admin users page
        print("Accessing admin users page...")
        admin_users = session.get('http://127.0.0.1:5000/admin/users')
        print(f"Admin users page status: {admin_users.status_code}")
        print(f"Admin users page URL: {admin_users.url}")
        
        if admin_users.status_code == 200:
            print("Admin users page loaded successfully!")
            return True
        else:
            print("Failed to access admin users page")
            return False
    else:
        print("Login failed!")
        # Check for flash messages
        soup = BeautifulSoup(response.text, 'html.parser')
        flash_messages = soup.find_all('div', class_='alert')
        for msg in flash_messages:
            print(f"Flash message: {msg.get_text().strip()}")
        return False

if __name__ == '__main__':
    test_login()