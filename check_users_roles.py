#!/usr/bin/env python
"""Script to check all users and their roles."""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.auth.models import User, Role

def check_users_roles():
    """Check all users and their roles."""
    app = create_app()
    
    with app.app_context():
        # Get all users
        users = User.query.all()
        print(f"Total users: {len(users)}")
        
        # Get all roles
        roles = Role.query.all()
        print(f"Total roles: {len(roles)}")
        for role in roles:
            print(f"  Role: {role.name} - {role.description}")
        
        print("\nUsers and their roles:")
        for user in users:
            role_names = [role.name for role in user.roles]
            print(f"  {user.username} ({user.email}) - Roles: {', '.join(role_names) if role_names else 'No roles'}")
        
        print("\nReceptionist users:")
        receptionists = [user for user in users if user.has_role('Receptionist')]
        if receptionists:
            for user in receptionists:
                print(f"  {user.username} ({user.email})")
        else:
            print("  No receptionist users found")
        
        print("User roles check completed successfully!")

if __name__ == '__main__':
    check_users_roles()