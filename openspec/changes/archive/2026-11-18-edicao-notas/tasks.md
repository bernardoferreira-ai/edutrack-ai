# Tasks — edicao-notas

## Frontend — pages/4_📊_Notas.py

- [x] Mover `DEFAULT_GRADES_BY_SUBJECT` para `st.session_state["grades_data"]` com `copy.deepcopy` na primeira carga
- [x] Garantir fallback automático para disciplinas do backend sem dados em `grades_data`
- [x] Adicionar botão **✏️ Editar Notas** / **✖ Cancelar Edição** com estado em `st.session_state[f"editing_{s_name}"]`
- [x] Implementar `st.form` com `number_input` (0.0–10.0, step 0.1) para cada avaliação
- [x] Implementar ação **💾 Salvar Alterações**: persistir em `session_state` + `st.rerun()`
- [x] Implementar ação **🔄 Restaurar Padrão**: reverter para `_DEFAULT_GRADES` + `st.rerun()`

## Verificação

- [x] Verificar sintaxe de todos os arquivos Python (`py_compile`) — OK
