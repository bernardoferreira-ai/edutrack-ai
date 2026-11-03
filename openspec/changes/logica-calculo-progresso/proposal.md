# Proposal: Progress Calculation Script for Subjects

## Why

Alunos precisam acompanhar de forma clara e precisa a evolução de suas obrigações acadêmicas em cada disciplina. Para viabilizar métricas de progresso e futuros relatórios de desempenho no EduTrack AI, é necessário um script Python dedicado que consulte as tarefas vinculadas a uma determinada disciplina via endpoints CRUD, calcule a porcentagem de conclusão (tarefas concluídas em relação ao total) e retorne o resultado em formato JSON estruturado.

## What Changes

Em conformidade estrita com a **Regra nº 1 de Escopo** do `AGENTS.md`, esta proposta abrange **SOMENTE** o que foi explicitamente solicitado pelo usuário:

- Criação do script Python `scripts/calculate_progress.py`.
- Implementação de função para consumir o endpoint CRUD `GET /academic_tasks` filtrando por `subject_id`.
- Implementação da lógica matemática de cálculo percentual: `(concluídas / total) * 100`, tratando o caso de divisão por zero (retornando `0.0` quando não houver tarefas cadastradas).
- Formatação e retorno dos dados em formato JSON contendo `subject_id`, `total_tasks`, `completed_tasks`, `pending_tasks` e `progress_percentage`.
- Suporte para execução direta via terminal (CLI) recebendo o identificador da disciplina.

*Nota de Escopo:* Não estão incluídas alterações em telas do Streamlit, novos endpoints ou tabelas no Xano, nem suítes de testes extras, visto que não foram solicitadas.

## Capabilities

### New Capabilities
- `progress-calculation`: Função e script utilitário para calcular a taxa de conclusão de tarefas de uma disciplina a partir dos endpoints CRUD com saída em JSON.

### Modified Capabilities
<!-- None -->

## Impact

- **Scripts Utilitários**: Criação do arquivo `scripts/calculate_progress.py`.
- **Backend / Frontend**: Nenhum impacto direto ou alteração em código existente.

