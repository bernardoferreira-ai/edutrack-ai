# Design: tema-escuro-botoes-vermelhos

## Overview
Implementar uma paleta de cores moderna em modo escuro em todo o EduTrack AI, com fundo principal em preto puxado para cinza escuro (`#0b0f19` a `#0f172a`), contêineres e cartões em cinza grafite (`#1e293b` / `#181f2e`), tipografia em tons claros de alta legibilidade (`#f8fafc` / `#e2e8f0`) e botões destacados em vermelho vibrante (`#ef4444` / `#dc2626`).

## Solução Visual

### 1. Configuração Global de Tema (`.streamlit/config.toml`)
- `base = "dark"`
- `backgroundColor = "#0b0f19"`
- `secondaryBackgroundColor = "#161e2e"`
- `textColor = "#f8fafc"`
- `primaryColor = "#ef4444"`

### 2. Estilização de Fundo e Cartões nas Páginas
- **Fundo Global:** `background: linear-gradient(180deg, #0b0f19 0%, #0f172a 50%, #0b0f19 100%)`.
- **Cabeçalhos de Página:** Gradientes escuros e sofisticados (ex.: `#0f172a` a `#1e1b4b` com bordas sutis e translúcidas).
- **Cartões de Conteúdo e Formulários:** Fundo grafite elegante (`#161e2e` / `#1e293b`), bordas sutis (`rgba(255, 255, 255, 0.08)`), textos brancos/claros e sombras profundas.
- **Expansores (`st.expander`):** Fundo `#161e2e`, borda `#334155`, texto claro.

### 3. Botões na Coloração Vermelha
- **Botões de Exclusão:**
  - `pages/1_📚_Disciplinas.py` (botão de excluir disciplina e botão de confirmação do modal).
  - `pages/2_📝_Tarefas.py` (botão de excluir tarefa nos cards e no gerenciamento).
- **Botão de Logout:**
  - `pages/3_👤_Perfil.py` (botão "🚪 Sair da Conta (Logout)" estilizado com destaque vermelho elegante).
- **Estilo dos Botões Vermelhos:**
  - `background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%)`
  - `color: #ffffff`
  - `box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35)`

### 4. Preservação de Lógica
- Todas as rotas, endpoints, tokens JWT, labels de formulários e opções são 100% mantidos.
