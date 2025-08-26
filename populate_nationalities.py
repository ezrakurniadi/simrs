import os
import sys
from app import create_app, db
from app.patients.models import Nationality
import uuid

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def populate_nationalities():
    app = create_app()
    with app.app_context():
        # Check if nationality table exists and has data
        existing_nationalities = Nationality.query.all()
        if existing_nationalities:
            print(f"Found {len(existing_nationalities)} existing nationalities. Skipping population.")
            return
        
        # Define the nationalities to add
        nationalities_data = [
            {"name": "Indonesian"},
            {"name": "American"},
            {"name": "European"},
            {"name": "Asian"},
            {"name": "African"},
            {"name": "Australian"},
            {"name": "Canadian"},
            {"name": "British"},
            {"name": "Chinese"},
            {"name": "Japanese"},
            {"name": "Korean"},
            {"name": "Indian"},
            {"name": "Brazilian"},
            {"name": "Mexican"},
            {"name": "Russian"},
            {"name": "Middle Eastern"}
        ]
        
        # Add nationalities to the database
        for nat_data in nationalities_data:
            # Check if nationality already exists
            existing = Nationality.query.filter_by(name=nat_data["name"]).first()
            if not existing:
                nationality = Nationality(
                    id=str(uuid.uuid4()),
                    name=nat_data["name"]
                )
                db.session.add(nationality)
        
        # Commit the changes
        db.session.commit()
        print(f"Added {len(nationalities_data)} nationalities to the database.")

if __name__ == "__main__":
    populate_nationalities()