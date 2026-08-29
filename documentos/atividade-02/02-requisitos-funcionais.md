# Requisitos Funcionais — VanTrack

Os requisitos funcionais descrevem as funcionalidades que o sistema
deve disponibilizar para atender às regras de negócio do VanTrack.

---

## RF-001 — Vincular usuário à empresa

**Título:**  
Vinculação por código de acesso.

**Descrição:**  
O sistema deve permitir que o usuário se vincule à empresa de transporte
por meio de um código fornecido pela empresa.

**Objetivo:**  
Garantir que somente usuários autorizados tenham acesso às vans,
rotas e alunos correspondentes.

**Stakeholders:**  
Responsável, aluno e empresa de transporte.

**Ator principal:**  
Responsável/aluno.

**Pré-condições:**  
- Usuário cadastrado no sistema.

**Entradas:**  
Código de vinculação.

**Processamento esperado:**  
O sistema deve validar o código informado e, caso seja válido,
associar o usuário à empresa, van e/ou aluno correspondente.

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
- Um código válido deve vincular o usuário à empresa, van e/ou aluno correspondente.
- Um código inválido, expirado ou desativado não deve permitir a vinculação.
- O usuário não deve receber acesso a alunos não vinculados.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

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
- Usuário sem autorização: bloquear a visualização.

**Regras de negócio relacionadas:**  
RN-002, RN-003, RN-012

**Prioridade:**  
Crítica

**Status:**  
Proposto

**Critérios de aceite:**  
- Apenas usuários autorizados devem visualizar a localização da van.
- A atualização da localização deve respeitar o intervalo definido no RNF-001.
- Em caso de perda de conectividade, deve ser exibida a última localização conhecida conforme RNF-003.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

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
Localização da van, localização do ponto e limite de proximidade configurado.

**Processamento esperado:**  
O sistema deve calcular a estimativa de chegada da van e disparar uma
notificação quando atingir o limite de proximidade configurado.

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
- A notificação deve ser disparada automaticamente.
- A mesma aproximação não deve gerar notificações duplicadas.
- Somente o responsável/aluno correspondente deve receber o aviso.
- A notificação deve utilizar o limite de proximidade configurado.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

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
- Confirmações realizadas dentro do prazo devem ser registradas.
- Aluno não confirmado no prazo deve ser considerado ausente.
- Alunos ausentes não devem ser incluídos na rota.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

---

## RF-005 — Cancelar utilização do transporte

**Título:**  
Cancelamento de presença.

**Descrição:**  
O sistema deve permitir que o aluno ou responsável cancele uma presença
previamente confirmada, desde que o embarque ainda não tenha sido registrado.

**Objetivo:**  
Permitir que imprevistos sejam refletidos na operação da rota.

**Stakeholders:**  
Aluno, responsável e motorista.

**Ator principal:**  
Aluno/responsável.

**Pré-condições:**  
- Presença previamente confirmada.
- Embarque ainda não registrado.

**Entradas:**  
Aluno e solicitação de cancelamento.

**Processamento esperado:**  
O sistema deve alterar o status do aluno para ausente e registrar
a data e o horário do cancelamento.

**Saídas/Resultados:**  
Presença cancelada.

**Pós-condições:**  
O aluno deixa de ser considerado na rota.

**Fluxos alternativos/exceções:**  
- Caso o embarque já tenha sido registrado, o sistema não deve permitir o cancelamento.

**Regras de negócio relacionadas:**  
RN-006

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- O cancelamento deve ser permitido enquanto não existir embarque registrado.
- Após o cancelamento, o aluno deve ser marcado como ausente.
- O cancelamento não deve ser permitido após o registro de embarque.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

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
- Existência de uma presença previamente confirmada.
- Presença posteriormente cancelada.

**Entradas:**  
Cancelamento do aluno e rota correspondente.

**Processamento esperado:**  
O sistema deve identificar o motorista responsável pela rota e enviar
uma notificação sobre o cancelamento.

**Saídas/Resultados:**  
Motorista notificado.

**Pós-condições:**  
Cancelamento registrado como comunicado.

**Fluxos alternativos/exceções:**  
Nenhum identificado.

