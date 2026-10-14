## 1. Backend Data Model (Xano)

- [ ] 1.1 Criar tabela `activity_grades` (`tables/activity_grades.xs`) com campos `id`, `created_at`, `user_id`, `student_id`, `activity_id`, `grade` e `feedback`, configurando índices primário e secundários.

## 2. Backend API Endpoint (Xano)

- [ ] 2.1 Criar API `POST /activity_grades` (`apis/activity_grades/activity_grades_POST.xs`) (para lançar nota) com validação de dados de entrada e persistência associada ao professor autenticado.

