## Context

The user requested planning the feature `feature-notas-atividades` to allow teachers to submit grades for students in specific activities.

Per `AGENTS.md`, the scope is strictly constrained:
- The task list and scope must contain ONLY the explicitly requested functionality.
- As emphasized in the golden rule of scope: do NOT create listing endpoints, GET APIs, frontend interfaces, or test suites unless explicitly requested.
- Responsibility ends at file generation; no push/sync/deploy to Xano.

## Goals / Non-Goals

**Goals:**
- Define the XanoScript database table for activity grades in `tables/activity_grades.xs`.
- Define the API endpoint `POST /activity_grades` in `apis/activity_grades/activity_grades_POST.xs` to record student grades.

**Non-Goals:**
- Creating GET / listing APIs (e.g. `GET /academic_tasks/{id}/grades` or `GET /users/{id}/grades` are strictly out of scope per `AGENTS.md`).
- Creating Streamlit frontend pages or components (out of scope).
- Creating automated test suites (out of scope).
- Pushing/deploying to Xano (developer's manual responsibility per `AGENTS.md`).

## Decisions

### 1. Table Schema (`tables/activity_grades.xs`)
- **Table Name**: `activity_grades`
- **Fields**:
  - `int id`: primary key auto-increment
  - `timestamp created_at?=now`: creation timestamp
  - `int user_id { table = "user" }`: teacher who recorded the grade (foreign key to `user`)
  - `int student_id { table = "user" }`: student receiving the grade (foreign key to `user`)
  - `int activity_id`: identifier of the target activity
  - `decimal grade`: grade value (e.g., min: 0)
  - `text? feedback filters=trim`: optional teacher notes/feedback
- **Indexes**:
  - `{type: "primary", field: [{name: "id"}]}`
  - `{type: "btree", field: [{name: "user_id", op: "asc"}]}`
  - `{type: "btree", field: [{name: "student_id", op: "asc"}]}`
  - `{type: "btree", field: [{name: "activity_id", op: "asc"}]}`

### 2. API Endpoint (`apis/activity_grades/activity_grades_POST.xs`)
- **Verb & Path**: `POST /activity_grades`
- **Group**: `Activity Grades`
- **Authentication**: Requires authenticated user (teacher).
- **Inputs**:
  - `int student_id`: identifier of the student
  - `int activity_id`: identifier of the activity
  - `decimal grade`: grade value
  - `text? feedback`: optional feedback
- **Logic**:
  - Preconditions: validate required fields (`student_id`, `activity_id`, `grade >= 0`).
  - Add record to `activity_grades` using `$auth.id` as `user_id`.
  - Return created record.

## Risks / Trade-offs

- **[Risk]** Relationship to users:
  → **Mitigation**: Existing authentication table in workspace is `table user` (`tables/882462_user.xs`). Both `user_id` and `student_id` reference `table = "user"`.

