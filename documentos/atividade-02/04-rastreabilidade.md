# Rastreabilidade — VanTrack

A matriz de rastreabilidade relaciona as regras de negócio (RN), os requisitos
funcionais (RF) e não funcionais (RNF), os casos de uso (UC) e o ponto do fluxo
em que cada regra é aplicada, permitindo responder:

> De onde surgiu esta funcionalidade?
> Quais partes do sistema serão afetadas se este requisito mudar?

---

## 1. Matriz RN ↔ RF/RNF ↔ UC ↔ Fluxo

| Regra de Negócio | Requisitos Funcionais | RNF | Casos de Uso | Fluxo/Cenário em que a regra é aplicada |
|---|---|---|---|---|
| RN-001 — Acesso vinculado à empresa | RF-001, RF-013 | RNF-002 | UC-B02, UC-S01, UC-S08 | UC-S01 passo 3 (validar código) e exceções E1/E2; UC-S08 passo 3 |
| RN-002 — Restrição de acesso aos dados do aluno | RF-001, RF-002, RF-003, RF-011, RF-012, RF-013 | RNF-002 | UC-S01, UC-S02, UC-S07, UC-S08, UC-S10, UC-I02, UC-I03 | UC-S02 passo 2 / E2; UC-S08 passo 3 / E1; UC-I02 passo 1; UC-I03 passo 2 |
| RN-003 — Consentimento para tratamento de localização | RF-002, RF-003, RF-016 | RNF-002 | UC-B02, UC-S02, UC-S10, UC-C01 | UC-C01 passos 5–6; pré-condição do UC-S02 |
| RN-004 — Prazo para confirmação de presença | RF-004, RF-007 | — | UC-B01, UC-S03, UC-E01, UC-R01, UC-S09 | UC-S03 passo 3 / E1; UC-R01 E1; gatilho do UC-S09 |
| RN-005 — Roteirização baseada nas presenças | RF-004, RF-007, RF-008 | — | UC-B01, UC-S03, UC-S09, UC-X02 | UC-S09 passos 1–4 / A1; UC-X02 passo 3 |
| RN-006 — Cancelamento da utilização do transporte | RF-005, RF-006, RF-008 | — | UC-B01, UC-S04, UC-X02 | UC-S04 passo 2 / E1 |
| RN-007 — Notificação de cancelamento | RF-006 | — | UC-S04, UC-I01 | UC-S04 passo 6 («include» UC-I01); UC-I01 passos 3–4 |
| RN-008 — Recálculo da rota após cancelamento | RF-008 | — | UC-S04, UC-X02 | Ponto de extensão do UC-S04 («extend» UC-X02); UC-X02 passos 1–4 / A1 |
| RN-009 — Vínculo obrigatório entre aluno e responsável | RF-001, RF-011, RF-016 | RNF-002 | UC-B02, UC-S01, UC-C01, UC-X01, UC-I02 | UC-X01 passo 5; UC-I02 passo 1 / A1 |
| RN-010 — Confirmação de embarque e desembarque | RF-009, RF-010, RF-011 | RNF-005 | UC-B01, UC-S05, UC-S06, UC-E02, UC-R02 | UC-S05 passos 1–2; UC-S06 passo 2; UC-R02 passo 3 |
| RN-011 — Sequência de embarque e desembarque | RF-010 | RNF-005 | UC-B01, UC-S06, UC-E02 | UC-S06 passo 3 / E1; UC-E02 A1 |
| RN-012 — Motorista ativo da van | RF-002, RF-007, RF-012, RF-014 | — | UC-ADM01, UC-S02, UC-S07, UC-S09, UC-I01 | UC-ADM01 passos 4–5; UC-I01 passo 2; pré-condições do UC-S07 e do UC-S09 |
| RN-013 — Restrição de acesso ao chat por vínculo | RF-013 | — | UC-S08, UC-I03 | UC-S08 passo 3 / E2; UC-I03 passo 4 (transmissão, sem conversa entre responsáveis) |
| RN-014 — Comunicação de atraso a todos os responsáveis da van | RF-012, RF-015 | — | UC-B01, UC-S07, UC-S11, UC-I03 | UC-S11 passo 3 / A1 (limiar de 10 minutos); UC-I03 passos 1–4 |
| RN-015 — Operação dependente de conectividade | **Cancelada** — reclassificada como RNF | RNF-003, RNF-006 | — | Tratada pelos RNF-003 e RNF-006 (ver tabela 2) |
| RN-016 — Autorização para dados de menores | RF-016 | RNF-002 | UC-B02, UC-C01, UC-X01 | Ponto de extensão do UC-C01 (passo 4 → UC-X01); UC-C01 E2; UC-X01 E1 |

