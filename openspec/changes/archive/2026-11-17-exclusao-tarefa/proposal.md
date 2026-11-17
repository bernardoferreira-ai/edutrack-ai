# Change Proposal: exclusao-tarefa

## Why
Permitir que os estudantes possam excluir tarefas acadêmicas diretamente na aplicação Streamlit (`pages/2_📝_Tarefas.py`), tanto individualmente em cada card de tarefa quanto através de um seletor de gerenciamento dedicado, garantindo a sincronização com o endpoint de exclusão do Xano e persistência consistente em modo local.

## What Changes
- Implementação da função `excluir_tarefa(task_id)` em `pages/2_📝_Tarefas.py`.
- Integração de botão `🗑️ Excluir Tarefa` nos cards individuais de tarefas e suporte a exclusão no card inicial de mockup.
- Adição de seção expansível de gerenciamento (`⚙️ Gerenciar Tarefas (Excluir)`) para exclusão de tarefas selecionadas via dropdown.
- Persistência das alterações de tarefas em memória via `st.session_state` em `services/task_service.py` para prevenir restauração indesejada no rerun do Streamlit.

## Impact
- **Backend:** Utiliza o endpoint existente `DELETE /academic_tasks/{id}` com autorização JWT.
- **Frontend:** Preserva a identidade visual e o layout existente das tarefas, adicionando opções de exclusão intuitivas e feedback imediato via `st.rerun()`.
