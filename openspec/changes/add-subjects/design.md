## Context

EduTrack AI is an academic assistant featuring a Streamlit frontend (`app.py`) and a Xano backend structure (`tables/`, `apis/`, `functions/`). The current UI has placeholder views for "Dashboard", "Disciplinas", and "Tarefas", with static metrics ("0 Active Subjects").

See `proposal.md` for motivation and `specs/subjects/spec.md` for functional requirements.

## Goals / Non-Goals

**Goals:**
- Define the Xano database schema for subjects (`subject` table) with relations, indexes, and status tracking.
- Specify REST API endpoints for subject CRUD operations in Xano.
- Integrate the Streamlit "Disciplinas" view with full listing, addition, and editing capabilities.
- Integrate the Streamlit "Dashboard" view to display dynamic metrics of active subjects.
- Provide a resilient API client in Streamlit with graceful fallback/mock support when Xano credentials or internet connection are unavailable.

**Non-Goals:**
- Academic task assignment or homework tracking (handled by the tasks feature).
- Grade calculations, GPA tracking, or syllabus parsing (future capabilities).
- Complex institutional or multi-tenant organizational hierarchies.

## Decisions

### 1. Data Model Structure (`tables/subject.xs`)
- **Fields:**
  - `int id` (primary key)
  - `timestamp created_at` (default `now`)
  - `int user_id` (foreign key to `user.id`, indexed)
  - `text name` (required, trimmed)
  - `text? code` (course code, e.g., "MAT101")
  - `text? professor` (instructor name)
  - `text? semester` (academic term, e.g., "2026.1")
  - `text? color` (hex color or tag for visual identification)
  - `enum status` (`values = ["active", "completed", "archived"]`, default `"active"`)
- **Rationale**: Keeps the academic course record lightweight yet extensible for upcoming task attachments and calendar scheduling.
- **Alternatives Considered**: Using a simple string list on the user table — rejected because relational subjects allow attaching tasks, notes, and attendance later.

### 2. Backend REST API Endpoints (`apis/subjects/`)
- `GET /subjects`: List subjects, with optional `status` filter query param.
- `POST /subjects`: Create a new subject with validation for `name`.
- `GET /subjects/{subject_id}`: Retrieve a single subject record.
- `PATCH /subjects/{subject_id}`: Partial update for subject attributes or status change.
- `DELETE /subjects/{subject_id}`: Delete a subject.
- **Rationale**: Conforms to RESTful conventions in Xano and straightforward consumption in Python/Streamlit.

### 3. Frontend Architecture (`app.py` & Service Layer)
- Introduce a lightweight service module (`services/subject_service.py` or helper functions) to encapsulate API calls.
- Support configuration via environment variables / `.env` / `st.secrets` (`XANO_API_URL`, `XANO_API_KEY`).
- Implement an in-memory/session-state fallback mode if the backend endpoint is unreachable or not yet deployed, allowing offline development and testing.
- **Rationale**: Decouples presentation in Streamlit from network/Xano details, preventing UI crashes if the API is offline.

### 4. Specialization & Role Alignment (`AGENTS.md`)
- Backend XanoScript files (tables, APIs) will be authored adhering to XanoScript syntax and delegated according to the guidelines in `AGENTS.md`.

## Risks / Trade-offs

- **[Risk]** Backend API may not be deployed to Xano cloud immediately during local frontend development.
  → **Mitigation**: The frontend service layer will feature a fallback mock/session-state store to ensure the Streamlit application remains functional and testable locally.
- **[Risk]** Subject deletion cascading impact on future tasks.
  → **Mitigation**: For now, simple deletion or status archiving (`status = "archived"`); when task management is added, cascade behavior will be handled explicitly.

