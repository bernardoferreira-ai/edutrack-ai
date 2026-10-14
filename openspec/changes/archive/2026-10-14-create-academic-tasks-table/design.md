## Context

The user requested planning the creation of the `academic_tasks` table to allow students to record and manage obligations (assignments, exams, projects) linked to academic subjects.

Requested fields:
- `title` (text)
- `description` (text)
- `due_date` (date)
- `status` (text)
- `subject_id` (reference to table `subjects`)

Per `AGENTS.md`, the scope is strictly constrained:
- Only the table schema definition is within scope.
- Automatically creating CRUD APIs, frontend Streamlit components, or automated tests is strictly forbidden.
- AI responsibilities end at generating/editing files; deploying/syncing to Xano is left to the developer.

## Goals / Non-Goals

**Goals:**
- Define the XanoScript database table for `academic_tasks` in `table/academic_tasks.xs`.
- Implement the exact requested schema:
  - `id`: integer primary key auto-increment
  - `created_at`: timestamp defaulting to now
  - `user_id`: integer foreign key referencing table `user`
  - `subject_id`: integer foreign key referencing table `subjects`
  - `title`: text, mandatory trimmed
  - `description`: text, optional trimmed
  - `due_date`: date, optional deadline
  - `status`: text, task status (e.g., default "pending")
- Configure table indexes: primary on `id`, btree on `user_id`, btree on `subject_id`, and btree on `created_at`.

**Non-Goals:**
- Creating REST API endpoints (strictly out of scope per `AGENTS.md`).
- Creating or modifying Streamlit frontend views (strictly out of scope per `AGENTS.md`).
- Creating automated test suites (strictly out of scope per `AGENTS.md`).
- Pushing/deploying changes to Xano (manual developer responsibility per `AGENTS.md`).

## Decisions

### 1. Table Schema (`table/academic_tasks.xs`)
- **Table Name**: `academic_tasks`
- **Auth Setting**: `auth = false`
- **Fields**:
  - `int id`
  - `timestamp created_at?=now`
  - `int user_id? { table = "user" }`
  - `int subject_id? { table = "subjects" }`
  - `text title filters=trim`
  - `text? description filters=trim`
  - `date? due_date`
  - `text? status?="pending" filters=trim`
- **Indexes**:
  - `{type: "primary", field: [{name: "id"}]}`
  - `{type: "btree", field: [{name: "user_id", op: "asc"}]}`
  - `{type: "btree", field: [{name: "subject_id", op: "asc"}]}`
  - `{type: "btree", field: [{name: "created_at", op: "desc"}]}`

### 2. Relational References
- `user_id` references `table = "user"` (the authentication table defined in `table/user.xs`).
- `subject_id` references `table = "subjects"` (the subjects table defined in `table/subjects.xs`).

## Risks / Trade-offs

- **[Risk]** Consistency with table naming:
  → **Mitigation**: The subjects table in this workspace is named `subjects` (`table/subjects.xs`). The foreign key definition in `academic_tasks.xs` explicitly references `table = "subjects"`.

