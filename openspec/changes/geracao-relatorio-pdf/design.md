# Design: Geração de Relatório PDF de Desempenho e Endpoint de Download

## Architecture Overview

O fluxo de geração e disponibilização do relatório de desempenho do aluno estrutura-se em dois componentes integrados:

1. **Camada de Processamento e Renderização (Python):**
   - O script `scripts/generate_student_report.py` obtém os dados do aluno (disciplinas cadastradas e tarefas atribuídas com seus respectivos status).
   - Calcula métricas consolidadas: taxa geral de conclusão, total de disciplinas, distribuição de tarefas concluídas vs. pendentes.
   - Renderiza o documento PDF utilizando um gerador nativo PDF 1.4 em Python puro, com suporte a margens, cartões de KPIs, barras visuais de progresso e tabelas estruturadas com cores e fontes padrão (Helvetica).

2. **Camada de Disponibilização (Xano Backend):**
   - Grupo de APIs `Reports` (`api/reports/reports.xs`).
   - Endpoint `GET /student_report` (`api/reports/student_report_GET.xs`) com proteção `auth = "user"`.
   - Consulta os dados pertencentes exclusivamente ao usuário autenticado (`user_id == $auth.id`), compila as métricas consolidadas e entrega o relatório para download.

```mermaid
flowchart TD
    subgraph Client["Cliente / Estudante"]
        Req["Solicita Relatório (CLI / HTTP)"]
    end

    subgraph Backend["Xano Backend (api/reports/)"]
        AuthCheck["Valida JWT ($auth.id)"]
        FetchData["Consulta subjects & academic_tasks do usuário"]
        FormatPayload["Prepara Relatório / Download"]
    end

    subgraph Script["Python Script (scripts/generate_student_report.py)"]
        Collect["Coleta Métricas Acadêmicas"]
        Compute["Calcula Progresso & Totais"]
        RenderPDF["Renderiza PDF Nativo 1.4"]
        SavePDF["Grava arquivo .pdf"]
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
  - `--student-name`: Nome do aluno para exibição no cabeçalho do documento (padrão: "Aluno EduTrack").
  - `--output`: Caminho do arquivo PDF gerado (padrão: `relatorio_desempenho.pdf`).
  - `--auth-token`: Token JWT para consulta de dados reais na API do Xano (opcional; se ausente, utiliza dados de contingência).
  - `--api-url`: URL base da API do Xano (opcional; utiliza `.env`).
  - `--json-output`: Flag para emitir as métricas em formato JSON no stdout.
- **Seções do Relatório PDF:**
  - **Cabeçalho:** Banner superior azul (`#1F3B8A`) com o título "EduTrack AI - Gestão Acadêmica" e subtítulo oficial.
  - **Identificação:** Nome do estudante e data/hora de emissão.
  - **Cartões de Indicadores (KPIs):** Total de disciplinas, total de tarefas, concluídas, pendentes e percentual global.
  - **Barra de Progresso:** Indicador visual de taxa geral de conclusão com preenchimento em verde.
  - **Tabela de Disciplinas:** Nome da disciplina, professor, tarefas concluídas/total e percentual individual.
  - **Quadro de Tarefas Recentes:** Lista das atividades com prazo e status visual ("Concluída" ou "Pendente").
  - **Rodapé:** Assinatura do sistema e nota pedagógica.

### 2. Endpoint Xano (`api/reports/`)
- **Arquivo `api/reports/reports.xs`:**
  - Define o grupo de APIs `Reports`.
- **Arquivo `api/reports/student_report_GET.xs`:**
  - `query student_report verb=GET` com `auth = "user"`.
  - Filtra disciplinas onde `user_id == $auth.id`.
  - Filtra tarefas onde `user_id == $auth.id`.
  - Agrega métricas e retorna o relatório estruturado para download.

