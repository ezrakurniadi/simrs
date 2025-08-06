#!/usr/bin/env python
"""Script to debug Flask-Migrate issues."""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.auth.models import db, User, Role
from flask_migrate import Migrate

def debug_migrations():
    """Debug Flask-Migrate issues."""
    print("Creating Flask app...")
    app = create_app()
    
    print("Initializing database...")
    with app.app_context():
        try:
            # Check if tables exist
            print("Checking existing tables...")
            tables = db.engine.table_names()
            print(f"Existing tables: {tables}")
            
            # Check if our models would create tables
            print("Checking model tables...")
            print(f"User table: {User.__tablename__}")
            print(f"Role table: {Role.__tablename__}")
            
            # Check if the association table exists in metadata
            from app.auth.models import user_roles
            print(f"Association table: {user_roles.name}")
            
            print("Database debug completed successfully!")
            
        except Exception as e:
            print(f"Database debug failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == '__main__':
    debug_migrations()