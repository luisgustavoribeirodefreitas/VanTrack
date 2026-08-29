# Requisitos Funcionais — VanTrack

Os requisitos funcionais descrevem as funcionalidades que o sistema
deve disponibilizar para atender às regras de negócio do VanTrack.

---

## RF-001 — Vincular usuário à empresa

**Título:**  
Vinculação por código de acesso.

**Descrição:**  
O sistema deve permitir que o usuário se vincule à empresa de transporte
por meio de um código válido fornecido pela empresa.

**Objetivo:**  
Garantir que somente usuários autorizados tenham acesso às vans,
rotas e alunos correspondentes.

**Stakeholders:**  
Responsável, aluno e empresa de transporte.

**Ator principal:**  
Responsável/aluno.

**Pré-condições:**  
- Usuário cadastrado no sistema.
- Código de vinculação válido.

**Entradas:**  
Código de vinculação.

**Processamento esperado:**  
O sistema deve validar o código informado e associar o usuário
à empresa, van e/ou aluno correspondente.

**Saídas/Resultados:**  
Usuário vinculado aos dados autorizados.

**Pós-condições:**  
O usuário passa a acessar as funcionalidades correspondentes ao vínculo.

**Fluxos alternativos/exceções:**  
- Código inválido: o sistema deve recusar a vinculação.
- Código expirado ou desativado: o sistema deve informar o usuário.

**Regras de negócio relacionadas:**  
RN-001, RN-002, RN-009

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- Código válido realiza a vinculação corretamente.
- Código inválido não permite acesso.
- O usuário não recebe acesso a alunos não vinculados.

---

## RF-002 — Rastrear localização da van

**Título:**  
Rastreamento da van em tempo real.

**Descrição:**  
O sistema deve exibir a localização atual da van no mapa para usuários
autorizados vinculados à rota.

**Objetivo:**  
Permitir que responsáveis e alunos acompanhem a aproximação da van.

**Stakeholders:**  
Responsável, aluno e motorista.

**Ator principal:**  
Responsável/aluno.

**Pré-condições:**  
- Usuário vinculado à van/rota.
- Compartilhamento de localização autorizado.
- Van em operação.

**Entradas:**  
Localização GPS da van e identificação da rota.

**Processamento esperado:**  
O sistema deve receber periodicamente a localização da van e atualizar
sua posição no mapa.

**Saídas/Resultados:**  
Localização atual da van exibida ao usuário autorizado.

**Pós-condições:**  
A última localização recebida permanece registrada.

**Fluxos alternativos/exceções:**  
- Perda de conectividade: exibir a última localização conhecida.
- Usuário sem autorização: bloquear visualização.

**Regras de negócio relacionadas:**  
RN-002, RN-003, RN-012

**Prioridade:**  
Crítica

**Status:**  
Proposto

**Critérios de aceite:**  
- Apenas usuários autorizados visualizam a van.
- A posição apresentada deve ser atualizada durante a operação.
- Em perda de sinal, a última posição conhecida deve permanecer disponível.

---

## RF-003 — Notificar proximidade da van

**Título:**  
Notificação automática de proximidade.

**Descrição:**  
O sistema deve notificar o responsável ou aluno quando a van estiver
próxima ao ponto de parada correspondente.

**Objetivo:**  
Reduzir o tempo de espera do aluno na rua.

**Stakeholders:**  
Responsável e aluno.

**Ator principal:**  
Sistema.

**Pré-condições:**  
- Rastreamento ativo.
- Ponto de parada cadastrado.
- Usuário vinculado à rota.

**Entradas:**  
Localização da van, localização do ponto e estimativa de chegada.

**Processamento esperado:**  
O sistema deve calcular a proximidade da van e disparar uma notificação
quando atingir o limite configurado.

**Saídas/Resultados:**  
Notificação de proximidade enviada.

**Pós-condições:**  
O envio deve ser registrado para evitar notificações duplicadas.

