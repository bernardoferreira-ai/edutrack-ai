# Proposal: Define Academic Tasks Table Schema

## Why

Permitir que o aluno registre e gerencie suas obrigações acadêmicas (como lições, provas e trabalhos) vinculadas a cada disciplina cursada no EduTrack AI. Atualmente, o sistema conta com a tabela de disciplinas (`subjects`), mas necessita da estrutura de dados para armazenar e organizar as tarefas acadêmicas.

## What Changes

Em estrita conformidade com a **Regra nº 1 de Escopo** do `AGENTS.md`, esta proposta abrange **SOMENTE** o que foi explicitamente solicitado pelo usuário:
- Definição do esquema da tabela de banco de dados `academic_tasks` no Xano (via XanoScript em `table/academic_tasks.xs`) contendo:
  - `id` (int, chave primária auto-incremento)
  - `created_at` (timestamp, padrão now)
  - `user_id` (int, chave estrangeira referenciando a tabela `user`)
  - `subject_id` (int, chave estrangeira referenciando a tabela `subjects`)
  - `title` (text, título da obrigação acadêmica)
  - `description` (text, descrição detalhada)
  - `due_date` (date, data limite de entrega)
  - `status` (text, status da tarefa, ex: "pending", "completed")
- Configuração de índices para otimização de consultas por usuário, disciplina e chave primária.

*Nota de Escopo:* Conforme as regras do projeto, NÃO estão incluídas tarefas de criação de endpoints REST (APIs GET/POST/PATCH/DELETE), telas de frontend no Streamlit ou testes automatizados, pois não foram explicitamente solicitados.

## Capabilities

### New Capabilities
- `academic-tasks`: Especificação do esquema de dados para a tabela `academic_tasks` no Xano, estabelecendo campos, tipos e relacionamentos com as tabelas `user` e `subjects`.

### Modified Capabilities
<!-- None -->

## Impact

- **Backend (Xano / XanoScript)**:
  - Adiciona o arquivo de definição de tabela `table/academic_tasks.xs`.
- **APIs e Frontend**: Nenhum impacto direto nesta etapa (fora de escopo).

