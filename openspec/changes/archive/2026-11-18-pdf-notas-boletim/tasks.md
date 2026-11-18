# Tasks — pdf-notas-boletim

## Backend / Script

- [x] Adicionar `DEFAULT_GRADES_BY_SUBJECT` com notas das 3 disciplinas em `generate_student_report.py`
- [x] Adicionar constante `APPROVAL_THRESHOLD = 7.0`
- [x] Expandir `PDFCanvas` para suporte a múltiplas páginas (`add_page()`)
- [x] Implementar `calculate_grades_metrics(subjects)` com média ponderada e status
- [x] Renderizar segunda página "Boletim de Notas" com badges coloridos e tabela de avaliações
- [x] Atualizar `generate_report_bytes()` para passar `grades_data`
- [x] Atualizar `generate_student_report_pdf()` para passar `grades_data`

## Verificação

- [x] Verificar sintaxe de todos os arquivos Python (`py_compile`)
- [x] Rodar testes unitários (`tests/test_task_service.py`) — 4/4 passando
- [x] Gerar PDF de teste e confirmar 2 páginas (`/Count 2` no xref)
