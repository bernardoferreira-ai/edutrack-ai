# Change Proposal: dashboard-home

## Why

O EduTrack AI precisa de uma página inicial que ofereça ao estudante uma visão rápida do semestre, consolidando indicadores, tarefas próximas, desempenho acadêmico e acesso às áreas principais da aplicação.

## What Changes

- Implementar o dashboard principal em `app.py`.
- Exibir saudação dinâmica por horário e resumo da data atual.
- Exibir indicadores de disciplinas ativas, tarefas concluídas, tarefas pendentes, média geral e progresso das tarefas.
- Exibir as próximas tarefas pendentes em ordem de vencimento.
- Exibir um resumo do boletim por disciplina.
- Exibir atalhos para Disciplinas, Tarefas, Perfil, Notas e Anotações.
- Preservar o comportamento existente de fallback local quando o usuário não estiver autenticado ou o Xano estiver indisponível.

## Capabilities

### New Capabilities

- `dashboard`: Visão acadêmica resumida e navegação rápida na página inicial.

### Modified Capabilities

<!-- Nenhuma especificação permanente existente será modificada. -->

## Impact

- **Interface:** Atualização da página inicial `app.py` com tema visual escuro e cartões informativos.
- **Dados:** Consumo dos serviços de disciplinas e tarefas e reutilização das notas disponíveis na sessão.
- **Backend:** Nenhuma nova API ou tabela Xano.
- **Escopo:** Somente a consolidação e apresentação das informações já disponíveis no EduTrack AI.
