# Patient Registration Route Changes

## 1. Update Route to Handle New Fields
- Update the patient registration route to handle the new fields for Problematic Patient, Loyalty Member, Chronic Condition, and Allergy Alert
- Add validation for the new fields

## Implementation Details

### Current Route (app/patients/routes.py)
```python
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.patients import bp
from app.utils import roles_required
from app.patients.forms import PatientForm, PatientSearchForm, VitalsForm, AllergyForm, MedicationForm, PatientRegistrationForm
from app.patients.models import Patient, Vitals, Allergy, Medication, db, PatientUser
from app.auth.models import User
from app.clinical_notes.models import ClinicalNote
from app.hospital.models import Admission

@bp.route('/patients/new', methods=['GET', 'POST'])
@roles_required('Receptionist')
def create_patient():
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        try:
            # Create new patient
            patient = Patient(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                date_of_birth=form.date_of_birth.data,
                gender=form.gender.data,
                address=form.address.data,
                phone=form.phone.data,
                email=form.email.data,
                id_type=form.id_type.data,
                id_card_number=form.id_card_number.data,
                blood_type=form.blood_type.data,
                birthplace=form.birthplace.data,
                marriage_status=form.marriage_status.data,
                nationality_id=form.nationality.data,
                is_vip=form.is_vip.data,
                is_problematic=form.is_problematic.data,
                is_loyalty_member=form.is_loyalty_member.data,
                ihs_number=form.ihs_number.data,
                has_chronic_condition=form.has_chronic_condition.data,
                has_allergy_alert=form.has_allergy_alert.data,
                preferred_communication=form.preferred_communication.data,
                preferred_language=form.preferred_language.data,
                emergency_contact_name=form.emergency_contact_name.data,
                emergency_contact_phone=form.emergency_contact_phone.data,
                emergency_contact_relationship=form.emergency_contact_relationship.data,
                insurance_provider=form.insurance_provider.data,
                is_deceased=form.is_deceased.data,
                created_by=str(current_user.id)  # Store the ID of the user creating the patient
            )

            # Add patient to database
            db.session.add(patient)
            db.session.commit()

            flash('Patient registered successfully!', 'success')
            return redirect(url_for('patients.index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while registering the patient. Please try again.', 'error')
            # Log the error for debugging (in a real application, you would use a proper logger)
            print(f"Error registering patient: {str(e)}")

    return render_template('patients/new.html', form=form)

@bp.route('/patients/<int:id>/edit', methods=['GET', 'POST'])
@roles_required('Receptionist')
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    form = PatientForm(obj=patient)

    if form.validate_on_submit():
        try:
            # Update patient information
            patient.first_name = form.first_name.data
            patient.last_name = form.last_name.data
            patient.date_of_birth = form.date_of_birth.data
            patient.gender = form.gender.data
            patient.address = form.address.data
            patient.phone = form.phone.data
            patient.email = form.email.data
            patient.id_type = form.id_type.data
            patient.id_card_number = form.id_card_number.data
            patient.blood_type = form.blood_type.data
            patient.birthplace = form.birthplace.data
            patient.marriage_status = form.marriage_status.data
            patient.nationality_id = form.nationality.data
            patient.is_vip = form.is_vip.data
            patient.is_problematic = form.is_problematic.data
            patient.is_loyalty_member = form.is_loyalty_member.data
            patient.ihs_number = form.ihs_number.data
            patient.has_chronic_condition = form.has_chronic_condition.data
            patient.has_allergy_alert = form.has_allergy_alert.data
            patient.preferred_communication = form.preferred_communication.data
            patient.preferred_language = form.preferred_language.data
            patient.emergency_contact_name = form.emergency_contact_name.data
            patient.emergency_contact_phone = form.emergency_contact_phone.data
            patient.emergency_contact_relationship = form.emergency_contact_relationship.data

            db.session.commit()

            flash('Patient information updated successfully!', 'success')
            return redirect(url_for('patients.view_patient', id=patient.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the patient. Please try again.', 'error')
            print(f"Error updating patient: {str(e)}")

    return render_template('patients/edit.html', form=form, patient=patient)
```

