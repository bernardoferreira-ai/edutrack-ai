## Context

A página inicial do EduTrack AI deve funcionar como um painel central para o estudante. Ela já deve consumir os serviços existentes de disciplinas e tarefas e reutilizar o estado de notas já mantido pela aplicação.

## Goals / Non-Goals

**Goals:**
- Mostrar uma visão resumida do semestre acadêmico.
- Calcular indicadores diretamente a partir dos dados disponíveis.
- Orientar o estudante para tarefas próximas e áreas críticas do desempenho.
- Preservar acesso rápido às principais páginas.
- Manter uma experiência funcional no modo local quando não houver token ou backend disponível.

**Non-Goals:**
- Criar novas APIs ou tabelas Xano.
- Persistir notas ou anotações no dashboard.
- Implementar calendário acadêmico completo.
- Alterar regras de aprovação ou cálculo das páginas existentes.

## Decisions

### 1. Componentes do dashboard

A página será organizada em:
- Banner de saudação e data.
- Cinco indicadores acadêmicos.
- Lista das tarefas pendentes mais próximas.
- Resumo do boletim por disciplina.
- Links rápidos para as cinco páginas principais.

**Rationale:** A organização permite encontrar prioridades e atalhos sem sair da página inicial.

### 2. Cálculo dos indicadores

- Disciplinas ativas: registros cujo status não seja `completed`.
- Tarefas concluídas: registros com status `completed` ou `concluida`.
- Tarefas pendentes: registros que não estejam concluídos.
- Progresso: percentual de tarefas concluídas sobre o total.
- Média geral: média simples das médias disponíveis por disciplina.

**Rationale:** Reutiliza as convenções já presentes na interface, sem introduzir novas regras de domínio.

### 3. Priorização de tarefas

As tarefas pendentes serão ordenadas pela data de vencimento, com destaque para vencidas, vencimento no dia atual e vencimento nos próximos três dias.

**Rationale:** Facilita identificar prioridades acadêmicas imediatas.

### 4. Dados locais e autenticação

Quando não houver token, a interface informará que está em modo local. Os serviços continuarão retornando dados locais ou de fallback, sem impedir a renderização do dashboard.

**Rationale:** Evita falhas visuais durante desenvolvimento e quando o backend estiver indisponível.

## Risks / Trade-offs

- **[Risk]** Dados locais podem ser interpretados como dados persistidos no Xano.
  → **Mitigation:** Exibir claramente a indicação de modo local no banner principal.
- **[Risk]** Datas inválidas podem dificultar a ordenação.
  → **Mitigation:** Registrar datas sem formato reconhecido no final da lista.
- **[Risk]** Concentração excessiva de informações em telas menores.
  → **Mitigation:** Usar grades responsivas e espaçamento adaptável.
