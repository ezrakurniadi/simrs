from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from app.nurse import bp
from app.utils import roles_required
from app.appointments.models import Appointment
from app.clinical_notes.models import ClinicalNote
from app.patients.models import Patient, Vitals, Allergy
from app.hospital.models import Admission, Bed, Ward
from app.auth.models import User
from datetime import date, datetime, timedelta


@bp.route('/patients')
@roles_required('Nurse')
def dashboard():
    try:
        # Get today's date
        today = date.today()
        
        # Get today's appointments (for all doctors, as nurses may assist with appointments)
        today_appointments = Appointment.query.filter(
            Appointment.scheduled_time >= today,
            Appointment.scheduled_time < today + timedelta(days=1)
        ).order_by(Appointment.scheduled_time).all()
        
        # Preload related data to avoid N+1 query problem
        for appointment in today_appointments:
            appointment.patient = Patient.query.get(appointment.patient_id)
            appointment.doctor = User.query.get(appointment.doctor_id)
            if appointment.room_id:
                from app.hospital.models import Room
                appointment.room = Room.query.get(appointment.room_id)
            else:
                appointment.room = None
        
        # Get recent patient encounters (last 5 vital signs recorded by any user)
        recent_encounters = Vitals.query.order_by(Vitals.date.desc()).limit(5).all()
        
        # Preload related data for vital signs
        for encounter in recent_encounters:
            encounter.patient = Patient.query.get(encounter.patient_id)
            encounter.recorder = User.query.get(encounter.recorded_by)
        
        # Get bed availability summary
        total_beds = Bed.query.count()
        occupied_beds = Bed.query.filter_by(is_occupied=True).count()
        available_beds = total_beds - occupied_beds
        
        # Get patients list (limited to 10 for dashboard)
        patients = Patient.query.limit(10).all()
        
        # Get recent admissions
        recent_admissions = Admission.query.filter_by(status='Admitted').order_by(Admission.admission_date.desc()).limit(5).all()
        
        # Preload related data for admissions
        for admission in recent_admissions:
            admission.patient = Patient.query.get(admission.patient_id)
            admission.bed = Bed.query.get(admission.bed_id)
            if admission.bed and admission.bed.ward_room:
                admission.ward = admission.bed.ward_room.ward
            else:
                admission.ward = None
        
        return render_template('nurse/dashboard.html',
                              today_appointments=today_appointments,
                              recent_encounters=recent_encounters,
                              total_beds=total_beds,
                              occupied_beds=occupied_beds,
                              available_beds=available_beds,
                              patients=patients,
                              recent_admissions=recent_admissions,
                              today=today)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        # Get today's date for error case
        today = date.today()
        return render_template('nurse/dashboard.html',
                              today_appointments=[],
                              recent_encounters=[],
                              total_beds=0,
                              occupied_beds=0,
                              available_beds=0,
                              patients=[],
                              recent_admissions=[],
                              today=today)