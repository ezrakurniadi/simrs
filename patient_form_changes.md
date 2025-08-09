# Patient Form Changes

## 1. Parameterize ID Type Field
- Change `id_type` from `StringField` to `SelectField`
- Fetch ID types from system parameters in the `__init__` method
- Update the choices dynamically based on API response

## 2. Implement Dropdown Menu for Blood Type
- Change `blood_type` from `StringField` to `SelectField`
- Add predefined options: A+, A-, B+, B-, AB+, AB-, O+, O-

## 3. Implement Dynamic Fields
- Add new fields:
  - `problematic_patient_reason` (TextAreaField)
  - `loyalty_member_number` (StringField)
  - `chronic_condition_details` (TextAreaField)
  - `allergy_alert_details` (TextAreaField)

## 4. Update Form Initialization
- Fetch ID types from API in the `__init__` method
- Set up dynamic fields based on user selection

## Implementation Details

### Current Form (app/patients/forms.py)
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
    loyalty_member = SelectField('Loyalty Member', choices=[(True, 'Yes'), (False, 'No')], default=False)
    ihs_number = StringField('IHS Number')
    chronic_condition = SelectField('Chronic Condition', choices=[(True, 'Yes'), (False, 'No')], default=False)
    allergy_alert = SelectField('Allergy Alert', choices=[(True, 'Yes'), (False, 'No')], default=False)
    preferred_communication = StringField('Preferred Communication Method')
    preferred_language = StringField('Preferred Language')
    emergency_contact_name = StringField('Emergency Contact Name')
    emergency_contact_phone = StringField('Emergency Contact Phone')
    emergency_contact_relationship = StringField('Emergency Contact Relationship')
    submit = SubmitField('Save Patient')
```

### Updated Form
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