---

## 2. Matriz RNF ↔ RF ↔ UC

| Requisito Não Funcional | Requisitos Funcionais | Casos de Uso | Onde aparece no comportamento |
|---|---|---|---|
| RNF-001 — Latência de atualização da localização | RF-002, RF-003 | UC-S02, UC-S10 | UC-S02 passo 5 (intervalo de atualização) |
| RNF-002 — Proteção de dados pessoais e de menores | RF-001, RF-002, RF-003, RF-004, RF-005, RF-009, RF-010, RF-011, RF-013, RF-016 | UC-S01, UC-S02, UC-S03, UC-S04, UC-S08, UC-C01, UC-X01, UC-I02 | Verificação de vínculo antes de liberar dados (UC-S02 passo 2, UC-S08 passo 3) e autorização de menores (UC-X01) |
| RNF-003 — Tratamento da perda de conectividade | RF-002, RF-003, RF-012, RF-013 | UC-S02, UC-S07, UC-S08, UC-S10 | UC-S02 E1; UC-S07 E1; UC-S08 E3; UC-S10 E1 |
| RNF-004 — Compatibilidade multiplataforma | RF-001 a RF-016 | Todos os casos de uso de sistema | Restrição para todo o sistema |
| RNF-005 — Usabilidade das ações do motorista | RF-009, RF-010, RF-012 | UC-S05, UC-S06, UC-S07, UC-R02 | UC-R02 passo 3 (uma única ação na tela da rota) |
| RNF-006 — Sincronização de check-ins offline | RF-009, RF-010 | UC-S05, UC-S06, UC-R02 | UC-S05 A1; UC-S06 A1; UC-R02 E1 |

---

## 3. Matriz RF ↔ UC

| Requisito Funcional | Caso(s) de uso |
|---|---|
| RF-001 — Vincular usuário à empresa | UC-B02, UC-S01 |
| RF-002 — Rastrear localização da van | UC-S02 |
| RF-003 — Notificar proximidade da van | UC-S10 |
| RF-004 — Confirmar presença | UC-B01, UC-S03, UC-E01, UC-R01 |
| RF-005 — Cancelar utilização do transporte | UC-B01, UC-S04, UC-R01 |
| RF-006 — Notificar motorista sobre cancelamento | UC-B01, UC-I01 |
| RF-007 — Gerar rota otimizada | UC-B01, UC-S09 |
| RF-008 — Recalcular rota após cancelamento | UC-B01, UC-X02 |
| RF-009 — Registrar embarque | UC-B01, UC-S05, UC-E02, UC-R02 |
| RF-010 — Registrar desembarque | UC-B01, UC-S06, UC-E02 |
| RF-011 — Notificar responsável sobre embarque e desembarque | UC-B01, UC-E02, UC-I02 |
| RF-012 — Emitir aviso geral de atraso | UC-B01, UC-S07, UC-I03 |
| RF-013 — Trocar mensagens pelo chat | UC-S08 |
| RF-014 — Vincular motorista à van | UC-ADM01 |
| RF-015 — Detectar atraso automático da rota | UC-S11, UC-I03 |
| RF-016 — Cadastrar aluno menor de idade | UC-B02, UC-C01, UC-X01 |

---

## 4. Análise da rastreabilidade

**Existem regras sem requisitos?**  
Não. Todas as regras ativas possuem ao menos um RF relacionado. A RN-015 foi
cancelada por descrever uma restrição técnica (dependência de internet), e não
uma política do negócio; seu comportamento foi mantido nos RNF-003 e RNF-006.

**Existem requisitos sem casos de uso?**  
Não. Todos os RF (RF-001 a RF-016) são realizados por pelo menos um caso de uso
de sistema, inclusão, extensão ou administrativo.

**Existem comportamentos sem relação aparente com requisito ou regra?**  
Na revisão foi encontrado o "Desfazer embarque em até 10 segundos" no UC-R02, que
não possuía RN nem RF de origem. O fluxo foi removido para não introduzir
comportamento sem justificativa. Os casos de uso de inclusão (UC-I01, UC-I02 e
UC-I03) não surgem de um pedido direto do ator, mas são justificados pelas
RN-007, RN-010 e RN-014 e pelos RF-006, RF-011 e RF-012.

**Isso necessariamente representa um erro?**  
Não. Um comportamento sem origem pode indicar uma regra ainda não documentada ou
uma decisão interna legítima de projeto. Por isso cada caso foi analisado
individualmente antes de ser removido ou mantido.
