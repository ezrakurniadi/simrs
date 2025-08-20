"""
Script to populate races table with comprehensive data.
This script should be run once after the database tables are created.
"""

import sys
import os
# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.system_params.models import db, Race

# Comprehensive race data (from the previous hardcoded list)
RACES_DATA = [
    {"name": "American Indian or Alaska Native", "description": "American Indian or Alaska Native race"},
    {"name": "Asian", "description": "Asian race"},
    {"name": "Black or African American", "description": "Black or African American race"},
    {"name": "Hispanic or Latino", "description": "Hispanic or Latino race"},
    {"name": "Native Hawaiian or Other Pacific Islander", "description": "Native Hawaiian or Other Pacific Islander race"},
    {"name": "White", "description": "White race"},
    {"name": "Other", "description": "Other race"},
    {"name": "Prefer not to say", "description": "Prefer not to say"}
]

def populate_races():
    """Populate the races table with data."""
    print("Populating races...")
    for race_data in RACES_DATA:
        # Check if race already exists
        existing = Race.query.filter_by(name=race_data['name']).first()
        if not existing:
            race = Race(**race_data)
            db.session.add(race)
            print(f"Added race: {race_data['name']}")
    
    db.session.commit()
    print("Races populated successfully.")

def main():
    """Main function to run the population script."""
    app = create_app()
    with app.app_context():
        # Populate data
        populate_races()
        
        print("Database population completed!")

if __name__ == '__main__':
    main()