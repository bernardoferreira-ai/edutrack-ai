## 1. Backend Data Model (Xano)

- [x] 1.1 Create `tables/882464_subject.xs` defining table `subject` with fields `id`, `created_at`, `user_id`, `name`, `code`, `professor`, `semester`, `color`, and `status`, and verify file syntax matches XanoScript table standards.
- [x] 1.2 Configure indexes (`primary` on `id`, `btree` on `user_id`, and `created_at`) in `tables/882464_subject.xs` and verify schema consistency.

## 2. Backend API Endpoints (Xano)

- [x] 2.1 Create API queries under `apis/subjects/` for listing subjects with optional status filtering (`GET /subjects`) and retrieving a single subject (`GET /subjects/{subject_id}`).
- [x] 2.2 Create API endpoints under `apis/subjects/` for creating (`POST /subjects`), updating (`PATCH /subjects/{subject_id}`), and deleting (`DELETE /subjects/{subject_id}`) subjects with input validation for mandatory `name`.

## 3. Frontend Client & Service Layer

- [x] 3.1 Create `services/subject_service.py` with methods to list, get, create, update, and delete subjects, supporting Xano REST integration and in-memory/session fallback mode.
- [x] 3.2 Create automated tests in `tests/test_subject_service.py` verifying subject CRUD operations and fallback behavior.

## 4. Frontend UI Integration (Streamlit)

- [x] 4.1 Update the "Disciplinas" view in `app.py` to render the list of registered subjects with details (code, professor, semester, status badge) and verify display rendering.
- [x] 4.2 Add subject creation form and edit/delete actions to the "Disciplinas" view in `app.py` and verify form submission persists records.
- [x] 4.3 Update the Dashboard view in `app.py` to compute and display the dynamic count of "Disciplinas Ativas" using the subject service, verifying the metric reflects real data.

## 5. End-to-End Verification

- [x] 5.1 Run test suite and launch Streamlit to verify full user journey: adding subjects, viewing list, checking Dashboard active metrics, and removing a subject.

