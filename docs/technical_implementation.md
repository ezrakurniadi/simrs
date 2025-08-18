# Patient Registration Form Technical Implementation

## 1. Form Class Updates
### Changes Made
- Updated `PatientForm` class in `app/patients/forms.py` to include all required fields
- Added dynamic fields:
  - `problematic_patient_reason` (TextAreaField)
  - `loyalty_member_number` (StringField)
  - `chronic_condition_details` (TextAreaField)
  - `allergy_alert_details` (TextAreaField)
- Changed `id_type` from `StringField` to `SelectField`
- Changed `blood_type` from `StringField` to `SelectField` with predefined options: A+, A-, B+, B-, AB+, AB-, O+, O-
- Ensured proper initialization of select fields with data from the database

### Implementation Details
```python
class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    address = TextAreaField('Address')
    phone = StringField('Phone')
    email = StringField('Email', validators=[Email()])
    id_type = SelectField(
        'ID Type',
        coerce=int,
        validators=[DataRequired()]
    )
    id_card_number = StringField(
        'ID Card Number',
        validators=[DataRequired()]
    )
    blood_type = SelectField(
        'Blood Type',
        choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                 ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        validators=[DataRequired()]
    )
    birthplace = StringField('Birthplace')
    marriage_status = SelectField('Marriage Status', choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')])
    nationality_id = SelectField('Nationality', coerce=str, choices=[])
    vip_status = SelectField('VIP Status', choices=[(True, 'Yes'), (False, 'No')], default=False)
    problematic_patient = SelectField('Problematic Patient', choices=[(True, 'Yes'), (False, 'No')], default=False)
    problematic_patient_reason = TextAreaField('Problematic Patient Reason', validators=[Optional()])
    loyalty_member = SelectField('Loyalty Member', choices=[(True, 'Yes'), (False, 'No')], default=False)
    loyalty_member_number = StringField('Loyalty Member Number', validators=[Optional()])
    ihs_number = StringField('IHS Number')
    chronic_condition = SelectField('Chronic Condition', choices=[(True, 'Yes'), (False, 'No')], default=False)
    chronic_condition_details = TextAreaField('Chronic Condition Details', validators=[Optional()])
    allergy_alert = SelectField('Allergy Alert', choices=[(True, 'Yes'), (False, 'No')], default=False)
    allergy_alert_details = TextAreaField('Allergy Alert Details', validators=[Optional()])
    preferred_communication = StringField('Preferred Communication Method')
    preferred_language = StringField('Preferred Language')
    emergency_contact_name = StringField('Emergency Contact Name')
    emergency_contact_phone = StringField('Emergency Contact Phone')
    emergency_contact_relationship = StringField('Emergency Contact Relationship')
    submit = SubmitField('Save Patient')

    def __init__(self, *args, db=None, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        # Fetch nationalities from the API
        try:
            response = requests.get(f"{current_app.config['API_BASE_URL']}/api/nationalities")
            if response.status_code == 200:
                nationalities = response.json()
                self.nationality_id.choices = [(str(n['id']), n['name']) for n in nationalities]
            else:
                self.nationality_id.choices = []
        except Exception as e:
            self.nationality_id.choices = []
            print(f"Error fetching nationalities: {e}")

        # Set ID types
        if db:
            self.id_type.choices = get_id_types(db)
```

## 2. Model Updates
### Changes Made
- Updated `Patient` model in `app/patients/models.py` to include new fields:
  - `problematic_patient_reason` (Text)
  - `loyalty_member_number` (String(50))
  - `chronic_condition_details` (Text)
  - `allergy_alert_details` (Text)

### Implementation Details
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
```

## 3. Template Updates
### Changes Made
- Updated `app/templates/patients/new.html` to include all fields from the form
- Implemented dynamic field display using JavaScript:
  - Problematic Patient reason field appears when Problematic Patient is set to "Yes"
  - Loyalty Member number field appears when Loyalty Member is set to "Yes"
  - Chronic Condition details field appears when Chronic Condition is set to "Yes"
  - Allergy Alert details field appears when Allergy Alert is set to "Yes"
- Improved UI/UX with better organization of fields into logical sections

### Implementation Details
The updated template includes all fields in a well-organized structure with dynamic field behavior controlled by JavaScript. The template uses Bootstrap classes for responsive design and proper form styling.

```html
{% extends "base.html" %}

