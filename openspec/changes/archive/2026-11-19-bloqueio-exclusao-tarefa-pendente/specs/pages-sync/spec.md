# pages-sync Specification

## Purpose
Define o comportamento da exclusão de tarefas pendentes na interface Streamlit.

## ADDED Requirements

### Requirement: Block Pending Task Deletion
The system SHALL prevent the exclusion of a pending academic task and SHALL instruct the user to complete it first.

#### Scenario: User tries to delete a pending task
- **WHEN** the user clicks to exclude an academic task with status `pending`
- **THEN** the system SHALL display a warning stating that the task is pending
- **AND** the system SHALL instruct the user to conclude the task before excluding it
- **AND** the system SHALL NOT display or enable the delete confirmation action

#### Scenario: User closes the pending task warning
- **WHEN** the user clicks `Entendi` in the pending task warning
- **THEN** the system SHALL close the dialog without deleting the task

#### Scenario: User tries to delete a completed task
- **WHEN** the user clicks to exclude an academic task with status `completed`
- **THEN** the system SHALL display the existing delete confirmation dialog
- **AND** the task SHALL be deleted only after explicit confirmation
