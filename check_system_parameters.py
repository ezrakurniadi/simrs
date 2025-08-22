import sys
import os
from app import create_app, db
from app.system_params.models import Ethnicity, Language

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_system_parameters():
    app = create_app()
    
    with app.app_context():
        print("Checking system parameters...")
        
        # Check ethnicities
        print("\n--- Ethnicities ---")
        ethnicities = Ethnicity.query.all()
        for ethnicity in ethnicities:
            print(f"ID: {ethnicity.id}, Name: {ethnicity.name}")
        
        # Check languages
        print("\n--- Languages ---")
        languages = Language.query.all()
        for language in languages:
            print(f"ID: {language.id}, Name: {language.name}, ISO Code: {language.iso_code}")

if __name__ == "__main__":
    check_system_parameters()