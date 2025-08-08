# Patient Model Changes

## 1. Add Fields for Additional Information
- Add fields for Problematic Patient reason, Loyalty Member number, Chronic Condition details, and Allergy Alert details

## Implementation Details

### Current Model (app/patients/models.py)
```python
from datetime import datetime
from app import db
from app.system_params.models import SystemParameter

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_type = db.Column(db.String(50), nullable=False)
    id_card_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    birthplace = db.Column(db.String(100), nullable=False)
    blood_type = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Updated Model
```python
from datetime import datetime
from app import db
from app.system_params.models import SystemParameter

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_type = db.Column(db.String(50), nullable=False)
    id_card_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    birthplace = db.Column(db.String(100), nullable=False)
    blood_type = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    problematic_patient = db.Column(db.Boolean, default=False)
    problematic_patient_reason = db.Column(db.Text, nullable=True)
    loyalty_member = db.Column(db.Boolean, default=False)
    loyalty_member_number = db.Column(db.String(50), nullable=True)
    chronic_condition = db.Column(db.Boolean, default=False)
    chronic_condition_details = db.Column(db.Text, nullable=True)
    allergy_alert = db.Column(db.Boolean, default=False)
    allergy_alert_details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)