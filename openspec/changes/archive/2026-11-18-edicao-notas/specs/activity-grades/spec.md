# activity-grades Specification

## Purpose
Define os requisitos de visualização e edição local de notas de avaliações por disciplina na tela Boletim & Notas do EduTrack AI.

## ADDED Requirements

### Requirement: Editar notas de avaliações localmente
O sistema SHALL permitir que o aluno edite as notas de cada avaliação diretamente na interface, com persistência durante a sessão.

#### Scenario: Aluno clica em "Editar Notas"
- **WHEN** o aluno clica no botão "✏️ Editar Notas" em um card de disciplina
- **THEN** o sistema exibe um formulário inline com um `number_input` (0.0–10.0) para cada avaliação, mostrando nome, tipo, peso e data de cada uma

#### Scenario: Aluno salva alterações
- **WHEN** o aluno altera as notas e clica em "💾 Salvar Alterações"
- **THEN** o sistema atualiza os valores em `st.session_state["grades_data"]`, fecha o formulário e recalcula automaticamente a média e o badge de status da disciplina

#### Scenario: Aluno restaura padrão
- **WHEN** o aluno clica em "🔄 Restaurar Padrão"
- **THEN** o sistema restaura as notas originais do fallback `_DEFAULT_GRADES` para aquela disciplina e recalcula a média

### Requirement: Persistir notas no session_state
O sistema SHALL armazenar as notas editadas em `st.session_state["grades_data"]` para que as edições persistam durante toda a sessão do usuário.

#### Scenario: Primeira carga da página
- **WHEN** a página de Notas é carregada pela primeira vez na sessão
- **THEN** o sistema inicializa `st.session_state["grades_data"]` com uma cópia profunda do dicionário `_DEFAULT_GRADES`

#### Scenario: Disciplina do backend sem dados cadastrados
- **WHEN** o backend retorna uma disciplina cujo nome não existe em `grades_data`
- **THEN** o sistema adiciona essa disciplina ao `grades_data` com o fallback `_EVAL_FALLBACK`