**Fluxos alternativos/exceções:**  
- Localização desatualizada: informar que a estimativa pode estar imprecisa.

**Regras de negócio relacionadas:**  
RN-002, RN-003

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- A notificação deve ser automática.
- A mesma aproximação não deve gerar notificações duplicadas.
- Somente o responsável/aluno correspondente recebe o aviso.

---

## RF-004 — Confirmar presença

**Título:**  
Confirmação de utilização do transporte.

**Descrição:**  
O sistema deve permitir que o aluno ou responsável confirme a utilização
da van até 30 minutos antes do horário previsto de saída do motorista.

**Objetivo:**  
Determinar quais alunos deverão compor a rota do dia.

**Stakeholders:**  
Aluno, responsável e motorista.

**Ator principal:**  
Aluno/responsável.

**Pré-condições:**  
- Aluno vinculado a uma rota.
- Prazo de confirmação ainda aberto.

**Entradas:**  
Aluno, data e confirmação de presença.

**Processamento esperado:**  
O sistema deve registrar a presença do aluno para o dia selecionado.

**Saídas/Resultados:**  
Presença registrada.

**Pós-condições:**  
O aluno passa a ser considerado na geração da rota.

**Fluxos alternativos/exceções:**  
- Após o limite de 30 minutos, sem confirmação, o aluno permanece ausente.

**Regras de negócio relacionadas:**  
RN-004, RN-005

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- Confirmações dentro do prazo são registradas.
- Aluno não confirmado no prazo é considerado ausente.
- Alunos ausentes não entram na rota.

---

## RF-005 — Cancelar utilização do transporte

**Título:**  
Cancelamento de presença.

**Descrição:**  
O sistema deve permitir que o aluno ou responsável cancele uma presença
previamente confirmada a qualquer momento.

**Objetivo:**  
Permitir que imprevistos sejam refletidos na operação da rota.

**Stakeholders:**  
Aluno, responsável e motorista.

**Ator principal:**  
Aluno/responsável.

**Pré-condições:**  
Presença previamente confirmada.

**Entradas:**  
Aluno e solicitação de cancelamento.

**Processamento esperado:**  
O sistema deve alterar o status do aluno para ausente e registrar o cancelamento.

**Saídas/Resultados:**  
Presença cancelada.

**Pós-condições:**  
O aluno deixa de ser considerado na rota.

**Fluxos alternativos/exceções:**  
Nenhuma identificada.

**Regras de negócio relacionadas:**  
RN-006

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- O cancelamento pode ser realizado após uma confirmação.
- Após o cancelamento, o aluno deve ser marcado como ausente.

---

## RF-006 — Notificar motorista sobre cancelamento

**Título:**  
Aviso de cancelamento ao motorista.

**Descrição:**  
O sistema deve notificar o motorista responsável quando um aluno
cancelar a utilização do transporte.

**Objetivo:**  
Manter o motorista informado sobre alterações na rota.

**Stakeholders:**  
Motorista, aluno e responsável.

**Ator principal:**  
Sistema.

**Pré-condições:**  
Existência de uma presença previamente confirmada e posteriormente cancelada.

**Entradas:**  
Cancelamento do aluno e rota correspondente.

**Processamento esperado:**  
O sistema deve identificar o motorista da rota e enviar uma notificação.

**Saídas/Resultados:**  
Motorista notificado.

**Pós-condições:**  
Cancelamento registrado como comunicado.

**Fluxos alternativos/exceções:**  
Nenhuma identificada.

**Regras de negócio relacionadas:**  
RN-006, RN-007

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- Todo cancelamento de presença confirmada gera uma notificação ao motorista correspondente.

---

## RF-007 — Gerar rota otimizada

**Título:**  
Geração dinâmica da rota diária.

**Descrição:**  
O sistema deve gerar a rota do motorista considerando apenas os alunos
com presença confirmada e a localização inicial identificada do motorista.

