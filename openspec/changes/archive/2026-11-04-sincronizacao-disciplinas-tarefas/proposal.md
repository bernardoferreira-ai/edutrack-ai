# Proposal: Sincronização das Páginas de Disciplinas e Tarefas com Xano

## Why

Atualmente, as páginas `pages/1_📚_Disciplinas.py` e `pages/2_📝_Tarefas.py` utilizam dados estáticos em memória (mockups simulados), impossibilitando a persistência real das disciplinas e tarefas no backend Xano. 
Com a implementação prévia dos endpoints CRUD das tabelas `subjects` e `academic_tasks` (Tarefa 12) e da autenticação de usuários (login/cadastro com JWT), é necessário conectar as duas telas aos serviços reais do Xano, permitindo que cada estudante visualize, cadastre, atualize e exclua apenas os seus próprios registros.

Para atender à exigência central desta mudança, a integração deve preservar integralmente a interface visual existente (layout, cores, fontes, títulos, abas, colunas, formulários e expanders), alterando pontualmente o código para alimentar os componentes com os dados retornados pelos endpoints REST do Xano.

## What Changes

Em estrita consonância com o pedido do usuário e a **Regra nº 1 de Escopo** do `AGENTS.md`:

1. **Serviços de Dados com Autenticação JWT (`services/`):**
   - Adequar `services/subject_service.py` para operar com o token JWT do usuário autenticado (`st.session_state["auth_token"]`), consumindo os endpoints `POST /subjects`, `GET /subjects`, `PATCH /subjects/{id}` e `DELETE /subjects/{id}`.
   - Criar `services/task_service.py` com métodos equivalentes para consumir os endpoints `POST /academic_tasks`, `GET /academic_tasks`, `PATCH /academic_tasks/{id}` e `DELETE /academic_tasks/{id}`, com suporte a filtros por `subject_id` e `status`.
   - Manter tratamento de exceções e modo fallback gracioso quando a API não estiver acessível ou sem autenticação.

2. **Integração de `pages/1_📚_Disciplinas.py`:**
   - Obter o token de autenticação da sessão do Streamlit.
   - Na aba `📋 Listar`: carregar dinamicamente as disciplinas do usuário autenticado via `GET /subjects` e exibi-las no `st.dataframe`, mantendo o mesmo layout visual, com suporte a ações de atualização e exclusão.
   - Na aba `➕ Nova Disciplina`: conectar o formulário existente (`form_disciplina` com `Nome da Disciplina`, `Nome do Professor`, `Dia da Aula` e botão `Salvar`) ao endpoint `POST /subjects`.
   - Preservar o título, abas, textos, componentes e organização original da página.

3. **Integração de `pages/2_📝_Tarefas.py`:**
   - Obter o token de autenticação da sessão do Streamlit.
   - Na barra superior: manter as duas colunas (`col1` e `col2`) com o campo `search` ("Buscar tarefa...") e o selectbox `filtro` ("Status": "Todas", "Pendente", "Concluída").
   - Na listagem: carregar dinamicamente as tarefas do usuário autenticado via `GET /academic_tasks`, filtrando por busca de texto e status.
   - Renderizar cada tarefa no formato original de `st.expander` ("📌 Tarefa: {title}"), exibindo **Disciplina:**, **Prazo:** e o checkbox interativo ("Marcar como Concluída") que dispara `PATCH /academic_tasks/{id}` para atualizar o status no Xano.
   - Disponibilizar cadastro e exclusão de tarefas sem descaracterizar a estrutura visual.

4. **Isolamento e Segurança Multi-tenant:**
   - Todas as requisições aos endpoints do Xano utilizarão o header `Authorization: Bearer <token>`, assegurando que cada usuário acesse e altere exclusivamente seus próprios dados.

## Capabilities

### New Capabilities
- `pages-sync`: Integração das telas do Streamlit (`pages/1_📚_Disciplinas.py` e `pages/2_📝_Tarefas.py`) com os endpoints CRUD do Xano via JWT, preservando a identidade visual original.

## Impact

- **Frontend (`pages/`):**
  - `pages/1_📚_Disciplinas.py`: consome `SubjectService` mantendo o layout intacto.
  - `pages/2_📝_Tarefas.py`: consome `TaskService` e `SubjectService` mantendo o layout intacto.
- **Serviços (`services/`):**
  - `services/subject_service.py`: suporte completo ao token de sessão e parâmetros do Xano.
  - `services/task_service.py`: novo módulo de integração com os endpoints de `academic_tasks`.
- **Backend (Xano):** Nenhum arquivo .xs ou tabela será alterado; os endpoints já criados na Tarefa 12 serão apenas consumidos.

