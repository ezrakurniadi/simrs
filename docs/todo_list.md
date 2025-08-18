# Todo List for Patient Registration Enhancements

## 1. Update the PatientForm class in app/patients/forms.py
- Parameterize the ID Type field
- Change the Blood Type field to a dropdown with predefined options

## 2. Update the patient registration template in app/templates/patients/new.html
- Dynamically display additional fields based on certain conditions:
  - Problematic Patient reason
  - Loyalty Member number
  - Chronic Condition details
  - Allergy Alert details

## 3. Update the Patient model in app/patients/models.py
- Add fields for:
  - Problematic Patient reason
  - Loyalty Member number
  - Chronic Condition details
  - Allergy Alert details

## 4. Update the patient registration route in app/patients/routes.py
- Handle the new fields and validation