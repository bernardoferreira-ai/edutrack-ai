# Proposal: Add Subjects (Disciplinas) Management

## Why

Students need a structured way to register, organize, and track their academic courses/subjects within EduTrack AI. Adding subjects management establishes the core academic entity that tasks, schedules, and AI study tracking will attach to.

## What Changes

- Introduce a data model for academic subjects (`subject` table) including subject name, code, instructor/professor name, semester, status, and associated user.
- Introduce backend CRUD API endpoints for managing subjects (list, retrieve, create, update, delete).
- Update the Streamlit frontend (`app.py`) under the "Disciplinas" navigation menu to list registered subjects, display subject details, and allow registering/editing subjects.
- Connect the "Disciplinas Ativas" metric on the Dashboard to reflect actual active subjects.

## Capabilities

### New Capabilities
- `subjects`: Academic subject/course management, enabling students to create, view, update, and manage course information and status.

### Modified Capabilities
<!-- None -->

## Impact

- **Backend**: New Xano table definition (`subject`) and REST API group/endpoints for subjects.
- **Frontend**: Streamlit application UI updates in `app.py` for the "Disciplinas" view and "Dashboard" metrics.
- **Dependencies**: No external library additions required; relies on existing Streamlit and Xano integration.

