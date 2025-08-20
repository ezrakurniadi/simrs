# Patient Routes Implementation

## Overview
This document describes the implementation of the patient management routes in the EHR system, including patient registration, viewing, editing, and deletion functionality.

## Route Implementation Details

### Patient Registration Route
- **Route**: `/patients/new`
- **Methods**: GET, POST
- **Access Control**: Restricted to Receptionist role
- **Functionality**:
  - Handles both displaying the registration form (GET) and processing form submission (POST)
  - Generates a unique Medical Record Number (MRN) for each new patient
  - Validates form data using WTForms validation
  - Creates a new Patient record in the database
  - Redirects to patient list on successful registration
  - Displays error messages on validation failures

### Patient View Route
- **Route**: `/patients/<id>`
- **Methods**: GET
- **Access Control**: Restricted to Doctor, Nurse, and Receptionist roles
- **Functionality**:
  - Retrieves patient information by ID
  - Displays patient details in a view-only format
  - Shows patient's admission status
  - Handles 404 errors for non-existent patients

### Patient Edit Route
- **Route**: `/patients/<id>/edit`
- **Methods**: GET, POST
- **Access Control**: Restricted to Receptionist role
- **Functionality**:
  - Handles both displaying the edit form (GET) and processing form submission (POST)
  - Populates form with existing patient data
  - Validates form data using WTForms validation
  - Updates patient record in the database
  - Prevents modification of auto-generated fields like MRN
  - Redirects to patient view on successful update
  - Displays error messages on validation failures

### Patient Delete Route
- **Route**: `/patients/<id>/delete`
- **Methods**: GET, POST
- **Access Control**: Restricted to Receptionist role
- **Functionality**:
  - Handles both displaying the delete confirmation (GET) and processing deletion (POST)
  - Retrieves patient information for confirmation display
  - Deletes patient record from the database
  - Redirects to patient list on successful deletion
  - Displays error messages on failure

### Patient List Route
- **Route**: `/patients/list`
- **Methods**: GET
- **Access Control**: Restricted to Receptionist, Doctor, and Nurse roles
- **Functionality**:
  - Retrieves all patients from the database
  - Displays patients in a tabular format
  - Provides links to view individual patient details

### Patient Search Route
- **Route**: `/patients/search`
- **Methods**: GET, POST
- **Access Control**: Restricted to Receptionist and Doctor roles
- **Functionality**:
  - Handles both displaying the search form (GET) and processing search queries (POST)
  - Filters patients based on search criteria (first name, last name, date of birth, gender, phone)
  - Displays search results in a tabular format

### Patient Dashboard Route
- **Route**: `/patients/dashboard`
- **Methods**: GET
- **Access Control**: Restricted to PatientUser role
- **Functionality**:
  - Displays patient-specific dashboard
  - Shows upcoming appointments
  - Shows appointment history
  - Preloads doctor information for appointments

### Patient Lab Results Route
- **Route**: `/patients/lab_results`
- **Methods**: GET
- **Access Control**: Restricted to PatientUser role
- **Functionality**:
  - Displays released lab results for the patient
  - Retrieves lab results from the database
  - Shows lab results in a tabular format

## Clinical Documentation Routes

### View Vitals Route
- **Route**: `/patients/<patient_id>/vitals`
- **Methods**: GET
- **Access Control**: Restricted to Doctor and Nurse roles
- **Functionality**:
  - Displays vital signs history for a patient
  - Retrieves vital signs ordered by date (most recent first)

### Add Vitals Route
- **Route**: `/patients/<patient_id>/vitals/new`
- **Methods**: GET, POST
- **Access Control**: Restricted to Doctor and Nurse roles
- **Functionality**:
  - Handles both displaying the vitals form (GET) and processing form submission (POST)
  - Creates new vital signs record in the database
  - Redirects to vitals view on successful recording

### View Encounters Route
- **Route**: `/patients/<patient_id>/encounters`
- **Methods**: GET
- **Access Control**: Restricted to Doctor and Nurse roles
- **Functionality**:
  - Displays chronological list of patient encounters
  - Combines clinical notes, vital signs, and lab results
  - Sorts encounters by date (most recent first)

### View Allergies Route
- **Route**: `/patients/<patient_id>/allergies`
- **Methods**: GET
- **Access Control**: Restricted to Doctor and Nurse roles
- **Functionality**:
  - Displays allergy history for a patient
  - Retrieves allergies ordered by recorded date (most recent first)

### Add Allergy Route
- **Route**: `/patients/<patient_id>/allergies/new`
- **Methods**: GET, POST
- **Access Control**: Restricted to Doctor and Nurse roles
- **Functionality**:
  - Handles both displaying the allergy form (GET) and processing form submission (POST)
  - Creates new allergy record in the database
  - Redirects to allergies view on successful recording

### Edit Allergy Route
- **Route**: `/patients/<patient_id>/allergies/<allergy_id>/edit`
- **Methods**: GET, POST
- **Access Control**: Restricted to Doctor and Nurse roles
- **Functionality**:
  - Handles both displaying the allergy edit form (GET) and processing form submission (POST)
  - Updates existing allergy record in the database
  - Redirects to allergies view on successful update

### View Medications Route
- **Route**: `/patients/<patient_id>/medications`
- **Methods**: GET
- **Access Control**: Restricted to Doctor and Nurse roles
- **Functionality**:
  - Displays medication history for a patient
  - Retrieves medications ordered by start date (most recent first)

### Prescribe Medication Route
- **Route**: `/patients/<patient_id>/medications/new`
- **Methods**: GET, POST
- **Access Control**: Restricted to Doctor role
- **Functionality**:
  - Handles both displaying the medication form (GET) and processing form submission (POST)
  - Creates new medication record in the database
  - Redirects to medications view on successful prescription

### Edit Medication Route
- **Route**: `/patients/<patient_id>/medications/<medication_id>/edit`
- **Methods**: GET, POST
- **Access Control**: Restricted to Doctor role
- **Functionality**:
  - Handles both displaying the medication edit form (GET) and processing form submission (POST)
  - Updates existing medication record in the database
  - Redirects to medications view on successful update

## Form Handling
- All form routes use WTForms for validation
- CSRF protection is implemented
- Proper error handling and user feedback
- Role-based access control enforced on all routes

## Database Integration
- SQLAlchemy ORM used for database operations
- Proper transaction handling with commit/rollback
- Foreign key relationships maintained
- UUID primary keys for scalability and security

## Error Handling
- Proper HTTP status codes for different scenarios
- User-friendly error messages
- Logging of errors for debugging
- Graceful handling of database errors