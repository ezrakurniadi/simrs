from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, current_user
from app.patients.auth import bp
from app.patients.auth_forms import PatientLoginForm, PatientRegistrationForm
from app.patients.models import PatientUser, Patient, db
from urllib.parse import urlparse

@bp.route('/patient/login', methods=['GET', 'POST'])
def patient_login():
    if current_user.is_authenticated and isinstance(current_user, PatientUser):
        return redirect(url_for('patients.patient_dashboard'))
    
    form = PatientLoginForm()
    if form.validate_on_submit():
        try:
            user = PatientUser.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('patient_auth.patient_login'))
            
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('patients.patient_dashboard')
            return redirect(next_page)
        except Exception as e:
            flash('An error occurred during login. Please try again.')
            # Log the error for debugging (in a real application, you would use a proper logger)
            print(f"Error during patient login: {str(e)}")
    
    return render_template('patients/auth/login.html', title='Patient Sign In', form=form)

@bp.route('/patient/logout')
def patient_logout():
    logout_user()
    return redirect(url_for('patient_auth.patient_login'))

@bp.route('/patient/register', methods=['GET', 'POST'])
def patient_register():
    if current_user.is_authenticated and isinstance(current_user, PatientUser):
        return redirect(url_for('patients.patient_dashboard'))
    
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        try:
            # Check if patient exists with the provided email
            patient = Patient.query.filter_by(email=form.email.data).first()
            if not patient:
                flash('No patient record found with this email address')
                return redirect(url_for('patient_auth.patient_register'))
            
            # Check if user account already exists for this patient
            existing_user = PatientUser.query.filter_by(patient_id=patient.id).first()
            if existing_user:
                flash('An account already exists for this patient')
                return redirect(url_for('patient_auth.patient_login'))
            
            # Create new patient user
            user = PatientUser(
                username=form.username.data,
                email=form.email.data,
                patient_id=patient.id
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now registered as a patient user!')
            return redirect(url_for('patient_auth.patient_login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.')
            # Log the error for debugging (in a real application, you would use a proper logger)
            print(f"Error during patient registration: {str(e)}")
    
    return render_template('patients/auth/register.html', title='Patient Register', form=form)