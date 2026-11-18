# edicao-notas

## Why
A tela de Notas (`4_📊_Notas.py`) exibia as avaliações apenas em modo leitura. O aluno não conseguia corrigir ou simular notas sem acesso direto ao código. A falta de uma forma de edição tornava o boletim estático e pouco útil para o planejamento acadêmico.

## What Changes
- Notas de avaliações movidas de um dicionário fixo para `st.session_state["grades_data"]`, inicializado com `copy.deepcopy` na primeira carga.
- Botão **✏️ Editar Notas** adicionado a cada card de disciplina — alterna abertura/fechamento do formulário inline.
- Formulário (`st.form`) com `number_input` (0.0–10.0, passo 0.1) para cada avaliação, exibindo nome, tipo, peso e data.
- Ação **💾 Salvar Alterações**: persiste as novas notas no `session_state` e relança o app via `st.rerun()`, recalculando automaticamente média e badge de status.
- Ação **🔄 Restaurar Padrão**: reverte as notas da disciplina para o fallback original (`_DEFAULT_GRADES`).
- Disciplinas vindas do backend sem dados em `grades_data` recebem fallback automaticamente.

## Impact
- `pages/4_📊_Notas.py`: modificado (refatoração do dicionário de notas + adição da UI de edição). Nenhuma outra página alterada.
- Comportamento visual e de cálculo de médias permanece idêntico — apenas adicionado o bloco de edição abaixo de cada card.
