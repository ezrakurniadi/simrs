#!/usr/bin/env python
"""Script to test user view functionality."""

import requests
from bs4 import BeautifulSoup

def test_user_view():
    """Test user view functionality."""
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
        
        # Access admin users page
        print("Accessing admin users page...")
        admin_users = session.get('http://127.0.0.1:5000/admin/users')
        print(f"Admin users page status: {admin_users.status_code}")
        
        if admin_users.status_code == 200:
            print("Admin users page loaded successfully!")
            
            # Parse the users page to find user links
            soup = BeautifulSoup(admin_users.text, 'html.parser')
            user_links = soup.find_all('a', href=lambda x: x and 'admin/users/' in x and 'view' in x)
            
            if user_links:
                # Get the first user view link
                user_view_url = user_links[0]['href']
                print(f"Found user view link: {user_view_url}")
                
                # Access the user view page
                print("Accessing user view page...")
                user_view = session.get(f'http://127.0.0.1:5000{user_view_url}')
                print(f"User view page status: {user_view.status_code}")
                print(f"User view page URL: {user_view.url}")
                
                if user_view.status_code == 200:
                    print("User view page loaded successfully!")
                    return True
                else:
                    print("Failed to load user view page")
                    return False
            else:
                print("No user view links found")
                # Let's try to access the admin user directly by ID
                print("Trying to access admin user by ID...")
                user_view = session.get('http://127.0.0.1:5000/admin/users/c98854cd-e686-4390-ba43-2f50b960e9df')
                print(f"User view page status: {user_view.status_code}")
                if user_view.status_code == 200:
                    print("User view page loaded successfully!")
                    return True
                else:
                    print("Failed to load user view page")
                    return False
        else:
            print("Failed to access admin users page")
            return False
    else:
        print("Login failed!")
        return False

if __name__ == '__main__':
    test_user_view()