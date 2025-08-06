# Hospital Management System Documentation

## Overview

This document provides an overview of the enhanced hospital management system, which includes new features for ward and room class management, as well as an intelligent patient placement service.

## New Features

### 1. Ward Management Enhancements

#### Preferred Room Class
Each ward can now have a preferred room class assigned to it. This allows administrators to specify which type of room is most suitable for a particular ward.

- **Field**: `preferred_room_class_id` in the Ward model
- **Usage**: When assigning patients to beds, the system will prioritize wards with a preferred room class that matches the patient's needs.

### 2. Room Class Enhancements

#### Care Level
Room classes can now have a care level assigned to them, such as "Intensive Care", "Intermediate Care", or "Basic Care".

- **Field**: `care_level` in the RoomClass model
- **Usage**: Used to match patients with appropriate care requirements to the right room class.

#### Specialty
Room classes can now have a specialty assigned to them, such as "Cardiology", "Orthopedics", or "General Medicine".

- **Field**: `specialty` in the RoomClass model
- **Usage**: Used to match patients with specific medical needs to specialized rooms.

### 3. Ward-Room Class Assignment

A new model has been introduced to manage the relationship between wards and room classes with additional configuration options.

#### WardRoomClassAssignment Model
- **Fields**:
  - `ward_id`: The ward associated with this assignment
  - `room_class_id`: The room class associated with this assignment
  - `priority`: Priority level for this assignment (higher numbers indicate higher priority)
  - `min_capacity`: Minimum capacity requirement for this assignment
  - `max_capacity`: Maximum capacity for this assignment
  - `is_active`: Whether this assignment is currently active

### 4. Patient Placement Service

An intelligent service has been implemented to optimize patient placement based on their needs and ward preferences.

#### PatientPlacementService Class
The service provides the following methods:

- `get_optimal_ward(patient, required_care_level, required_specialty)`: Returns the optimal ward for a patient based on their needs
- `get_optimal_bed(patient, ward, required_care_level, required_specialty)`: Returns the optimal bed for a patient in a specific ward
- `place_patient(patient, required_care_level, required_specialty)`: Places a patient in the optimal ward and bed

The service considers the following factors when determining optimal placement:
- Ward preferred room class
- Ward-room class assignments and their priorities
- Available bed capacity
- Matching care level and specialty requirements

## Database Schema Changes

### Ward Table
- Added `preferred_room_class_id` column (foreign key to room_class table)

### RoomClass Table
- Added `care_level` column (string)
- Added `specialty` column (string)

### WardRoomClassAssignment Table
- New table with the following columns:
  - `id` (primary key)
  - `ward_id` (foreign key to ward table)
  - `room_class_id` (foreign key to room_class table)
  - `priority` (integer)
  - `min_capacity` (integer)
  - `max_capacity` (integer)
  - `is_active` (boolean)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)
  - `created_by` (string)
  - `updated_by` (string)
  - `additional_data` (JSONB)

## User Interface Changes

### Ward Management
- New field for selecting preferred room class in ward creation and editing forms
- Display of preferred room class in ward list view

### Room Class Management
- New fields for care level and specialty in room class creation and editing forms
- Display of care level and specialty in room class list view

### Ward-Room Class Assignment Management
- New section in the admin interface for managing ward-room class assignments
- CRUD operations for ward-room class assignments

## API Routes

### Ward Management
- `GET /admin/wards`: List all wards
- `GET /admin/wards/new`: Create new ward form
- `POST /admin/wards/new`: Create new ward
- `GET /admin/wards/<id>/edit`: Edit ward form
- `POST /admin/wards/<id>/edit`: Update ward
- `POST /admin/wards/<id>/delete`: Delete ward

### Room Class Management
- `GET /admin/room_classes`: List all room classes
- `GET /admin/room_classes/new`: Create new room class form
- `POST /admin/room_classes/new`: Create new room class
- `GET /admin/room_classes/<id>/edit`: Edit room class form
- `POST /admin/room_classes/<id>/edit`: Update room class
- `POST /admin/room_classes/<id>/delete`: Delete room class

### Ward-Room Class Assignment Management
- `GET /admin/ward_room_class_assignments`: List all ward-room class assignments
- `GET /admin/ward_room_class_assignments/new`: Create new ward-room class assignment form
- `POST /admin/ward_room_class_assignments/new`: Create new ward-room class assignment
- `GET /admin/ward_room_class_assignments/<id>/edit`: Edit ward-room class assignment form
- `POST /admin/ward_room_class_assignments/<id>/edit`: Update ward-room class assignment
- `POST /admin/ward_room_class_assignments/<id>/delete`: Delete ward-room class assignment

## Future Improvements

1. Add more sophisticated matching algorithms to the PatientPlacementService
2. Implement capacity management for wards and room classes
3. Add reporting features for ward and room class utilization
4. Implement automated patient placement suggestions in the UI