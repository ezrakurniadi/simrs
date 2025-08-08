# Patient Registration Template Changes

## 1. Update ID Type Field
- Change from text input to dropdown menu

## 2. Update Blood Type Field
- Change from text input to dropdown menu with predefined options

## 3. Add Dynamic Fields
- Add fields for Problematic Patient reason, Loyalty Member number, Chronic Condition details, and Allergy Alert details
- Use JavaScript to dynamically show/hide these fields based on user selection

## 4. Add JavaScript for Dynamic Field Display
- Add event listeners to toggle visibility of additional fields based on user selection

## Implementation Details

### Current Template (app/templates/patients/new.html)
```html
<div class="row">
    <div class="col-md-6">
        <div class="mb-3">
            {{ form.id_type.label(class="form-label") }}
            {{ form.id_type(class="form-control") }}
            {% if form.id_type.errors %}
                <div class="text-danger">
                    {% for error in form.id_type.errors %}
                        <small>{{ error }}</small>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    </div>
    <div class="col-md-6">
        <div class="mb-3">
            {{ form.id_card_number.label(class="form-label") }}
            {{ form.id_card_number(class="form-control") }}
            {% if form.id_card_number.errors %}
                <div class="text-danger">
                    {% for error in form.id_card_number.errors %}
                        <small>{{ error }}</small>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6">
        <div class="mb-3">
            {{ form.blood_type.label(class="form-label") }}
            {{ form.blood_type(class="form-control") }}
            {% if form.blood_type.errors %}
                <div class="text-danger">
                    {% for error in form.blood_type.errors %}
                        <small>{{ error }}</small>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    </div>
    <div class="col-md-6">
        <div class="mb-3">
            {{ form.birthplace.label(class="form-label") }}
            {{ form.birthplace(class="form-control") }}
            {% if form.birthplace.errors %}
                <div class="text-danger">
                    {% for error in form.birthplace.errors %}
                        <small>{{ error }}</small>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    </div>
</div>
```

### Updated Template
```html
<div class="row">
    <div class="col-md-6">
        <div class="mb-3">
            {{ form.id_type.label(class="form-label") }}
            {{ form.id_type(class="form-select") }}
            {% if form.id_type.errors %}
                <div class="text-danger">
                    {% for error in form.id_type.errors %}
                        <small>{{ error }}</small>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    </div>
    <div class="col-md-6">
        <div class="mb-3">
            {{ form.id_card_number.label(class="form-label") }}
            {{ form.id_card_number(class="form-control") }}
            {% if form.id_card_number.errors %}
                <div class="text-danger">
                    {% for error in form.id_card_number.errors %}
                        <small>{{ error }}</small>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6">
        <div class="mb-3">
            {{ form.blood_type.label(class="form-label") }}
            {{ form.blood_type(class="form-select") }}
            {% if form.blood_type.errors %}
                <div class="text-danger">
                    {% for error in form.blood_type.errors %}
                        <small>{{ error }}</small>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    </div>
    <div class="col-md-6">
        <div class="mb-3">
            {{ form.birthplace.label(class="form-label") }}
            {{ form.birthplace(class="form-control") }}
            {% if form.birthplace.errors %}
                <div class="text-danger">
                    {% for error in form.birthplace.errors %}
                        <small>{{ error }}</small>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6">
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
    </div>
    <div class="col-md-6">
        <div class="mb-3">
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
    </div>
</div>

<div class="row">
    <div class="col-md-6">
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
    </div>
    <div class="col-md-6">
        <div class="mb-3">
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
    </div>
</div>

<div class="row">
    <div class="col-md-6">
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
    </div>
    <div class="col-md-6">
        <div class="mb-3">
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
    </div>
</div>

<div class="row">
    <div class="col-md-6">
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
    </div>
    <div class="col-md-6">
        <div class="mb-3">
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

<script>
document.addEventListener('DOMContentLoaded', function() {
    const problematicPatientField = document.querySelector('select[name="problematic_patient"]');
    const problematicPatientReasonField = document.querySelector('textarea[name="problematic_patient_reason"]');
    const loyaltyMemberField = document.querySelector('select[name="loyalty_member"]');
    const loyaltyMemberNumberField = document.querySelector('input[name="loyalty_member_number"]');
    const chronicConditionField = document.querySelector('select[name="chronic_condition"]');
    const chronicConditionDetailsField = document.querySelector('textarea[name="chronic_condition_details"]');
    const allergyAlertField = document.querySelector('select[name="allergy_alert"]');
    const allergyAlertDetailsField = document.querySelector('textarea[name="allergy_alert_details"]');

    function toggleFieldVisibility(field, targetField) {
        if (field.value === 'True') {
            targetField.style.display = 'block';
        } else {
            targetField.style.display = 'none';
        }
    }

    toggleFieldVisibility(problematicPatientField, problematicPatientReasonField);
    toggleFieldVisibility(loyaltyMemberField, loyaltyMemberNumberField);
    toggleFieldVisibility(chronicConditionField, chronicConditionDetailsField);
    toggleFieldVisibility(allergyAlertField, allergyAlertDetailsField);

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