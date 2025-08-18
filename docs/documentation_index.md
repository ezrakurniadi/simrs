# Documentation Index

This document provides a comprehensive overview of all documentation files in the project, their purposes, and their relationships to one another. The documentation is organized to support clear navigation and understanding of the project structure.

## 1. Project Planning

### [docs/plan.md](plan.md)
- **Purpose**: Central document containing the sprint-based development plan for the EHR system. Outlines project goals, user stories, and tasks for each sprint from project setup to advanced features.
- **Relationships**: 
  - Primary planning document that drives all development activities
  - References specific implementation details that are documented in other files
  - Provides the overall roadmap that other documentation supports

## 2. Project Status

### [docs/project_status.md](project_status.md)
- **Purpose**: Consolidated status document that tracks the implementation progress of the patient registration form enhancements. Combines information from previous todo_list.md, implementation_status.md, and patient_registration_summary.md files.
- **Relationships**:
  - Derived from and replaces multiple previous status tracking files
  - Provides implementation details that support the high-level planning in plan.md
  - References technical implementation details documented in docs/technical_implementation.md

## 3. Technical Implementation

### [docs/technical_implementation.md](technical_implementation.md)
- **Purpose**: Comprehensive technical documentation of the patient registration form enhancements. Consolidates information from previous patient_form_changes.md, patient_model_changes.md, patient_template_changes.md, patient_route_changes.md, and template_implementation_plan.md files.
- **Relationships**:
  - Contains detailed implementation specifics for form, model, template, and route changes
  - Supports the status tracking in docs/project_status.md
  - Provides technical details that implement the requirements outlined in plan.md

### [docs/test_plan.md](test_plan.md)
- **Purpose**: Detailed test plan for the patient registration form, including test cases for form creation, validation, submission, rendering, database integration, and edge cases. Enhanced from the previous patient_test_plan.md file.
- **Relationships**:
  - Validates the implementation documented in docs/technical_implementation.md
  - Ensures the implemented features meet the requirements in plan.md
  - Provides confidence in the quality of the implementation tracked in docs/project_status.md

## 4. Domain-Specific Documentation

### [docs/hospital_management.md](hospital_management.md)
- **Purpose**: Documentation for hospital management features including clinic, room, doctor, schedule, ward, room class, and bed management.
- **Relationships**:
  - Part of the broader EHR system documented in plan.md
  - Independent of patient registration enhancements but part of the same system
  - May interact with patient data through appointment scheduling and inpatient management

### [docs/patient_registration.md](patient_registration.md)
- **Purpose**: Guidelines and requirements for patient registration, serving as the reference for implementing the patient registration form.
- **Relationships**:
  - Primary reference for implementing the patient registration form
  - Directly informs the implementation documented in docs/technical_implementation.md
  - Requirements are validated by the test cases in docs/test_plan.md