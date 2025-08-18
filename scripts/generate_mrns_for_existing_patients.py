#!/usr/bin/env python
"""
Script to generate MRNs for existing patients in the database.
This script should be run once after deploying the MRN feature to assign 
MRNs to all patients who don't already have one.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.patients.models import Patient, generate_mrn

def generate_mrns_for_existing_patients():
    """Generate MRNs for all existing patients who don't have one."""
    app = create_app()
    
    with app.app_context():
        # Get all patients without an MRN
        patients_without_mrn = Patient.query.filter(
            (Patient.mrn.is_(None)) | (Patient.mrn == '')
        ).all()
        
        print(f"Found {len(patients_without_mrn)} patients without MRNs")
        
        # Generate MRNs for each patient
        for i, patient in enumerate(patients_without_mrn, 1):
            # Generate a new MRN
            new_mrn = generate_mrn()
            
            # Assign the MRN to the patient
            patient.mrn = new_mrn
            
            # Print progress
            print(f"Assigned MRN {new_mrn} to patient {patient.first_name} {patient.last_name}")
            
            # Commit every 100 patients to avoid memory issues with large datasets
            if i % 100 == 0:
                db.session.commit()
                print(f"Committed {i} patients...")
        
        # Commit any remaining patients
        db.session.commit()
        
        print(f"Successfully assigned MRNs to {len(patients_without_mrn)} patients")

if __name__ == "__main__":
    generate_mrns_for_existing_patients()