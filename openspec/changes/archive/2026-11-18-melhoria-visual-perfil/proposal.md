# Change Proposal: melhoria-visual-perfil

## Why
A tela de perfil (`pages/3_👤_Perfil.py`) possui uma interface básica e heterogênea: a visualização autenticada contém cartões simples com formatação textual crua e a tela de login/cadastro utiliza componentes nativos padrão do Streamlit sem estilização temática ou cartões de destaque. Uma melhoria visual moderna, limpa e harmoniosa eleva a experiência do usuário, mantendo exatamente as mesmas opções, formulários, botões e funcionalidades originais.

## What Changes
- Refinar visualmente a página `pages/3_👤_Perfil.py` aplicando CSS customizado consistente (paleta moderna com tons suaves, gradientes sutis, cantos arredondados, sombras elegantes e tipografia refinada).
- Aprimorar o estado não autenticado (Login e Cadastro): adicionar cabeçalho visual convidativo, cartão de boas-vindas com ícone e abas estilizadas para os formulários de autenticação.
- Aprimorar o estado autenticado: estilizar o resumo do usuário com card de identificação (avatar/ícone, badges de status e função, organização métrica dos dados da conta), caixa de download do Relatório de Desempenho e botão de logout integrado.
- Preservar rigorosamente todas as opções, inputs (`name`, `email`, `password`), botões, integrações com `AuthService` e geração de PDF.

## Impact
- **Interface e Experiência:** Visual moderno, alinhado e agradável sem alterar o fluxo ou as opções do usuário.
- **Backend e Lógica:** Nenhuma alteração de APIs, serviços ou lógica de backend (`AuthService` permanece idêntico).
- **Escopo:** Estritamente limitado a melhorias visuais de CSS e layout na página de Perfil.
