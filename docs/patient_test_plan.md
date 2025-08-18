# Patient Registration Form Test Plan

## 1. Test Form Creation
- Verify that all fields are present in the PatientRegistrationForm
- Verify that all fields are present in the PatientForm (edit form)
- Verify that new dynamic fields are included:
  - problematic_patient_reason
  - loyalty_member_number
  - chronic_condition_details
  - allergy_alert_details

## 2. Test Form Validation
- Test validation for required fields
- Test validation for email format
- Test validation for date format
- Test validation for new dynamic fields when their corresponding boolean fields are True

## 3. Test Form Submission
- Test successful submission with all fields filled correctly
- Test submission with dynamic fields filled when their corresponding boolean fields are True
- Test submission with dynamic fields empty when their corresponding boolean fields are False

## 4. Test Form Rendering
- Verify that the form renders correctly in the browser
- Verify that dynamic fields are hidden by default
- Verify that dynamic fields appear when their corresponding boolean fields are set to True
- Verify that dynamic fields disappear when their corresponding boolean fields are set to False

## 5. Test Database Integration
- Verify that submitted data is correctly stored in the database
- Verify that dynamic field data is correctly stored when their corresponding boolean fields are True
- Verify that dynamic field data is not stored (or stored as NULL) when their corresponding boolean fields are False

## 6. Test Edge Cases
- Test submission with very long text in text fields
- Test submission with special characters in text fields
- Test submission with empty optional fields
- Test submission with invalid data types

## Updated Test Code

### Current Test Code (tests/test_patient_forms.py)
```python
import unittest
from flask import Flask
from flask_testing import TestCase
from app import create_app
from app.patients.forms import PatientForm, PatientRegistrationForm
from app.patients.models import Patient, db

class TestPatientForms(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_patient_registration_form(self):
        form = PatientRegistrationForm()
        self.assertIsNotNone(form.first_name)
        self.assertIsNotNone(form.last_name)
        self.assertIsNotNone(form.date_of_birth)
        self.assertIsNotNone(form.gender)
        self.assertIsNotNone(form.address)
        self.assertIsNotNone(form.phone)
        self.assertIsNotNone(form.email)
        self.assertIsNotNone(form.emergency_contact_name)
        self.assertIsNotNone(form.emergency_contact_phone)
        self.assertIsNotNone(form.emergency_contact_relationship)
        self.assertIsNotNone(form.insurance_provider)
        self.assertIsNotNone(form.is_deceased)

        # Test form validation
        form.first_name.data = 'John'
        form.last_name.data = 'Doe'
        form.date_of_birth.data = '1980-01-01'
        form.gender.data = 'Male'
        self.assertTrue(form.validate())

    def test_patient_edit_form(self):
        form = PatientForm()
        self.assertIsNotNone(form.first_name)
        self.assertIsNotNone(form.last_name)
        self.assertIsNotNone(form.date_of_birth)
        self.assertIsNotNone(form.gender)
        self.assertIsNotNone(form.address)
        self.assertIsNotNone(form.phone)
        self.assertIsNotNone(form.email)
        self.assertIsNotNone(form.id_type)
        self.assertIsNotNone(form.id_card_number)
        self.assertIsNotNone(form.blood_type)
        self.assertIsNotNone(form.birthplace)
        self.assertIsNotNone(form.marriage_status)
        self.assertIsNotNone(form.nationality_id)
        self.assertIsNotNone(form.vip_status)
        self.assertIsNotNone(form.problematic_patient)
        self.assertIsNotNone(form.loyalty_member)
        self.assertIsNotNone(form.ihs_number)
        self.assertIsNotNone(form.chronic_condition)
        self.assertIsNotNone(form.allergy_alert)
        self.assertIsNotNone(form.preferred_communication)
        self.assertIsNotNone(form.preferred_language)
        self.assertIsNotNone(form.emergency_contact_name)
        self.assertIsNotNone(form.emergency_contact_phone)
        self.assertIsNotNone(form.emergency_contact_relationship)

        # Test form validation
        form.first_name.data = 'Jane'
        form.last_name.data = 'Doe'
        form.date_of_birth.data = '1990-01-01'
        form.gender.data = 'Female'
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
```

