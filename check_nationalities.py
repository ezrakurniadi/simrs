import os
import sys
from app import create_app, db
from app.patients.models import Nationality

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_nationalities():
    app = create_app()
    with app.app_context():
        # Check if nationality table exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'nationality' in tables:
            print("'nationality' table exists")
            
            # Get all nationalities
            nationalities = Nationality.query.all()
            print(f"Found {len(nationalities)} nationalities:")
            for nationality in nationalities:
                print(f"  - {nationality.name} (ID: {nationality.id})")
        else:
            print("'nationality' table does NOT exist")

if __name__ == "__main__":
    check_nationalities()