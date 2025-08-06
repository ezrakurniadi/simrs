from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.appointments import bp
from app.appointments.forms import AppointmentForm
from app.appointments.models import Appointment, db
from app.patients.models import Patient
from app.auth.models import User

@bp.route('/appointments', methods=['GET'])
def list_appointments():
    appointments = Appointment.query.all()
    
    # Preload related data to avoid N+1 query problem
    for appointment in appointments:
        appointment.patient = Patient.query.get(appointment.patient_id)
        appointment.doctor = User.query.get(appointment.doctor_id)
        if appointment.room_id:
            from app.hospital.models import Room
            appointment.room = Room.query.get(appointment.room_id)
        else:
            appointment.room = None
    return render_template('appointments/list.html', appointments=appointments, current_user=current_user)

@bp.route('/appointments/<id>', methods=['GET'])
def view_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    # Get patient and doctor details
    patient = Patient.query.get(appointment.patient_id)
    doctor = User.query.get(appointment.doctor_id)
    
    # Get room details if room is assigned
    room = None
    if appointment.room_id:
        from app.hospital.models import Room
        room = Room.query.get(appointment.room_id)
    return render_template('appointments/view.html', appointment=appointment, patient=patient, doctor=doctor, room=room)

@bp.route('/appointments/new', methods=['GET', 'POST'])
def create_appointment():
    form = AppointmentForm()
    
    # Populate patient choices
    patients = Patient.query.all()
    form.patient_id.choices = [(patient.id, f"{patient.first_name} {patient.last_name}") for patient in patients]
    
    # Populate doctor choices (assuming doctors are users with a specific role)
    doctors = User.query.all()  # In a real application, you might filter by role
    form.doctor_id.choices = [(doctor.id, f"Dr. {doctor.first_name} {doctor.last_name}") for doctor in doctors]
    
    # Populate room choices
    from app.hospital.models import Room
    rooms = Room.query.all()
    form.room_id.choices = [('', 'Select a room')] + [(room.id, room.name) for room in rooms]
    
    if form.validate_on_submit():
        try:
            # Create new appointment
            appointment = Appointment(
                patient_id=form.patient_id.data,
                doctor_id=form.doctor_id.data,
                room_id=form.room_id.data if form.room_id.data else None,
                scheduled_time=form.scheduled_time.data,
                duration=form.duration.data,
                status=form.status.data,
                notes=form.notes.data,
                created_by=str(current_user.id)  # Store the ID of the user creating the appointment
            )
            
            # Add appointment to database
            db.session.add(appointment)
            db.session.commit()
            
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('appointments.list_appointments'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while booking the appointment. Please try again.', 'error')
            # Log the error for debugging (in a real application, you would use a proper logger)
            print(f"Error booking appointment: {str(e)}")
    elif form.is_submitted():
        # Form was submitted but failed validation
        flash('Please correct the errors below.', 'error')
    
    return render_template('appointments/new.html', form=form)

@bp.route('/appointments/<id>/edit', methods=['GET', 'POST'])
def edit_appointment(id):
    # Check if user is authenticated
    if not current_user.is_authenticated:
        flash('You must be logged in to edit an appointment.', 'error')
        return redirect(url_for('auth.login'))
    
    # Allow access to Receptionist, Doctor, and Admin roles
    if not (current_user.has_role('Receptionist') or current_user.has_role('Doctor') or current_user.has_role('Admin')):
        flash('You do not have permission to edit appointments.', 'error')
        return redirect(url_for('appointments.list_appointments'))
    
    appointment = Appointment.query.get_or_404(id)
    form = AppointmentForm(obj=appointment)
    
    # Populate patient choices
    patients = Patient.query.all()
    form.patient_id.choices = [(patient.id, f"{patient.first_name} {patient.last_name}") for patient in patients]
    
    # Populate doctor choices (assuming doctors are users with a specific role)
    doctors = User.query.all()  # In a real application, you might filter by role
    form.doctor_id.choices = [(doctor.id, f"Dr. {doctor.first_name} {doctor.last_name}") for doctor in doctors]
    
    # Populate room choices
    from app.hospital.models import Room
    rooms = Room.query.all()
    form.room_id.choices = [('', 'Select a room')] + [(room.id, room.name) for room in rooms]
    
    if form.validate_on_submit():
        try:
            # Update appointment
            appointment.patient_id = form.patient_id.data
            appointment.doctor_id = form.doctor_id.data
            appointment.room_id = form.room_id.data if form.room_id.data else None
            appointment.scheduled_time = form.scheduled_time.data
            appointment.duration = form.duration.data
            appointment.status = form.status.data
            appointment.notes = form.notes.data
            appointment.updated_by = str(current_user.id)  # Store the ID of the user updating the appointment
            
            # Commit changes to database
            db.session.commit()
            
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('appointments.view_appointment', id=appointment.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the appointment. Please try again.', 'error')
            # Log the error for debugging (in a real application, you would use a proper logger)
            print(f"Error updating appointment: {str(e)}")
    elif form.is_submitted():
        # Form was submitted but failed validation
        flash('Please correct the errors below.', 'error')
    
    # Pre-populate form with existing data
    form.patient_id.data = appointment.patient_id
    form.doctor_id.data = appointment.doctor_id
    form.room_id.data = appointment.room_id
    form.scheduled_time.data = appointment.scheduled_time
    form.duration.data = appointment.duration
    form.status.data = appointment.status
    form.notes.data = appointment.notes
    
    return render_template('appointments/edit.html', form=form, appointment=appointment)


@bp.route('/appointments/calendar', methods=['GET'])
def calendar():
    # Check if user is authenticated and has appropriate role
    if not current_user.is_authenticated:
        flash('You must be logged in to view the calendar.', 'error')
        return redirect(url_for('auth.login'))
    
    # Allow access to Receptionist, Doctor, Nurse, and Admin roles
    if not (current_user.has_role('Receptionist') or current_user.has_role('Doctor') or current_user.has_role('Nurse') or current_user.has_role('Admin')):
        flash('You do not have permission to view the calendar.', 'error')
        return redirect(url_for('appointments.list_appointments'))
    
    return render_template('appointments/calendar.html')


@bp.route('/api/appointments/calendar', methods=['GET'])
def calendar_data():
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return {'error': 'Authentication required'}, 401
    
    # Allow access to Receptionist, Doctor, Nurse, and Admin roles
    if not (current_user.has_role('Receptionist') or current_user.has_role('Doctor') or current_user.has_role('Nurse') or current_user.has_role('Admin')):
        return {'error': 'Permission denied'}, 403
    
    # Get all appointments
    appointments = Appointment.query.all()
    
    # Format appointments for FullCalendar
    events = []
    for appointment in appointments:
        # Get patient and doctor details
        patient = Patient.query.get(appointment.patient_id)
        doctor = User.query.get(appointment.doctor_id)
        
        # Get room details if room is assigned
        room_name = None
        if appointment.room_id:
            from app.hospital.models import Room
            room = Room.query.get(appointment.room_id)
            if room:
                room_name = room.name
        
        # Create event object for FullCalendar
        event = {
            'id': appointment.id,
            'title': f"{patient.first_name} {patient.last_name} - {doctor.first_name} {doctor.last_name}",
            'start': appointment.scheduled_time.isoformat(),
            'end': (appointment.scheduled_time.replace(minute=appointment.scheduled_time.minute + appointment.duration)).isoformat(),
            'appointment_id': appointment.id,
            'extendedProps': {
                'patient_name': f"{patient.first_name} {patient.last_name}",
                'doctor_name': f"Dr. {doctor.first_name} {doctor.last_name}",
                'room_name': room_name,
                'status': appointment.status,
                'appointment_id': appointment.id
            }
        }
        events.append(event)
    
    return {'events': events}


@bp.route('/appointments/today', methods=['GET'])
def today_appointments():
    # Check if user is authenticated
    if not current_user.is_authenticated:
        flash('You must be logged in to view today\'s appointments.', 'error')
        return redirect(url_for('auth.login'))
    
    # Check if user has doctor or receptionist role
    if not (current_user.has_role('Doctor') or current_user.has_role('Receptionist')):
        flash('You do not have permission to view today\'s appointments.', 'error')
        return redirect(url_for('appointments.list_appointments'))
    
    # Get today's date
    from datetime import datetime, date
    today = date.today()
    
    # Get appointments for today
    # For doctors, show only their appointments
    # For receptionists, show all appointments
    if current_user.has_role('Doctor'):
        appointments = Appointment.query.filter(
            Appointment.doctor_id == current_user.id,
            db.func.date(Appointment.scheduled_time) == today
        ).all()
    else:  # Receptionist
        appointments = Appointment.query.filter(
            db.func.date(Appointment.scheduled_time) == today
        ).all()
    
    
    return render_template('appointments/today.html', appointments=appointments, today=today)


@bp.route('/appointments/<id>/delete', methods=['POST'])
def delete_appointment(id):
    # Check if user is authenticated
    if not current_user.is_authenticated:
        flash('You must be logged in to delete an appointment.', 'error')
        return redirect(url_for('auth.login'))
    
    # Allow access to Receptionist, Doctor, and Admin roles
    if not (current_user.has_role('Receptionist') or current_user.has_role('Doctor') or current_user.has_role('Admin')):
        flash('You do not have permission to delete appointments.', 'error')
        return redirect(url_for('appointments.list_appointments'))
    
    appointment = Appointment.query.get_or_404(id)
    
    try:
        # Delete appointment from database
        db.session.delete(appointment)
        db.session.commit()
        
        flash('Appointment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the appointment. Please try again.', 'error')
        # Log the error for debugging (in a real application, you would use a proper logger)
        print(f"Error deleting appointment: {str(e)}")
    
    return redirect(url_for('appointments.list_appointments'))