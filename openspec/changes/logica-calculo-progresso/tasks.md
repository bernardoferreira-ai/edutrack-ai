## 1. Progress Calculation Script

- [x] 1.1 Criar `scripts/calculate_progress.py` com a função de consulta de tarefas via endpoint `GET /academic_tasks` filtrando por `subject_id` e enviando token de autenticação.
- [x] 1.2 Implementar a lógica de cálculo de progresso percentual (`concluídas / total * 100`) com proteção contra divisão por zero e formatação do resultado em JSON.
- [x] 1.3 Implementar a interface de linha de comando (CLI) em `scripts/calculate_progress.py` para receber argumentos (`--subject-id`) e imprimir o JSON formatado.
