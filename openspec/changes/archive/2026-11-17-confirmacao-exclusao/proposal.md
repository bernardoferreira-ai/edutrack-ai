# Change Proposal: confirmacao-exclusao

## Why
Atualmente, ao clicar no botão de exclusão de uma disciplina ou tarefa, a exclusão é efetuada imediatamente, aumentando o risco de perdas acidentais de dados acadêmicos cadastrados pelos alunos. A implementação de uma etapa de confirmação prévia ("Você realmente deseja excluir?") previne exclusões involuntárias e aprimora a experiência e segurança do usuário.

## What Changes
- Implementar função de confirmação de exclusão na página de Disciplinas (`pages/1_📚_Disciplinas.py`).
- Implementar função de confirmação de exclusão na página de Tarefas (`pages/2_📝_Tarefas.py`).
- Exibir mensagem/modal de confirmação perguntando se o usuário realmente deseja excluir o item específico, com botões para confirmar ou cancelar a operação.
- Executar a exclusão definitiva apenas após o consentimento explícito do usuário.

## Impact
- **Segurança de Dados:** Elimina exclusões acidentais por cliques involuntários.
- **Backend:** Mantém o uso dos endpoints existentes `DELETE /subjects/{id}` e `DELETE /academic_tasks/{academic_tasks_id}` sem alterações na API do Xano.
- **Interface e Layout:** Preserva a integridade visual das páginas e a organização dos elementos existentes.
