# Design: exclusao-tarefa

## Arquitetura da Exclusão de Tarefas

### 1. Camada de Serviço (`services/task_service.py`)
- O método `delete_task(task_id, token)` despacha a requisição HTTP `DELETE /academic_tasks/{task_id}` para o Xano.
- Em ambiente offline ou local, a lista de tarefas padrão é armazenada em `st.session_state["_task_fallback_store"]`, permitindo que exclusões locais persistam durante o ciclo de vida da sessão.

### 2. Interface do Usuário (`pages/2_📝_Tarefas.py`)
- A função utilitária `excluir_tarefa(task_id)` centraliza a chamada ao serviço.
- Botões de exclusão são expostos em dois pontos:
  1. Card individual da tarefa (`📌 ...`).
  2. Expander de gerenciamento (`⚙️ Gerenciar Tarefas (Excluir)`) com selectbox.
