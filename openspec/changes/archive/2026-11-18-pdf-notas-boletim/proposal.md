# pdf-notas-boletim

## Why
O PDF gerado pelo botão "Baixar Relatório PDF" na página de Perfil não incluía nenhuma informação de notas, apesar da tela `4_📊_Notas.py` já exibir o boletim por disciplina. O aluno precisava ter as notas disponíveis também no relatório impresso/exportado.

## What Changes
- Adição de constante `DEFAULT_GRADES_BY_SUBJECT` em `scripts/generate_student_report.py` com notas das 3 disciplinas (igual ao fallback da tela de Notas).
- Adição de constante `APPROVAL_THRESHOLD = 7.0`.
- Expansão da classe `PDFCanvas` para suporte a múltiplas páginas via `add_page()`.
- Nova função `calculate_grades_metrics(subjects)` que calcula média ponderada e status de aprovação.
- Renderização de uma **segunda página** no PDF com o "Boletim de Notas por Disciplina": badge colorido por status (verde ≥ 7.0, laranja 5.0–6.9, vermelho < 5.0), tabela de avaliações individuais com notas coloridas.
- `generate_report_bytes()` e `generate_student_report_pdf()` atualizados para computar e passar `grades_data`.

## Impact
- `scripts/generate_student_report.py`: modificado (adição de ~120 linhas, nenhuma linha removida de comportamento existente).
- PDF gerado passa de 1 para 2 páginas.
- Nenhuma outra página ou serviço afetado.