**Regras de negócio relacionadas:**  
RN-006, RN-007

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- Todo cancelamento válido de presença confirmada deve gerar uma notificação ao motorista correspondente.
- A notificação deve identificar o aluno cujo transporte foi cancelado.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

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
- Pontos de parada dos alunos cadastrados.
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
- Nenhum aluno confirmado: nenhuma parada de aluno deve ser gerada.

**Regras de negócio relacionadas:**  
RN-004, RN-005, RN-012

**Prioridade:**  
Crítica

**Status:**  
Proposto

**Critérios de aceite:**  
- Alunos ausentes não devem aparecer como parada.
- Todos os alunos confirmados devem aparecer na rota.
- A localização inicial do motorista deve ser considerada no cálculo.
- A rota deve ser disponibilizada ao motorista antes do início do trajeto.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

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
- Aluno presente na rota realizou um cancelamento válido.

**Entradas:**  
Rota atual, cancelamento, alunos ainda confirmados e localização atual da van.

**Processamento esperado:**  
O sistema deve remover o ponto correspondente ao aluno cancelado e
recalcular o percurso a partir da localização atual da van, considerando
os alunos ainda confirmados.

**Saídas/Resultados:**  
Nova rota disponibilizada ao motorista.

**Pós-condições:**  
O motorista passa a visualizar a rota atualizada.

**Fluxos alternativos/exceções:**  
- Caso não restem alunos confirmados, a rota ficará sem paradas de alunos.

**Regras de negócio relacionadas:**  
RN-005, RN-006, RN-008

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- O aluno cancelado não deve permanecer na rota.
- Os demais alunos confirmados devem continuar presentes.
- O recálculo deve considerar a localização atual da van.
- A nova rota deve ser disponibilizada ao motorista.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

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
O sistema deve registrar o embarque do aluno com data, horário e
localização, quando disponível.

**Saídas/Resultados:**  
Aluno marcado como embarcado.

**Pós-condições:**  
Registro de embarque armazenado.

**Fluxos alternativos/exceções:**  
- Aluno ausente não deve possuir check-in esperado.
- Sem conectividade no momento do registro: o check-in deve ser armazenado localmente no dispositivo do motorista e sincronizado automaticamente ao reconectar, sem bloquear o registro.

**Regras de negócio relacionadas:**  
RN-010, RN-015

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- O motorista deve conseguir registrar o embarque.
- Data e horário do embarque devem ser armazenados.
- A localização do embarque deve ser armazenada quando disponível.
- O status do aluno deve ser alterado para embarcado.
- Um check-in registrado offline deve ser sincronizado automaticamente ao reconectar, sem perda de dados.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

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
- Embarque previamente registrado para o mesmo trajeto.

**Entradas:**  
Aluno, data, horário e localização.

**Processamento esperado:**  
O sistema deve validar o embarque anterior e registrar o desembarque
com data, horário e localização, quando disponível.

**Saídas/Resultados:**  
Aluno marcado como desembarcado.

**Pós-condições:**  
Registro de desembarque armazenado.

**Fluxos alternativos/exceções:**  
- Sem embarque previamente registrado, o sistema não deve permitir o registro válido do desembarque.
- Sem conectividade no momento do registro: o check-in deve ser armazenado localmente no dispositivo do motorista e sincronizado automaticamente ao reconectar, sem bloquear o registro.

**Regras de negócio relacionadas:**  
RN-010, RN-011, RN-015

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- O sistema não deve permitir um desembarque válido sem embarque anterior.
- Data e horário do desembarque devem ser armazenados.
- A localização do desembarque deve ser armazenada quando disponível.
- O status do aluno deve ser alterado para desembarcado.
- Um check-in registrado offline deve ser sincronizado automaticamente ao reconectar, sem perda de dados.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

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
- Check-in de embarque ou desembarque registrado.
- Responsável vinculado ao aluno.

**Entradas:**  
Registro de check-in e responsável vinculado.

**Processamento esperado:**  
O sistema deve identificar os responsáveis vinculados ao aluno e enviar
a notificação correspondente ao evento registrado.

