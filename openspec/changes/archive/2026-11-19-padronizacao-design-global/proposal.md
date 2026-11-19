# Change Proposal: padronizacao-design-global

## Why
O EduTrack AI possui estilos consistentes em partes do aplicativo, mas ainda repete regras visuais entre páginas. Uma padronização visual melhora hierarquia, espaçamento, contraste, responsividade e aparência profissional sem alterar os recursos existentes.

## What Changes
- Criar `services/design_service.py` com CSS compartilhado para o sistema visual.
- Aplicar a camada visual ao Dashboard, Disciplinas, Tarefas, Perfil e Notas.
- Padronizar tipografia, cartões, bordas, sombras, tabs, expanders, controles, tabelas, badges e responsividade.
- Preservar todos os campos, textos, dados, formulários, APIs e regras de negócio.

## Impact
- **Interface:** Visual mais consistente e organizado em todas as páginas.
- **Backend:** Nenhuma alteração.
- **Escopo:** Estritamente limitado ao design e apresentação.
