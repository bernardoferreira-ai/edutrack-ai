# Proposal: CRUD Endpoints for Subjects and Academic Tasks

## Why

Para que o EduTrack AI opere como uma plataforma completa de gestão acadêmica, os alunos precisam ser capazes de cadastrar, consultar, atualizar e remover suas disciplinas (`subjects`) e obrigações acadêmicas (`academic_tasks`). Além disso, por questões de segurança e privacidade em ambiente multi-tenant, cada usuário autenticado deve acessar estritamente os seus próprios dados, sendo mandatório o isolamento por `user_id`.

## What Changes

Em conformidade estrita com a **Regra nº 1 de Escopo** do `AGENTS.md`, esta proposta abrange **SOMENTE** o que foi explicitamente solicitado pelo usuário:

- **CRUD para a tabela `subjects` (sob o grupo de APIs `Subjects`):**
  - `POST /subjects`: Criação de disciplina atribuindo automaticamente `user_id = $auth.id`.
  - `GET /subjects`: Listagem de disciplinas filtrando exclusivamente por `user_id == $auth.id`.
  - `GET /subjects/{id}`: Obtenção de uma disciplina específica com validação de que pertence a `$auth.id`.
  - `PATCH /subjects/{id}`: Atualização parcial de disciplina com validação de propriedade (`user_id == $auth.id`).
  - `DELETE /subjects/{id}`: Exclusão de disciplina com validação de propriedade (`user_id == $auth.id`).

- **CRUD para a tabela `academic_tasks` (sob o grupo de APIs `Academic Tasks`):**
  - `POST /academic_tasks`: Criação de tarefa vinculada a uma disciplina do aluno e atribuindo `user_id = $auth.id`.
  - `GET /academic_tasks`: Listagem de tarefas filtrando exclusivamente por `user_id == $auth.id` (com suporte a filtros opcionais por `subject_id` e `status`).
  - `GET /academic_tasks/{id}`: Obtenção de tarefa específica com validação de que pertence a `$auth.id`.
  - `PATCH /academic_tasks/{id}`: Atualização de tarefa com validação de propriedade (`user_id == $auth.id`).
  - `DELETE /academic_tasks/{id}`: Exclusão de tarefa com validação de propriedade (`user_id == $auth.id`).

- **Isolamento de Segurança:**
  - Todos os endpoints exigem autenticação (`auth = "user"`).
  - Nenhuma operação permite leitura ou mutação de registros pertencentes a outros usuários.

*Nota de Escopo:* Não estão incluídas alterações em páginas do Streamlit, novas tabelas ou suítes de testes automatizados, pois não foram explicitamente solicitadas.

## Capabilities

### New Capabilities
- `subjects-api`: Endpoints RESTful CRUD completos para gestão de disciplinas com isolamento por usuário autenticado.
- `academic-tasks-api`: Endpoints RESTful CRUD completos para gestão de obrigações acadêmicas com isolamento por usuário autenticado.

### Modified Capabilities
<!-- None -->

## Impact

- **Backend (Xano / XanoScript)**:
  - Cria o grupo de APIs `api/subjects/subjects.xs` e os endpoints `POST`, `GET`, `GET by ID`, `PATCH` e `DELETE`.
  - Cria o grupo de APIs `api/academic_tasks/academic_tasks.xs` e os endpoints `POST`, `GET`, `GET by ID`, `PATCH` e `DELETE`.
- **Frontend**: Nenhum impacto direto nesta etapa.

