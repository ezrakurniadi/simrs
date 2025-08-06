from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from app.receptionist import bp
from app.utils import roles_required
from app.appointments.models import Appointment
from app.patients.models import Patient
from app.auth.models import User
from datetime import date, datetime, timedelta


@bp.route('/dashboard')
@roles_required('Receptionist')
def dashboard():
    try:
        # Get today's date
        today = date.today()
        
        # Get today's appointments
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
        
        # Get upcoming appointments (next 7 days)
        upcoming_appointments = Appointment.query.filter(
            Appointment.scheduled_time >= today + timedelta(days=1),
            Appointment.scheduled_time < today + timedelta(days=8)
        ).order_by(Appointment.scheduled_time).all()
        
        # Preload related data for upcoming appointments
        for appointment in upcoming_appointments:
            appointment.patient = Patient.query.get(appointment.patient_id)
            appointment.doctor = User.query.get(appointment.doctor_id)
            if appointment.room_id:
                from app.hospital.models import Room
                appointment.room = Room.query.get(appointment.room_id)
            else:
                appointment.room = None
        
        # Get recent patient registrations (last 5 patients)
        recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(5).all()
        
        return render_template('receptionist/dashboard.html',
                              today_appointments=today_appointments,
                              upcoming_appointments=upcoming_appointments,
                              recent_patients=recent_patients,
                              today=today)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        # Get today's date for error case
        today = date.today()
        return render_template('receptionist/dashboard.html',
                              today_appointments=[],
                              upcoming_appointments=[],
                              recent_patients=[],
                              today=today)