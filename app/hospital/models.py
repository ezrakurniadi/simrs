import uuid
from sqlalchemy.dialects.postgresql import JSONB
from app.auth.models import User, db
from app.patients.models import Patient

# Outpatient Models

class Hospital(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases

class Clinic(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hospital_id = db.Column(db.String(36), db.ForeignKey('hospital.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases
    
    # Relationships
    hospital = db.relationship('Hospital', backref=db.backref('clinics', lazy=True))

class Room(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clinic_id = db.Column(db.String(36), db.ForeignKey('clinic.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases
    
    # Relationships
    clinic = db.relationship('Clinic', backref=db.backref('rooms', lazy=True))

class DoctorProfile(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    hospital_id = db.Column(db.String(36), db.ForeignKey('hospital.id'), nullable=False)
    specialization = db.Column(db.String(100))
    license_number = db.Column(db.String(50), unique=True)
    education = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases
    
    # Relationships
    user = db.relationship('User', backref=db.backref('doctor_profile', uselist=False))
    hospital = db.relationship('Hospital', backref=db.backref('doctors', lazy=True))

class DoctorSchedule(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    doctor_id = db.Column(db.String(36), db.ForeignKey('doctor_profile.id'), nullable=False)
    clinic_id = db.Column(db.String(36), db.ForeignKey('clinic.id'), nullable=False)
    day_of_week = db.Column(db.Integer)  # 0=Sunday, 1=Monday, etc.
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    slot_duration = db.Column(db.Integer, default=30)  # Duration in minutes
    max_patients = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases
    
    # Relationships
    doctor = db.relationship('DoctorProfile', backref=db.backref('schedules', lazy=True))
    clinic = db.relationship('Clinic', backref=db.backref('doctor_schedules', lazy=True))

# Inpatient Models

class Ward(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hospital_id = db.Column(db.String(36), db.ForeignKey('hospital.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    floor = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases
    preferred_room_class_id = db.Column(db.String(36), db.ForeignKey('room_class.id'))
    
    # Relationships
    hospital = db.relationship('Hospital', backref=db.backref('wards', lazy=True))
    preferred_room_class = db.relationship('RoomClass', foreign_keys=[preferred_room_class_id])

class RoomClass(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    daily_rate = db.Column(db.Float)
    care_level = db.Column(db.String(50))  # e.g., "ICU", "General", "Maternity"
    specialty = db.Column(db.String(100))  # e.g., "Cardiology", "Orthopedics"
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases

class WardRoom(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ward_id = db.Column(db.String(36), db.ForeignKey('ward.id'), nullable=False)
    room_class_id = db.Column(db.String(36), db.ForeignKey('room_class.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases
    
    # Relationships
    ward = db.relationship('Ward', backref=db.backref('rooms', lazy=True))
    room_class = db.relationship('RoomClass', backref=db.backref('ward_rooms', lazy=True))

class WardRoomClassAssignment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ward_id = db.Column(db.String(36), db.ForeignKey('ward.id'), nullable=False)
    room_class_id = db.Column(db.String(36), db.ForeignKey('room_class.id'), nullable=False)
    priority = db.Column(db.Integer, default=1)  # 1 = Primary, 2 = Secondary, etc.
    min_capacity = db.Column(db.Integer, default=0)
    max_capacity = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases
    
    # Relationships
    ward = db.relationship('Ward', backref=db.backref('room_class_assignments', lazy=True))
    room_class = db.relationship('RoomClass', backref=db.backref('ward_assignments', lazy=True))


class Bed(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ward_room_id = db.Column(db.String(36), db.ForeignKey('ward_room.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_occupied = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases
    
    # Relationships
    ward_room = db.relationship('WardRoom', backref=db.backref('beds', lazy=True))


class Admission(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    bed_id = db.Column(db.String(36), db.ForeignKey('bed.id'), nullable=False)
    admitted_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    admission_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    discharge_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Admitted')  # Admitted, Discharged, Transferred
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases
    
    # Relationships
    patient = db.relationship('Patient', backref=db.backref('admissions', lazy=True))
    bed = db.relationship('Bed', backref=db.backref('admissions', lazy=True))
    admitting_user = db.relationship('User', backref=db.backref('admitted_patients', lazy=True))