{% block title %}Register New Patient{% endblock %}

{% block content %}
<h1>Register New Patient</h1>

<form method="POST" action="{{ url_for('patients.create_patient') }}">
    {{ form.hidden_tag() }}

    <div class="row">
        <!-- Personal Information Section -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="card-title">Personal Information</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        {{ form.first_name.label(class="form-label") }}
                        {{ form.first_name(class="form-control") }}
                        {% if form.first_name.errors %}
                            <div class="text-danger">
                                {% for error in form.first_name.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <!-- Additional fields omitted for brevity -->
                </div>
            </div>
        </div>

        <!-- Contact Information Section -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="card-title">Contact Information</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        {{ form.address.label(class="form-label") }}
                        {{ form.address(class="form-control", rows="3") }}
                        {% if form.address.errors %}
                            <div class="text-danger">
                                {% for error in form.address.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <!-- Additional fields omitted for brevity -->
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <!-- Emergency Contact Section -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="card-title">Emergency Contact</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        {{ form.emergency_contact_name.label(class="form-label") }}
                        {{ form.emergency_contact_name(class="form-control") }}
                        {% if form.emergency_contact_name.errors %}
                            <div class="text-danger">
                                {% for error in form.emergency_contact_name.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <!-- Additional fields omitted for brevity -->
                </div>
            </div>
        </div>

        <!-- Insurance Information Section -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="card-title">Insurance Information</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        {{ form.insurance_provider.label(class="form-label") }}
                        {{ form.insurance_provider(class="form-control") }}
                        {% if form.insurance_provider.errors %}
                            <div class="text-danger">
                                {% for error in form.insurance_provider.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <!-- Status Section -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="card-title">Status</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        {{ form.is_deceased.label(class="form-label") }}
                        {{ form.is_deceased(class="form-select") }}
                        {% if form.is_deceased.errors %}
                            <div class="text-danger">
                                {% for error in form.is_deceased.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        {{ form.vip_status.label(class="form-label") }}
                        {{ form.vip_status(class="form-select") }}
                        {% if form.vip_status.errors %}
                            <div class="text-danger">
                                {% for error in form.vip_status.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        {{ form.problematic_patient.label(class="form-label") }}
                        {{ form.problematic_patient(class="form-select") }}
                        {% if form.problematic_patient.errors %}
                            <div class="text-danger">
                                {% for error in form.problematic_patient.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <div class="mb-3" id="problematic_patient_reason_field" style="display: none;">
                        {{ form.problematic_patient_reason.label(class="form-label") }}
                        {{ form.problematic_patient_reason(class="form-control") }}
                        {% if form.problematic_patient_reason.errors %}
                            <div class="text-danger">
                                {% for error in form.problematic_patient_reason.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        {{ form.loyalty_member.label(class="form-label") }}
                        {{ form.loyalty_member(class="form-select") }}
                        {% if form.loyalty_member.errors %}
                            <div class="text-danger">
                                {% for error in form.loyalty_member.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <div class="mb-3" id="loyalty_member_number_field" style="display: none;">
                        {{ form.loyalty_member_number.label(class="form-label") }}
                        {{ form.loyalty_member_number(class="form-control") }}
                        {% if form.loyalty_member_number.errors %}
                            <div class="text-danger">
                                {% for error in form.loyalty_member_number.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        {{ form.chronic_condition.label(class="form-label") }}
                        {{ form.chronic_condition(class="form-select") }}
                        {% if form.chronic_condition.errors %}
                            <div class="text-danger">
                                {% for error in form.chronic_condition.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <div class="mb-3" id="chronic_condition_details_field" style="display: none;">
                        {{ form.chronic_condition_details.label(class="form-label") }}
                        {{ form.chronic_condition_details(class="form-control") }}
                        {% if form.chronic_condition_details.errors %}
                            <div class="text-danger">
                                {% for error in form.chronic_condition_details.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        {{ form.allergy_alert.label(class="form-label") }}
                        {{ form.allergy_alert(class="form-select") }}
                        {% if form.allergy_alert.errors %}
                            <div class="text-danger">
                                {% for error in form.allergy_alert.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <div class="mb-3" id="allergy_alert_details_field" style="display: none;">
                        {{ form.allergy_alert_details.label(class="form-label") }}
                        {{ form.allergy_alert_details(class="form-control") }}
                        {% if form.allergy_alert_details.errors %}
                            <div class="text-danger">
                                {% for error in form.allergy_alert_details.errors %}
                                    <small>{{ error }}</small>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="mb-3">
        {{ form.submit(class="btn btn-primary") }}
        <a href="{{ url_for('patients.index') }}" class="btn btn-secondary">Cancel</a>
    </div>
</form>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const problematicPatientField = document.querySelector('select[name="problematic_patient"]');
    const problematicPatientReasonField = document.getElementById('problematic_patient_reason_field');
    const loyaltyMemberField = document.querySelector('select[name="loyalty_member"]');
    const loyaltyMemberNumberField = document.getElementById('loyalty_member_number_field');
    const chronicConditionField = document.querySelector('select[name="chronic_condition"]');
    const chronicConditionDetailsField = document.getElementById('chronic_condition_details_field');
    const allergyAlertField = document.querySelector('select[name="allergy_alert"]');
    const allergyAlertDetailsField = document.getElementById('allergy_alert_details_field');

    function toggleFieldVisibility(field, targetField) {
        if (field.value === 'True') {
            targetField.style.display = 'block';
        } else {
            targetField.style.display = 'none';
        }
    }

    // Initial setup
    toggleFieldVisibility(problematicPatientField, problematicPatientReasonField);
    toggleFieldVisibility(loyaltyMemberField, loyaltyMemberNumberField);
    toggleFieldVisibility(chronicConditionField, chronicConditionDetailsField);
    toggleFieldVisibility(allergyAlertField, allergyAlertDetailsField);

    // Event listeners
    problematicPatientField.addEventListener('change', function() {
        toggleFieldVisibility(problematicPatientField, problematicPatientReasonField);
    });

    loyaltyMemberField.addEventListener('change', function() {
        toggleFieldVisibility(loyaltyMemberField, loyaltyMemberNumberField);
    });

    chronicConditionField.addEventListener('change', function() {
        toggleFieldVisibility(chronicConditionField, chronicConditionDetailsField);
    });

    allergyAlertField.addEventListener('change', function() {
        toggleFieldVisibility(allergyAlertField, allergyAlertDetailsField);
    });
});
</script>
{% endblock %}
```

## 4. Route Updates
### Changes Made
- Updated patient registration route in `app/patients/routes.py` to handle new fields
- Updated patient edit route in `app/patients/routes.py` to handle new fields
- Added proper conditional logic to store dynamic field data only when their corresponding boolean fields are True

### Implementation Details
```python
@bp.route('/patients/new', methods=['GET', 'POST'])
@roles_required('Receptionist')
def create_patient():
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        try:
            # Create new patient
            patient = Patient(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                date_of_birth=form.date_of_birth.data,
                gender=form.gender.data,
                address=form.address.data,
                phone=form.phone.data,
                email=form.email.data,
                id_type=form.id_type.data,
                id_card_number=form.id_card_number.data,
                blood_type=form.blood_type.data,
                birthplace=form.birthplace.data,
                marriage_status=form.marriage_status.data,
                nationality_id=form.nationality.data,
                vip_status=form.vip_status.data,
                problematic_patient=form.problematic_patient.data,
                problematic_patient_reason=form.problematic_patient_reason.data if form.problematic_patient.data == 'True' else None,
                loyalty_member=form.loyalty_member.data,
                loyalty_member_number=form.loyalty_member_number.data if form.loyalty_member.data == 'True' else None,
                ihs_number=form.ihs_number.data,
                chronic_condition=form.chronic_condition.data,
                chronic_condition_details=form.chronic_condition_details.data if form.chronic_condition.data == 'True' else None,
                allergy_alert=form.allergy_alert.data,
                allergy_alert_details=form.allergy_alert_details.data if form.allergy_alert.data == 'True' else None,
                preferred_communication=form.preferred_communication.data,
                preferred_language=form.preferred_language.data,
                emergency_contact_name=form.emergency_contact_name.data,
                emergency_contact_phone=form.emergency_contact_phone.data,
                emergency_contact_relationship=form.emergency_contact_relationship.data,
                insurance_provider=form.insurance_provider.data,
                is_deceased=form.is_deceased.data,
                created_by=str(current_user.id)  # Store the ID of the user creating the patient
            )

            # Add patient to database
            db.session.add(patient)
            db.session.commit()

            flash('Patient registered successfully!', 'success')
            return redirect(url_for('patients.index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while registering the patient. Please try again.', 'error')
            # Log the error for debugging (in a real application, you would use a proper logger)
            print(f"Error registering patient: {str(e)}")

    return render_template('patients/new.html', form=form)

@bp.route('/patients/<int:id>/edit', methods=['GET', 'POST'])
@roles_required('Receptionist')
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    form = PatientForm(obj=patient)

    if form.validate_on_submit():
        try:
            # Update patient information
            patient.first_name = form.first_name.data
            patient.last_name = form.last_name.data
            patient.date_of_birth = form.date_of_birth.data
            patient.gender = form.gender.data
            patient.address = form.address.data
            patient.phone = form.phone.data
            patient.email = form.email.data
            patient.id_type = form.id_type.data
            patient.id_card_number = form.id_card_number.data
            patient.blood_type = form.blood_type.data
            patient.birthplace = form.birthplace.data
            patient.marriage_status = form.marriage_status.data
            patient.nationality_id = form.nationality.data
            patient.vip_status = form.vip_status.data
            patient.problematic_patient = form.problematic_patient.data
            patient.problematic_patient_reason = form.problematic_patient_reason.data if form.problematic_patient.data == 'True' else None
            patient.loyalty_member = form.loyalty_member.data
            patient.loyalty_member_number = form.loyalty_member_number.data if form.loyalty_member.data == 'True' else None
            patient.ihs_number = form.ihs_number.data
            patient.chronic_condition = form.chronic_condition.data
            patient.chronic_condition_details = form.chronic_condition_details.data if form.chronic_condition.data == 'True' else None
            patient.allergy_alert = form.allergy_alert.data
            patient.allergy_alert_details = form.allergy_alert_details.data if form.allergy_alert.data == 'True' else None
            patient.preferred_communication = form.preferred_communication.data
            patient.preferred_language = form.preferred_language.data
            patient.emergency_contact_name = form.emergency_contact_name.data
            patient.emergency_contact_phone = form.emergency_contact_phone.data
            patient.emergency_contact_relationship = form.emergency_contact_relationship.data

            db.session.commit()

            flash('Patient information updated successfully!', 'success')
            return redirect(url_for('patients.view_patient', id=patient.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the patient. Please try again.', 'error')
            print(f"Error updating patient: {str(e)}")

    return render_template('patients/edit.html', form=form, patient=patient)
```

## 5. Implementation Details

### Dynamic Fields Implementation
The dynamic fields implementation uses JavaScript to show/hide additional fields based on user selections:
- When a user selects "Yes" for Problematic Patient, the Problematic Patient Reason field appears
- When a user selects "Yes" for Loyalty Member, the Loyalty Member Number field appears
- When a user selects "Yes" for Chronic Condition, the Chronic Condition Details field appears
- When a user selects "Yes" for Allergy Alert, the Allergy Alert Details field appears

This approach improves the user experience by only showing relevant fields when needed, reducing clutter on the form.

### Data Storage
The implementation ensures that data for dynamic fields is only stored when their corresponding boolean fields are set to True:
- If Problematic Patient is "No", the Problematic Patient Reason field data is not stored
- If Loyalty Member is "No", the Loyalty Member Number field data is not stored
- If Chronic Condition is "No", the Chronic Condition Details field data is not stored
- If Allergy Alert is "No", the Allergy Alert Details field data is not stored

This approach ensures data integrity and reduces unnecessary storage of empty fields.