# subjects-api Specification

## Purpose

Define the RESTful CRUD endpoints for academic subjects in EduTrack AI, ensuring strict user-level data isolation where each authenticated user can only access and modify their own records.

## Requirements

### Requirement: Create Subject (POST /subjects)
The system SHALL provide an endpoint `POST /subjects` requiring user authentication that creates a new subject record, automatically setting `user_id` to the authenticated user's ID (`$auth.id`).

#### Scenario: User successfully creates a subject
- **WHEN** an authenticated user sends a valid POST request to `/subjects` with mandatory field `name`
- **THEN** system stores the subject with `user_id = $auth.id` and returns the created record

#### Scenario: Creation without mandatory name
- **WHEN** an authenticated user sends a POST request with missing or empty `name`
- **THEN** system rejects the request with a bad request error

### Requirement: List User Subjects (GET /subjects)
The system SHALL provide an endpoint `GET /subjects` requiring user authentication that retrieves only the subjects where `user_id` matches the authenticated user (`$auth.id`).

#### Scenario: User lists their subjects
- **WHEN** an authenticated user requests `GET /subjects`
- **THEN** system returns only subject records owned by that user, never returning records of other users

### Requirement: Get Subject by ID (GET /subjects/{id})
The system SHALL provide an endpoint `GET /subjects/{id}` requiring user authentication that retrieves a single subject only if it belongs to the authenticated user.

#### Scenario: User retrieves an owned subject
- **WHEN** an authenticated user requests `GET /subjects/{id}` for a subject they own
- **THEN** system returns the requested subject record

#### Scenario: User attempts to retrieve another user's subject
- **WHEN** an authenticated user requests `GET /subjects/{id}` for a subject owned by a different user
- **THEN** system rejects the request with an access denied or not found error

### Requirement: Update Subject (PATCH /subjects/{id})
The system SHALL provide an endpoint `PATCH /subjects/{id}` requiring user authentication that allows updating fields of a subject only if it belongs to the authenticated user.

#### Scenario: User updates an owned subject
- **WHEN** an authenticated user sends a PATCH request to `/subjects/{id}` for their own subject
- **THEN** system updates the specified fields and returns the updated record

#### Scenario: Unauthorized update attempt
- **WHEN** an authenticated user sends a PATCH request to `/subjects/{id}` for a subject owned by another user
- **THEN** system rejects the request without modifying any data

### Requirement: Delete Subject (DELETE /subjects/{id})
The system SHALL provide an endpoint `DELETE /subjects/{id}` requiring user authentication that deletes a subject only if it belongs to the authenticated user.

#### Scenario: User deletes an owned subject
- **WHEN** an authenticated user sends a DELETE request to `/subjects/{id}` for their own subject
- **THEN** system removes the record from the database

#### Scenario: Unauthorized delete attempt
- **WHEN** an authenticated user sends a DELETE request to `/subjects/{id}` for a subject owned by another user
- **THEN** system rejects the request without removing any data

