## Purpose

Provides academic subject and course management capabilities, allowing students to register, view, update, and organize their enrolled subjects and track active courses.

## ADDED Requirements

### Requirement: Create Subject
The system SHALL allow users to create a new subject by providing a mandatory subject name, along with optional metadata including subject code, professor/instructor name, semester, and color tag.

#### Scenario: Successful subject creation
- **WHEN** a user submits a valid subject name and associated metadata
- **THEN** the system stores the new subject record with an active status and returns the created subject

#### Scenario: Creation failure when name is missing
- **WHEN** a user attempts to create a subject without providing a subject name
- **THEN** the system rejects the operation and returns a descriptive validation error

### Requirement: List Subjects
The system SHALL allow users to retrieve the list of registered subjects, with support for filtering by active or completed status.

#### Scenario: Retrieve subjects list
- **WHEN** a user navigates to the subjects section or requests the subject list
- **THEN** the system returns all subjects associated with the user

#### Scenario: Filter subjects by active status
- **WHEN** a user filters the subjects list by status "active"
- **THEN** the system returns only subjects marked with an active status

### Requirement: View Subject Details
The system SHALL allow users to view detailed information for a specific subject by its unique identifier.

#### Scenario: View existing subject
- **WHEN** a user requests the details of an existing subject ID
- **THEN** the system returns the complete subject details including name, code, professor, semester, and status

#### Scenario: Subject not found
- **WHEN** a user requests details for a non-existent subject ID
- **THEN** the system returns a not found error

### Requirement: Update Subject
The system SHALL allow users to modify details of an existing subject, including name, professor, semester, color, and status (e.g. active, completed, archived).

#### Scenario: Successful subject update
- **WHEN** a user submits updated information for an existing subject
- **THEN** the system persists the changes and returns the updated subject record

### Requirement: Delete Subject
The system SHALL allow users to delete an existing subject record.

#### Scenario: Successful subject deletion
- **WHEN** a user confirms deletion of a subject
- **THEN** the system deletes the record and removes it from the subjects list

### Requirement: Active Subjects Dashboard Metric
The system SHALL calculate the total count of active subjects and display it on the main dashboard metrics.

#### Scenario: Display active subjects count on dashboard
- **WHEN** the dashboard view is rendered
- **THEN** the "Disciplinas Ativas" metric displays the current count of subjects with active status

