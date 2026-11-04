# Proposal: Geração de Relatório PDF de Desempenho do Aluno

## Why

Para que os estudantes e orientadores do EduTrack AI possam acompanhar formalmente a evolução acadêmica, é essencial disponibilizar um relatório consolidado em formato PDF contendo os indicadores de desempenho do aluno (disciplinas matriculadas, tarefas concluídas/pendentes e taxa de conclusão). Além da geração do documento via script Python, é necessário fornecer um endpoint seguro no backend Xano que permita ao aluno autenticado realizar o download desse relatório de desempenho diretamente.

## What Changes

Em estrita observância à **Regra nº 1 de Escopo** do `AGENTS.md`, esta proposta abrange **SOMENTE** o que foi explicitamente solicitado pelo usuário:

1. **Script Python para Geração do Relatório PDF (`scripts/generate_student_report.py`):**
   - Coleta os dados acadêmicos do aluno (disciplinas e tarefas) consumindo os endpoints existentes do Xano via JWT ou dados locais.
   - Gera um arquivo PDF formatado contendo:
     - Identificação do aluno e data/hora de emissão.
     - Resumo geral de desempenho (total de disciplinas, tarefas, concluídas, pendentes e taxa de conclusão).
     - Detalhamento por disciplina com indicador de progresso.
     - Quadro resumido de tarefas e status.
   - Suporte a execução via linha de comando (CLI) com parâmetros configuráveis (`--output`, `--student-name`, `--auth-token`, `--api-url`, `--json-output`).

2. **Endpoint no Xano para Download do Relatório (`api/reports/`):**
   - Criação do grupo de APIs `Reports` (`api/reports/reports.xs`).
   - Endpoint `GET /student_report` em `api/reports/student_report_GET.xs` com autenticação do aluno (`auth = "user"`).
   - Valida a identidade do aluno autenticado via `$auth.id` e disponibiliza os dados/relatório de desempenho pertencentes exclusivamente ao usuário autenticado para download.

## Capabilities

### New Capabilities
- `pdf-report`: Geração programática de relatório de desempenho acadêmico em formato PDF e endpoint seguro no Xano para download do documento pelo aluno autenticado.

## Impact

- **Scripts (`scripts/`):**
  - Criação de `scripts/generate_student_report.py`.
- **Backend (Xano / XanoScript):**
  - Criação de `api/reports/reports.xs` (grupo de APIs).
  - Criação de `api/reports/student_report_GET.xs` (endpoint autenticado de download do relatório).

