import os
import sys
from app import create_app, db
from sqlalchemy import text

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_tables():
    app = create_app()
    with app.app_context():
        # Get all table names using inspector
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("Database tables:")
        for table in tables:
            print(f"  - {table}")
        
        # Check if 'user' table exists
        if 'user' in tables:
            print("\n'user' table exists")
        else:
            print("\n'user' table does NOT exist")

if __name__ == "__main__":
    check_tables()