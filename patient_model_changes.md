# Patient Model Changes

## 1. Add Fields for Additional Information
- Add fields for Problematic Patient reason, Loyalty Member number, Chronic Condition details, and Allergy Alert details

## Implementation Details

### Current Model (app/patients/models.py)
```python
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
import uuid
from app.system_params.models import Nationality

class Patient(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    id_type = db.Column(db.String(50), nullable=True)
    id_card_number = db.Column(db.String(50), nullable=True)
    blood_type = db.Column(db.String(5), nullable=True)
    birthplace = db.Column(db.String(100), nullable=True)
    marriage_status = db.Column(db.String(20), nullable=True)
    nationality_id = db.Column(db.String(36), db.ForeignKey('nationality.id'), nullable=True)
    vip_status = db.Column(db.Boolean, default=False)
    problematic_patient = db.Column(db.Boolean, default=False)
    loyalty_member = db.Column(db.Boolean, default=False)
    ihs_number = db.Column(db.String(50), nullable=True)
    chronic_condition = db.Column(db.Boolean, default=False)
    allergy_alert = db.Column(db.Boolean, default=False)
    preferred_communication = db.Column(db.String(50), nullable=True)
    preferred_language = db.Column(db.String(50), nullable=True)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_phone = db.Column(db.String(20), nullable=True)
    emergency_contact_relationship = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(50), nullable=True)
    insurance_provider = db.Column(db.String(100), nullable=True)
    is_deceased = db.Column(db.Boolean, default=False)
```

### Updated Model
```python
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
import uuid
from app.system_params.models import Nationality

class Patient(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    id_type = db.Column(db.String(50), nullable=True)
    id_card_number = db.Column(db.String(50), nullable=True)
    blood_type = db.Column(db.String(5), nullable=True)
    birthplace = db.Column(db.String(100), nullable=True)
    marriage_status = db.Column(db.String(20), nullable=True)
    nationality_id = db.Column(db.String(36), db.ForeignKey('nationality.id'), nullable=True)
    vip_status = db.Column(db.Boolean, default=False)
    problematic_patient = db.Column(db.Boolean, default=False)
    problematic_patient_reason = db.Column(db.Text, nullable=True)
    loyalty_member = db.Column(db.Boolean, default=False)
    loyalty_member_number = db.Column(db.String(50), nullable=True)
    ihs_number = db.Column(db.String(50), nullable=True)
    chronic_condition = db.Column(db.Boolean, default=False)
    chronic_condition_details = db.Column(db.Text, nullable=True)
    allergy_alert = db.Column(db.Boolean, default=False)
    allergy_alert_details = db.Column(db.Text, nullable=True)
    preferred_communication = db.Column(db.String(50), nullable=True)
    preferred_language = db.Column(db.String(50), nullable=True)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_phone = db.Column(db.String(20), nullable=True)
    emergency_contact_relationship = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(50), nullable=True)
    insurance_provider = db.Column(db.String(100), nullable=True)
    is_deceased = db.Column(db.Boolean, default=False)