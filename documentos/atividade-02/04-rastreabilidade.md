# Rastreabilidade — VanTrack

A matriz de rastreabilidade apresenta a relação entre as regras de negócio,
os requisitos funcionais e os requisitos não funcionais do VanTrack.

| Regra de Negócio | Requisitos Funcionais relacionados | RNF relacionados |
|---|---|---|
| RN-001 — Acesso vinculado à empresa | RF-001, RF-013 | RNF-002 |
| RN-002 — Restrição de acesso aos dados do aluno | RF-001, RF-002, RF-003, RF-011, RF-012, RF-013 | RNF-002 |
| RN-003 — Consentimento para tratamento de localização | RF-002, RF-003 | RNF-002 |
| RN-004 — Prazo para confirmação de presença | RF-004, RF-007 | — |
| RN-005 — Roteirização baseada nas presenças | RF-004, RF-007, RF-008 | — |
| RN-006 — Cancelamento da utilização do transporte | RF-005, RF-006, RF-008 | — |
| RN-007 — Notificação de cancelamento | RF-006 | — |
| RN-008 — Recálculo da rota após cancelamento | RF-008 | — |
| RN-009 — Vínculo obrigatório aluno–responsável | RF-001, RF-011 | RNF-002 |
| RN-010 — Confirmação de embarque e desembarque | RF-009, RF-010, RF-011 | RNF-005 |
| RN-011 — Sequência de embarque e desembarque | RF-010 | RNF-005 |
| RN-012 — Motorista ativo da van | RF-002, RF-007, RF-012, RF-014 | — |
| RN-013 — Restrição de Acesso ao Chat por Vínculo | RF-013 | — |
| RN-014 — Comunicação de Atraso a Todos os Responsáveis da Van | RF-012, RF-015 | — |
| RN-015 — Operação Dependente de Conectividade | RF-002, RF-003, RF-009, RF-010, RF-012, RF-013 | RNF-003, RNF-006 |
| RN-016 — Autorização para Dados de Menores | RF-016 | RNF-002 |

## Rastreabilidade dos Requisitos Não Funcionais

| Requisito Não Funcional | Requisitos Funcionais relacionados |
|---|---|
| RNF-001 — Latência de atualização da localização | RF-002, RF-003 |
| RNF-002 — Proteção de dados pessoais e de menores | RF-001, RF-002, RF-003, RF-004, RF-005, RF-009, RF-010, RF-011, RF-013, RF-016 |
| RNF-003 — Tratamento da perda de conectividade | RF-002, RF-003, RF-012, RF-013 |
| RNF-004 — Compatibilidade multiplataforma | RF-001 a RF-013 |
| RNF-005 — Usabilidade das ações do motorista | RF-009, RF-010, RF-012 |
| RNF-006 — Sincronização de check-ins offline | RF-009, RF-010 |
