# Patient Registration Template Implementation

## Overview
This document describes the implementation of the patient registration template in the EHR system, including the structure, dynamic field behavior, and UI/UX enhancements.

## Template Structure
The patient registration template is located at `app/templates/patients/new.html` and follows a structured layout with the following sections:

### Personal Information Section
- Contains basic patient information fields:
  - First Name (required)
  - Last Name (required)
  - Date of Birth (required)
  - Gender (required)
  - ID Type (required)
  - ID Card Number (required)
  - Birthplace
  - Blood Type
  - Marriage Status
  - Medical Record Number (MRN) (auto-generated, read-only)
  - Race
  - Ethnicity

### Contact Information Section
- Contains patient contact details:
  - Address (required)
  - Phone (required)
  - Email
  - Preferred Communication Method

### Emergency Contact Section
- Contains emergency contact information:
  - Emergency Contact Name (required)
  - Emergency Contact Phone (required)
  - Emergency Contact Relationship (required)

### Payor Information Section
- Contains insurance and payment information:
  - Payor Type
  - Payor Detail (dynamically populated based on Payor Type)
  - Insurance Policy/ID Number
  - Insurance Group Number
  - Guarantor Name
  - Guarantor Relationship to Patient
  - Guarantor Phone
  - Guarantor Address

### Status Section
- Contains various status fields with dynamic behavior:
  - Status (Deceased/Alive)
  - VIP Status (Yes/No)
  - Problematic Patient (Yes/No)
  - Problematic Patient Reason (appears when Problematic Patient is Yes)
  - Loyalty Member (Yes/No)
  - Loyalty Member Number (appears when Loyalty Member is Yes)
  - Chronic Condition (Yes/No)
  - Chronic Condition Details (appears when Chronic Condition is Yes)
  - Allergy Alert (Yes/No)
  - Allergy Alert Details (appears when Allergy Alert is Yes)

### Consent and Privacy Section
- Contains consent and privacy fields:
  - Consent to Treat (required)
  - Privacy Practices Acknowledged (required)

## Dynamic Field Behavior
The template implements dynamic field visibility using JavaScript:

1. **Problematic Patient Reason Field**
   - Appears when Problematic Patient is set to "Yes"
   - Hidden when Problematic Patient is set to "No"

2. **Loyalty Member Number Field**
   - Appears when Loyalty Member is set to "Yes"
   - Hidden when Loyalty Member is set to "No"

3. **Chronic Condition Details Field**
   - Appears when Chronic Condition is set to "Yes"
   - Hidden when Chronic Condition is set to "No"

4. **Allergy Alert Details Field**
   - Appears when Allergy Alert is set to "Yes"
   - Hidden when Allergy Alert is set to "No"

## UI/UX Enhancements

### Accessibility Features
- Proper ARIA attributes for screen readers
- Keyboard navigation support
- Focus management for dynamic fields
- Form validation with accessible error messages

### Responsive Design
- Grid-based layout using CSS Grid
- Responsive card sections that adapt to different screen sizes
- Mobile-friendly form controls

### Enhanced Form Controls
- Select2 integration for enhanced dropdowns with search functionality:
  - Ethnicity dropdown with AJAX search
  - Preferred Language dropdown with AJAX search
- Dynamic payor dropdowns:
  - Payor Type dropdown populated from API
  - Payor Detail dropdown dynamically populated based on selected Payor Type

### Form Validation
- Client-side validation with visual feedback
- Server-side validation with error display
- Required field indicators
- Invalid field highlighting

## JavaScript Implementation

### Dynamic Field Visibility
The template uses JavaScript to control the visibility of conditional fields:

```javascript
function toggleFieldVisibility(field, targetField) {
    if (field.value === 'True') {
        targetField.style.display = 'block';
        targetField.setAttribute('aria-hidden', 'false');
        // Focus the first input in the revealed field
        const firstInput = targetField.querySelector('input, select, textarea');
        if (firstInput) {
            firstInput.focus();
        }
    } else {
        targetField.style.display = 'none';
        targetField.setAttribute('aria-hidden', 'true');
    }
}
```

### Enhanced Keyboard Navigation
The template includes enhanced keyboard navigation for better accessibility:

```javascript
// Enhanced keyboard navigation for the form
const formGroups = form.querySelectorAll('.mb-3');
formGroups.forEach(group => {
    const inputs = group.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                // Find the next focusable element
                const focusableElements = form.querySelectorAll('input, select, textarea, button, a');
                const currentIndex = Array.from(focusableElements).indexOf(this);
                if (currentIndex < focusableElements.length - 1) {
                    e.preventDefault();
                    focusableElements[currentIndex + 1].focus();
                }
            }
        });
    });
});
```

### Select2 Integration
The template uses Select2 for enhanced dropdown functionality:

```javascript
// Initialize Select2 for ethnicity dropdown with AJAX search
$('#ethnicity').select2({
    placeholder: 'Select Ethnicity',
    allowClear: true,
    width: '100%',
    dropdownAutoWidth: true,
    ajax: {
        url: '/api/ethnicities',
        dataType: 'json',
        delay: 250,
        data: function (params) {
            return {
                search: params.term
            };
        },
        processResults: function (data) {
            return {
                results: data
            };
        },
        cache: true
    },
    minimumInputLength: 1
});
```

## CSS Styling
The template uses custom CSS defined in `app/static/css/patient-registration.css` for:

- Grid layout styling
- Card section styling
- Form control styling
- Responsive design adjustments
- Dynamic field styling