**Objetivo:**  
Reduzir deslocamentos desnecessários e otimizar o percurso.

**Stakeholders:**  
Motorista e empresa de transporte.

**Ator principal:**  
Sistema.

**Pré-condições:**  
- Prazo de confirmação encerrado.
- Pontos dos alunos cadastrados.
- Localização inicial do motorista disponível.

**Entradas:**  
Alunos confirmados, pontos de parada e localização inicial do motorista.

**Processamento esperado:**  
O sistema deve calcular uma rota otimizada contendo somente os pontos
dos alunos confirmados.

**Saídas/Resultados:**  
Rota do dia disponibilizada ao motorista.

**Pós-condições:**  
Rota pronta para início do trajeto.

**Fluxos alternativos/exceções:**  
- Nenhum aluno confirmado: nenhuma parada de aluno será gerada.

**Regras de negócio relacionadas:**  
RN-004, RN-005, RN-012

**Prioridade:**  
Crítica

**Status:**  
Proposto

**Critérios de aceite:**  
- Alunos ausentes não aparecem como parada.
- Todos os alunos confirmados aparecem na rota.
- A localização inicial do motorista é considerada no cálculo.

---

## RF-008 — Recalcular rota após cancelamento

**Título:**  
Recálculo dinâmico da rota.

**Descrição:**  
O sistema deve recalcular a rota quando um aluno presente nela cancelar
a utilização do transporte.

**Objetivo:**  
Evitar deslocamentos para pontos que não precisam mais ser atendidos.

**Stakeholders:**  
Motorista e empresa de transporte.

**Ator principal:**  
Sistema.

**Pré-condições:**  
- Rota já gerada.
- Aluno presente na rota realizou cancelamento.

**Entradas:**  
Rota atual, cancelamento e alunos ainda confirmados.

**Processamento esperado:**  
O sistema deve remover o ponto cancelado e calcular novamente o percurso.

**Saídas/Resultados:**  
Nova rota disponibilizada ao motorista.

**Pós-condições:**  
Motorista passa a visualizar a rota atualizada.

**Fluxos alternativos/exceções:**  
- Caso não restem alunos confirmados, a rota ficará sem paradas de alunos.

**Regras de negócio relacionadas:**  
RN-005, RN-006, RN-008

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- O aluno cancelado não permanece na rota.
- Os demais alunos confirmados continuam presentes.
- A nova rota é disponibilizada ao motorista.

---

## RF-009 — Registrar embarque

**Título:**  
Check-in de embarque.

**Descrição:**  
O sistema deve permitir que o motorista registre o embarque do aluno.

**Objetivo:**  
Registrar que o aluno entrou na van e permitir o acompanhamento pelo responsável.

**Stakeholders:**  
Motorista, aluno e responsável.

**Ator principal:**  
Motorista.

**Pré-condições:**  
- Rota ativa.
- Aluno confirmado para o transporte.

**Entradas:**  
Aluno, data, horário e localização.

**Processamento esperado:**  
O sistema deve registrar o embarque do aluno.

**Saídas/Resultados:**  
Aluno marcado como embarcado.

**Pós-condições:**  
Registro de embarque armazenado.

**Fluxos alternativos/exceções:**  
- Aluno ausente não deve possuir check-in esperado.

**Regras de negócio relacionadas:**  
RN-010

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- O motorista consegue registrar o embarque.
- Data e horário são armazenados.
- O status do aluno muda para embarcado.

---

## RF-010 — Registrar desembarque

**Título:**  
Check-in de desembarque.

**Descrição:**  
O sistema deve permitir que o motorista registre o desembarque do aluno
após seu embarque.

**Objetivo:**  
Registrar a chegada do aluno ao destino.

**Stakeholders:**  
Motorista, aluno e responsável.

**Ator principal:**  
Motorista.

**Pré-condições:**  
Embarque previamente registrado para o mesmo trajeto.

