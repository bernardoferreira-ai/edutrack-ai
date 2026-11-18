# pages-sync Specification

## Purpose
Specify delete confirmation dialog mechanisms for subjects and academic tasks across the Streamlit application pages.

## ADDED Requirements

### Requirement: Subject Delete Confirmation
The system SHALL prompt the user with a confirmation message ("Você realmente deseja excluir?") before executing the deletion of any subject on `pages/1_📚_Disciplinas.py`.

#### Scenario: User triggers subject deletion
- **WHEN** a user clicks the delete button for a subject
- **THEN** the system SHALL display a confirmation prompt requesting confirmation before calling `DELETE /subjects/{id}`

#### Scenario: User cancels subject deletion
- **WHEN** a user selects the cancel option in the subject deletion prompt
- **THEN** the system SHALL dismiss the prompt without deleting the subject

#### Scenario: User confirms subject deletion
- **WHEN** a user confirms the subject deletion prompt
- **THEN** the system SHALL delete the subject record and refresh the view

### Requirement: Task Delete Confirmation
The system SHALL prompt the user with a confirmation message ("Você realmente deseja excluir?") before executing the deletion of any academic task on `pages/2_📝_Tarefas.py`.

#### Scenario: User triggers task deletion
- **WHEN** a user clicks the delete button for an academic task
- **THEN** the system SHALL display a confirmation prompt requesting confirmation before calling `DELETE /academic_tasks/{id}`

#### Scenario: User cancels task deletion
- **WHEN** a user selects the cancel option in the task deletion prompt
- **THEN** the system SHALL dismiss the prompt without deleting the task

#### Scenario: User confirms task deletion
- **WHEN** a user confirms the task deletion prompt
- **THEN** the system SHALL delete the task record and refresh the view
