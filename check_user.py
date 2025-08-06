#!/usr/bin/env python
"""Script to check user information."""

from app import create_app
from app.auth.models import User

def check_user():
    """Check user information."""
    app = create_app()
    
    with app.app_context():
        try:
            user = User.query.first()
            if user:
                print(f"User: {user.username}, ID: {user.id}")
                print(f"Email: {user.email}")
                print(f"Roles: {[role.name for role in user.roles]}")
            else:
                print("No users found")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    check_user()