from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.patients import bp
from app.utils import roles_required
from app.patients.forms import PatientForm, PatientSearchForm, VitalsForm, AllergyForm, MedicationForm
from app.patients.models import Patient, Vitals, Allergy, Medication, db, PatientUser
from app.auth.models import User
from app.clinical_notes.models import ClinicalNote
from app.hospital.models import Admission
def is_patient_admitted(patient_id):
    """Check if a patient is currently admitted"""
    admission = Admission.query.filter_by(
        patient_id=patient_id,
        status='Admitted'
    ).first()
    return admission is not None

@bp.route('/')
@bp.route('/patients')
@roles_required('Receptionist', 'Doctor', 'Nurse')
def index():
    return render_template('patients/index.html')

@bp.route('/patients', methods=['GET'])
@roles_required('Receptionist', 'Doctor', 'Nurse')
def list_patients():
    # Get all patients
    patients = Patient.query.all()
    return render_template('patients/list.html', patients=patients)

@bp.route('/patients/<int:id>', methods=['GET'])
@roles_required('Doctor', 'Nurse', 'Receptionist')
def view_patient(id):
    patient = Patient.query.get_or_404(id)
    is_admitted = is_patient_admitted(patient.id)
    return render_template('patients/view.html', patient=patient, is_admitted=is_admitted)

    return render_template('patients/view.html', patient=patient)

@bp.route('/patients/new', methods=['GET', 'POST'])
@roles_required('Receptionist')
def create_patient():
    form = PatientForm()
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
def edit_patient(id):
    # TODO: Implement patient edit logic
    return render_template('patients/edit.html')

# Test route for role-based access control decorator
@bp.route('/patients/test_doctor_only', methods=['GET'])
@roles_required('Doctor')
def test_doctor_only():
    return "Success! You are a Doctor or have Doctor role."

@bp.route('/patients/test_receptionist_only', methods=['GET'])
@roles_required('Receptionist')
def test_receptionist_only():
    return "Success! You are a Receptionist or have Receptionist role."

@bp.route('/patients/test_multiple_roles', methods=['GET'])
@roles_required('Doctor', 'Nurse')
def test_multiple_roles():
    return "Success! You are either a Doctor or Nurse (or have one of these roles)."

@bp.route('/patients/search', methods=['GET', 'POST'])
@roles_required('Receptionist', 'Doctor')
def search_patients():
    form = PatientSearchForm()
    patients = []
    if form.validate_on_submit() or request.method == 'GET':
        # Build query based on form data
        query = Patient.query
        
        if form.first_name.data:
            query = query.filter(Patient.first_name.ilike(f"%{form.first_name.data}%"))
        if form.last_name.data:
            query = query.filter(Patient.last_name.ilike(f"%{form.last_name.data}%"))
        if form.date_of_birth.data:
            query = query.filter(Patient.date_of_birth == form.date_of_birth.data)
        if form.gender.data:
            query = query.filter(Patient.gender == form.gender.data)
        if form.phone.data:
            query = query.filter(Patient.phone.ilike(f"%{form.phone.data}%"))
        
        patients = query.all()
    
    return render_template('patients/search.html', form=form, patients=patients)

