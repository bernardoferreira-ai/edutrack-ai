# Design: melhoria-visual-caixa-auth

## Overview
Aprimorar exclusivamente o design visual, proporção e estilização da caixa onde é feito o login e o cadastro na página `pages/3_👤_Perfil.py`, aplicando CSS focado no contêiner `[data-testid="stForm"]` e centralização responsiva na tela.

## Solução Visual

### 1. Centralização da Caixa de Autenticação
- Em vez de deixar o formulário esticado por toda a largura da página (`layout="wide"`), centralizar a caixa com uma proporção equilibrada (ex.: coluna central com `[1, 2.2, 1]` ou contêiner delimitador `max-width: 520px`).
- Isso cria uma experiência de cartão de autenticação autêntica e focada.

### 2. Estilização do Contêiner do Formulário (`st.form`)
- **Fundo e Borda:** Fundo branco puro (`#ffffff`), borda suave (`1px solid #e2e8f0`), cantos arredondados (`18px`).
- **Sombra e Elevação:** `box-shadow: 0 12px 32px -4px rgba(15, 23, 42, 0.08)`.
- **Espaçamento Interno:** Padding confortável (`2rem 2.2rem`).

### 3. Botões e Campos de Entrada
- **Botões de Submissão:** Botões "Entrar" e "Cadastrar" destacados com gradiente (`linear-gradient(135deg, #4338ca 0%, #3b82f6 100%)`), cantos arredondados de `12px` e sombra elegante.
- **Campos de Texto:** Bordas com cantos arredondados de `10px` e destaque ao foco.

### 4. Preservação de Integridade
- Todas as opções, nomes de campos, placeholders, keys, chamadas a `auth_service.login`, `auth_service.signup`, `st.session_state` e redirecionamentos permanecem inalterados.
