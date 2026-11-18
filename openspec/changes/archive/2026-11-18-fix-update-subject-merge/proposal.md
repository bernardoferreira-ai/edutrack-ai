# fix-update-subject-merge

## Why
O endpoint `PATCH /subjects/{id}` no Xano exige que os campos `name`, `teacher` e `hours` sejam enviados em toda requisição (campos obrigatórios no schema do endpoint). O método `update_subject` em `subject_service.py` enviava apenas os campos explicitamente passados pelo chamador, causando erros de validação do Xano sempre que o usuário editava apenas o nome ou apenas o professor da disciplina.

## What Changes
- `update_subject` em `services/subject_service.py` passa a realizar um `GET subjects/{id}` antes do `PATCH` para buscar o registro atual.
- Os valores atuais são usados como base; os campos passados pelo chamador têm prioridade máxima (merge "incoming sobrescreve current").
- Os campos obrigatórios do endpoint (`name`, `teacher`, `hours`) são sempre garantidos no payload, mesmo que o chamador envie apenas um deles.
- Se o `GET` falhar (offline / timeout), o service prossegue com o que foi passado — o comportamento de erro permanece inalterado.
- O fallback offline (sem token) não é afetado.
- **Nenhuma mudança de assinatura** — chamadores existentes (`pages/1_📚_Disciplinas.py`) não precisam de alteração.

## Impact
- `services/subject_service.py`: modificado (método `update_subject`, +~32 linhas).
- Nenhuma outra página, serviço ou arquivo afetado.
