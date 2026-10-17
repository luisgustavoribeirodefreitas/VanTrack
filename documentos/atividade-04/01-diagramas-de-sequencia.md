# Diagramas de Sequência — VanTrack

Cada diagrama de sequência refina um cenário de um caso de uso documentado em
[01-casos-de-uso.md](../atividade-03/01-casos-de-uso.md). O caminho seguido foi:

```text
CASO DE USO → CENÁRIO → PASSOS → RESPONSABILIDADES → PARTICIPANTES → MENSAGENS → DIAGRAMA
```

Os fluxos alternativos (A) e exceções (E) relevantes aparecem com os fragmentos
`alt`, `opt` e `loop`, e os casos de uso de inclusão/extensão aparecem como `ref`.
As regras de negócio (RN) e os requisitos não funcionais (RNF) aplicados são
indicados nas próprias mensagens, mantendo a rastreabilidade RN → RF → UC → Sequência.

Os scripts PlantUML estão em [`scripts/`](scripts/) e as imagens em [`imagens/`](imagens/).

---

## 1. Distribuição de responsabilidades

Os diagramas de sistema seguem a separação em camadas, para que nenhum objeto
concentre todas as responsabilidades:

| Camada | Notação | Exemplos | Responsabilidade |
|---|---|---|---|
| Interface (boundary) | `boundary` | TelaPresenca, TelaRotaDoDia, TelaChat, PainelVans | Interagir com o ator: exibir dados e receber ações. Não contém regra de negócio. |
| Controle / Aplicação | `control` + serviço | PresencaController → PresencaService | O controller recebe a requisição da tela; o serviço coordena o caso de uso (consultar, validar, criar, persistir e responder). |
| Domínio | `entity` | Presenca, Trajeto, Rota, Aluno, Conversa, Van | Concentrar as regras que pertencem ao próprio conceito do negócio. |
| Infraestrutura | `database` / sistema externo | PresencaRepository, Serviço de Geolocalização, Serviço de Notificação | Persistir dados e integrar com serviços externos. |

### Responsabilidade de cada participante e origem na análise

| Participante | Responsabilidade | Justificativa (de onde surgiu) |
|---|---|---|
| Presenca | Saber se pode ser cancelada (`podeCancelar`), registrar embarque/desembarque e validar se já houve embarque (`possuiEmbarque`). | RN-006, RN-010, RN-011 — regras sobre o estado da presença do aluno. |
| Trajeto | Informar se o prazo de confirmação está aberto (`prazoConfirmacaoAberto`). | RN-004 — o prazo depende do horário de saída do trajeto. |
| Rota | Manter paradas e percurso, remover parada, calcular desvio de horário e verificar limite de proximidade. | RN-005, RN-008, RN-014; RF-003, RF-007, RF-008, RF-015. |
| Aluno | Saber se é menor de idade, registrar consentimento/autorização e decidir se pode ser ativado. | RN-003, RN-009, RN-016. |
| Van | Manter um único vínculo ativo com motorista, encerrando o anterior. | RN-012. |
| Conversa | Verificar se o usuário pode acessar a conversa e manter o histórico. | RN-001, RN-002, RN-013. |
| CodigoAcesso / Vinculo | Validar o código da empresa e representar o vínculo usuário–van–aluno. | RN-001, RN-002, RN-009. |
| AvisoAtraso / AutorizacaoLegal | Registrar avisos de atraso (manual ou automático) e autorizações do responsável legal. | RN-014, RN-016. |
| *Service (PresencaService, EmbarqueService, RotaService, AtrasoService, ChatService, AlunoService, VanService, VinculoService, RastreamentoService, ProximidadeService) | Coordenar os passos de cada caso de uso, na ordem do fluxo principal. | Um serviço por grupo de casos de uso, para o controller não fazer tudo. |
| NotificacaoService | Montar e enviar notificações, sendo reutilizado pelos casos de uso de inclusão. | UC-I01, UC-I02, UC-I03 (comportamento obrigatório e reutilizado). |
| AgendadorRotas / MonitorAtraso | Receber os disparos do ator Tempo. | UC-S09 e UC-S11 são iniciados pela passagem do tempo, não por um usuário. |
| *Repository | Buscar e salvar entidades. | Persistência fica na infraestrutura, fora do domínio. |
| ArmazenamentoLocal | Guardar check-ins sem conexão e sincronizar ao reconectar. | RNF-006. |
| Serviço de Geolocalização / Serviço de Notificação | Sistemas externos que fornecem posição/trajetos e entregam notificações push. | Atores secundários do diagrama de casos de uso. |

### Por que alguns diagramas usam outra notação

- **Casos de uso de negócio (UC-B01, UC-B02)**: descrevem o processo do negócio,
  independente do software, por isso só aparecem os atores.
- **Casos de uso essenciais (UC-E01, UC-E02)**: descrevem a intenção, sem tecnologia,
  por isso o sistema aparece como um único participante.
