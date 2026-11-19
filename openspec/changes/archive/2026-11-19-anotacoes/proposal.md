# Change Proposal: anotacoes

## Why
O EduTrack AI precisava de um local para o usuário registrar lembretes, ideias e conteúdos importantes do estudo e acessá-los posteriormente.

## What Changes
- Criar a página `pages/5_📝_Anotações.py`.
- Permitir criar, editar, excluir, buscar e filtrar anotações por categoria.
- Persistir as anotações em `data/notes.json` no ambiente local.
- Adicionar o acesso às Anotações no dashboard e na navegação do Streamlit.
- Ignorar a pasta `data/` no Git para evitar versionar dados pessoais.

## Impact
- **Interface:** Nova página de Anotações integrada ao tema visual existente.
- **Dados:** Persistência local em JSON.
- **Backend:** Nenhuma alteração nas APIs ou tabelas do Xano.
- **Escopo:** Somente a funcionalidade de anotações solicitada.
