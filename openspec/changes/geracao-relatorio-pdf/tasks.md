## 1. Script de Geração de PDF

- [x] 1.1 Criar o script Python em `scripts/generate_student_report.py` para consolidar o desempenho do aluno (disciplinas e tarefas concluídas/pendentes) e gerar o arquivo PDF formatado.
- [x] 1.2 Implementar argumentos de linha de comando (CLI) em `scripts/generate_student_report.py` para definir caminho de saída (`--output`), nome do aluno e parâmetros de conexão.

## 2. Endpoint no Xano

- [x] 2.1 Criar o grupo de APIs `Reports` em `api/reports/reports.xs`.
- [x] 2.2 Criar o endpoint `GET /student_report` em `api/reports/student_report_GET.xs` com autenticação JWT (`auth = "user"`) para disponibilizar o relatório de desempenho do aluno autenticado.

