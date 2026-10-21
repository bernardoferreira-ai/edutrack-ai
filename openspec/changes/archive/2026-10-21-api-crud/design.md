## Context

The user requested planning the creation of complete CRUD endpoints (POST, GET, PATCH, DELETE) for tables `subjects` and `academic_tasks`, with a mandatory security constraint: each authenticated user must only access and manage their own data.

Per `AGENTS.md`:
- Scope is strictly bounded: only the backend API endpoints requested are planned.
- Frontend modifications, automated tests, and deployment/push to Xano are excluded.

## Goals / Non-Goals

**Goals:**
- Implement the `Subjects` API group and endpoints in `api/subjects/`:
  - `POST /subjects`: create new subject owned by `$auth.id`.
  - `GET /subjects`: list only subjects where `user_id == $auth.id`.
  - `GET /subjects/{id}`: get single subject owned by `$auth.id`.
  - `PATCH /subjects/{id}`: update subject owned by `$auth.id`.
  - `DELETE /subjects/{id}`: delete subject owned by `$auth.id`.
- Implement the `Academic Tasks` API group and endpoints in `api/academic_tasks/`:
  - `POST /academic_tasks`: create new task owned by `$auth.id`.
  - `GET /academic_tasks`: list only tasks where `user_id == $auth.id`, with optional filters (`subject_id`, `status`).
  - `GET /academic_tasks/{id}`: get single task owned by `$auth.id`.
  - `PATCH /academic_tasks/{id}`: update task owned by `$auth.id`.
  - `DELETE /academic_tasks/{id}`: delete task owned by `$auth.id`.
- Enforce authentication (`auth = "user"`) across all 10 endpoints.
- Enforce strict tenancy isolation through query filtering and precondition checks verifying `user_id == $auth.id`.

**Non-Goals:**
- Frontend Streamlit modifications (out of scope).
- Automated test suites (out of scope).
- Table schema modifications (out of scope, tables `table/subjects.xs` and `table/academic_tasks.xs` already exist).
- Deploying or syncing to Xano (strictly prohibited by `AGENTS.md` Rule #2).

## Decisions

### 1. Directory Structure & Naming
- Group `api/subjects/`:
  - `subjects.xs` (api_group definition)
  - `subjects_POST.xs`
  - `subjects_GET.xs`
  - `subject_id_GET.xs`
  - `subject_id_PATCH.xs`
  - `subject_id_DELETE.xs`
- Group `api/academic_tasks/`:
  - `academic_tasks.xs` (api_group definition)
  - `academic_tasks_POST.xs`
  - `academic_tasks_GET.xs`
  - `academic_task_id_GET.xs`
  - `academic_task_id_PATCH.xs`
  - `academic_task_id_DELETE.xs`

### 2. Security & Multi-Tenancy Architecture
- **Authentication**: All endpoints declare `auth = "user"`, populating `$auth.id`.
- **Creation (POST)**: The `user_id` attribute is unconditionally set to `$auth.id` in `db.add` data payloads, ignoring any spoofed client value.
- **Listing (GET)**: The `db.query` blocks apply mandatory `where = { user_id: $auth.id }`.
- **Individual Access / Modification (GET by ID, PATCH, DELETE)**:
  - First queries the existing record by `id`.
  - Enforces `precondition ($record != null && $record.user_id == $auth.id)` returning error type `notfound` or `accessdenied`.
  - Prevents IDOR (Insecure Direct Object Reference) and information leakage across users.

### 3. Input Validation
- Mandatory fields checked via preconditions (e.g., `name` in subjects, `title` and `subject_id` in academic tasks).
- Optional fields trimmed and sanitized where applicable.

## Risks / Trade-offs

- **[Risk]** Cross-tenant task creation: A user might pass a `subject_id` that belongs to another user.
  → **Mitigation**: In `POST /academic_tasks`, verify that the referenced `subject_id` exists and has `user_id == $auth.id` prior to task creation.

