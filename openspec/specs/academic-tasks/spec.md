# academic-tasks Specification

## Purpose

Define the data structure and schema for academic tasks, allowing students to record and manage obligations (assignments, exams, projects) linked to academic subjects in EduTrack AI.

## Requirements

### Requirement: Academic Tasks Table Schema Definition
The system SHALL define the `academic_tasks` table containing the following fields: `id` (integer, primary key auto-increment), `created_at` (timestamp, default now), `user_id` (integer, foreign key referencing the `user` table), `subject_id` (integer, foreign key referencing the `subjects` table), `title` (text, mandatory title), `description` (text, task description details), `due_date` (date, deadline for the task), and `status` (text, current task state).

#### Scenario: Schema definition loading
- **WHEN** the `academic_tasks` table schema is loaded in Xano
- **THEN** the table contains fields `id`, `created_at`, `user_id`, `subject_id`, `title`, `description`, `due_date`, and `status` with their respective data types

#### Scenario: Mandatory task title
- **WHEN** validating an academic task record against the schema
- **THEN** the `title` field is required and trimmed

### Requirement: Foreign Key Relationships
The system SHALL establish foreign key relationships on `user_id` referencing the `user` authentication table and `subject_id` referencing the `subjects` table.

#### Scenario: Relational link to user and subject
- **WHEN** inspecting the foreign key definitions in `academic_tasks`
- **THEN** `user_id` references table `user` and `subject_id` references table `subjects`

### Requirement: Table Indexing
The system SHALL configure indexes on the `academic_tasks` table comprising a primary index on `id`, a btree index on `user_id`, a btree index on `subject_id`, and a btree index on `created_at`.

#### Scenario: Index verification
- **WHEN** the database indexing configuration is loaded
- **THEN** a primary index on `id` and secondary btree indexes on `user_id`, `subject_id`, and `created_at` are present

