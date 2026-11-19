# dashboard Specification

## Purpose

Define a página inicial do EduTrack AI com visão resumida do semestre, tarefas prioritárias, boletim acadêmico e atalhos para as principais funcionalidades.

## ADDED Requirements

### Requirement: Exibir saudação personalizada no dashboard

O sistema SHALL exibir uma saudação dinâmica conforme o horário do dia e identificar o usuário autenticado ou um nome padrão.

#### Scenario: Usuário autenticado abre o dashboard

- **WHEN** o usuário possui perfil salvo na sessão
- **THEN** o sistema exibe o nome disponível do usuário na saudação

#### Scenario: Usuário não autenticado abre o dashboard

- **WHEN** não existe token de autenticação na sessão
- **THEN** o sistema exibe uma saudação padrão para estudante e indica o modo local

### Requirement: Exibir indicadores acadêmicos

O sistema SHALL apresentar disciplinas ativas, tarefas concluídas, tarefas pendentes, média geral e progresso das tarefas.

#### Scenario: Existem dados acadêmicos disponíveis

- **WHEN** o dashboard recebe disciplinas e tarefas
- **THEN** o sistema calcula e exibe os indicadores correspondentes

#### Scenario: Não existem tarefas cadastradas

- **WHEN** a lista de tarefas está vazia
- **THEN** o sistema exibe progresso igual a zero por cento

### Requirement: Exibir tarefas pendentes prioritárias

O sistema SHALL ordenar as tarefas pendentes pela data de vencimento e apresentar até oito tarefas próximas.

#### Scenario: Existem tarefas pendentes com prazos válidos

- **WHEN** o dashboard renderiza a seção de próximas tarefas
- **THEN** o sistema apresenta as tarefas pendentes mais próximas primeiro

#### Scenario: Não existem tarefas pendentes

- **WHEN** todas as tarefas estão concluídas
- **THEN** o sistema exibe uma mensagem informando que não há pendências

### Requirement: Exibir resumo do boletim

O sistema SHALL apresentar uma média e um status resumido para cada disciplina disponível.

#### Scenario: A disciplina possui avaliações

- **WHEN** existem notas associadas ao nome da disciplina
- **THEN** o sistema calcula a média, aplica o status correspondente e exibe o resultado

#### Scenario: A disciplina não possui avaliações

- **WHEN** não existem notas associadas à disciplina
- **THEN** o sistema exibe que não há notas para aquela disciplina

### Requirement: Exibir acesso rápido às páginas

O sistema SHALL disponibilizar links rápidos para Disciplinas, Tarefas, Perfil, Notas e Anotações.

#### Scenario: Usuário seleciona um acesso rápido

- **WHEN** o usuário seleciona um dos atalhos do dashboard
- **THEN** o sistema abre a página correspondente