### Updated Test Code
```python
import unittest
from flask import Flask
from flask_testing import TestCase
from app import create_app
from app.patients.forms import PatientForm, PatientRegistrationForm
from app.patients.models import Patient, db

class TestPatientForms(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_patient_registration_form(self):
        form = PatientRegistrationForm()
        self.assertIsNotNone(form.first_name)
        self.assertIsNotNone(form.last_name)
        self.assertIsNotNone(form.date_of_birth)
        self.assertIsNotNone(form.gender)
        self.assertIsNotNone(form.address)
        self.assertIsNotNone(form.phone)
        self.assertIsNotNone(form.email)
        self.assertIsNotNone(form.emergency_contact_name)
        self.assertIsNotNone(form.emergency_contact_phone)
        self.assertIsNotNone(form.emergency_contact_relationship)
        self.assertIsNotNone(form.insurance_provider)
        self.assertIsNotNone(form.is_deceased)
        # New fields
        self.assertIsNotNone(form.vip_status)
        self.assertIsNotNone(form.problematic_patient)
        self.assertIsNotNone(form.problematic_patient_reason)
        self.assertIsNotNone(form.loyalty_member)
        self.assertIsNotNone(form.loyalty_member_number)
        self.assertIsNotNone(form.chronic_condition)
        self.assertIsNotNone(form.chronic_condition_details)
        self.assertIsNotNone(form.allergy_alert)
        self.assertIsNotNone(form.allergy_alert_details)
        self.assertIsNotNone(form.id_type)
        self.assertIsNotNone(form.id_card_number)
        self.assertIsNotNone(form.blood_type)
        self.assertIsNotNone(form.birthplace)
        self.assertIsNotNone(form.marriage_status)
        self.assertIsNotNone(form.preferred_communication)
        self.assertIsNotNone(form.preferred_language)

        # Test form validation
        form.first_name.data = 'John'
        form.last_name.data = 'Doe'
        form.date_of_birth.data = '1980-01-01'
        form.gender.data = 'Male'
        self.assertTrue(form.validate())

    def test_patient_edit_form(self):
        form = PatientForm()
        self.assertIsNotNone(form.first_name)
        self.assertIsNotNone(form.last_name)
        self.assertIsNotNone(form.date_of_birth)
        self.assertIsNotNone(form.gender)
        self.assertIsNotNone(form.address)
        self.assertIsNotNone(form.phone)
        self.assertIsNotNone(form.email)
        self.assertIsNotNone(form.id_type)
        self.assertIsNotNone(form.id_card_number)
        self.assertIsNotNone(form.blood_type)
        self.assertIsNotNone(form.birthplace)
        self.assertIsNotNone(form.marriage_status)
        self.assertIsNotNone(form.nationality_id)
        self.assertIsNotNone(form.vip_status)
        self.assertIsNotNone(form.problematic_patient)
        self.assertIsNotNone(form.problematic_patient_reason)
        self.assertIsNotNone(form.loyalty_member)
        self.assertIsNotNone(form.loyalty_member_number)
        self.assertIsNotNone(form.ihs_number)
        self.assertIsNotNone(form.chronic_condition)
        self.assertIsNotNone(form.chronic_condition_details)
        self.assertIsNotNone(form.allergy_alert)
        self.assertIsNotNone(form.allergy_alert_details)
        self.assertIsNotNone(form.preferred_communication)
        self.assertIsNotNone(form.preferred_language)
        self.assertIsNotNone(form.emergency_contact_name)
        self.assertIsNotNone(form.emergency_contact_phone)
        self.assertIsNotNone(form.emergency_contact_relationship)

        # Test form validation
        form.first_name.data = 'Jane'
        form.last_name.data = 'Doe'
        form.date_of_birth.data = '1990-01-01'
        form.gender.data = 'Female'
        self.assertTrue(form.validate())

    def test_patient_form_with_dynamic_fields(self):
        form = PatientForm()
        
        # Test validation with dynamic fields when corresponding boolean is True
        form.first_name.data = 'Jane'
        form.last_name.data = 'Doe'
        form.date_of_birth.data = '1990-01-01'
        form.gender.data = 'Female'
        form.problematic_patient.data = 'True'
        form.problematic_patient_reason.data = 'Patient has a history of aggressive behavior'
        form.loyalty_member.data = 'True'
        form.loyalty_member_number.data = 'LM123456'
        form.chronic_condition.data = 'True'
        form.chronic_condition_details.data = 'Patient has diabetes and hypertension'
        form.allergy_alert.data = 'True'
        form.allergy_alert_details.data = 'Patient is allergic to penicillin'
        
        self.assertTrue(form.validate())
        
        # Test validation with dynamic fields when corresponding boolean is False
        form.problematic_patient.data = 'False'
        form.problematic_patient_reason.data = ''  # Should be ignored
        form.loyalty_member.data = 'False'
        form.loyalty_member_number.data = ''  # Should be ignored
        form.chronic_condition.data = 'False'
        form.chronic_condition_details.data = ''  # Should be ignored
        form.allergy_alert.data = 'False'
        form.allergy_alert_details.data = ''  # Should be ignored
        
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()