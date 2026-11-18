# Change Proposal: pagina-notas

## Why
O EduTrack AI já possui a base de dados para notas acadêmicas (`activity_grades`), porém os alunos ainda não dispunham de uma interface gráfica dedicada para consultar suas notas de trabalhos e provas por matéria. A criação da página `pages/4_📊_Notas.py` permite ao aluno acompanhar o rendimento acadêmico em tempo real, visualizando médias, status de aprovação em cores e a pontuação necessária para atingir a meta.

## What Changes
- Criar a nova página `pages/4_📊_Notas.py` integrada à navegação multipágina do Streamlit.
- Apresentar cards individuais para cada disciplina cadastrada exibindo:
  - Nome da disciplina e professor responsável.
  - Discriminação das notas obtidas em trabalhos e provas.
  - Cálculo automático da média atual do aluno.
  - Badges de status coloridos: verde para média $\ge 7.0$ (Aprovado / Bom desempenho), amarelo para atenção (5.0 a 6.9) e vermelho para alerta crítico ($< 5.0$).
  - Indicador de quantos pontos faltam para atingir a nota mínima de aprovação ($7.0$).
- Utilizar a paleta em modo escuro (fundo preto/cinza escuro, cards grafite `#161e2e` e detalhes em vermelho) em total harmonia com as demais páginas.

## Impact
- **Interface e Usabilidade:** Nova página intuitiva e visualmente alinhada ao tema da plataforma.
- **Backend:** Consome os dados de disciplinas e estrutura de notas do usuário autenticado via token JWT, mantendo modo fallback offline para demonstração local.
- **Escopo:** Estritamente limitado à criação e exibição da página de notas `pages/4_📊_Notas.py`.
