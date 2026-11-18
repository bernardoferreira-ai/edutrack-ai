# Design: pagina-notas

## Overview
Implementar a página `pages/4_📊_Notas.py` para visualização e cálculo do desempenho de avaliações por disciplina, com cartões temáticos escuros, badges coloridos de status de aprovação e métricas de pontuação restante.

## Arquitetura da Solução

### 1. Cabeçalho e Shell da Página
- Título principal: `📊 Boletim & Notas`.
- Subtítulo com instrução clara para acompanhamento das notas de trabalhos e provas.
- Badge temático no cabeçalho.

### 2. Cards por Disciplina
Para cada disciplina listada (obtida via `SubjectService` ou fallback local):
- **Topo do Card:**
  - Nome da Matéria (`📚 {subject_name}`) e Professor (`👨‍🏫 {teacher}`).
  - Badge de Status:
    - 🟢 `Aprovado (Média: X.X)` quando média $\ge 7.0$.
    - 🟡 `Em Atenção (Média: X.X)` quando $5.0 \le$ média $< 7.0$.
    - 🔴 `Crítico / Reprovado (Média: X.X)` quando média $< 5.0$.
- **Corpo do Card:**
  - Tabela ou grade de avaliações detalhadas (ex.: Trabalho 01, Prova Bimestral, Atividade Prática) com peso e nota individual.
  - Barra de progresso visual (`st.progress`) representando o percentual da nota alcançada frente à nota máxima (10.0).
- **Rodapé do Card (Meta de Aprovação):**
  - Métrica explicativa: Se a média for $< 7.0$, indica: *"Faltam X.X pontos para atingir a nota mínima de aprovação (7.0)"*.
  - Se $\ge 7.0$, indica: *"Meta de aprovação atingida com sucesso!"*.

### 3. Paleta Visual
- Integrado ao tema escuro global: fundo `#0b0f19` a `#0f172a`, cards em `#161e2e`, textos `#f8fafc`, bordas `#334155` e botões de ação na coloração vermelha.
