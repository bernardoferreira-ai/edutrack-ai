## 1. Academic Tasks Table Schema (Xano)

- [x] 1.1 Criar `table/academic_tasks.xs` definindo a tabela `academic_tasks` com os campos `id`, `created_at`, `user_id` (FK para `user`), `subject_id` (FK para `subjects`), `title`, `description`, `due_date` e `status`, seguindo o padrão XanoScript.
- [x] 1.2 Configurar índices (`primary` em `id`, `btree` em `user_id`, `btree` em `subject_id` e `btree` em `created_at`) no arquivo `table/academic_tasks.xs`.

