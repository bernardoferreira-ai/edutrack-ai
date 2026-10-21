# Proposal: User Registration and Login in Profile Page

## Why

Atualmente, o aplicativo Streamlit do EduTrack AI possui a página `pages/3_👤_Perfil.py` vazia e não fornece uma interface para que os usuários realizem cadastro (signup) ou autenticação (login) na plataforma. Para que os alunos e professores possam acessar seus recursos acadêmicos de forma personalizada e segura, é necessário implementar o fluxo de autenticação e exibição do perfil do usuário utilizando os endpoints existentes do Xano (`auth/login`, `auth/signup`, `auth/me`).

## What Changes

Em estrita conformidade com a **Regra nº 1 de Escopo** do `AGENTS.md`, este plano contempla **SOMENTE** o que foi explicitamente solicitado pelo usuário:
- Implementação da interface e lógica de autenticação em `pages/3_👤_Perfil.py`:
  - Formulário de Login conectando ao endpoint `POST auth/login`.
  - Formulário de Cadastro (Signup) conectando ao endpoint `POST auth/signup` para registrar novos usuários na tabela `user`.
  - Exibição dos dados do usuário logado através do endpoint `GET auth/me`.
  - Gerenciamento de sessão autenticada utilizando `st.session_state` (`auth_token`, `user_profile`).
  - Opção de Logout para limpar a sessão ativa.
- Integração de serviço/cliente HTTP para comunicação com a API de autenticação do Xano.

*Nota de Escopo:* Não serão criadas novas tabelas no backend nem novos endpoints, aproveitando os endpoints já existentes (`auth/login`, `auth/signup`, `auth/me`) e a tabela `user`.

## Capabilities

### New Capabilities
- `user-auth`: Fluxo de cadastro, login e visualização de perfil no Streamlit (`pages/3_👤_Perfil.py`), integrado aos endpoints `auth/login`, `auth/signup` e `auth/me` do Xano.

### Modified Capabilities
<!-- None -->

## Impact

- **Frontend (Streamlit)**:
  - Implementa a página `pages/3_👤_Perfil.py`.
  - Adiciona serviço ou cliente de autenticação para chamada dos endpoints.
- **Backend (Xano)**:
  - Nenhum novo endpoint ou tabela precisa ser criado; consome as rotas já existentes no grupo `Authentication`.

