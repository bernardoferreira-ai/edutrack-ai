# progress-calculation Specification

## Purpose

Define the requirements for calculating the progress percentage of an academic subject based on its associated tasks retrieved from EduTrack AI's CRUD endpoints, returning the results in JSON format.

## ADDED Requirements

### Requirement: Progress Percentage Calculation
The system SHALL calculate the completion progress percentage for a subject as `(completed_tasks / total_tasks) * 100.0`, rounded to two decimal places. If a subject has no tasks (`total_tasks == 0`), the system SHALL set `progress_percentage` to `0.0`.

#### Scenario: Subject with mixed completed and pending tasks
- **WHEN** a subject has 10 total tasks, with 7 completed and 3 pending
- **THEN** system computes `progress_percentage` as `70.0`

#### Scenario: Subject with no tasks
- **WHEN** a subject has 0 registered tasks
- **THEN** system computes `progress_percentage` as `0.0` without division-by-zero errors

#### Scenario: Subject with all tasks completed
- **WHEN** a subject has 5 total tasks and all 5 are marked as completed
- **THEN** system computes `progress_percentage` as `100.0`

### Requirement: CRUD Endpoint Integration
The system SHALL retrieve the academic tasks of a subject by querying the `GET /academic_tasks` CRUD endpoint filtering by `subject_id` and providing a valid Bearer authentication token.

#### Scenario: Querying tasks via CRUD API
- **WHEN** the progress calculation function is invoked with a valid `subject_id` and authentication token
- **THEN** system performs an HTTP GET request to `/academic_tasks?subject_id={subject_id}` and processes the returned list of tasks

#### Scenario: API request failure or connection error
- **WHEN** the CRUD API is unreachable or returns an HTTP error
- **THEN** system raises an appropriate exception or outputs a JSON error description

### Requirement: JSON Response Structure
The system SHALL return the calculation results as a JSON object containing `subject_id`, `total_tasks`, `completed_tasks`, `pending_tasks`, and `progress_percentage`.

#### Scenario: Structured JSON output
- **WHEN** the progress calculation finishes successfully
- **THEN** system outputs a valid JSON object matching the schema:
  ```json
  {
    "subject_id": 1,
    "total_tasks": 10,
    "completed_tasks": 7,
    "pending_tasks": 3,
    "progress_percentage": 70.0
  }
  ```

