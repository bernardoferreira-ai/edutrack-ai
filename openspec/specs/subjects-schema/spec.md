# Subjects Schema Specification

## Purpose

Defines the structural schema for the academic subjects database table, specifying fields for subject name, teacher, workload hours, and user ownership in Xano.

## Requirements

### Requirement: Subjects Table Schema Definition
The system SHALL define the `subjects` table containing the following fields: `id` (integer, primary key auto-increment), `created_at` (timestamp, default now), `name` (text, mandatory subject name), `teacher` (text, instructor or professor name), `hours` (integer, workload hours), and `user_id` (integer, foreign key referencing the user table).

#### Scenario: Schema structure definition
- **WHEN** the `subjects` table schema is loaded in Xano
- **THEN** the table contains fields `id`, `created_at`, `name`, `teacher`, `hours`, and `user_id` with their respective data types

#### Scenario: Mandatory subject name
- **WHEN** validating a subject record against the schema
- **THEN** the `name` field is required and trimmed

### Requirement: User Relationship and Foreign Key
The system SHALL establish a relational foreign key on the `user_id` field referencing the authentication `user` table.

#### Scenario: Relational link to user
- **WHEN** inspecting the `user_id` field definition in the `subjects` table
- **THEN** it references the `user` authentication table

### Requirement: Table Indexing
The system SHALL define indexes on the `subjects` table comprising a primary index on `id`, a btree index on `user_id`, and a btree index on `created_at`.

#### Scenario: Index configuration
- **WHEN** the database indexing configuration is loaded
- **THEN** a primary index on `id` and secondary btree indexes on `user_id` and `created_at` are present

