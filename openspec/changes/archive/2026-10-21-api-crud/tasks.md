## 1. Subjects CRUD Endpoints (Xano)

- [x] 1.1 Criar api_group `Subjects` em `api/subjects/subjects.xs`.
- [x] 1.2 Criar endpoint `POST /subjects` (`api/subjects/subjects_POST.xs`) com autenticação obrigatória (`auth = "user"`), validação de entrada e atribuição automática de `user_id = $auth.id`.
- [x] 1.3 Criar endpoint `GET /subjects` (`api/subjects/subjects_GET.xs`) com autenticação obrigatória e filtro mandatório por `user_id == $auth.id`.
- [x] 1.4 Criar endpoint `GET /subjects/{id}` (`api/subjects/subject_id_GET.xs`) com autenticação obrigatória e verificação de propriedade (`user_id == $auth.id`).
- [x] 1.5 Criar endpoint `PATCH /subjects/{id}` (`api/subjects/subject_id_PATCH.xs`) com autenticação obrigatória e validação de propriedade (`user_id == $auth.id`) antes da atualização.
- [x] 1.6 Criar endpoint `DELETE /subjects/{id}` (`api/subjects/subject_id_DELETE.xs`) com autenticação obrigatória e validação de propriedade (`user_id == $auth.id`) antes da exclusão.

## 2. Academic Tasks CRUD Endpoints (Xano)

- [x] 2.1 Criar api_group `Academic Tasks` em `api/academic_tasks/academic_tasks.xs`.
- [x] 2.2 Criar endpoint `POST /academic_tasks` (`api/academic_tasks/academic_tasks_POST.xs`) com autenticação obrigatória (`auth = "user"`), validação de que `subject_id` pertence ao usuário logado e atribuição de `user_id = $auth.id`.
- [x] 2.3 Criar endpoint `GET /academic_tasks` (`api/academic_tasks/academic_tasks_GET.xs`) com autenticação obrigatória, filtro mandatório por `user_id == $auth.id` e suporte a filtros opcionais (`subject_id`, `status`).
- [x] 2.4 Criar endpoint `GET /academic_tasks/{id}` (`api/academic_tasks/academic_task_id_GET.xs`) com autenticação obrigatória e verificação de propriedade (`user_id == $auth.id`).
- [x] 2.5 Criar endpoint `PATCH /academic_tasks/{id}` (`api/academic_tasks/academic_task_id_PATCH.xs`) com autenticação obrigatória e validação de propriedade (`user_id == $auth.id`) antes da atualização.
- [x] 2.6 Criar endpoint `DELETE /academic_tasks/{id}` (`api/academic_tasks/academic_task_id_DELETE.xs`) com autenticação obrigatória e validação de propriedade (`user_id == $auth.id`) antes da exclusão.
