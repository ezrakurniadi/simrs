#!/usr/bin/env python
"""Script to check if roles exist in the database."""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.auth.models import db, Role

def check_roles():
    """Check if roles exist in the database."""
    app = create_app()
    
    with app.app_context():
        roles = Role.query.all()
        if roles:
            print("Existing roles:")
            for role in roles:
                print(f"  - {role.name}: {role.description}")
        else:
            print("No roles found in the database.")

if __name__ == '__main__':
    check_roles()