**Saídas/Resultados:**  
Notificação enviada ao responsável.

**Pós-condições:**  
Evento registrado como comunicado.

**Fluxos alternativos/exceções:**  
Nenhum identificado.

**Regras de negócio relacionadas:**  
RN-002, RN-009, RN-010

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- O registro de embarque deve gerar uma notificação.
- O registro de desembarque deve gerar uma notificação.
- Apenas os responsáveis vinculados ao aluno devem receber o aviso.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

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
- Rota ativa.

**Entradas:**  
Aviso de atraso e, quando informado, motivo ou nova previsão.

**Processamento esperado:**  
O sistema deve identificar os responsáveis vinculados aos alunos da rota
ativa e enviar o aviso simultaneamente.

**Saídas/Resultados:**  
Notificações de atraso enviadas.

**Pós-condições:**  
Aviso registrado na rota.

**Fluxos alternativos/exceções:**  
Atraso abaixo do limiar mínimo configurado: não é necessário aviso manual (aplica-se principalmente ao disparo automático do RF-015).

**Regras de negócio relacionadas:**  
RN-002, RN-012, RN-014

**Prioridade:**  
Alta

**Status:**  
Proposto

**Critérios de aceite:**  
- O motorista não deve precisar selecionar cada responsável individualmente.
- Apenas os responsáveis vinculados à rota ativa devem receber o aviso.
- O aviso deve ser enviado a todos os responsáveis correspondentes em uma única ação do motorista.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

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
- Usuário vinculado à rota.

**Entradas:**  
Mensagem e participante autorizado.

**Processamento esperado:**  
O sistema deve armazenar e entregar mensagens apenas entre usuários
autorizados e vinculados à mesma rota.

**Saídas/Resultados:**  
Mensagem entregue e registrada.

**Pós-condições:**  
Histórico da conversa atualizado.

**Fluxos alternativos/exceções:**  
- Usuário sem vínculo com a rota não poderá acessar a conversa.
- Responsável tenta acessar conversa de van à qual seu aluno não está vinculado: o sistema deve bloquear o acesso.

**Regras de negócio relacionadas:**  
RN-001, RN-002, RN-013

**Prioridade:**  
Média

**Status:**  
Proposto

**Critérios de aceite:**  
- Usuários sem vínculo com a rota não devem acessar o chat correspondente.
- Mensagens enviadas devem permanecer disponíveis no histórico.
- Apenas usuários autorizados da mesma rota devem participar da conversa.
- Um responsável não deve visualizar ou enviar mensagens em conversas de outros responsáveis, mesmo vinculados à mesma van.
- O aviso geral de atraso (RF-012) é uma transmissão do motorista para todos os responsáveis, não configurando conversa privada entre responsáveis.

**Casos de uso relacionados:**  
Não definido nesta etapa.

**Tarefas relacionadas:**  
Não definido nesta etapa.

**Casos de teste relacionados:**  
Não definido nesta etapa.

## RF-014 — Vincular motorista à van

**Título:**
Vinculação e substituição de motorista responsável.

**Descrição:**
O sistema deve permitir vincular um motorista responsável a uma van, encerrando automaticamente qualquer vínculo ativo anterior antes de ativar o novo.

**Objetivo:**
Garantir que cada van tenha exatamente um motorista ativo por vez, com rastreabilidade de quem opera o veículo.

**Stakeholders:**
Motorista e empresa de transporte.

**Ator principal:**
Empresa de transporte.

**Pré-condições:**

* Van cadastrada no sistema.
* Motorista cadastrado no sistema.

**Entradas:**
Van, motorista e data/horário de início do vínculo.

**Processamento esperado:**
O sistema deve encerrar o vínculo ativo anterior da van (se existir), registrando a data/horário de encerramento, e então ativar o novo vínculo motorista–van.

**Saídas/Resultados:**
Vínculo motorista–van ativo atualizado.

**Pós-condições:**
A van passa a ter um único motorista ativo.

**Fluxos alternativos/exceções:**

* Tentativa de ativar um segundo motorista sem encerrar o vínculo anterior: o sistema deve encerrar automaticamente o vínculo anterior antes de ativar o novo.

