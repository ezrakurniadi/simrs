# EHR Development: Sprint Plan

This document outlines a sprint-based development plan for the Electronic Health Record (EHR) system. The plan is structured to deliver incremental value, starting with core functionalities and progressively adding more advanced features. Each sprint is designed to be approximately 2 weeks long.

## Sprint 0: Project Setup & Foundation

**Goal:** Prepare the development environment, set up a modular and versioned project structure using Blueprints, and establish the foundational database schema for users and roles.

### User Stories & Tasks

**As a developer, I want to set up a modular project structure so that I have a clean, organized, and scalable codebase.**
- Initialize a Flask project with a standard directory structure:
  - app/ (main application package)
    - __init__.py
    - models/
    - static/
    - templates/
    - auth/ (Blueprint)
    - patients/ (Blueprint)
    - appointments/ (Blueprint)
    - admin/ (Blueprint)
- Structure the application using Flask Blueprints. Each core feature (e.g., patients, appointments, auth, admin) will reside in its own directory
- Within each Blueprint folder, organize the code into separate files for routes (routes.py), models (models.py), and forms (forms.py)
- Plan for API versioning by prefixing API-related Blueprints (e.g., /api/v1/patients)

**As a developer, I want to configure the development environment so I can start building.**
- Set up a virtual environment and install necessary libraries (Flask, SQLAlchemy, Flask-Login, Flask-SQLAlchemy, Flask-Migrate, etc.)
- Configure PostgreSQL database and establish a connection using Flask-SQLAlchemy
- Set up configuration files for different environments (development, testing, production)

**As a developer, I want to define the initial database models and authentication so that I can store core application data and manage users.**
- Create initial database models for User and Role within an auth Blueprint:
  - User: id, username, email, password_hash, first_name, last_name, created_at
  - Role: id, name, description
- Implement basic user authentication (login, logout, registration) within the auth Blueprint using Flask-Login
- Create a script to seed the database with initial roles (e.g., 'Admin', 'Doctor', 'Receptionist', 'Lab Technician', 'Nurse')
- Create a basic layout template using Jinja2 with a navigation bar that can be extended by other templates
- Implement password hashing with bcrypt

## Sprint 1: Core Patient Administration & RBAC

**Goal:** Implement core patient management features and establish the Role-Based Access Control (RBAC) enforcement mechanism to secure all subsequent features.

### User Stories & Tasks

**As a developer, I want to enforce access control so that only authorized users can perform actions.**
- Create a route decorator (e.g., @roles_required('Doctor')) that checks the current user's role before allowing access to a route
- Implement session management and CSRF protection

**As a Receptionist, I want to register a new patient so that their information is in the system.**
- Create the Patient model within the patients Blueprint:
  - Patient: id, first_name, last_name, date_of_birth, gender, address, phone, email, created_at
- Create a form for patient registration using Flask-WTF
- Implement the backend logic and routes, securing them with the @roles_required('Receptionist') decorator
- Add input validation and sanitization

**As a Receptionist or Doctor, I want to search for a patient so that I can quickly find their record.**
- Create a patient search page and implement the search logic. Secure the route with @roles_required('Receptionist', 'Doctor')
- Implement search by name, ID, or other relevant criteria

**As a Doctor or Nurse, I want to view a patient's profile so that I can see their basic information.**
- Create a patient detail page. Secure the route with @roles_required('Doctor', 'Nurse', 'Receptionist')
- Display patient demographics and summary information

## Sprint 2: Appointment Scheduling

**Goal:** Build the appointment scheduling module, ensuring all new routes are secured by the RBAC system.

### User Stories & Tasks

**As a Receptionist, I want to schedule an appointment for a patient so that they can see a doctor.**
- Create the Appointment model within the appointments Blueprint:
  - Appointment: id, patient_id, doctor_id, room_id, scheduled_time, duration, status, notes
- Create a form to book a new appointment, linking it to a patient and a doctor
- Develop a calendar view (e.g., using a library like FullCalendar.js). Secure all creation/editing routes
- Implement appointment conflict detection

**As a Doctor, I want to see my schedule for the day so that I know which patients I will be seeing.**
- Create a "Today's Appointments" view for logged-in doctors within the appointments Blueprint. Secure the route for doctors
- Implement filtering and sorting options

**As a Receptionist, I want to be able to reschedule or cancel an appointment.**
- Add functionality to edit and delete existing appointments. Secure these actions by role
- Implement appointment status tracking

## Sprint 3: Basic Clinical Documentation

**Goal:** Enable clinicians to document patient encounters, with all actions restricted to appropriate clinical roles.

### User Stories & Tasks

**As a Doctor or Nurse, I want to record vital signs for a patient during a visit.**
- Create a Vitals model and add a section to the patient's chart to enter vital signs. Secure with @roles_required('Doctor', 'Nurse'):
  - VitalSigns: id, patient_id, recorded_by, date, bp_systolic, bp_diastolic, heart_rate, temperature, weight, height
- Implement data validation for vital signs ranges

**As a Doctor, I want to write clinical notes for a patient encounter.**
- Create a ClinicalNote model and a text editor for writing notes. Secure with @roles_required('Doctor'):
  - ClinicalNote: id, patient_id, written_by, date, note_type, content
- Implement note templates for common encounter types

**As a Doctor or Nurse, I want to view a patient's past clinical notes and vital signs.**
- Display a chronological list of past encounters on the patient chart. Secure with @roles_required('Doctor', 'Nurse')
- Implement filtering by date range and note type

## Sprint 4: Medication and Allergy Management

**Goal:** Implement features for managing patient medications and allergies, secured for clinical staff.

### User Stories & Tasks

