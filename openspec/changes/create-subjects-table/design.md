## Context

The user requested defining the schema for the `subjects` table with fields `id (auto)`, `name (text)`, `teacher (text)`, `hours (int)`, and `user_id (FK to user/users authentication table)`.

Per `AGENTS.md`, the scope is strictly constrained:
- The task list and implementation must contain ONLY the table schema definition.
- Automatically creating CRUD APIs, frontend components, or tests is strictly forbidden.
- AI responsibilities end at generating/editing files; deploying/syncing to Xano is left to the developer.

See `proposal.md` for motivation and `specs/subjects-schema/spec.md` for functional requirements.

## Goals / Non-Goals

**Goals:**
- Define the XanoScript database table for `subjects` in `tables/subjects.xs` (or `tables/882465_subjects.xs`).
- Implement the exact requested schema:
  - `id`: integer primary key auto-increment
  - `created_at`: timestamp auto-defaulting to now
  - `user_id`: integer foreign key referencing the `user` authentication table
  - `name`: text, mandatory trimmed
  - `teacher`: text, optional trimmed
  - `hours`: integer, workload hours (minimum 0)
- Configure table indexes: primary index on `id`, secondary btree index on `user_id`, and btree index on `created_at`.

**Non-Goals:**
- Creating REST API endpoints for subjects (strictly out of scope per `AGENTS.md`).
- Creating or editing frontend views or Streamlit code (strictly out of scope per `AGENTS.md`).
- Creating automated test suites (strictly out of scope per `AGENTS.md`).
- Pushing/deploying changes to Xano (developer's manual responsibility per `AGENTS.md`).

## Decisions

### 1. Table Schema & Syntax (`tables/subjects.xs`)
- **Table Name**: `subjects` (explicitly requested by user)
- **Table Configuration**: `auth = false` (standard table, not the auth identity table)
- **Fields**:
  - `int id`
  - `timestamp created_at?=now`
  - `int user_id { table = "user" }`
  - `text name filters=trim`
  - `text? teacher filters=trim`
  - `int? hours filters=min:0`
- **Indexes**:
  - `{type: "primary", field: [{name: "id"}]}`
  - `{type: "btree", field: [{name: "user_id", op: "asc"}]}`
  - `{type: "btree", field: [{name: "created_at", op: "desc"}]}`

### 2. File Location
- Place the file at `tables/subjects.xs` adhering to the project's Xano table conventions.

## Risks / Trade-offs

- **[Risk]** Relationship table reference (`user` vs `users`).
  → **Mitigation**: The existing workspace table is `tables/882462_user.xs` (`table user`). Therefore, the relational constraint references `table = "user"`.

