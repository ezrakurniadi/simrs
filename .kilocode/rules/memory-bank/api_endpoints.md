# API Endpoints for System Parameters

## Overview
This document describes the RESTful API endpoints available for accessing system parameters and related data in the EHR system.

## System Parameter Endpoints

### ID Types
- **Endpoint**: `/api/id-types`
- **Method**: GET
- **Description**: Retrieve all active ID types
- **Response**: JSON array of ID types with id and name properties

### Payor Types
- **Endpoint**: `/api/payor-types`
- **Method**: GET
- **Description**: Retrieve all active payor types
- **Response**: JSON array of payor types with id and name properties

### Payor Details
- **Endpoint**: `/api/payor-details/<int:payor_type_id>`
- **Method**: GET
- **Description**: Retrieve all active payor details for a specific payor type
- **Response**: JSON array of payor details with id and name properties

### Ethnicities
- **Endpoint**: `/api/ethnicities`
- **Method**: GET
- **Description**: Retrieve all ethnicities with optional search parameter
- **Parameters**: 
  - search (optional): Search term to filter ethnicities
- **Response**: JSON object with results array containing ethnicity objects with id and text properties

### Languages
- **Endpoint**: `/api/languages`
- **Method**: GET
- **Description**: Retrieve all languages with optional search parameter
- **Parameters**: 
  - search (optional): Search term to filter languages
- **Response**: JSON object with results array containing language objects with id and text properties

### Nationalities
- **Endpoint**: `/api/nationalities`
- **Method**: GET
- **Description**: Retrieve all nationalities
- **Response**: JSON array of nationalities with id and name properties

### Races
- **Endpoint**: `/api/races`
- **Method**: GET
- **Description**: Retrieve all races
- **Response**: JSON array of races with id and text properties

## Patient Endpoints (Planned)

### List Patients
- **Endpoint**: `/api/patients`
- **Method**: GET
- **Description**: Retrieve list of patients
- **Status**: TODO - Implementation pending

### Get Patient
- **Endpoint**: `/api/patients/<int:id>`
- **Method**: GET
- **Description**: Retrieve specific patient by ID
- **Status**: TODO - Implementation pending

### Create Patient
- **Endpoint**: `/api/patients`
- **Method**: POST
- **Description**: Create new patient
- **Status**: TODO - Implementation pending

### Update Patient
- **Endpoint**: `/api/patients/<int:id>`
- **Method**: PUT
- **Description**: Update existing patient
- **Status**: TODO - Implementation pending

### Delete Patient
- **Endpoint**: `/api/patients/<int:id>`
- **Method**: DELETE
- **Description**: Delete patient
- **Status**: TODO - Implementation pending

## Appointment Endpoints (Planned)

### List Appointments
- **Endpoint**: `/api/appointments`
- **Method**: GET
- **Description**: Retrieve list of appointments
- **Status**: TODO - Implementation pending

### Get Appointment
- **Endpoint**: `/api/appointments/<int:id>`
- **Method**: GET
- **Description**: Retrieve specific appointment by ID
- **Status**: TODO - Implementation pending

### Create Appointment
- **Endpoint**: `/api/appointments`
- **Method**: POST
- **Description**: Create new appointment
- **Status**: TODO - Implementation pending

### Update Appointment
- **Endpoint**: `/api/appointments/<int:id>`
- **Method**: PUT
- **Description**: Update existing appointment
- **Status**: TODO - Implementation pending

### Delete Appointment
- **Endpoint**: `/api/appointments/<int:id>`
- **Method**: DELETE
- **Description**: Delete appointment
- **Status**: TODO - Implementation pending