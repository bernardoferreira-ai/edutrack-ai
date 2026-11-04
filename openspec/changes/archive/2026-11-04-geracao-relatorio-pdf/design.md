# Design: Geração de Relatório PDF de Desempenho e Endpoint de Download

## Architecture Overview

O fluxo de geração e disponibilização do relatório de desempenho do aluno estrutura-se em dois componentes integrados:

1. **Camada de Processamento e Renderização (Python):**
   - O script `scripts/generate_student_report.py` obtém os dados do aluno (disciplinas cadastradas e tarefas atribuídas com seus respectivos status).
   - Calcula métricas consolidadas: taxa geral de conclusão, total de disciplinas, distribuição de tarefas concluídas vs. pendentes.
   - Renderiza o documento PDF utilizando a biblioteca `reportlab` (SimpleDocTemplate, Paragraph, Table, Spacer, colors) gerando um layout limpo e profissional.

2. **Camada de Disponibilização (Xano Backend):**
   - Grupo de APIs `Reports` (`api/reports/reports.xs`).
   - Endpoint `GET /student_report` (`api/reports/student_report_GET.xs`) com proteção `auth = "user"`.
   - Consulta os dados pertencentes ao usuário autenticado (`user_id == $auth.id`), compila as métricas consolidadas e entrega o relatório/arquivo para download.

```mermaid
flowchart TD
    subgraph Client["Cliente / Estudante"]
        Req["Solicita Relatório (CLI / HTTP)"]
    end

    subgraph Backend["Xano Backend (api/reports/)"]
        AuthCheck["Valida JWT ($auth.id)"]
        FetchData["Consulta subjects & academic_tasks do usuário"]
        FormatPayload["Prepara Relatório / Arquivo"]
    end

    subgraph Script["Python Script (scripts/generate_student_report.py)"]
        Collect["Coleta Métricas Acadêmicas"]
        Compute["Calcula Progresso & Totais"]
        RenderPDF["Renderiza PDF via ReportLab"]
        SavePDF["Salva arquivo .pdf"]
    end

    Req -->|GET /student_report (Bearer JWT)| AuthCheck
    AuthCheck --> FetchData
    FetchData --> FormatPayload
    FormatPayload -->|Retorna Download/Dados| Req

    Req -->|Executa CLI python scripts/generate_student_report.py| Collect
    Collect --> Compute
    Compute --> RenderPDF
    RenderPDF --> SavePDF
```

## Detalhamento dos Componentes

### 1. Script Python (`scripts/generate_student_report.py`)
- **Entrada:**
  - `--student-name`: Nome do aluno (padrão: "Aluno EduTrack" ou extraído da sessão/API).
  - `--output`: Caminho do arquivo PDF gerado (padrão: `relatorio_desempenho.pdf`).
  - `--auth-token`: Token JWT para consulta dos dados reais no Xano (opcional; se ausente, utiliza dados consolidados do ambiente local).
  - `--api-url`: URL base da API do Xano (opcional; usa `.env`).
- **Seções do Relatório PDF:**
  - **Cabeçalho:** Logotipo/Título "EduTrack AI - Relatório de Desempenho Acadêmico", data e horário de emissão.
  - **Dados do Aluno:** Nome do estudante e identificação.
  - **Quadro Resumo de Indicadores:** Total de disciplinas, total de tarefas, tarefas concluídas, tarefas pendentes, percentual de conclusão global.
  - **Tabela de Disciplinas e Tarefas:** Listagem estruturada de disciplinas com a quantidade de tarefas concluídas e percentual individual.
- **Biblioteca:** `reportlab` para composição de páginas, tabelas e estilos tipográficos.

### 2. Endpoint Xano (`api/reports/`)
- **Arquivo `api/reports/reports.xs`:**
  - Define o `api_group "Reports"`.
- **Arquivo `api/reports/student_report_GET.xs`:**
  - `query "student_report" verb=GET` com `auth = "user"`.
  - Filtra disciplinas onde `user_id == $auth.id`.
  - Filtra tarefas onde `user_id == $auth.id`.
  - Agrega métricas e retorna a estrutura consolidada para download do relatório.

