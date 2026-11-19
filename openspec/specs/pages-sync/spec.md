# pages-sync Specification

## Purpose

Define the functional and interface requirements for synchronizing the Streamlit pages (`pages/1_📚_Disciplinas.py` and `pages/2_📝_Tarefas.py`) with Xano's CRUD endpoints for `subjects` and `academic_tasks`, enforcing JWT user authentication and preserving the exact visual appearance of the existing screens.

## Requirements

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

### Requirement: Task Deletion on Tarefas Page
The system SHALL allow users to delete an academic task from `pages/2_📝_Tarefas.py`, dispatching a `DELETE /academic_tasks/{id}` request with the JWT bearer token or removing the record from local session fallback store.

#### Scenario: User deletes a task from card expander
- **WHEN** an authenticated or local user clicks the "Excluir Tarefa" button inside a task expander
- **THEN** the system SHALL remove the task from the database or session state, display a confirmation message, and refresh the interface

#### Scenario: User deletes a task from management section
- **WHEN** a user selects a task in the "Gerenciar Tarefas (Excluir)" expander and clicks "Excluir Tarefa Selecionada"
- **THEN** the system SHALL delete the selected task and update the list

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

### Requirement: Enhanced Card and Box Containers Design
The system SHALL render visually enhanced card containers, expander boxes, and informational badges across `pages/1_📚_Disciplinas.py` and `pages/2_📝_Tarefas.py`, preserving all existing forms, inputs, buttons, options, and confirmation dialogs.

#### Scenario: Rendering styled task cards and expanders
- **WHEN** a user navigates to `pages/2_📝_Tarefas.py`
- **THEN** the system SHALL display task expanders and filter panels with refined borders, shadows, rounded corners, and styled discipline/due date badges

#### Scenario: Rendering styled subject cards and expanders
- **WHEN** a user navigates to `pages/1_📚_Disciplinas.py`
- **THEN** the system SHALL display subject tabs, table containers, and management expanders with cohesive card styling and clean layout

### Requirement: Dark Theme and Red Button Accents
The system SHALL apply a dark background color scheme (black tending to dark grey) across platform pages and render selected action buttons (such as deletion and logout actions) with a red color scheme, preserving all existing options, labels, inputs, and functions.

#### Scenario: User views pages in dark theme
- **WHEN** a user navigates through the application pages (`app.py`, Disciplinas, Tarefas, Perfil)
- **THEN** the system SHALL render dark grey backgrounds with high-contrast readable typography and styled dark content containers

#### Scenario: User views deletion and action buttons
- **WHEN** a user views task or subject deletion buttons and the profile logout action
- **THEN** the system SHALL render those buttons with a vibrant red styling

### Requirement: Visual Structure and Layout Preservation
The system SHALL preserve the exact visual appearance, component hierarchy, labels, and layout of `pages/1_📚_Disciplinas.py` and `pages/2_📝_Tarefas.py` without modifying colors, fonts, spacing, icons, or component arrangements.

#### Scenario: Rendering Disciplinas page
- **WHEN** the Disciplinas page is rendered
- **THEN** the system SHALL retain the page configuration, title "Gestão de Disciplinas", the two tabs `["📋 Listar", "➕ Nova Disciplina"]`, the form structure with fields for name, teacher, and weekday, and the dataframe table

#### Scenario: Rendering Tarefas page
- **WHEN** the Tarefas page is rendered
- **THEN** the system SHALL retain the title "Minhas Tarefas", the two-column filter layout (`[3, 1]`) with search box and status dropdown, the markdown divider, and the expander structure with title, discipline, due date, and checkbox

### Requirement: Shared EduTrack Visual System
The system SHALL apply a shared visual style to the Dashboard and the Disciplinas, Tarefas, Perfil, and Notas pages while preserving all existing controls and data.

#### Scenario: User navigates across pages
- **WHEN** the user opens or navigates between application pages
- **THEN** the system SHALL present consistent typography, spacing, card borders, shadows, tabs, expanders, controls, tables, and responsive layouts

#### Scenario: Existing options remain unchanged
- **WHEN** the shared design is applied
- **THEN** the system SHALL preserve existing labels, fields, data, buttons, authentication flows, and backend integrations

