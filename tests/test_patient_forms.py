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