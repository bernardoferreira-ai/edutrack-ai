# Change Proposal: bloqueio-exclusao-tarefa-pendente

## Why
Uma tarefa pendente representa uma atividade que ainda não foi concluída. Permitir sua exclusão diretamente pode remover um item acadêmico antes que o aluno registre sua conclusão. É necessário impedir essa ação e orientar o usuário.

## What Changes
- Validar o status da tarefa antes de confirmar sua exclusão.
- Exibir uma mensagem informando que a tarefa está pendente.
- Orientar o usuário a concluir a tarefa antes de excluí-la.
- Bloquear o botão de confirmação de exclusão para tarefas pendentes.
- Aplicar a validação aos cards individuais e ao gerenciador de seleção.

## Impact
- **Interface:** Atualização do diálogo de exclusão em `pages/2_📝_Tarefas.py`.
- **Backend:** Nenhuma alteração nos endpoints ou tabelas do Xano.
- **Dados:** Tarefas pendentes não podem ser excluídas pela interface até serem concluídas.
