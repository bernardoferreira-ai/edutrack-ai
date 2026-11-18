# Change Proposal: melhoria-visual-caixas

## Why
As caixas, expansores e painéis de conteúdo nas páginas de Tarefas (`pages/2_📝_Tarefas.py`) e Disciplinas (`pages/1_📚_Disciplinas.py`) utilizam um visual genérico com bordas e espaçamentos simples. Refinar o design visual desses elementos (caixas de filtro, expansores de tarefas e gerenciamento, cartões de cadastro e tabela de disciplinas) confere um padrão visual moderno, coeso e agradável, alinhado ao estilo da página de perfil, sem alterar nenhuma funcionalidade, campo ou opção existente.

## What Changes
- Aprimorar o estilo CSS das caixas expansoras (`stExpander`) em ambas as páginas, com bordas translúcidas elegantes, fundo com leve gradiente, cantos arredondados modernos e sombras suaves.
- Refinar os cartões internos das tarefas em `pages/2_📝_Tarefas.py`: apresentar as informações de disciplina e prazo com badges e tipografia estilizada, além de melhorar o espaçamento dos botões de ação e checkboxes.
- Aprimorar os contêineres e caixas de formulário e gerenciamento em `pages/1_📚_Disciplinas.py`: estilizar as seções de listagem e cadastro com cartões modernos e hierarquia limpa.
- Preservar rigorosamente todos os campos, inputs, botões, opções de seleção, chaves de sessão e fluxos de negócio.

## Impact
- **Interface e Usabilidade:** Design moderno, limpo e harmonioso para as caixas de tarefas e disciplinas.
- **Backend:** Nenhuma alteração nas integrações com o Xano ou nos serviços `TaskService` e `SubjectService`.
- **Compatibilidade:** Totalmente compatível com as regras de preservação de opções e comportamento da aplicação.
