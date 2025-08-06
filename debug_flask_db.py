#!/usr/bin/env python
"""Script to debug Flask-Migrate commands."""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.auth.models import db
from flask_migrate import Migrate

def debug_flask_db():
    """Debug Flask-Migrate commands."""
    print("Creating Flask app...")
    app = create_app()
    
    print("Initializing Flask-Migrate...")
    migrate = Migrate(app, db)
    
    print("App config:")
    print(f"  SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print(f"  FLASK_ENV: {app.config.get('FLASK_ENV')}")
    
    with app.app_context():
        try:
            print("Database engine info:")
            print(f"  Database URL: {db.engine.url}")
            
            # Try to connect to the database
            print("Testing database connection...")
            connection = db.engine.connect()
            print("  Connection successful!")
            connection.close()
            
            # Check current revision
            from alembic.runtime.migration import MigrationContext
            from alembic.script import ScriptDirectory
            from flask_migrate import Config
            
            # Try to get current revision
            try:
                config = Config("migrations/alembic.ini")
                config.set_main_option("script_location", "migrations")
                script = ScriptDirectory.from_config(config)
                migration_context = MigrationContext.configure(db.engine.connect())
                current_rev = migration_context.get_current_revision()
                print(f"  Current revision: {current_rev}")
            except Exception as e:
                print(f"  Could not get current revision: {e}")
            
            print("Database debug completed successfully!")
            
        except Exception as e:
            print(f"Database debug failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == '__main__':
    debug_flask_db()