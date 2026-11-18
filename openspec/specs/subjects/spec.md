# subjects Specification

## Purpose
Define os requisitos para o serviço de gestão de disciplinas, incluindo o comportamento correto de atualização parcial de campos via endpoint PATCH.

## Requirements

### Requirement: Merge automático de campos obrigatórios no PATCH
O sistema SHALL buscar o registro atual da disciplina antes de enviar o PATCH ao Xano, garantindo que todos os campos obrigatórios do endpoint (`name`, `teacher`, `hours`) estejam presentes no payload.

#### Scenario: Chamador atualiza apenas o nome
- **WHEN** `update_subject` é chamado com apenas `name` como campo
- **THEN** o sistema faz `GET /subjects/{id}`, mescla os valores atuais de `teacher` e `hours` ao payload e envia o `PATCH` completo ao Xano sem erro de validação

#### Scenario: Chamador atualiza apenas o professor
- **WHEN** `update_subject` é chamado com apenas `teacher` como campo
- **THEN** o sistema faz `GET /subjects/{id}`, mescla os valores atuais de `name` e `hours` ao payload e envia o `PATCH` completo ao Xano sem erro de validação

#### Scenario: GET de busca falha antes do PATCH
- **WHEN** o `GET /subjects/{id}` retorna erro ou timeout
- **THEN** o sistema prossegue com o payload parcial; o erro de validação do Xano, se ocorrer, é propagado normalmente ao chamador

#### Scenario: Atualização em modo offline (sem token)
- **WHEN** não há token de autenticação disponível
- **THEN** o sistema atualiza apenas os campos recebidos no store local de fallback, sem tentativa de GET ou PATCH ao Xano
