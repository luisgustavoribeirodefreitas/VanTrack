# Requisitos Não Funcionais — VanTrack

Os requisitos não funcionais definem características de qualidade,
restrições técnicas e critérios mensuráveis que devem ser atendidos
pelo VanTrack.

---

## RNF-001 — Latência de atualização da localização

**Categoria:**  
Desempenho

**Descrição:**  
O sistema deve atualizar a posição da van no mapa dos usuários em
intervalo máximo de 15 segundos, quando houver conectividade disponível.

**Justificativa:**  
O rastreamento precisa apresentar informações suficientemente atuais
para permitir o acompanhamento da aproximação da van.

**Métrica/Critério mensurável:**  
A defasagem entre a localização recebida da van e a localização exibida
no aplicativo não deverá ultrapassar 15 segundos em pelo menos 95% das atualizações.

**Escopo:**  
Rastreamento e notificação de proximidade.

**Prioridade:**  
Crítica

**Status:**  
Proposto

**Requisitos relacionados:**  
RF-002, RF-003

**Casos de teste relacionados:**  
Não definido nesta etapa.

---

## RNF-002 — Proteção de dados pessoais e de menores

**Categoria:**  
Segurança

**Descrição:**  
O sistema deve controlar o acesso e o tratamento dos dados pessoais,
incluindo dados de localização e informações de alunos menores de idade.

**Justificativa:**  
O VanTrack utiliza informações pessoais e de localização de alunos,
responsáveis e motoristas.

**Métrica/Critério mensurável:**  
- 100% dos alunos menores de idade cadastrados devem possuir ao menos um responsável vinculado.
- 100% das solicitações de acesso aos dados dos alunos devem validar o vínculo e a autorização do usuário antes da liberação das informações.
- 100% dos alunos menores ativados devem possuir registro de autorização do responsável legal.

**Escopo:**  
Todo o sistema.

**Prioridade:**  
Crítica

**Status:**  
Proposto

**Requisitos relacionados:**  
RF-001, RF-002, RF-003, RF-004, RF-005, RF-009, RF-010, RF-011, RF-013, RF-016

**Casos de teste relacionados:**  
Não definido nesta etapa.

---

## RNF-003 — Tratamento da perda de conectividade

**Categoria:**  
Disponibilidade

**Descrição:**  
Quando não houver atualização de dados em tempo real por perda de conectividade (localização, notificações de atraso, chat), o sistema deverá manter visível a última informação conhecida e informar ao usuário que os dados estão desatualizados, nunca apresentando uma localização desatualizada como se fosse atual.

**Justificativa:**  
O rastreamento depende de conectividade e podem existir trechos sem sinal.

**Métrica/Critério mensurável:**  
O aviso de ausência de atualização deve ser exibido em até 30 segundos
após a identificação da perda de conectividade.

**Escopo:**  
Rastreamento da van, notificações de atraso e proximidade, e chat.

**Prioridade:**  
Alta

**Status:**  
Proposto

**Requisitos relacionados:**  
RF-002, RF-003, RF-012, RF-013

**Casos de teste relacionados:**  
Não definido nesta etapa.

## RNF-006 — Sincronização de check-ins offline

**Categoria:**
Confiabilidade

**Descrição:**
Check-ins de embarque e desembarque registrados sem conectividade devem ser sincronizados automaticamente ao reconectar.

**Justificativa:**
O motorista pode operar trechos sem sinal e não deve ficar impedido de registrar embarque/desembarque.

**Métrica/Critério mensurável:**
100% dos check-ins registrados offline devem ser sincronizados em até 5 minutos após o restabelecimento da conectividade.

**Escopo:**
Check-in de embarque e desembarque.

**Prioridade:**
Alta

**Status:**
Proposto

**Requisitos relacionados:**
RF-009, RF-010

**Casos de teste relacionados:**
Não definido nesta etapa.


---

## RNF-004 — Compatibilidade multiplataforma

**Categoria:**  
Compatibilidade

**Descrição:**  
O sistema deve disponibilizar as funcionalidades previstas para o MVP
nas plataformas definidas para o VanTrack.

**Justificativa:**  
O projeto prevê utilização em Android, iOS e Web.

**Métrica/Critério mensurável:**  
100% das funcionalidades previstas para o MVP devem ser testáveis e
executáveis nas plataformas Android, iOS e Web antes da conclusão da versão.

**Escopo:**  
Todo o sistema.

**Prioridade:**  
Alta

**Status:**  
Proposto

**Requisitos relacionados:**  
RF-001 a RF-013

**Casos de teste relacionados:**  
Não definido nesta etapa.

---

## RNF-005 — Usabilidade das ações do motorista

**Categoria:**  
Usabilidade

**Descrição:**  
As ações operacionais mais frequentes do motorista devem exigir o
mínimo de interação possível durante a execução da rota.

**Justificativa:**  
O motorista precisa registrar embarques, desembarques e avisos sem
realizar navegação excessiva pelo aplicativo.

**Métrica/Critério mensurável:**  
As ações de check-in de embarque, check-in de desembarque e emissão de
aviso geral de atraso devem estar disponíveis diretamente na tela de
operação da rota e ser executáveis com uma única ação principal.

**Escopo:**  
Check-in e comunicação de atraso.

**Prioridade:**  
Alta

**Status:**  
Proposto

**Requisitos relacionados:**  
RF-009, RF-010, RF-012

**Casos de teste relacionados:**  
Não definido nesta etapa.
