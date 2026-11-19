# Design: padronizacao-design-global

## Contexto
As páginas possuem CSS próprio e elementos visuais semelhantes duplicados. A padronização centraliza regras recorrentes em um único serviço Python.

## Decisão
Criar `apply_edutrack_design()` em `services/design_service.py`. Cada página continuará com seu conteúdo e estilos específicos, recebendo apenas a camada visual compartilhada.

## Princípios
- Preservar todas as opções existentes.
- Manter o tema escuro atual.
- Usar bordas, sombras e raios consistentes.
- Melhorar responsividade em telas menores.
- Evitar alterar dados, serviços, rotas ou fluxos de autenticação.
