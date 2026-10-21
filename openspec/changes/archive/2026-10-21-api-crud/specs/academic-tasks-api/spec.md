# academic-tasks-api Specification

## Purpose

Define the RESTful CRUD endpoints for academic tasks in EduTrack AI, ensuring strict user-level data isolation where each student can only create, view, update, and delete their own obligations.

## ADDED Requirements

### Requirement: Create Academic Task (POST /academic_tasks)
The system SHALL provide an endpoint `POST /academic_tasks` requiring user authentication that creates a new task record, automatically setting `user_id` to the authenticated user's ID (`$auth.id`).

#### Scenario: User successfully creates a task
- **WHEN** an authenticated user sends a valid POST request to `/academic_tasks` with mandatory `title` and valid `subject_id`
- **THEN** system stores the task associated with `user_id = $auth.id` and returns the created record

#### Scenario: Creation with missing mandatory title
- **WHEN** an authenticated user sends a POST request with missing or empty `title`
- **THEN** system rejects the request with a validation error

### Requirement: List User Academic Tasks (GET /academic_tasks)
The system SHALL provide an endpoint `GET /academic_tasks` requiring user authentication that retrieves only task records owned by the authenticated user (`user_id == $auth.id`), supporting optional filtering by `subject_id` and `status`.

#### Scenario: Listing only owned tasks
- **WHEN** an authenticated user requests `GET /academic_tasks`
- **THEN** system returns only tasks where `user_id == $auth.id`

#### Scenario: Listing with subject filter
- **WHEN** an authenticated user requests `GET /academic_tasks?subject_id=1`
- **THEN** system returns only tasks owned by the user linked to `subject_id = 1`

### Requirement: Get Academic Task by ID (GET /academic_tasks/{id})
The system SHALL provide an endpoint `GET /academic_tasks/{id}` requiring user authentication that retrieves a single task only if it belongs to the authenticated user.

#### Scenario: User retrieves an owned task
- **WHEN** an authenticated user requests `GET /academic_tasks/{id}` for a task they own
- **THEN** system returns the requested task record

#### Scenario: User attempts to access another user's task
- **WHEN** an authenticated user requests `GET /academic_tasks/{id}` for a task owned by another user
- **THEN** system rejects the request with an access denied or not found error

### Requirement: Update Academic Task (PATCH /academic_tasks/{id})
The system SHALL provide an endpoint `PATCH /academic_tasks/{id}` requiring user authentication that updates task fields only if the task belongs to the authenticated user.

#### Scenario: User updates an owned task
- **WHEN** an authenticated user sends a PATCH request to `/academic_tasks/{id}` for their own task
- **THEN** system updates the specified fields and returns the updated record

#### Scenario: Unauthorized update attempt
- **WHEN** an authenticated user sends a PATCH request to `/academic_tasks/{id}` for a task owned by another user
- **THEN** system rejects the request without modifying any record

### Requirement: Delete Academic Task (DELETE /academic_tasks/{id})
The system SHALL provide an endpoint `DELETE /academic_tasks/{id}` requiring user authentication that removes a task only if it belongs to the authenticated user.

#### Scenario: User deletes an owned task
- **WHEN** an authenticated user sends a DELETE request to `/academic_tasks/{id}` for their own task
- **THEN** system removes the record from the database

#### Scenario: Unauthorized delete attempt
- **WHEN** an authenticated user sends a DELETE request to `/academic_tasks/{id}` for a task owned by another user
- **THEN** system rejects the request without deleting any record

