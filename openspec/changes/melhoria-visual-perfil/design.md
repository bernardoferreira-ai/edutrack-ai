# Design: melhoria-visual-perfil

## Overview
Aprimorar o design visual da página `pages/3_👤_Perfil.py` por meio de injeção de CSS customizado via `st.markdown`, cartões informativos bem espaçados, badges de status e hierarquia visual clara, cobrindo tanto o estado autenticado quanto os formulários de login/cadastro, sem alterar nenhuma funcionalidade, campo ou fluxo existente.

## Solução Visual

### 1. Paleta de Cores e Estilo Geral
- **Fundo da página:** Gradiente suave de fundo (`#f8fafc` a `#eef2ff`), garantindo leitura confortável e sensação moderna.
- **Cartões e Contêineres:** Bordas arredondadas (`18px` a `24px`), sombras suaves (`rgba(15, 23, 42, 0.05)`), bordas translúcidas sutis (`rgba(99, 102, 241, 0.15)`).
- **Tipografia e Hierarquia:** Títulos em negrito com cores contrastantes (`#0f172a`), legendas e metadados em cinza suave (`#64748b`), badges arredondados (`pill badges`) para status e funções.

### 2. Estado Não Autenticado (Login / Cadastro)
- **Cabeçalho:** Banner de boas-vindas com título "Acesso à Plataforma", ícone de boas-vindas e subtítulo instrutivo.
- **Card dos Formulários:** Envolver as abas de Login e Cadastro em um card com fundo branco e elevação visual, mantendo os mesmos campos (`email`, `password`, `name`) e botões de submissão ("Entrar" e "Cadastrar").

### 3. Estado Autenticado (Meu Perfil)
- **Header do Perfil:** Card de destaque com avatar comemorativo/acadêmico, título "Meu Perfil", e badge "Conta Ativa".
- **Cartão de Dados do Usuário:** Apresentação em grade com métricas estilizadas (Nome, E-mail, Função/Role com badge colorido e data de cadastro/Membro desde).
- **Seção Relatório de Desempenho:** Card dedicado para download do relatório acadêmico em PDF com botão `st.download_button` destacado e ícones limpos.
- **Ações da Conta:** Botão de logout com espaçamento e estilo claro de encerramento de sessão.

### 4. Preservação de Opções e Lógica
- Todos os `key` de componentes, nomes de campos, chamadas a `auth_service.login`, `auth_service.signup`, `auth_service.get_me` e `generate_report_bytes` permanecem exatamente iguais.
