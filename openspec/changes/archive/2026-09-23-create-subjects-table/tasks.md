## 1. Subjects Table Schema (Xano)

- [x] 1.1 Create `tables/subjects.xs` defining table `subjects` with fields `id` (int), `created_at` (timestamp), `user_id` (int, foreign key referencing table `user`), `name` (text), `teacher` (text), and `hours` (int), verifying syntax against XanoScript table standards.
- [x] 1.2 Configure indexes (`primary` on `id`, `btree` on `user_id`, and `btree` on `created_at`) in `tables/subjects.xs` and verify schema consistency.

