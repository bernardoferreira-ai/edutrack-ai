# Proposal: Geração de Relatório PDF de Desempenho do Aluno

## Why

Para que os estudantes e orientadores do EduTrack AI possam acompanhar formalmente a evolução acadêmica, é essencial disponibilizar um relatório consolidado em formato PDF contendo os indicadores de desempenho do aluno (disciplinas matriculadas, tarefas concluídas/pendentes e taxa de conclusão). Além da geração autônoma do documento via script Python, é necessário fornecer um endpoint seguro no backend Xano que permita ao aluno autenticado realizar o download desse relatório diretamente.

## What Changes

Em estrita observância à **Regra nº 1 de Escopo** do `AGENTS.md`, esta proposta abrange **SOMENTE** o que foi explicitamente solicitado:

1. **Script Python para Geração do Relatório PDF (`scripts/generate_student_report.py`):**
   - Coleta os dados acadêmicos do aluno (disciplinas e tarefas) consumindo os endpoints existentes ou dados de desempenho.
   - Gera um arquivo PDF formatado contendo:
     - Identificação do aluno e data de emissão.
     - Resumo geral de desempenho (total de tarefas, tarefas concluídas, tarefas pendentes, percentual global de progresso).
     - Detalhamento por disciplina com status das tarefas associadas.
   - Suporte a execução via linha de comando (CLI) com parâmetros de saída configuráveis (`--output-path`, `--student-id` / token).

2. **Endpoint no Xano para Download do Relatório (`api/reports/`):**
   - Criação do grupo de API `Reports` (`api/reports/reports.xs`).
   - Endpoint `GET /student_report` (ou `GET /reports/performance_pdf`) com autenticação do aluno (`auth = "user"`).
   - Valida a identidade do aluno autenticado via `$auth.id` e disponibiliza o download/conteúdo do relatório de desempenho do próprio usuário.

## Capabilities

### New Capabilities
- `pdf-report`: Geração programática de relatório de desempenho acadêmico em formato PDF e endpoint seguro no Xano para download do documento pelo aluno autenticado.

## Impact

- **Scripts (`scripts/`):**
  - Adição de `scripts/generate_student_report.py`.
- **Backend (Xano / XanoScript):**
  - Criação de `api/reports/reports.xs` (grupo de APIs).
  - Criação de `api/reports/student_report_GET.xs` (endpoint autenticado de download do relatório).
- **Dependências (`requirements.txt`):**
  - Adição da biblioteca `reportlab` para renderização de PDF via Python.

