# pages-sync Specification

## Purpose
Specify task deletion capabilities on the Tarefas page (`pages/2_📝_Tarefas.py`) synchronized with Xano and fallback state.

## ADDED Requirements

### Requirement: Task Deletion on Tarefas Page
The system SHALL allow users to delete an academic task from `pages/2_📝_Tarefas.py`, dispatching a `DELETE /academic_tasks/{id}` request with the JWT bearer token or removing the record from local session fallback store.

#### Scenario: User deletes a task from card expander
- **WHEN** an authenticated or local user clicks the "Excluir Tarefa" button inside a task expander
- **THEN** the system SHALL remove the task from the database or session state, display a confirmation message, and refresh the interface

#### Scenario: User deletes a task from management section
- **WHEN** a user selects a task in the "Gerenciar Tarefas (Excluir)" expander and clicks "Excluir Tarefa Selecionada"
- **THEN** the system SHALL delete the selected task and update the list
