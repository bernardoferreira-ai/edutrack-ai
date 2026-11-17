# Design: confirmacao-exclusao

## Overview
Implementar caixas/modais de confirmação de exclusão em `pages/1_📚_Disciplinas.py` e `pages/2_📝_Tarefas.py` utilizando `@st.dialog` (nativo do Streamlit 1.64.0) com fallback transparente via `st.session_state`.

## Arquitetura da Solução

### 1. Padrão de Diálogo de Confirmação (`@st.dialog`)
Streamlit 1.64.0 suporta o decorador `@st.dialog("Confirmar Exclusão")`, que abre um modal limpo sobre a página:

- **Disciplina (`confirmar_exclusao_disciplina`):**
  - Exibe: `Você realmente deseja excluir a disciplina "{nome}"?`
  - Botão de confirmação: `Sim, excluir` (executa `subject_service.delete_subject(subject_id, token)`).
  - Botão de cancelamento: `Cancelar` (fecha o diálogo via `st.rerun()`).

- **Tarefa (`confirmar_exclusao_tarefa`):**
  - Exibe: `Você realmente deseja excluir a tarefa "{titulo}"?`
  - Botão de confirmação: `Sim, excluir` (executa `task_service.delete_task(task_id, token)`).
  - Botão de cancelamento: `Cancelar` (fecha o diálogo via `st.rerun()`).

### 2. Acionamento nas Telas
- **Em Disciplinas:** O botão `🗑️ Excluir` da seção `⚙️ Gerenciar Disciplina (Editar / Excluir)` abre o diálogo de confirmação.
- **Em Tarefas:** Tanto o botão `🗑️ Excluir Tarefa` nos cards individuais quanto o botão `🗑️ Excluir Tarefa Selecionada` na seção de gerenciamento acionam o diálogo de confirmação.
