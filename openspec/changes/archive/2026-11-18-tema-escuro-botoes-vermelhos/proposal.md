# Change Proposal: tema-escuro-botoes-vermelhos

## Why
O usuário solicitou uma mudança na identidade visual do aplicativo: aplicar um fundo preto puxado para o cinza escuro em todo o site, acompanhado de botões com coloração vermelha para ações de destaque e exclusão, mantendo todas as opções, dados e funcionalidades intactos.

## What Changes
- Configurar o tema global escuro em `.streamlit/config.toml` (fundo escuro puxado para cinza `#0f172a` / `#121214`, texto claro `#f8fafc`, acentos em vermelho).
- Atualizar os estilos CSS de fundo e cartões em `app.py`, `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py` e `pages/3_👤_Perfil.py` para usar a paleta escura (fundo cinza escuro profundo, cartões em cinza grafite elegante `#1e293b` / `#18181b` e textos em alto contraste).
- Aplicar a coloração vermelha (`#ef4444` / `#dc2626`) em botões de ação e destaque (ex.: botões de exclusão de disciplinas e tarefas, logout e ações prioritárias), garantindo visibilidade e apelo visual moderno.
- Preservar rigorosamente todas as regras de negócio, formulários, chaves de sessão, conexões com o Xano e fluxos da aplicação.

## Impact
- **Interface e Estilo:** Novo visual com tema escuro (preto/cinza escuro) e detalhes em vermelho.
- **Backend:** Nenhuma alteração nas APIs, tabelas ou serviços de backend.
- **Escopo:** Estritamente limitado à paleta de cores de fundo, cartões e botões.
