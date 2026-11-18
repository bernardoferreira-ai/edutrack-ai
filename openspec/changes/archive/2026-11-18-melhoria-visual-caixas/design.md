# Design: melhoria-visual-caixas

## Overview
Aprimorar o design visual das caixas (`st.expander`), painéis de filtro e cartões de conteúdo nas páginas `pages/1_📚_Disciplinas.py` e `pages/2_📝_Tarefas.py`, aplicando CSS personalizado moderno para elevação, sombras, cantos arredondados, badges informativos e espaçamento equilibrado.

## Solução Visual

### 1. Caixas Expansoras (`st.expander`)
- **Estilização Global de Expansores:**
  - Borda sutil com gradiente/translúcida (`1px solid rgba(99, 102, 241, 0.16)`).
  - Fundo branco com leve elevação (`box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05)`).
  - Cantos arredondados elegantes (`border-radius: 16px`).
  - Cabeçalho do expander com tipografia nítida e transição suave ao expandir.

### 2. Caixas de Tarefas em `pages/2_📝_Tarefas.py`
- **Painel de Busca e Filtro:** Cartão superior refinado com fundo branco, cantos arredondados de `18px`, inputs alinhados e espaçamento harmonioso.
- **Card Interno da Tarefa:**
  - Apresentar "Disciplina" e "Prazo" com pequenos badges informativos e ícones elegantes (`📚 Disciplina`, `📅 Prazo`).
  - Distribuir a ação de marcar como concluída e o botão de exclusão de forma espaçada e equilibrada.
- **Expansores de Gerenciamento e Nova Tarefa:** Estilizados com cartões internos claros e botões destacados.

### 3. Caixas de Disciplinas em `pages/1_📚_Disciplinas.py`
- **Abas e Cartão de Conteúdo:** Refinamento dos contêineres de abas (`Listar` e `Nova Disciplina`) com cantos arredondados, bordas sutis e fundo com leve transparência.
- **Expander de Gerenciamento (Editar / Excluir):** Alinhamento das colunas de edição e exclusão com divisórias limpas e botões visualmente integrados.

### 4. Preservação de Integridade
- Todas as opções, inputs, botões, labels, diálogos de confirmação de exclusão (`@st.dialog`) e funções permanecem idênticos.
