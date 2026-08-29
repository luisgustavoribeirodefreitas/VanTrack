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
100% dos alunos menores de idade cadastrados devem possuir responsável
vinculado e os dados protegidos por controle de acesso.

**Escopo:**  
Todo o sistema.

**Prioridade:**  
Crítica

**Status:**  
Proposto

**Requisitos relacionados:**  
RF-001, RF-002, RF-003, RF-004, RF-005, RF-009, RF-010, RF-011, RF-013

---

## RNF-003 — Tratamento da perda de conectividade

**Categoria:**  
Disponibilidade

**Descrição:**  
Quando não houver atualização da localização da van por perda de
conectividade, o sistema deve manter visível a última localização conhecida
e informar ao usuário que os dados estão desatualizados.

**Justificativa:**  
O rastreamento depende de conectividade e podem existir trechos sem sinal.

**Métrica/Critério mensurável:**  
O aviso de ausência de atualização deve ser exibido em até 30 segundos
após a identificação da perda de conectividade.

**Escopo:**  
Rastreamento da van.

**Prioridade:**  
Alta

**Status:**  
Proposto

**Requisitos relacionados:**  
RF-002

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
As funcionalidades previstas para o MVP devem ser testadas e executáveis
nas plataformas Android, iOS e Web antes da conclusão da versão.

**Escopo:**  
Todo o sistema.

**Prioridade:**  
Alta

**Status:**  
Proposto

**Requisitos relacionados:**  
RF-001 a RF-013

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