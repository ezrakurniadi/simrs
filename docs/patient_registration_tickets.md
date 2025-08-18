# Patient Registration Enhancement Tickets

## Priority 1: Regulatory/Compliance Requirements (High Priority)

### Ticket 1: Add Medical Record Number (MRN) Field
- **Description**: Add a system-generated Medical Record Number field to comply with regulatory requirements
- **Implementation**:
  - Add MRN field to Patient model
  - Add MRN field to PatientForm and PatientRegistrationForm
  - Add MRN field to patient registration and edit templates
  - Implement auto-generation of unique MRN on patient creation
- **Business Impact**: High - Required for patient identification and regulatory compliance
- **Compliance**: HIPAA, Joint Commission standards

### Ticket 2: Add Race and Ethnicity Fields
- **Description**: Add Race and Ethnicity fields for public health reporting requirements
- **Implementation**:
  - Add race and ethnicity fields to Patient model
  - Add race and ethnicity fields to PatientForm and PatientRegistrationForm
  - Add race and ethnicity fields to patient registration and edit templates
  - Implement proper validation and data storage
- **Business Impact**: High - Required for public health reporting
- **Compliance**: Public Health reporting requirements

### Ticket 3: Enhance Insurance Information Collection
- **Description**: Implement complete insurance information collection including policy numbers and guarantor information
- **Implementation**:
  - Add insurance policy/ID number field to Patient model
  - Add insurance group number field to Patient model
  - Add guarantor information fields to Patient model
  - Add corresponding fields to forms and templates
- **Business Impact**: High - Critical for billing and insurance verification
- **Compliance**: Insurance and billing compliance

### Ticket 4: Implement Consent and Privacy Practice Tracking
- **Description**: Add tracking for patient consent to treatment and privacy practices acknowledgment
- **Implementation**:
  - Add consent_to_treat field to Patient model
  - Add privacy_practices_acknowledged field to Patient model
  - Add corresponding fields to forms and templates
  - Implement proper validation and data storage
- **Business Impact**: High - Required for HIPAA compliance
- **Compliance**: HIPAA requirements

## Priority 2: Clinical Safety Enhancements (Medium Priority)

### Ticket 5: Enhance Allergy Tracking
- **Description**: Implement specific allergy types rather than generic alert flag
- **Implementation**:
  - Create separate Allergy model with specific types
  - Add relationship between Patient and Allergy models
  - Create AllergyForm for detailed allergy recording
  - Update templates to display detailed allergy information
- **Business Impact**: Medium - Important for patient safety
- **Compliance**: Clinical safety standards

### Ticket 6: Add Infectious Disease and Isolation Precautions
- **Description**: Add flags for infectious disease and isolation precautions
- **Implementation**:
  - Add isolation_precaution_type field to Patient model
  - Add infectious_disease_status field to Patient model
  - Add corresponding fields to forms and templates
- **Business Impact**: Medium - Important for infection control
- **Compliance**: Infection control protocols

### Ticket 7: Add Physiological State and Implant Tracking
- **Description**: Add tracking for physiological states and implanted devices
- **Implementation**:
  - Add physiological_state field to Patient model
  - Add implanted_devices field to Patient model
  - Add corresponding fields to forms and templates
- **Business Impact**: Medium - Important for clinical decision-making
- **Compliance**: Clinical safety standards

## Priority 3: Operational Enhancements (Low Priority)

### Ticket 8: Enhance Patient Name Fields
- **Description**: Add middle name/initial and suffix fields for better patient identification
- **Implementation**:
  - Add middle_name field to Patient model
  - Add suffix field to Patient model
  - Add corresponding fields to forms and templates
- **Business Impact**: Low - Minor enhancement to patient identification

### Ticket 9: Enhance Contact Information Fields
- **Description**: Add detailed contact information including multiple phone numbers and separate mailing address
- **Implementation**:
  - Add home_phone, work_phone, mobile_phone fields to Patient model
  - Add mailing_address field to Patient model
  - Add corresponding fields to forms and templates
- **Business Impact**: Low - Operational enhancement

### Ticket 10: Add Care Coordination Information
- **Description**: Add fields for Primary Care Physician and Referring Physician information
- **Implementation**:
  - Add primary_care_physician field to Patient model
  - Add referring_physician field to Patient model
  - Add corresponding fields to forms and templates
- **Business Impact**: Low - Care coordination enhancement

### Ticket 11: Enhance Communication Preferences
- **Description**: Add detailed communication preferences tracking
- **Implementation**:
  - Add communication_preferences field to Patient model
  - Add preferred_contact_method field to Patient model
  - Add corresponding fields to forms and templates
- **Business Impact**: Low - Operational enhancement

### Ticket 12: Enhance Social/Operational Flags
- **Description**: Add additional social and operational patient flags
- **Implementation**:
  - Add employment_status field to Patient model
  - Add homeless_status field to Patient model
  - Add frequent_no_show flag to Patient model
  - Add corresponding fields to forms and templates
- **Business Impact**: Low - Operational enhancement