# Proposal: feature-notas-atividades

## Why

Permitir que o professor lance notas para os alunos em atividades específicas no EduTrack AI. Atualmente, o sistema não possui uma estrutura de dados e nem um endpoint dedicado para o registro e atribuição de notas em atividades acadêmicas.

## What Changes

Em estrita conformidade com a **Regra nº 1 de Escopo** do `AGENTS.md`, este plano contempla **SOMENTE** o que foi explicitamente solicitado pelo usuário:

- Criação da tabela `activity_grades` no Xano (via XanoScript) para armazenar as notas atribuídas aos alunos nas atividades.
- Criação do endpoint de API `POST /activity_grades` para permitir que o professor autenticado lance notas.

*Nota de Escopo:* Conforme as regras do projeto, NÃO estão incluídas tarefas de listagem (GET), consulta de notas, interfaces frontend ou testes, pois não foram explicitamente solicitadas.

## Capabilities

### New Capabilities
- `activity-grades`: Estrutura de dados e endpoint POST para registro e atribuição de notas de atividades por professores.

### Modified Capabilities
<!-- None -->

## Impact

- **Backend (Xano / XanoScript)**:
  - Adiciona o arquivo de definição de tabela `tables/activity_grades.xs`.
  - Adiciona o arquivo de endpoint `apis/activity_grades/activity_grades_POST.xs`.
- **Frontend / Outros**: Nenhum impacto direto.