**As a Doctor or Nurse, I want to record a patient's allergies.**
- Create an Allergy model and a module to add, edit, and view patient allergies. Secure appropriately by role:
  - Allergy: id, patient_id, allergen, reaction, severity, recorded_date
- Implement allergy alert system for patient safety

**As a Doctor, I want to prescribe a medication to a patient.**
- Create a Medication model and a form to prescribe medication. Secure with @roles_required('Doctor'):
  - Medication: id, patient_id, prescribed_by, drug_name, dosage, frequency, start_date, end_date, status
- Implement prescription validation and drug interaction checking

**As a Doctor or Nurse, I want to see a list of a patient's current and past medications.**
- Display the patient's medication history on their chart. Secure appropriately by role
- Implement medication status tracking (active, discontinued, expired)

## Sprint 5: Lab Orders and Results (CPOE - Phase 1)

**Goal:** Introduce functionality for ordering and viewing lab results, with distinct permissions for different roles.

### User Stories & Tasks

**As a Doctor, I want to order a lab test for a patient.**
- Create LabOrder and LabResult models:
  - LabOrder: id, patient_id, ordered_by, test_type, order_date, status
  - LabResult: id, order_id, performed_by, result_data, result_date
- Create an interface to order common lab tests. Secure with @roles_required('Doctor')
- Implement lab order tracking and status updates

**As a Lab Technician, I want to see a list of pending lab orders and enter results.**
- Create a dashboard for lab technicians. Secure with @roles_required('Lab Technician')
- Create a form for lab technicians to input results. Secure with @roles_required('Lab Technician')
- Implement result validation and flagging for abnormal values

**As a Doctor, I want to view the results of a lab test I ordered.**
- Display the lab results in the patient's chart. Secure with @roles_required('Doctor')
- Implement result trending and comparison with previous results

## Sprint 6: Role Management UI

**Goal:** Provide administrators with a user interface to manage user roles and assignments.

### User Stories & Tasks

**As an Administrator, I want a UI to manage user roles and permissions so I can control system access.**
- Implement a UI for creating, editing, and deleting roles
- Create an interface to assign roles to users
- Secure this entire Blueprint with @roles_required('Admin')
- Implement audit logging for role changes

## Sprint 7: System Parameter Management

**Goal:** Allow Administrators to manage the core operational structure and parameters of the hospital for both outpatient and inpatient services.

### User Stories & Tasks

**As an Administrator, I want to manage the hospital's structure, including its clinics, rooms, doctors, schedules, and inpatient wards.**
- Create a new admin Blueprint for these management functions
- Create/update models for:
  - Outpatient: Hospital, Clinic, Room (for outpatient), DoctorProfile, DoctorSchedule
  - Inpatient: Ward, RoomClass (e.g., VIP, Class 1), WardRoom, and Bed
- Build UI forms for the Admin to set the main Hospital name and details
- Build UI forms (CRUD) for Admins to manage Clinics (outpatient) and Wards (inpatient)
- Build UI forms for Admins to manage RoomClasses for wards, including specifying the number of beds per class
- Build UI forms for Admins to manage outpatient Rooms and inpatient WardRooms
- Build a UI for Admins to manage Doctor Profiles and their weekly Schedules
- Update the appointment booking logic to check against the detailed doctor/room availability schedule
- Secure this entire Blueprint with @roles_required('Admin')

## Sprint 8: Patient Portal (MVP)

**Goal:** Launch the first version of the patient portal, which will have its own authentication and authorization logic.

### User Stories & Tasks

**As a Patient, I want to securely log in to the patient portal.**
- Create a separate login and registration process for patients
- Implement patient-specific authentication with different security requirements
- Implement secure password reset functionality

**As a Patient, I want to view my basic health profile and upcoming appointments.**
- Create a dashboard for patients to see their demographic information and appointment schedule
- Implement data filtering to show only patient-relevant information

**As a Patient, I want to view my lab results.**
- Display released lab results in the patient portal
- Implement result release status tracking and patient notification

## Sprint 9: Inpatient Management (ADT) - MVP

**Goal:** Implement the basic workflow for Admission, Discharge, and Transfer (ADT) of inpatients.

### User Stories & Tasks

**As an Admissions Clerk or Nurse, I want to admit a patient to an available bed.**
- Create an Admission model to track inpatient stays:
  - Admission: id, patient_id, bed_id, admitted_by, admission_date, discharge_date, status
- Build a UI to view available beds by ward and class
- Implement logic to assign a patient to a specific bed, changing the bed's status to 'Occupied'
- Implement admission validation and conflict checking

**As a Nurse, I want to view all patients currently admitted to my ward.**
- Create a ward dashboard showing occupied beds and patient details
- Implement real-time bed status updates

**As a Nurse, I want to transfer a patient from one bed to another.**
- Implement a transfer workflow that updates the patient's location and bed status
- Implement transfer validation and conflict checking

**As a Nurse, I want to discharge a patient.**
- Implement a discharge workflow that frees up the bed and concludes the inpatient stay record
- Implement discharge summary generation

## Future Sprints (Advanced Features)

- Clinical Decision Support: Implement alerts for drug interactions, clinical guideline integration
- Reporting & Analytics: Develop standard and custom reporting modules
- Telemedicine: Integrate secure video consultations
- Billing & Insurance: Build out the billing module and insurance claims processing
- API and Mobile Support: Implement JWT-based authentication for the /api/v1 endpoints. Develop API endpoints for core features to support a mobile application and third-party integrations
- Advanced Interoperability: Implement FHIR APIs for data exchange with other systems
- Mobile Application: Develop a native or hybrid mobile app for providers and patients
