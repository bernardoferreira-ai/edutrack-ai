# activity-grades Specification

## Purpose
Specify the student grades visualization interface in `pages/4_📊_Notas.py` displaying assignment and exam evaluations, current averages, approval status badges, and remaining points required for approval.

## ADDED Requirements

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
