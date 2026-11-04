# pages-sync Specification

## Purpose

Define the functional and interface requirements for synchronizing the Streamlit pages (`pages/1_📚_Disciplinas.py` and `pages/2_📝_Tarefas.py`) with Xano's CRUD endpoints for `subjects` and `academic_tasks`, enforcing JWT user authentication and preserving the exact visual appearance of the existing screens.

## ADDED Requirements

### Requirement: Subjects Synchronization in Disciplinas Page
The system SHALL retrieve subjects belonging to the authenticated user from `GET /subjects` and register new subjects via `POST /subjects` on `pages/1_📚_Disciplinas.py`, using the JWT bearer token from `st.session_state["auth_token"]`.

#### Scenario: User views their registered subjects
- **WHEN** an authenticated user opens the Disciplinas page and selects the list tab
- **THEN** the system SHALL invoke `GET /subjects` with the user's JWT token and render the retrieved subjects in the dataframe component

#### Scenario: User registers a new subject
- **WHEN** an authenticated user fills in the subject form in the new subject tab and clicks "Salvar"
- **THEN** the system SHALL send a `POST /subjects` request containing `name`, `teacher`, and workload hours with the JWT token, persisting the record in Xano and confirming creation

#### Scenario: User updates or deletes a subject
- **WHEN** an authenticated user modifies or deletes a subject from their list
- **THEN** the system SHALL send a `PATCH /subjects/{id}` or `DELETE /subjects/{id}` request with the JWT token and update the displayed dataframe

### Requirement: Academic Tasks Synchronization in Tarefas Page
The system SHALL retrieve academic tasks belonging to the authenticated user from `GET /academic_tasks` and update task status via `PATCH /academic_tasks/{id}` on `pages/2_📝_Tarefas.py`, using the JWT bearer token from `st.session_state["auth_token"]`.

#### Scenario: User views and filters tasks
- **WHEN** an authenticated user accesses the Tarefas page and uses the search input or status selectbox
- **THEN** the system SHALL query `GET /academic_tasks` with the JWT token and display matching tasks in individual expander components

#### Scenario: User toggles task completion
- **WHEN** an authenticated user toggles the "Marcar como Concluída" checkbox inside a task expander
- **THEN** the system SHALL send a `PATCH /academic_tasks/{id}` request updating the `status` field to "completed" or "pending" and reflect the change immediately

#### Scenario: User creates or removes a task
- **WHEN** an authenticated user creates a new task or deletes an existing task
- **THEN** the system SHALL invoke `POST /academic_tasks` or `DELETE /academic_tasks/{id}` with the JWT token and refresh the task view

### Requirement: Visual Structure and Layout Preservation
The system SHALL preserve the exact visual appearance, component hierarchy, labels, and layout of `pages/1_📚_Disciplinas.py` and `pages/2_📝_Tarefas.py` without modifying colors, fonts, spacing, icons, or component arrangements.

#### Scenario: Rendering Disciplinas page
- **WHEN** the Disciplinas page is rendered
- **THEN** the system SHALL retain the page configuration, title "Gestão de Disciplinas", the two tabs `["📋 Listar", "➕ Nova Disciplina"]`, the form structure with fields for name, teacher, and weekday, and the dataframe table

#### Scenario: Rendering Tarefas page
- **WHEN** the Tarefas page is rendered
- **THEN** the system SHALL retain the title "Minhas Tarefas", the two-column filter layout (`[3, 1]`) with search box and status dropdown, the markdown divider, and the expander structure with title, discipline, due date, and checkbox