@bp.route('/patients/<int:patient_id>/vitals', methods=['GET'])
@roles_required('Doctor', 'Nurse')
def view_vitals(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    vitals = Vitals.query.filter_by(patient_id=patient.id).order_by(Vitals.date.desc()).all()
    return render_template('patients/vitals/view.html', patient=patient, vitals=vitals)

@bp.route('/patients/<int:patient_id>/vitals/new', methods=['GET', 'POST'])
@roles_required('Doctor', 'Nurse')
def add_vitals(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = VitalsForm()
    
    if form.validate_on_submit():
        try:
            vitals = Vitals(
                patient_id=patient.id,
                recorded_by=str(current_user.id),
                date=form.date.data,
                bp_systolic=form.bp_systolic.data,
                bp_diastolic=form.bp_diastolic.data,
                heart_rate=form.heart_rate.data,
                temperature=form.temperature.data,
                weight=form.weight.data,
                height=form.height.data
            )
            
            db.session.add(vitals)
            db.session.commit()
            
            flash('Vital signs recorded successfully!', 'success')
            return redirect(url_for('patients.view_vitals', patient_id=patient.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while recording vital signs. Please try again.', 'error')
            print(f"Error recording vital signs: {str(e)}")
    
    return render_template('patients/vitals/new.html', form=form, patient=patient)

@bp.route('/patients/<int:patient_id>/encounters', methods=['GET'])
@roles_required('Doctor', 'Nurse')
def view_encounters(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Get all clinical notes for this patient
    clinical_notes = ClinicalNote.query.filter_by(patient_id=patient.id).order_by(ClinicalNote.date.desc()).all()
    
    # Get all vital signs for this patient
    vitals = Vitals.query.filter_by(patient_id=patient.id).order_by(Vitals.date.desc()).all()
    
    # Combine and sort all encounters by date
    encounters = []
    
    # Add clinical notes to encounters list
    for note in clinical_notes:
        encounters.append({
            'type': 'clinical_note',
            'date': note.date,
            'data': note
        })
    
    # Add vital signs to encounters list
    for vital in vitals:
        encounters.append({
            'type': 'vital_signs',
            'date': vital.date,
            'data': vital
        })
    
    # Add lab results to encounters list
    from app.lab.models import LabOrder, LabResult
    lab_orders = LabOrder.query.filter_by(patient_id=patient.id).order_by(LabOrder.order_date.desc()).all()
    for order in lab_orders:
        # Only include completed lab orders that have results
        if order.status == 'Completed' and order.lab_results:
            for result in order.lab_results:
                encounters.append({
                    'type': 'lab_result',
                    'date': result.result_date,
                    'data': {
                        'order': order,
                        'result': result
                    }
                })
    
    # Sort encounters by date (most recent first)
    # Sort encounters by date (most recent first)
    encounters.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template('patients/encounters.html', patient=patient, encounters=encounters)

# Allergy routes
@bp.route('/patients/<int:patient_id>/allergies', methods=['GET'])
@roles_required('Doctor', 'Nurse')
def view_allergies(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    allergies = Allergy.query.filter_by(patient_id=patient.id).order_by(Allergy.recorded_date.desc()).all()
    return render_template('patients/allergies/view.html', patient=patient, allergies=allergies)

@bp.route('/patients/<int:patient_id>/allergies/new', methods=['GET', 'POST'])
@roles_required('Doctor', 'Nurse')
def add_allergy(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = AllergyForm()
    
    # Set default recorded_date to current time
    if not form.recorded_date.data:
        from datetime import datetime
        form.recorded_date.data = datetime.now()
    
    if form.validate_on_submit():
        try:
            allergy = Allergy(
                patient_id=patient.id,
                allergen=form.allergen.data,
                reaction=form.reaction.data,
                severity=form.severity.data,
                recorded_date=form.recorded_date.data,
                recorded_by=str(current_user.id)
            )
            
            db.session.add(allergy)
            db.session.commit()
            
            flash('Allergy recorded successfully!', 'success')
            return redirect(url_for('patients.view_allergies', patient_id=patient.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while recording the allergy. Please try again.', 'error')
            print(f"Error recording allergy: {str(e)}")
    
    return render_template('patients/allergies/new.html', form=form, patient=patient)

@bp.route('/patients/<int:patient_id>/allergies/<allergy_id>/edit', methods=['GET', 'POST'])
@roles_required('Doctor', 'Nurse')
def edit_allergy(patient_id, allergy_id):
    patient = Patient.query.get_or_404(patient_id)
    allergy = Allergy.query.get_or_404(allergy_id)
    
    # Ensure the allergy belongs to the patient
    if allergy.patient_id != patient.id:
        flash('Allergy not found for this patient.', 'error')
        return redirect(url_for('patients.view_allergies', patient_id=patient.id))
    
    form = AllergyForm(obj=allergy)
    
    if form.validate_on_submit():
        try:
            allergy.allergen = form.allergen.data
            allergy.reaction = form.reaction.data
            allergy.severity = form.severity.data
            allergy.recorded_date = form.recorded_date.data
            allergy.recorded_by = str(current_user.id)
            
            db.session.commit()
            
            flash('Allergy updated successfully!', 'success')
            return redirect(url_for('patients.view_allergies', patient_id=patient.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the allergy. Please try again.', 'error')
            print(f"Error updating allergy: {str(e)}")
    
    return render_template('patients/allergies/edit.html', form=form, patient=patient, allergy=allergy)

# Medication routes
@bp.route('/patients/<int:patient_id>/medications', methods=['GET'])
@roles_required('Doctor', 'Nurse')
def view_medications(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    medications = Medication.query.filter_by(patient_id=patient.id).order_by(Medication.start_date.desc()).all()
    return render_template('patients/medications/view.html', patient=patient, medications=medications)

@bp.route('/patients/<int:patient_id>/medications/new', methods=['GET', 'POST'])
@roles_required('Doctor')
def prescribe_medication(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = MedicationForm()
    
    # Set default start_date to current date
    if not form.start_date.data:
        from datetime import date
        form.start_date.data = date.today()
    
    if form.validate_on_submit():
        try:
            medication = Medication(
                patient_id=patient.id,
                prescribed_by=str(current_user.id),
                drug_name=form.drug_name.data,
                dosage=form.dosage.data,
                frequency=form.frequency.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                status=form.status.data
            )
            
            db.session.add(medication)
            db.session.commit()
            
            flash('Medication prescribed successfully!', 'success')
            return redirect(url_for('patients.view_medications', patient_id=patient.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while prescribing the medication. Please try again.', 'error')
            print(f"Error prescribing medication: {str(e)}")
    
    return render_template('patients/medications/new.html', form=form, patient=patient)

@bp.route('/patients/<int:patient_id>/medications/<medication_id>/edit', methods=['GET', 'POST'])
@roles_required('Doctor')
def edit_medication(patient_id, medication_id):
    patient = Patient.query.get_or_404(patient_id)
    medication = Medication.query.get_or_404(medication_id)
    
    # Ensure the medication belongs to the patient
    if medication.patient_id != patient.id:
        flash('Medication not found for this patient.', 'error')
        return redirect(url_for('patients.view_medications', patient_id=patient.id))
    
    form = MedicationForm(obj=medication)
    
    if form.validate_on_submit():
        try:
            medication.drug_name = form.drug_name.data
            medication.dosage = form.dosage.data
            medication.frequency = form.frequency.data
            medication.start_date = form.start_date.data
            medication.end_date = form.end_date.data
            medication.status = form.status.data
            
            db.session.commit()
            
            flash('Medication updated successfully!', 'success')
            return redirect(url_for('patients.view_medications', patient_id=patient.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the medication. Please try again.', 'error')
            print(f"Error updating medication: {str(e)}")
    
    return render_template('patients/medications/edit.html', form=form, patient=patient, medication=medication)

@bp.route('/patients/dashboard')
def patient_dashboard():
    # Check if current user is a PatientUser
    if not isinstance(current_user, PatientUser):
        flash('Access denied. Patients only.', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        # Get upcoming appointments for the patient
        from app.appointments.models import Appointment
        from app.auth.models import User
        from datetime import datetime
        upcoming_appointments = Appointment.query.filter(
            Appointment.patient_id == current_user.patient.id,
            Appointment.scheduled_time >= datetime.now(),
            Appointment.status == 'Scheduled'
        ).order_by(Appointment.scheduled_time.asc()).limit(5).all()
        
        # Preload doctor information for upcoming appointments
        for appointment in upcoming_appointments:
            appointment.doctor = User.query.get(appointment.doctor_id)
        
        # Get appointment history for the patient
        appointment_history = Appointment.query.filter(
            Appointment.patient_id == current_user.patient.id,
            (Appointment.scheduled_time < datetime.now()) | (Appointment.status != 'Scheduled')
        ).order_by(Appointment.scheduled_time.desc()).limit(5).all()
        
        # Preload doctor information for appointment history
        for appointment in appointment_history:
            appointment.doctor = User.query.get(appointment.doctor_id)
        
        return render_template('patients/dashboard.html',
                             patient=current_user.patient,
                             upcoming_appointments=upcoming_appointments,
                             appointment_history=appointment_history)
    except Exception as e:
        flash('An error occurred while loading the dashboard. Please try again.', 'error')
        # Log the error for debugging (in a real application, you would use a proper logger)
        print(f"Error loading patient dashboard: {str(e)}")
        return redirect(url_for('patient_auth.patient_login'))

@bp.route('/patients/lab_results', methods=['GET'])
def view_lab_results():
    # Check if current user is a PatientUser
    if not isinstance(current_user, PatientUser):
        flash('Access denied. Patients only.', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        # Get released lab results for the patient
        from app.lab.models import LabOrder, LabResult
        lab_results = db.session.query(LabResult).join(LabOrder).filter(
            LabOrder.patient_id == current_user.patient.id,
            LabResult.released == True
        ).order_by(LabResult.result_date.desc()).all()
        
        return render_template('patients/lab_results.html',
                             patient=current_user.patient,
                             lab_results=lab_results)
    except Exception as e:
        flash('An error occurred while loading lab results. Please try again.', 'error')
        print(f"Error loading patient lab results: {str(e)}")
        return redirect(url_for('patients.patient_dashboard'))