### Updated Route
```python
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.patients import bp
from app.utils import roles_required
from app.patients.forms import PatientForm, PatientSearchForm, VitalsForm, AllergyForm, MedicationForm, PatientRegistrationForm
from app.patients.models import Patient, Vitals, Allergy, Medication, db, PatientUser
from app.auth.models import User
from app.clinical_notes.models import ClinicalNote
from app.hospital.models import Admission

@bp.route('/patients/new', methods=['GET', 'POST'])
@roles_required('Receptionist')
def create_patient():
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        try:
            # Create new patient
            patient = Patient(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                date_of_birth=form.date_of_birth.data,
                gender=form.gender.data,
                address=form.address.data,
                phone=form.phone.data,
                email=form.email.data,
                id_type=form.id_type.data,
                id_card_number=form.id_card_number.data,
                blood_type=form.blood_type.data,
                birthplace=form.birthplace.data,
                marriage_status=form.marriage_status.data,
                nationality_id=form.nationality.data,
                vip_status=form.vip_status.data,
                problematic_patient=form.problematic_patient.data,
                problematic_patient_reason=form.problematic_patient_reason.data if form.problematic_patient.data == 'True' else None,
                loyalty_member=form.loyalty_member.data,
                loyalty_member_number=form.loyalty_member_number.data if form.loyalty_member.data == 'True' else None,
                ihs_number=form.ihs_number.data,
                chronic_condition=form.chronic_condition.data,
                chronic_condition_details=form.chronic_condition_details.data if form.chronic_condition.data == 'True' else None,
                allergy_alert=form.allergy_alert.data,
                allergy_alert_details=form.allergy_alert_details.data if form.allergy_alert.data == 'True' else None,
                preferred_communication=form.preferred_communication.data,
                preferred_language=form.preferred_language.data,
                emergency_contact_name=form.emergency_contact_name.data,
                emergency_contact_phone=form.emergency_contact_phone.data,
                emergency_contact_relationship=form.emergency_contact_relationship.data,
                insurance_provider=form.insurance_provider.data,
                is_deceased=form.is_deceased.data,
                created_by=str(current_user.id)  # Store the ID of the user creating the patient
            )

            # Add patient to database
            db.session.add(patient)
            db.session.commit()

            flash('Patient registered successfully!', 'success')
            return redirect(url_for('patients.index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while registering the patient. Please try again.', 'error')
            # Log the error for debugging (in a real application, you would use a proper logger)
            print(f"Error registering patient: {str(e)}")

    return render_template('patients/new.html', form=form)

@bp.route('/patients/<int:id>/edit', methods=['GET', 'POST'])
@roles_required('Receptionist')
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    form = PatientForm(obj=patient)

    if form.validate_on_submit():
        try:
            # Update patient information
            patient.first_name = form.first_name.data
            patient.last_name = form.last_name.data
            patient.date_of_birth = form.date_of_birth.data
            patient.gender = form.gender.data
            patient.address = form.address.data
            patient.phone = form.phone.data
            patient.email = form.email.data
            patient.id_type = form.id_type.data
            patient.id_card_number = form.id_card_number.data
            patient.blood_type = form.blood_type.data
            patient.birthplace = form.birthplace.data
            patient.marriage_status = form.marriage_status.data
            patient.nationality_id = form.nationality.data
            patient.vip_status = form.vip_status.data
            patient.problematic_patient = form.problematic_patient.data
            patient.problematic_patient_reason = form.problematic_patient_reason.data if form.problematic_patient.data == 'True' else None
            patient.loyalty_member = form.loyalty_member.data
            patient.loyalty_member_number = form.loyalty_member_number.data if form.loyalty_member.data == 'True' else None
            patient.ihs_number = form.ihs_number.data
            patient.chronic_condition = form.chronic_condition.data
            patient.chronic_condition_details = form.chronic_condition_details.data if form.chronic_condition.data == 'True' else None
            patient.allergy_alert = form.allergy_alert.data
            patient.allergy_alert_details = form.allergy_alert_details.data if form.allergy_alert.data == 'True' else None
            patient.preferred_communication = form.preferred_communication.data
            patient.preferred_language = form.preferred_language.data
            patient.emergency_contact_name = form.emergency_contact_name.data
            patient.emergency_contact_phone = form.emergency_contact_phone.data
            patient.emergency_contact_relationship = form.emergency_contact_relationship.data

            db.session.commit()

            flash('Patient information updated successfully!', 'success')
            return redirect(url_for('patients.view_patient', id=patient.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the patient. Please try again.', 'error')
            print(f"Error updating patient: {str(e)}")

    return render_template('patients/edit.html', form=form, patient=patient)