**Regras de negócio relacionadas:**
RN-012

**Prioridade:**
Média

**Status:**
Proposto

**Critérios de aceite:**

* Uma van não deve possuir mais de um motorista ativo simultaneamente.
* Ao vincular um novo motorista, o vínculo anterior deve ser encerrado antes da ativação do novo.
* O histórico de vínculos (motorista, van, período) deve ficar registrado.

**Casos de uso relacionados:**
Não definido nesta etapa.

**Tarefas relacionadas:**
Não definida nesta etapa.

**Casos de teste relacionados:**
Não definido nesta etapa.

## RF-015 — Detectar atraso automático da rota

**Título:**
Detecção automática de desvio de horário.

**Descrição:**
O sistema deve comparar o horário previsto de chegada com o horário real/estimado da van e, ao ultrapassar um limiar configurado, disparar automaticamente o aviso de atraso (RF-012).

**Objetivo:**
Reduzir a dependência do acionamento manual do motorista para avisos de atraso.

**Stakeholders:**
Motorista, responsável, aluno e empresa de transporte.

**Ator principal:**
Sistema.

**Pré-condições:**

* Rota ativa.
* Limiar mínimo de atraso configurado.

**Entradas:**
Horário previsto, horário real/estimado e limiar configurado.

**Processamento esperado:**
O sistema deve calcular o desvio entre horário previsto e real e, se o desvio ultrapassar o limiar configurado, disparar o fluxo de notificação de atraso (RF-012) automaticamente.

**Saídas/Resultados:**
Aviso de atraso disparado automaticamente, quando aplicável.

**Pós-condições:**
Atraso automático registrado como comunicado.

**Fluxos alternativos/exceções:**

* Desvio abaixo do limiar configurado: nenhuma notificação deve ser gerada.

**Regras de negócio relacionadas:**
RN-014

**Prioridade:**
Alta

**Status:**
Proposto

**Critérios de aceite:**

* Um desvio acima do limiar configurado deve disparar a notificação automaticamente, sem ação do motorista.
* Um desvio abaixo do limiar não deve gerar notificação.
* O motorista deve poder complementar o motivo do atraso após o disparo automático.

**Casos de uso relacionados:**
Não definido nesta etapa.

**Tarefas relacionadas:**
Não definida nesta etapa.

**Casos de teste relacionados:**
Não definido nesta etapa.

## RF-016 — Cadastrar aluno menor de idade

**Título:**
Cadastro de aluno menor com autorização do responsável legal.

**Descrição:**
O sistema deve permitir o cadastro de um aluno menor de idade, mas somente concluir e ativar esse cadastro após o registro da autorização do responsável legal.

**Objetivo:**
Garantir conformidade com a LGPD no tratamento de dados de menores.

**Stakeholders:**
Responsável legal, aluno e empresa de transporte.

**Ator principal:**
Responsável legal.

**Pré-condições:**

* Aluno identificado como menor de idade no cadastro.

**Entradas:**
Dados do aluno, indicador de menoridade e autorização do responsável legal.

**Processamento esperado:**
O sistema deve bloquear a ativação do cadastro do aluno menor até que a autorização do responsável legal seja registrada.

**Saídas/Resultados:**
Cadastro do aluno ativado somente após autorização registrada.

**Pós-condições:**
Aluno menor apto a ser vinculado a uma van/rota.

**Fluxos alternativos/exceções:**

* Aluno maior de idade: depende apenas do próprio consentimento, sem exigir esta autorização.

**Regras de negócio relacionadas:**
RN-016, RN-009

**Prioridade:**
Crítica

**Status:**
Proposto

**Critérios de aceite:**

* O cadastro de um aluno menor não deve ser ativado sem autorização do responsável legal registrada.
* Alunos maiores de idade não devem exigir essa autorização.
* Nenhuma coleta de dado pessoal ou de localização do menor deve ocorrer antes da autorização.

**Casos de uso relacionados:**
Não definido nesta etapa.

**Tarefas relacionadas:**
Não definida nesta etapa.

**Casos de teste relacionados:**
Não definido nesta etapa.