**Entradas:**  
Aluno, data, horário e localização.

**Processamento esperado:**  
O sistema deve validar o embarque anterior e registrar o desembarque.

**Saídas/Resultados:**  
Aluno marcado como desembarcado.

**Pós-condições:**  
Registro de desembarque armazenado.

**Fluxos alternativos/exceções:**  
- Sem embarque registrado: impedir ou alertar sobre o registro inválido.

**Regras de negócio relacionadas:**  
RN-010, RN-011

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- Não permitir desembarque válido sem embarque anterior.
- Data e horário são registrados.

---

## RF-011 — Notificar responsável sobre embarque e desembarque

**Título:**  
Notificação de movimentação do aluno.

**Descrição:**  
O sistema deve notificar o responsável quando o motorista registrar
o embarque ou desembarque do aluno.

**Objetivo:**  
Informar automaticamente ao responsável a situação do aluno.

**Stakeholders:**  
Responsável, motorista e aluno.

**Ator principal:**  
Sistema.

**Pré-condições:**  
Check-in de embarque ou desembarque registrado.

**Entradas:**  
Registro de check-in e responsável vinculado.

**Processamento esperado:**  
O sistema deve identificar o responsável correspondente e enviar a notificação.

**Saídas/Resultados:**  
Notificação enviada ao responsável.

**Pós-condições:**  
Evento registrado como comunicado.

**Regras de negócio relacionadas:**  
RN-002, RN-009, RN-010

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- Embarque gera notificação.
- Desembarque gera notificação.
- Apenas os responsáveis vinculados ao aluno recebem o aviso.

---

## RF-012 — Emitir aviso geral de atraso

**Título:**  
Comunicação de atraso da rota.

**Descrição:**  
O sistema deve permitir que o motorista envie um aviso de atraso
simultaneamente aos responsáveis vinculados à rota ativa.

**Objetivo:**  
Evitar comunicação individual por aplicativos externos.

**Stakeholders:**  
Motorista, responsável e aluno.

**Ator principal:**  
Motorista.

**Pré-condições:**  
Rota ativa.

**Entradas:**  
Aviso de atraso e, quando informado, motivo ou nova previsão.

**Processamento esperado:**  
O sistema deve identificar os responsáveis da rota e enviar o aviso.

**Saídas/Resultados:**  
Notificações de atraso enviadas.

**Pós-condições:**  
Aviso registrado na rota.

**Fluxos alternativos/exceções:**  
Nenhuma identificada.

**Regras de negócio relacionadas:**  
RN-002, RN-012

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- O motorista não precisa selecionar cada responsável individualmente.
- Apenas os responsáveis vinculados à rota recebem o aviso.

---

## RF-013 — Trocar mensagens pelo chat

**Título:**  
Chat entre usuários vinculados à rota.

**Descrição:**  
O sistema deve permitir a troca de mensagens entre motorista,
responsáveis e alunos autorizados da mesma rota.

**Objetivo:**  
Centralizar a comunicação relacionada ao transporte no VanTrack.

**Stakeholders:**  
Motorista, responsável e aluno.

**Ator principal:**  
Motorista, responsável ou aluno.

**Pré-condições:**  
Usuário vinculado à rota.

**Entradas:**  
Mensagem e participante autorizado.

**Processamento esperado:**  
O sistema deve armazenar e entregar mensagens apenas entre usuários
autorizados daquela rota.

**Saídas/Resultados:**  
Mensagem entregue e registrada.

**Pós-condições:**  
Histórico da conversa atualizado.

**Fluxos alternativos/exceções:**  
- Usuário sem vínculo com a rota não poderá acessar a conversa.

**Regras de negócio relacionadas:**  
RN-001, RN-002

**Prioridade:**  
Média

**Status:**  
Proposto

**Critérios de aceite:**  
- Usuários sem vínculo não acessam o chat.
- Mensagens enviadas ficam disponíveis no histórico.