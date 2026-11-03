## 1. Services Integration Layer

- [x] 1.1 Atualizar `services/subject_service.py` para aceitar e enviar o token de autenticação JWT (`Bearer`) em todas as operações CRUD (`list_subjects`, `create_subject`, `update_subject`, `delete_subject`), conectando aos endpoints `/subjects` do Xano.
- [x] 1.2 Criar `services/task_service.py` implementando as operações CRUD completas (`list_tasks`, `create_task`, `update_task`, `delete_task`) para consumir os endpoints `/academic_tasks` do Xano utilizando o token JWT (`Bearer`).

## 2. Streamlit Pages Synchronization

- [x] 2.1 Integrar `pages/1_📚_Disciplinas.py` com `SubjectService`, obtendo o token JWT de `st.session_state`, carregando as disciplinas cadastradas na aba de listagem (`st.dataframe`), cadastrando novas no formulário existente e permitindo atualizar e excluir registros, sem alterar o layout ou design visual.
- [x] 2.2 Integrar `pages/2_📝_Tarefas.py` com `TaskService`, obtendo o token JWT de `st.session_state`, carregando e filtrando as tarefas por busca e status, atualizando o status de conclusão via checkbox nos expanders e permitindo cadastrar e excluir registros, sem alterar o layout ou design visual.

