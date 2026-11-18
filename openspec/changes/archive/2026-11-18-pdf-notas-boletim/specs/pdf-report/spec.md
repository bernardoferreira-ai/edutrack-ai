# pdf-report Specification

## Purpose
Define os requisitos para geração do relatório PDF de desempenho acadêmico do estudante, incluindo o boletim de notas por disciplina.

## ADDED Requirements

### Requirement: Incluir boletim de notas no PDF
O sistema SHALL gerar um PDF com segunda página contendo o boletim de notas por disciplina.

#### Scenario: Aluno baixa o relatório PDF
- **WHEN** o aluno clica em "Baixar Relatório PDF" na página de Perfil
- **THEN** o PDF gerado contém uma segunda página com as notas de cada disciplina, média ponderada e status de aprovação com indicação visual por cor

### Requirement: Calcular média ponderada por disciplina
O sistema SHALL calcular a média ponderada das avaliações lançadas para cada disciplina.

#### Scenario: Disciplina com avaliações lançadas
- **WHEN** existem avaliações com nota e peso definidos para uma disciplina
- **THEN** o sistema calcula `soma(nota * peso) / soma(pesos)` e exibe com 1 casa decimal

#### Scenario: Avaliação pendente
- **WHEN** uma avaliação não possui nota lançada
- **THEN** ela é exibida como "Pendente" e excluída do cálculo da média

### Requirement: Classificar status de aprovação por cor
O sistema SHALL exibir badge colorido indicando o status do aluno em cada disciplina.

#### Scenario: Média igual ou acima de 7.0
- **WHEN** a média calculada é >= 7.0
- **THEN** o badge exibe "Aprovado" na cor verde

#### Scenario: Média entre 5.0 e 6.9
- **WHEN** a média calculada está entre 5.0 e 6.9 (inclusive)
- **THEN** o badge exibe "Em Recuperacao" na cor laranja, com a pontuação faltante

#### Scenario: Média abaixo de 5.0
- **WHEN** a média calculada é < 5.0
- **THEN** o badge exibe "Atencao Critica" na cor vermelha, com a pontuação faltante
