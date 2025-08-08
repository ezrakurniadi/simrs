# Patient Registration Route Changes

## 1. Update Route to Handle New Fields
- Update the patient registration route to handle the new fields for Problematic Patient, Loyalty Member, Chronic Condition, and Allergy Alert
- Add validation for the new fields

## Implementation Details

### Current Route (app/patients/routes.py)
```python
from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.patients.forms import PatientForm
from app.patients.models import Patient
from app.system_params.models import SystemParameter
from flask_login import login_required

@patients_blueprint.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            id_type=form.id_type.data,
            id_card_number=form.id_card_number.data,
            name=form.name.data,
            birthdate=form.birthdate.data,
            birthplace=form.birthplace.data,
            blood_type=form.blood_type.data,
            address=form.address.data,
            phone=form.phone.data,
            email=form.email.data
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient registered successfully', 'success')
        return redirect(url_for('patients.view', patient_id=patient.id))
    return render_template('patients/new.html', form=form)
```

### Updated Route
```python
from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.patients.forms import PatientForm
from app.patients.models import Patient
from app.system_params.models import SystemParameter
from flask_login import login_required

@patients_blueprint.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            id_type=form.id_type.data,
            id_card_number=form.id_card_number.data,
            name=form.name.data,
            birthdate=form.birthdate.data,
            birthplace=form.birthplace.data,
            blood_type=form.blood_type.data,
            address=form.address.data,
            phone=form.phone.data,
            email=form.email.data,
            problematic_patient=form.problematic_patient.data,
            problematic_patient_reason=form.problematic_patient_reason.data if form.problematic_patient.data else None,
            loyalty_member=form.loyalty_member.data,
            loyalty_member_number=form.loyalty_member_number.data if form.loyalty_member.data else None,
            chronic_condition=form.chronic_condition.data,
            chronic_condition_details=form.chronic_condition_details.data if form.chronic_condition.data else None,
            allergy_alert=form.allergy_alert.data,
            allergy_alert_details=form.allergy_alert_details.data if form.allergy_alert.data else None
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient registered successfully', 'success')
        return redirect(url_for('patients.view', patient_id=patient.id))
    return render_template('patients/new.html', form=form)