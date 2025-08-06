from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from app.hospital.models import DoctorSchedule, Room
from app.appointments.models import Appointment
from datetime import datetime, timedelta

class AppointmentForm(FlaskForm):
    patient_id = SelectField('Patient', validators=[DataRequired()])
    doctor_id = SelectField('Doctor', validators=[DataRequired()])
    room_id = SelectField('Room')
    scheduled_time = DateTimeField('Scheduled Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    status = SelectField('Status', choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Scheduled')
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Appointment')
    
    def validate(self, extra_validators=None):
        # Run default validation first
        if not super(AppointmentForm, self).validate(extra_validators):
            return False
            
        # Check if doctor is available at the scheduled time
        if self.scheduled_time.data and self.doctor_id.data and self.duration.data:
            if not self._is_doctor_available(self.scheduled_time.data, self.duration.data, self.doctor_id.data, self.scheduled_time.data):
                self.scheduled_time.errors.append('Doctor is not available at the selected time.')
                return False
                
        # Check if room is available at the scheduled time
        if self.scheduled_time.data and self.room_id.data and self.duration.data:
            if not self._is_room_available(self.scheduled_time.data, self.duration.data, self.room_id.data):
                self.scheduled_time.errors.append('Room is not available at the selected time.')
                return False
                
        return True
        
    def _is_doctor_available(self, scheduled_time, duration, doctor_id, appointment_date):
        # Check if doctor has a schedule for the day
        day_of_week = scheduled_time.weekday()  # Monday is 0 and Sunday is 6
        # Adjust to match DoctorSchedule where Sunday is 0
        day_of_week = (day_of_week + 1) % 7
        
        doctor_schedule = DoctorSchedule.query.filter_by(
            doctor_id=doctor_id,
            day_of_week=day_of_week,
            is_active=True
        ).first()
        
        if not doctor_schedule:
            return False
            
        # Check if the scheduled time is within the doctor's working hours
        scheduled_time_only = scheduled_time.time()
        end_time = (datetime.combine(datetime.today(), scheduled_time_only) + timedelta(minutes=duration)).time()
        
        if scheduled_time_only < doctor_schedule.start_time or end_time > doctor_schedule.end_time:
            return False
            
        # Check for existing appointments that would conflict
        end_time_dt = scheduled_time + timedelta(minutes=duration)
        
        conflicting_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.scheduled_time < end_time_dt,
            Appointment.scheduled_time + timedelta(minutes=Appointment.duration) > scheduled_time,
            Appointment.status != 'Cancelled'
        ).count()
        
        # Check if doctor has reached max patients for the time slot
        if conflicting_appointments >= doctor_schedule.max_patients:
            return False
            
        return True
        
    def _is_room_available(self, scheduled_time, duration, room_id):
        # Check if room is active
        room = Room.query.get(room_id)
        if not room or not room.is_active:
            return False
            
        # Check for existing appointments that would conflict
        end_time_dt = scheduled_time + timedelta(minutes=duration)
        
        conflicting_appointments = Appointment.query.filter(
            Appointment.room_id == room_id,
            Appointment.scheduled_time < end_time_dt,
            Appointment.scheduled_time + timedelta(minutes=Appointment.duration) > scheduled_time,
            Appointment.status != 'Cancelled'
        ).count()
        
        # Check if room capacity is reached (for simplicity, we assume 1 appointment per room at a time)
        if conflicting_appointments >= room.capacity:
            return False
            
        return True