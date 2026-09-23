# Proposal: Define Subjects Table Schema

## Why

Establish the official XanoScript database schema for the `subjects` table, allowing EduTrack AI to record subject names, assigned teachers, course hours, and associate each subject with an authenticated user, adhering strictly to the scoping rules in `AGENTS.md`.

## What Changes

- Define the XanoScript database table `subjects` with the exact requested fields:
  - `id` (int, auto-increment primary key)
  - `created_at` (timestamp, default now)
  - `name` (text, trimmed)
  - `teacher` (text, teacher name)
  - `hours` (int, course workload hours)
  - `user_id` (int, foreign key referencing the `user` table)
- Configure table indexes: primary key index on `id`, btree index on `user_id`, and btree index on `created_at`.
- Strict scope adherence: This change does NOT include CRUD APIs, frontend UI, or automated tests, complying with `AGENTS.md`.

## Capabilities

### New Capabilities
- `subjects-schema`: Schema specification for the `subjects` database table in Xano, establishing data types, fields (`name`, `teacher`, `hours`, `user_id`), and relational constraints.

### Modified Capabilities
<!-- None -->

## Impact

- **Backend**: Adds or updates the table definition file in `tables/` (e.g. `tables/subjects.xs`).
- **APIs & Frontend**: None. Excluded from scope per `AGENTS.md` guidelines.

