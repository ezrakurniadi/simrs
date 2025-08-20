# EHR System Architecture

## System Overview
The EHR system is built using Flask, a Python web framework, with a modular architecture based on Blueprints. The system follows a Model-View-Controller (MVC) pattern with additional service layers for complex business logic.

## Core Components

### Flask Blueprints
- **auth**: Authentication and user management
- **patients**: Patient registration, management, and clinical documentation
- **appointments**: Appointment scheduling and management
- **clinical_notes**: Clinical note creation and management
- **lab**: Laboratory order and result management
- **hospital**: Hospital structure management (wards, rooms, doctors)
- **admin**: System administration and configuration
- **api**: RESTful API endpoints for frontend and external integrations
- **system_params**: System parameter management

### Data Models
- **Patient**: Core patient information with extended demographic and insurance data
- **User**: Authentication and role-based access control
- **Appointment**: Appointment scheduling with doctor and room assignments
- **ClinicalNote**: Clinical documentation with templates
- **Vitals**: Patient vital signs recording
- **Allergy**: Patient allergy tracking with severity levels
- **Medication**: Patient medication prescriptions
- **SystemParameter**: Configuration parameters for the system
- **PayorType/PayorDetail**: Insurance and payment information
- **IDType**: Identification type management
- **Race/Ethnicity/Language**: Demographic data management

### Key Technical Decisions
1. **UUID-based Primary Keys**: All primary keys use UUIDs for better scalability and security
2. **Role-Based Access Control**: Decorator-based access control for routes
3. **Dynamic Form Fields**: JavaScript-enhanced forms with conditional field visibility
4. **Auto-generated MRN**: Automatic generation of Medical Record Numbers
5. **Database Relationships**: Proper foreign key relationships with backref for easy querying
6. **API-first Approach**: RESTful API endpoints for all major functionality

### Component Relationships
- Patients are the central entity with relationships to appointments, clinical notes, vitals, allergies, and medications
- Users have roles that determine their access to different parts of the system
- Hospital entities (wards, rooms, doctors) are managed separately but connect to patient admissions
- System parameters provide configuration data for dropdowns and other UI elements

### Critical Implementation Paths
1. **Patient Registration**: Complex form with dynamic fields and auto-generated MRN
2. **Appointment Scheduling**: Calendar-based interface with conflict detection
3. **Clinical Documentation**: Rich text editing with template support
4. **Inpatient Management**: Admission, discharge, and transfer workflows
5. **Role Management**: Administrative interface for user roles and permissions
6. **System Configuration**: Management of hospital structure and system parameters

## Source Code Paths
- `app/` - Main application package
  - `auth/` - Authentication and user management
  - `patients/` - Patient registration and clinical documentation
  - `appointments/` - Appointment scheduling
  - `clinical_notes/` - Clinical note management
  - `lab/` - Laboratory order and result management
  - `hospital/` - Hospital structure management
  - `admin/` - System administration
  - `api/` - RESTful API endpoints
  - `system_params/` - System parameter management
  - `static/` - Static assets (CSS, JavaScript)
  - `templates/` - HTML templates
- `docs/` - Project documentation
- `migrations/` - Database migration scripts