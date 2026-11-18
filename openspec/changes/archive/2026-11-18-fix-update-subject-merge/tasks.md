# Tasks — fix-update-subject-merge

## Backend / Service

- [x] Adicionar lógica de `GET subjects/{id}` antes do `PATCH` em `update_subject`
- [x] Implementar merge: campos incoming sobrescrevem campos atuais do Xano
- [x] Garantir que `name`, `teacher` e `hours` estejam sempre no payload do PATCH
- [x] Preservar comportamento quando GET falha (prosseguir com payload parcial)
- [x] Manter fallback offline inalterado (atualiza apenas o store local)

## Verificação

- [x] Verificar sintaxe de `services/subject_service.py` via `ast.parse` — OK
- [x] Confirmar que assinatura de `update_subject` não foi alterada (compatibilidade com chamadores existentes)