- **Casos de uso reais (UC-R01, UC-R02)**: focam nas telas e botões, por isso
  mostram as telas e o servidor.

---

## 2. Casos de uso de sistema

### UC-S01 — Vincular Usuário à Empresa
Cenário: fluxo principal + A1 (mais de um aluno) + E1/E2 (código inválido ou expirado). Regras: RN-001, RN-002, RN-009.

![UC-S01](imagens/UC-S01.png)

### UC-S02 — Acompanhar Van em Tempo Real
Cenário: fluxo principal com `loop` de atualização (RNF-001) + A1 (rota não iniciada) + E1 (sem conectividade) + E2 (sem vínculo).

![UC-S02](imagens/UC-S02.png)

### UC-S03 — Confirmar Presença
Cenário: fluxo principal + A1 (presença já confirmada) + E1 (prazo encerrado — RN-004, verificado pela entidade Trajeto).

![UC-S03](imagens/UC-S03.png)

### UC-S04 — Cancelar Utilização do Transporte
Cenário: fluxo principal com `ref` para o «include» UC-I01 e `opt` para o «extend» UC-X02 + E1 (embarque já registrado — RN-006).

![UC-S04](imagens/UC-S04.png)

### UC-S05 — Registrar Embarque
Cenário: fluxo principal + A1 (sem conectividade — RNF-006), com `ref` para o «include» UC-I02.

![UC-S05](imagens/UC-S05.png)

### UC-S06 — Registrar Desembarque
Cenário: fluxo principal + E1 (sem embarque — RN-011, verificado pela entidade Presenca) + A1 (sem conectividade).

![UC-S06](imagens/UC-S06.png)

### UC-S07 — Emitir Aviso de Atraso
Cenário: fluxo principal com `ref` para o «include» UC-I03 + A1 (complementar aviso automático) + E1 (sem conectividade).

![UC-S07](imagens/UC-S07.png)

### UC-S08 — Trocar Mensagens pelo Chat
Cenário: fluxo principal + E1/E2 (acesso negado — RN-013) + E3 (sem conectividade).

![UC-S08](imagens/UC-S08.png)

### UC-S09 — Gerar Rota Otimizada
Cenário: disparo pelo ator Tempo + A1 (nenhum aluno confirmado) + E1 (localização do motorista indisponível).

![UC-S09](imagens/UC-S09.png)

### UC-S10 — Notificar Proximidade da Van
Cenário: `loop` para cada parada pendente + A1 (aviso já enviado) + A2 (limite não atingido) + E1 (localização desatualizada).

![UC-S10](imagens/UC-S10.png)

### UC-S11 — Detectar Atraso Automaticamente
Cenário: disparo periódico pelo ator Tempo + limiar de 10 minutos (RN-014) + A1 (desvio abaixo do limiar).

![UC-S11](imagens/UC-S11.png)

---

## 3. Casos de uso de inclusão e extensão

### UC-I01 — Notificar Motorista sobre Cancelamento («include» de UC-S04)

![UC-I01](imagens/UC-I01.png)

### UC-I02 — Notificar Responsável sobre Embarque/Desembarque («include» de UC-S05 e UC-S06)

![UC-I02](imagens/UC-I02.png)

### UC-I03 — Notificar Responsáveis sobre Atraso («include» de UC-S07 e UC-S11)

![UC-I03](imagens/UC-I03.png)

### UC-X01 — Registrar Autorização do Responsável Legal («extend» de UC-C01)

![UC-X01](imagens/UC-X01.png)

### UC-X02 — Recalcular Rota («extend» de UC-S04)

![UC-X02](imagens/UC-X02.png)

---

## 4. Cadastro, abstrato e administrativo

### UC-C01 — Manter Aluno (cenário "cadastrar")

![UC-C01](imagens/UC-C01.png)

### UC-A01 — Manter Cadastro Base (abstrato)

![UC-A01](imagens/UC-A01.png)

### UC-ADM01 — Vincular Motorista à Van

![UC-ADM01](imagens/UC-ADM01.png)

---

## 5. Casos de uso reais

### UC-R01 — Confirmar Presença pelo Aplicativo

![UC-R01](imagens/UC-R01.png)

### UC-R02 — Registrar Embarque pela Tela da Rota

![UC-R02](imagens/UC-R02.png)

---

## 6. Casos de uso essenciais

### UC-E01 — Confirmar Utilização do Transporte

![UC-E01](imagens/UC-E01.png)

### UC-E02 — Registrar Movimentação do Aluno

![UC-E02](imagens/UC-E02.png)

---

## 7. Casos de uso de negócio

### UC-B01 — Realizar Transporte Escolar Diário

![UC-B01](imagens/UC-B01.png)

### UC-B02 — Aderir ao Transporte da Empresa

![UC-B02](imagens/UC-B02.png)
