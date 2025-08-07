from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from app.doctor import bp
from app.utils import roles_required
from app.appointments.models import Appointment
from app.clinical_notes.models import ClinicalNote
from app.lab.models import LabOrder
from app.patients.models import Patient
from app.auth.models import User
from datetime import date, datetime, timedelta


@bp.route('/doctor')
@roles_required('Doctor')
def dashboard():
    # Get today's date
    today = date.today()
    
    # Get today's appointments for the current doctor
    today_appointments = Appointment.query.filter(
        Appointment.doctor_id == current_user.id,
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
    
    # Get recent patient encounters (last 5 clinical notes written by this doctor)
    recent_encounters = ClinicalNote.query.filter_by(written_by=current_user.id)\
        .order_by(ClinicalNote.date.desc()).limit(5).all()
    
    # Preload related data for clinical notes
    for encounter in recent_encounters:
        encounter.patient = Patient.query.get(encounter.patient_id)
        encounter.author = User.query.get(encounter.written_by)
    
    # Get pending lab results to review (lab orders ordered by this doctor that are completed but not yet reviewed)
    # For simplicity, we'll show all completed lab orders ordered by this doctor
    pending_lab_results = LabOrder.query.filter_by(ordered_by=current_user.id, status='Completed')\
        .order_by(LabOrder.order_date.desc()).limit(5).all()
    
    # Preload related data for lab orders
    for lab_order in pending_lab_results:
        lab_order.patient = Patient.query.get(lab_order.patient_id)
        lab_order.orderer = User.query.get(lab_order.ordered_by)
    
    return render_template('doctor/dashboard.html',
                          today_appointments=today_appointments,
                          recent_encounters=recent_encounters,
                          pending_lab_results=pending_lab_results,
                          today=today)