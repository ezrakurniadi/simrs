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
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
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
        self.assertIsNotNone(form.insurance_policy_id)
        self.assertIsNotNone(form.insurance_group_number)
        self.assertIsNotNone(form.guarantor_name)
        self.assertIsNotNone(form.guarantor_relationship)
        self.assertIsNotNone(form.guarantor_phone)
        self.assertIsNotNone(form.guarantor_address)
        self.assertIsNotNone(form.is_deceased)

        # Test form validation with required choices set
        form.first_name.data = 'John'
        form.last_name.data = 'Doe'
        form.date_of_birth.data = '1980-01-01'
        form.gender.data = 'Male'
        form.id_type.choices = [('1', 'KTP')]
        form.id_type.data = '1'
        form.id_card_number.data = '123456789'
        form.blood_type.data = 'A+'
        form.marriage_status.data = 'Single'
        form.nationality_id.choices = [('1', 'Indonesia')]
        form.nationality_id.data = '1'
        form.vip_status.data = 'False'
        form.problematic_patient.data = 'False'
        form.loyalty_member.data = 'False'
        form.chronic_condition.data = 'False'
        form.allergy_alert.data = 'False'
        form.race.data = ''
        form.ethnicity.data = ''
        form.is_deceased.data = 'False'
        form.email.data = 'john.doe@example.com'
        # Test new insurance and guarantor fields
        form.insurance_provider.data = 'ABC Insurance'
        form.insurance_policy_id.data = 'POL123456'
        form.insurance_group_number.data = 'GRP789012'
        form.guarantor_name.data = 'Jane Smith'
        form.guarantor_relationship.data = 'Spouse'
        form.guarantor_phone.data = '555-1234'
        form.guarantor_address.data = '123 Main St, City, State'
        # Test new consent and privacy fields
        form.consent_to_treat.data = 'True'
        form.privacy_practices_acknowledged.data = 'True'
        # Print form errors for debugging
        if not form.validate():
            print("Form errors:", form.errors)
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
        self.assertIsNotNone(form.insurance_provider)
        self.assertIsNotNone(form.insurance_policy_id)
        self.assertIsNotNone(form.insurance_group_number)
        self.assertIsNotNone(form.guarantor_name)
        self.assertIsNotNone(form.guarantor_relationship)
        self.assertIsNotNone(form.guarantor_phone)
        self.assertIsNotNone(form.guarantor_address)
        self.assertIsNotNone(form.chronic_condition)
        self.assertIsNotNone(form.allergy_alert)
        self.assertIsNotNone(form.preferred_communication)
        self.assertIsNotNone(form.preferred_language)
        self.assertIsNotNone(form.emergency_contact_name)
        self.assertIsNotNone(form.emergency_contact_phone)
        self.assertIsNotNone(form.emergency_contact_relationship)

        # Test form validation with required choices set
        form.first_name.data = 'Jane'
        form.last_name.data = 'Doe'
        form.date_of_birth.data = '1990-01-01'
        form.gender.data = 'Female'
        form.id_type.choices = [('1', 'KTP')]
        form.id_type.data = '1'
        form.id_card_number.data = '123456789'
        form.blood_type.data = 'A+'
        form.marriage_status.data = 'Single'
        form.nationality_id.choices = [('1', 'Indonesia')]
        form.nationality_id.data = '1'
        form.vip_status.data = 'False'
        form.problematic_patient.data = 'False'
        form.loyalty_member.data = 'False'
        form.chronic_condition.data = 'False'
        form.allergy_alert.data = 'False'
        form.race.data = ''
        form.ethnicity.data = ''
        form.is_deceased.data = 'False'
        form.email.data = 'jane.doe@example.com'
        # Test new insurance and guarantor fields
        form.insurance_provider.data = 'XYZ Insurance'
        form.insurance_policy_id.data = 'POL987654'
        form.insurance_group_number.data = 'GRP321098'
        form.guarantor_name.data = 'John Smith'
        form.guarantor_relationship.data = 'Spouse'
        form.guarantor_phone.data = '555-5678'
        form.guarantor_address.data = '456 Oak Ave, City, State'
        # Test new consent and privacy fields
        form.consent_to_treat.data = 'True'
        form.privacy_practices_acknowledged.data = 'True'
        # Print form errors for debugging
        if not form.validate():
            print("Form errors:", form.errors)
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()