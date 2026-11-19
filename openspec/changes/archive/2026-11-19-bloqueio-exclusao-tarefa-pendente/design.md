# Design: bloqueio-exclusao-tarefa-pendente

## Overview
A validação será feita no diálogo existente de exclusão antes da apresentação da confirmação normal.

## Arquitetura da Solução

### 1. Status da Tarefa
O diálogo `confirmar_exclusao_tarefa` recebe `task_status` e verifica se o status normalizado é `pending`.

### 2. Tarefa Pendente
Quando o status é pendente, o diálogo exibe:

- Aviso indicando que a tarefa está pendente.
- Informação solicitando que a tarefa seja concluída primeiro.
- Botão `Entendi` para fechar o diálogo.
- Nenhum botão de confirmação de exclusão.

### 3. Tarefa Concluída
Tarefas com status `completed` continuam usando a confirmação atual com as opções `Sim, excluir` e `Cancelar`.

### 4. Acionamento
Os cards individuais e o gerenciador por seleção passam o status da tarefa selecionada ao diálogo.
