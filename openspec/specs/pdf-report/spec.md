# pdf-report Specification

## Purpose

Define the requirements for generating a student academic performance PDF report via Python and providing a secure Xano backend endpoint for authenticated students to download their report.

## Requirements

### Requirement: Academic Performance PDF Generation Script
The system SHALL provide a Python script in `scripts/generate_student_report.py` that consolidates student academic metrics (disciplines, total tasks, completed tasks, pending tasks, and completion rate) and outputs a formatted PDF report file.

#### Scenario: Successful PDF generation for a student
- **WHEN** the script is executed with valid student identifier or authentication token and an output path
- **THEN** the system SHALL generate a valid PDF file at the specified location containing the student's academic performance metrics and return a success status

#### Scenario: Script execution with custom output file path
- **WHEN** the script is executed specifying the `--output` parameter
- **THEN** the system SHALL write the generated PDF report directly to the provided destination path

#### Scenario: Student with no registered tasks or disciplines
- **WHEN** the script is executed for a student with zero registered tasks or disciplines
- **THEN** the system SHALL generate the PDF displaying zero totals and 0.0% completion without throwing computational or division-by-zero errors

### Requirement: Xano Endpoint for Report Download
The system SHALL provide an authenticated endpoint `GET /student_report` in Xano under the `Reports` API group that generates or retrieves the student's performance report for the authenticated user (`$auth.id`) and serves it for download.

#### Scenario: Authenticated user requests report download
- **WHEN** an authenticated user issues a GET request to `/student_report` with a valid JWT bearer token
- **THEN** the system SHALL return the performance report corresponding exclusively to the authenticated student (`user_id == $auth.id`)

#### Scenario: Unauthenticated request to report download
- **WHEN** an unauthenticated request is sent to `/student_report` without a valid token
- **THEN** the system SHALL reject the request with an unauthorized error (HTTP 401)

