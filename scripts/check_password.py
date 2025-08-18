#!/usr/bin/env python
"""Script to check user password."""

from app import create_app
from app.auth.models import User

def check_password():
    """Check user password."""
    app = create_app()
    
    with app.app_context():
        user = User.query.filter_by(username='admin').first()
        if user:
            print(f"User: {user.username}")
            print(f"Password hash: {user.password_hash}")
            print(f"Password check: {user.check_password('password')}")
        else:
            print("No admin user found")

if __name__ == '__main__':
    check_password()