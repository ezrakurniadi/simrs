# Hospital Management System Features

## Overview
This document describes the hospital management features implemented in the EHR system, including clinic, room, doctor, schedule, ward, room class, and bed management.

## Outpatient Management

### Clinics
- Clinics represent different departments or specialties in the hospital
- Each clinic has a name and description
- Clinics are managed through the admin interface

### Rooms
- Rooms are physical spaces within clinics where patient visits occur
- Each room has a name and is associated with a specific clinic
- Rooms are managed through the admin interface

### Doctors
- Doctor profiles contain information about medical staff
- Each doctor has a name, specialty, and contact information
- Doctors are managed through the admin interface

### Doctor Schedules
- Doctor schedules define when doctors are available for appointments
- Schedules include day of week, start time, end time, and associated clinic/room
- Schedules are managed through the admin interface
- Appointment booking logic checks against doctor schedules to prevent conflicts

## Inpatient Management

### Wards
- Wards represent different sections of the hospital for inpatient care
- Each ward has a name, description, and specialty
- Wards are managed through the admin interface

### Room Classes
- Room classes define different levels of service for inpatient rooms
- Examples include VIP, Class 1, Class 2, etc.
- Each room class has a name and description
- Room classes are managed through the admin interface

### Ward Rooms
- Ward rooms are physical rooms within wards
- Each ward room is associated with a specific ward and room class
- Ward rooms are managed through the admin interface

### Beds
- Beds are individual patient accommodation units within ward rooms
- Each bed has a name/number and status (Available, Occupied, Reserved, Out of Service)
- Beds are managed through the admin interface
- Admission logic assigns patients to specific beds
- Bed status is updated during admission, discharge, and transfer processes

## Implementation Details

### Data Models
- All hospital entities are implemented as SQLAlchemy models
- Proper foreign key relationships are defined between entities
- UUID primary keys are used for better scalability and security

### Admin Interface
- CRUD operations for all hospital entities
- Web forms for data entry using WTForms
- Role-based access control restricting access to Admin users

### API Endpoints
- RESTful API endpoints for hospital entities
- JSON responses for frontend integration
- Proper error handling and validation

## Integration Points

### Patient Registration
- Nationality dropdown populated from hospital management data

### Appointment Scheduling
- Doctor and room selection based on hospital structure
- Conflict detection using doctor schedules

### Inpatient Management (ADT)
- Admission workflow uses ward, room class, ward room, and bed data
- Transfer workflow updates bed assignments
- Discharge workflow frees up bed resources