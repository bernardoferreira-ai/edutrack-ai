# Design: botoes-auth-vermelho

## Overview
Ajustar a propriedade de cor de fundo e sombra dos botões do formulário de autenticação dentro de `.auth-card-container [data-testid="stForm"] button` em `pages/3_👤_Perfil.py` para utilizar o gradiente vermelho padrão do aplicativo.

## Solução Visual
- **Fundo do Botão:** `linear-gradient(135deg, #b91c1c 0%, #dc2626 50%, #ef4444 100%) !important`
- **Texto:** Branco com peso 700 (`color: #ffffff !important; font-weight: 700;`)
- **Sombra:** `box-shadow: 0 6px 20px -2px rgba(220, 38, 38, 0.45) !important`
- **Hover:** `linear-gradient(135deg, #991b1b 0%, #b91c1c 100%) !important` com sombra elevada.
