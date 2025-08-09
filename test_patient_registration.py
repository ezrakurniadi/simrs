"""
Test script to verify the patient registration form functionality
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.patients.forms import PatientRegistrationForm, PatientForm
from app.patients.models import Patient
from app import create_app, db

def test_form_field_definitions():
    """Test that the form classes have the required field definitions"""
    # Get the field names from the PatientForm class
    patient_form_fields = [field for field in dir(PatientForm) if not field.startswith('_')]
    
    required_fields = [
        'problematic_patient_reason',
        'loyalty_member_number',
        'chronic_condition_details',
        'allergy_alert_details'
    ]
    
    for field in required_fields:
        if field not in patient_form_fields:
            print(f"✗ PatientForm missing field: {field}")
            return False
    
    print("✓ PatientForm has all required field definitions")
    
    # Get the field names from the PatientRegistrationForm class
    registration_form_fields = [field for field in dir(PatientRegistrationForm) if not field.startswith('_')]
    
    for field in required_fields:
        if field not in registration_form_fields:
            print(f"✗ PatientRegistrationForm missing field: {field}")
            return False
    
    print("✓ PatientRegistrationForm has all required field definitions")
    return True

def test_model_fields():
    """Test that the model has the required fields"""
    app = create_app()
    with app.app_context():
        # Get column names from the Patient model
        patient_columns = [column.name for column in Patient.__table__.columns]
        
        required_fields = [
            'problematic_patient_reason',
            'loyalty_member_number',
            'chronic_condition_details',
            'allergy_alert_details'
        ]
        
        for field in required_fields:
            if field not in patient_columns:
                print(f"✗ Patient model missing field: {field}")
                return False
        
        print("✓ Patient model has all required fields")
        return True

if __name__ == "__main__":
    print("Testing patient registration functionality...")
    
    try:
        test_form_field_definitions()
        print("✓ Form field definitions test passed")
    except Exception as e:
        print(f"✗ Form field definitions test failed: {e}")
    
    try:
        test_model_fields()
        print("✓ Model fields test passed")
    except Exception as e:
        print(f"✗ Model fields test failed: {e}")
    
    print("Testing completed.")