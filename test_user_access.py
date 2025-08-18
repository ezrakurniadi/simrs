#!/usr/bin/env python
"""Script to test user data access."""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.auth.models import User

def test_user_access():
    """Test that we can access user data."""
    app = create_app()
    
    with app.app_context():
        # Count users
        user_count = User.query.count()
        print(f"Total users: {user_count}")
        
        # Get first user
        first_user = User.query.first()
        if first_user:
            print(f"First user: {first_user.username} ({first_user.email})")
        else:
            print("No users found")
        
        print("User data access test completed successfully!")

if __name__ == '__main__':
    test_user_access()