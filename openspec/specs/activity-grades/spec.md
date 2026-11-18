# activity-grades Specification

## Purpose

Define the data structure and API endpoint for allowing teachers to submit grades for students on specific academic activities in EduTrack AI.

## Requirements

### Requirement: Activity Grades Table Schema
The system SHALL define the `activity_grades` table with fields `id` (integer, primary key auto-increment), `created_at` (timestamp, default now), `user_id` (integer, foreign key referencing the authenticated teacher in `user` table), `student_id` (integer, foreign key referencing the student in `user` table), `activity_id` (integer, referencing the specific academic activity), `grade` (decimal, numeric grade value), and `feedback` (optional text for teacher remarks).

#### Scenario: Activity grades table schema definition
- **WHEN** the `activity_grades` table schema is loaded in Xano
- **THEN** the table contains fields `id`, `created_at`, `user_id`, `student_id`, `activity_id`, `grade`, and `feedback` with appropriate types and relational references

### Requirement: Post Activity Grade Endpoint
The system SHALL provide an API endpoint `POST /activity_grades` that allows an authenticated teacher to submit a grade for a student in a specific activity.

#### Scenario: Teacher successfully submits a grade
- **WHEN** an authenticated user sends a valid POST request to `/activity_grades` with `student_id`, `activity_id`, and `grade`
- **THEN** the system persists the grade record associated with the authenticated `user_id` and returns the created record

#### Scenario: Validation fails on invalid input
- **WHEN** an authenticated user sends a POST request with missing required fields (`student_id`, `activity_id`, or `grade`)
- **THEN** the system rejects the request with an appropriate validation error

### Requirement: Student Grades Visualization Page
The system SHALL provide a dedicated grades view in `pages/4_📊_Notas.py` presenting subject cards with current grade averages, color-coded approval status badges, and indicators of remaining points needed to achieve approval.

#### Scenario: User views subject grades card
- **WHEN** a user opens `pages/4_📊_Notas.py`
- **THEN** the system SHALL display distinct cards for each subject with individual evaluation scores for assignments and exams, calculated average, and approval status badge

#### Scenario: Visual indicator for passing grade
- **WHEN** a subject's calculated average is greater than or equal to 7.0
- **THEN** the system SHALL render a green approval badge and indicate that the approval threshold has been met

#### Scenario: Visual indicator for below passing grade
- **WHEN** a subject's calculated average is below 7.0
- **THEN** the system SHALL render an attention or critical badge (yellow or red) and display the exact points remaining to reach the 7.0 approval threshold

