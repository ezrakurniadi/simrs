from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, IntegerField, TimeField
from wtforms.validators import DataRequired, Length, Email, Optional, NumberRange


class HospitalForm(FlaskForm):
    name = StringField('Hospital Name', validators=[DataRequired(), Length(max=100)])
    code = StringField('Hospital Code', validators=[DataRequired(), Length(max=20)])
    address = TextAreaField('Address', validators=[Length(max=500)])
    phone = StringField('Phone', validators=[Length(max=20)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    submit = SubmitField('Save Hospital')


class ClinicForm(FlaskForm):
    name = StringField('Clinic Name', validators=[DataRequired(), Length(max=100)])
    code = StringField('Clinic Code', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    is_active = BooleanField('Active')
    submit = SubmitField('Save Clinic')


class WardForm(FlaskForm):
    name = StringField('Ward Name', validators=[DataRequired(), Length(max=100)])
    code = StringField('Ward Code', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    floor = StringField('Floor', validators=[Length(max=20)])
    preferred_room_class_id = SelectField('Preferred Room Class', coerce=str, validators=[Optional()])
    is_active = BooleanField('Active')
    submit = SubmitField('Save Ward')

class RoomClassForm(FlaskForm):
    name = StringField('Room Class Name', validators=[DataRequired(), Length(max=50)])
    code = StringField('Room Class Code', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    daily_rate = StringField('Daily Rate', validators=[Optional()])
    care_level = StringField('Care Level', validators=[Length(max=50)])
    specialty = StringField('Specialty', validators=[Length(max=100)])
    is_active = BooleanField('Active')
    submit = SubmitField('Save Room Class')


class WardRoomClassAssignmentForm(FlaskForm):
    ward_id = SelectField('Ward', coerce=str, validators=[DataRequired()])
    room_class_id = SelectField('Room Class', coerce=str, validators=[DataRequired()])
    priority = IntegerField('Priority', validators=[NumberRange(min=1)], default=1)
    min_capacity = IntegerField('Minimum Capacity', validators=[NumberRange(min=0)], default=0)
    max_capacity = IntegerField('Maximum Capacity', validators=[Optional()])
    is_active = BooleanField('Active')
    submit = SubmitField('Save Assignment')


class DoctorProfileForm(FlaskForm):
    user_id = SelectField('User', coerce=str, validators=[DataRequired()])
    hospital_id = SelectField('Hospital', coerce=str, validators=[DataRequired()])
    specialization = StringField('Specialization', validators=[Length(max=100)])
    license_number = StringField('License Number', validators=[Length(max=50)])
    education = TextAreaField('Education', validators=[Length(max=500)])
    experience_years = IntegerField('Years of Experience', validators=[Optional(), NumberRange(min=0)])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    is_active = BooleanField('Active')
    submit = SubmitField('Save Doctor')


class DoctorScheduleForm(FlaskForm):
    doctor_id = SelectField('Doctor', coerce=str, validators=[DataRequired()])
    clinic_id = SelectField('Clinic', coerce=str, validators=[DataRequired()])
    day_of_week = SelectField('Day of Week', choices=[
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday')
    ], coerce=int, validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    slot_duration = IntegerField('Slot Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)], default=30)
    max_patients = IntegerField('Max Patients', validators=[DataRequired(), NumberRange(min=1)], default=10)
    is_active = BooleanField('Active')
    submit = SubmitField('Save Schedule')


class BedAssignmentForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=str, validators=[DataRequired()])
    bed_id = SelectField('Bed', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Assign Bed')


class TransferForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=str, validators=[DataRequired()])
    current_bed_id = SelectField('Current Bed', coerce=str, validators=[DataRequired()])
    new_bed_id = SelectField('New Bed', coerce=str, validators=[DataRequired()])
    reason = TextAreaField('Reason for Transfer', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Transfer Patient')


class DischargeForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=str, validators=[DataRequired()])
    bed_id = SelectField('Bed', coerce=str, validators=[DataRequired()])
    reason = TextAreaField('Reason for Discharge', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Discharge Patient')