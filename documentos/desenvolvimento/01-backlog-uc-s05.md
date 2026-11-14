# Backlog — Desenvolvimento do UC-S05 Registrar Embarque

Caso de uso escolhido para implementação: **UC-S05 — Registrar Embarque**, com o
**UC-I02 — Notificar Responsável sobre Embarque/Desembarque** (`<<include>>`) e o
fluxo alternativo **A1 — Sem conectividade** (RNF-006).

Base da implementação (já modelada no 1º bimestre):

| Artefato | Onde |
|---|---|
| Caso de uso de sistema (UC-S05), essencial (UC-E02) e real (UC-R02) | [Casos de uso](../atividade-03/01-casos-de-uso.md) |
| Diagramas de sequência UC-S05, UC-R02 e UC-I02 | [Diagramas de sequência](../atividade-04/01-diagramas-de-sequencia.md) |
| Entidades Rota, Presença, Embarque, Notificação | [Mapa de dados](../atividade-01/03-mapa-dados.md) |
| Requisitos | RF-009, RF-011, RNF-002, RNF-005, RNF-006 |
| Regras de negócio | RN-002, RN-009, RN-010, RN-012 |

Duração: **1 sprint de 7 dias**, 5 membros (A a E). Preencham o nome de cada um na tabela
da seção 4. **Entrega final da disciplina: 02/12 às 19:31** (seção 11).

---

## 1. Escopo

**Dentro do escopo**

- Motorista abre a tela "Rota do dia" e vê só os alunos confirmados, na ordem da rota.
- Motorista toca em "Embarcou" e o embarque é salvo com data, horário e localização (quando disponível).
- Responsáveis vinculados ao aluno recebem o aviso de embarque (UC-I02).
- Sem conexão, o embarque fica salvo no aparelho, aparece como "Pendente de sincronização" e é enviado sozinho ao reconectar.

**Fora do escopo (substituído por dados de seed)**

| Pré-condição do UC-S05 | Como fica nesta entrega |
|---|---|
| Rota ativa (UC-S09 Gerar Rota Otimizada) | Rota do dia já criada no seed, com a ordem das paradas fixa |
| Presença confirmada (UC-S03) | Presenças já confirmadas no seed |
| Cadastro e vínculo (UC-C01, UC-S01, UC-ADM01) | Usuários, aluno–responsável e motorista–van já criados no seed |
| Login e cadastro de usuário | Login simples só com os usuários do seed |
| Mapa na tela da rota | Opcional; a lista de paradas é o suficiente para o caso de uso |

---

## 2. Combinados do Dia 1 (todos juntos, ~1h)

Sem isso as 5 frentes não andam em paralelo. Saiam da reunião com:

1. **Stack (definida)** — app em **Flutter** (Android, iOS e Web, RNF-004), API REST em
   **Dart com Dart Frog** e **Supabase usado só como banco PostgreSQL** (o app não acessa
   o Supabase direto). Detalhes e bibliotecas no "Contexto do projeto" de
   [02-prompts-llm.md](02-prompts-llm.md).
2. **Jira e branches (exigência da disciplina)** — no Jira: um **Epic** "UC-S05 Registrar
   Embarque", uma **Story** por história da seção 4 e uma **Task** por item `[ ]` da seção 4.
   Problemas achados nos testes viram **Bug**. **Cada task (ou bug) vira uma branch** no
   GitHub, no padrão do professor: `task-<número>-<descricao-curta>`
   (ex.: `task-18-endpoint-registrar-embarque`). Commits começam com a chave do Jira, e cada
   branch vira um PR para a `main`, revisado por outro membro. A lista completa de tasks,
   com donos, dias e dependências, está em [04-tasks-jira.md](04-tasks-jira.md) (e no CSV
   para importar no Jira).
3. **Contrato da API (seção 3)** — revisado e aprovado por todos. Quem consome a API
   começa com dados mockados seguindo esse contrato.
4. **Diagrama de classes e arquitetura (exigência da disciplina)** — o Membro B faz no Dia 1
   o diagrama de classes do UC-S05 e a organização em camadas e diretórios
   (`03-arquitetura.md`), e a equipe revisa no fim do dia. O código segue esse diagrama.
5. **Nomes das classes** — usar os mesmos dos diagramas de sequência
   (`EmbarqueController`, `EmbarqueService`, `Presenca`, `PresencaRepository`,
   `NotificacaoService`, `VinculoRepository`, `NotificacaoRepository`, `TelaRotaDoDia`,
   `ArmazenamentoLocal`). Isso mostra ao professor que o código segue o modelo.
6. **Dados do seed (seção 6)** — todos testam com os mesmos dados.

---

## 3. Contrato da API (rascunho para o Dia 1)

Autenticação simplificada: `GET /usuarios` lista os usuários do seed (nome e papel) para a
tela de login, e `POST /login` com o id e o papel de um deles devolve um token; as demais
rotas exigem o token no header `Authorization` e sabem quem é o usuário e o seu papel.

### `GET /rotas/{rotaId}/alunos`

Usado pela tela "Rota do dia". Só o motorista ativo da van da rota pode chamar (RN-012).
Alunos ausentes não aparecem (exceção da RN-010).

```json
[
  {
    "alunoId": 1,
    "nome": "Ana Souza",
    "ordem": 1,
    "pontoParada": { "endereco": "Rua X, 100", "latitude": -23.40, "longitude": -51.93 },
    "status": "CONFIRMADO"
  }
]
```

`status`: `CONFIRMADO` ou `EMBARCADO`.

### `POST /rotas/{rotaId}/embarques`

```json
{
  "registroId": "2b1f0c3e-...-uuid-gerado-no-aparelho",
  "alunoId": 1,
  "dataHora": "2026-11-16T06:42:10-03:00",
  "latitude": -23.40,
  "longitude": -51.93
}
```

- `registroId` é gerado no aparelho e torna o envio **idempotente**: se o mesmo registro
  chegar duas vezes (comum na sincronização offline), o servidor não duplica nem
  notifica de novo.
- `dataHora` é a do **momento do toque**, não a do envio. Assim o embarque feito offline
  guarda o horário real.
- `latitude`/`longitude` são opcionais ("quando disponível").

| Resposta | Quando |
|---|---|
| `201` `{ "alunoId": 1, "status": "EMBARCADO" }` | Embarque registrado |
| `200` (mesmo corpo) | `registroId` já processado antes |
| `403` | Usuário não é o motorista ativo da van (RN-012) |
| `404` | Rota ou aluno não existe |
| `409` | Aluno não está confirmado nessa rota ou já embarcou com outro `registroId` |

### `POST /rotas/{rotaId}/embarques/sincronizar`

Recebe `{ "registros": [ ...mesmo formato acima... ] }` e devolve o resultado de cada
registro (`registroId` + código). Internamente chama o mesmo `EmbarqueService`.

### `GET /notificacoes?desde={dataHora}`

Avisos do usuário logado (responsável). Só retorna avisos de alunos vinculados a ele (RN-002).

```json
[
  {
    "id": 10,
    "tipo": "EMBARQUE",
    "alunoNome": "Ana Souza",
    "mensagem": "Ana Souza embarcou na van às 06:42.",
    "dataHora": "2026-11-16T06:42:10-03:00",
    "lida": false
  }
]
```

### `PATCH /notificacoes/{id}/lida`

Marca o aviso como lido (chamado quando a tela "Avisos" exibe o aviso).

### Contrato interno do app: módulo de embarque (D ↔ E)

A tela (Membro D) nunca chama a API de embarque diretamente: ela usa este módulo.
O D cria a classe abstrata e a versão só online (`ModuloEmbarqueOnline`); o E cria uma
segunda implementação com a fila offline (`ModuloEmbarqueComFila`) e troca uma linha no
`main.dart`. **Ninguém muda a classe abstrata sem combinar.** Assim os dois trabalham em
paralelo sem mexer nos mesmos arquivos.

Arquivo `app/lib/embarque/aplicacao/modulo_embarque.dart`:

```dart
enum StatusEnvio { enviado, pendente }

class ResultadoEmbarque {
  final String registroId; // UUID gerado no aparelho
  final int alunoId;
  final DateTime dataHora; // momento do toque
  final StatusEnvio status;
  const ResultadoEmbarque(this.registroId, this.alunoId, this.dataHora, this.status);
}

class RegistroPendente {
  final String registroId;
  final int alunoId;
  final DateTime dataHora;
  const RegistroPendente(this.registroId, this.alunoId, this.dataHora);
}

/// Avisado quando um pendente sai da fila.
class EventoPendente {
  final String registroId;
  final int alunoId;
  final bool sincronizado; // true: servidor aceitou; false: servidor rejeitou
  final int? codigoHttp;   // preenchido quando rejeitado (ex.: 409)
  const EventoPendente(this.registroId, this.alunoId, this.sincronizado, [this.codigoHttp]);
}

/// Erro da API que a tela precisa mostrar (403, 404 ou 409). Nunca vai para a fila.
class EmbarqueException implements Exception {
  final int codigoHttp;
  final String mensagem;
  const EmbarqueException(this.codigoHttp, this.mensagem);
}

abstract class ModuloEmbarque {
  /// Captura data/hora e localização (opcional, até 2 s), gera o registroId e envia.
  /// Lança EmbarqueException em 403/404/409.
  Future<ResultadoEmbarque> registrarEmbarque(int rotaId, int alunoId);

  Future<List<RegistroPendente>> listarPendentes(int rotaId);

  Stream<EventoPendente> get aoMudarPendentes;
}
```

---

## 4. Divisão por membro

| Membro | Nome | Frente | Classes do diagrama |
|---|---|---|---|
| A | | Backend base, seed e integração | `Presenca`, `PresencaRepository`, `VinculoRepository` |
| B | | Diagrama de classes e backend do embarque | `EmbarqueController`, `EmbarqueService` |
| C | | Login simplificado e notificação ponta a ponta (UC-I02) | `NotificacaoService`, `NotificacaoRepository` |
| D | | App do motorista (UC-R02) | `TelaRotaDoDia` |
| E | | Modo offline e sincronização (A1, RNF-006) | `ArmazenamentoLocal` |

### Membro A — Backend base, seed e integração

**História:** Como equipe, queremos o projeto do servidor com o modelo de dados e os
dados de teste prontos, para que todas as frentes trabalhem sobre a mesma base.

Tarefas:

- [ ] Criar o projeto do backend e a conexão com o banco.
- [ ] Criar as entidades: Empresa, Van, Motorista, VínculoMotoristaVan, Responsável, Aluno,
      Vínculo aluno–responsável (N:N), PontoParada, Rota, Presença, Embarque.
- [ ] Criar o seed da seção 6.
- [ ] `GET /rotas/{rotaId}/alunos` (só confirmados, na ordem; só o motorista ativo).
- [ ] A partir do Dia 4: integrar as branches, rodar os testes de aceitação da seção 7 e
      montar o roteiro da demo. Cada falha encontrada vira um Bug no Jira.
- [ ] Dia 7: conferir as exigências da disciplina (seção 11) para a entrega.

Critérios de aceite:

- O seed cria tudo com um único comando.
- O aluno ausente do seed não aparece em `GET /rotas/{rotaId}/alunos`.
- Um motorista que não é o ativo da van recebe `403`.

Rastreabilidade: RN-002, RN-010 (exceção), RN-012, RNF-002.

### Membro B — Backend do embarque

**História:** Como motorista, quero registrar que o aluno entrou na van, para que o
embarque fique registrado com data, horário e local.

Tarefas:

- [ ] `EmbarqueController` com `POST /rotas/{rotaId}/embarques`.
- [ ] **Dia 1:** diagrama de classes do UC-S05 (com UC-I02 e o A1) e organização em camadas
      e diretórios, em `03-arquitetura.md`, para a equipe revisar no fim do dia.
- [ ] `EmbarqueService.registrarEmbarque`: busca a presença, chama
      `Presenca.registrarEmbarque()` (a própria entidade valida o status, RN-010) e salva.
- [ ] Validações: motorista ativo (RN-012), aluno confirmado na rota, sem embarque
      duplicado (`409`).
- [ ] Idempotência pelo `registroId`.
- [ ] `POST /rotas/{rotaId}/embarques/sincronizar` (lote, reaproveitando o service).
- [ ] Chamar `NotificacaoService.notificarMovimentacao(presenca, EMBARQUE)` depois de salvar
      (ponto do `<<include>>`; enquanto o C não termina, usar uma versão vazia).
- [ ] Testes unitários do `EmbarqueService` (um por linha da tabela de respostas).

Critérios de aceite:

- Embarque salvo com data/hora enviada pelo aparelho e localização quando informada.
- Mesmo `registroId` enviado duas vezes gera um único embarque e uma única notificação.
- Aluno não confirmado ou já embarcado retorna `409`.

- [ ] Dia 6: atualizar o diagrama de classes, a árvore de diretórios real e a
      rastreabilidade em `03-arquitetura.md`, conferindo se o código bate com o diagrama.

Rastreabilidade: RF-009, RN-010, RN-012, RNF-006 (lado do servidor).

### Membro C — Notificação ponta a ponta (UC-I02)

**História:** Como responsável, quero ser avisado quando meu filho embarcar, para saber
que ele está a caminho.

Tarefas:

- [ ] Entidade `Notificacao` (tipo do evento, destinatário, data/hora, lida).
- [ ] `NotificacaoService.notificarMovimentacao(presenca, tipo)`: busca os responsáveis do
      aluno, monta a mensagem com o horário, cria uma notificação por responsável e
      registra o evento como comunicado.
- [ ] Fluxo A1 do UC-I02: aluno maior sem responsável → não envia nada e retorna normalmente.
- [ ] `GET /notificacoes` filtrando pelo usuário logado (RN-002).
- [ ] Tela "Avisos" do responsável no app: lista os avisos e atualiza sozinha a cada
      ~10 s (polling).
- [ ] Dias 1–2: login simplificado (`GET /usuarios`, `POST /login` e o middleware que
      identifica o usuário e o papel). Os outros endpoints dependem dele.
- [ ] Dias 6–7: roteiro da demo e prints do Jira para as evidências.
- [ ] Extra, só se der tempo: push real (Firebase Cloud Messaging). Não é requisito para a entrega.

Critérios de aceite:

- O aluno com 2 responsáveis gera 2 notificações; o aluno maior sem responsável gera 0.
- Um responsável não vê aviso de aluno de outra família.
- O aviso aparece na tela do responsável em até ~10 s após o embarque.

Rastreabilidade: RF-011, RN-002, RN-009, RNF-002.

### Membro D — App do motorista (UC-R02)

**História:** Como motorista, quero registrar o embarque com um toque na tela da rota,
sem navegar pelo app enquanto dirijo.

Tarefas:

- [ ] Criar o projeto do app e a tela de login (escolher usuário do seed).
- [ ] Tela "Rota do dia": lista de paradas na ordem, com a próxima parada destacada.
- [ ] Botão grande "Embarcou" ao lado de cada aluno (uma única ação, RNF-005).
- [ ] Ao tocar: chamar `registrarEmbarque` do módulo de embarque (contrato na seção 3).
      O D cria a classe abstrata e a versão só online (`ModuloEmbarqueOnline`): captura
      data/hora e localização (no máximo 2 s; sem GPS, envia sem localização), gera o
      `registroId` e chama a API.
- [ ] Sucesso: check verde, mover o aluno para a seção "Na van" e destacar a próxima parada.
- [ ] Mostrar mensagens de erro (`403`, `409`).
- [ ] Começar com dados mockados no formato da seção 3 e trocar pela API no Dia 3.

Critérios de aceite:

- Registrar um embarque exige um toque, a partir da tela da rota.
- Depois do toque o aluno aparece em "Na van" e a próxima parada é destacada.
- Funciona no Android e na Web (RNF-004); iOS se alguém tiver como testar.

Rastreabilidade: RF-009, RNF-004, RNF-005, UC-R02.

### Membro E — Modo offline e sincronização (A1, RNF-006)

**História:** Como motorista, quero registrar o embarque mesmo sem sinal, para não ficar
travado em trechos sem cobertura.

Tarefas:

- [ ] `ArmazenamentoLocal`: fila persistente no aparelho (sobrevive a fechar o app).
- [ ] Detectar se há conexão; sem conexão, o toque em "Embarcou" vai para a fila em vez da API.
- [ ] Ícone "Pendente de sincronização" no aluno até o envio ser confirmado.
- [ ] Ao reconectar, enviar a fila para `POST .../embarques/sincronizar` e tirar da fila só o
      que o servidor confirmou (`201` ou `200`).
- [ ] Tentar de novo periodicamente enquanto houver pendentes (meta: até 5 min após reconectar).
- [ ] Criar `ModuloEmbarqueComFila`, outra implementação da classe abstrata do D
      (contrato na seção 3), que decide sozinha entre API e fila, e trocá-la no `main.dart`.
      O D continua dono da tela.

Critérios de aceite:

- Em modo avião o embarque é aceito e o aluno mostra "Pendente de sincronização".
- Ao reconectar, o embarque chega ao servidor com o **horário do toque** e o responsável
  só então recebe o aviso.
- Fechar e abrir o app offline não perde os pendentes.
- Uma falha no meio da sincronização não duplica embarques (graças ao `registroId`).

- [ ] Dia 6: revisar os documentos do 1º bimestre que a implementação mudou (mapa de
      dados, diagramas de sequência, regras e requisitos).

Rastreabilidade: RNF-006, fluxo A1 do UC-S05, exceção E1 do UC-R02.

---

## 5. Cronograma da semana

| Dia | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Reunião de combinados (seção 2) · projeto backend + entidades | Reunião · diagrama de classes e arquitetura (equipe revisa no fim do dia) | Reunião · tabela de notificação + login simplificado | Reunião · projeto do app + login | Reunião · estudo de armazenamento local e detecção de rede |
| 2 | Seed + `GET /rotas/{id}/alunos` | `POST /embarques` + validações | `NotificacaoService` + A1 | Tela "Rota do dia" com mock | Fila local com mock |
| 3 | Revisar PRs, ajudar quem travou | Idempotência + sincronizar em lote | `GET /notificacoes` | **Integração 1:** tela ligada na API real (caminho online) | Ligar a fila na tela do D |
| 4 | Integrar branches | Testes unitários + ligar no `NotificacaoService` real | Tela "Avisos" do responsável | Ajustes visuais, próxima parada | Sincronização automática ao reconectar |
| 5 | **Integração 2:** testes de aceitação (seção 7) com todos | Correções | Correções | Correções | Correções |
| 6–7 | Conferir as exigências da entrega (seção 11) | Diagrama de classes e arquitetura finais | Roteiro da demo e evidências do Jira | Folga / bônus (seção 9) | Revisão dos artefatos do 1º bimestre |

Ponto de controle diário de 15 min: o que fiz, o que vou fazer, onde travei.
Mover as tasks no quadro do Jira ao longo do dia; os prints servem de evidência.

---

## 6. Dados do seed

| Dado | Valor |
|---|---|
| Empresa | 1 empresa |
| Van | 1 van |
| Motoristas | 2: um **ativo** na van e um **sem vínculo** (para testar a RN-012) |
| Rota | Rota de **hoje**, trajeto "ida", situação ativa, com 4 paradas em ordem |
| Aluno 1 — Ana Souza | Menor, **2 responsáveis**, presença confirmada, parada 1 |
| Aluno 2 — Beatriz Reis | Menor, 1 responsável, presença confirmada, parada 2 |
| Aluno 3 — Carlos Lima | **Maior de idade sem responsável**, presença confirmada, parada 3 (A1 do UC-I02) |
| Aluno 4 — Bruno Alves | Menor, 1 responsável, **ausente** (não pode aparecer na lista) |
| Responsáveis | 4 (dois do Aluno 1, um do Aluno 2, um do Aluno 4) |

---

## 7. Testes de aceitação (roteiro da demo)

Cada teste aponta o fluxo do caso de uso que ele demonstra.

| # | Cenário | Resultado esperado | Fluxo / regra |
|---|---|---|---|
| 1 | Motorista ativo abre a rota | Vê os alunos 1, 2 e 3 na ordem; o aluno 4 não aparece | UC-S05 passo 1, RN-010 |
| 2 | Toca "Embarcou" no aluno 1 | Check verde, aluno em "Na van", próxima parada destacada | UC-S05 passos 2 a 4, UC-R02 |
| 3 | Os 2 responsáveis do aluno 1 abrem "Avisos" | Ambos veem o aviso com o horário | UC-I02 fluxo principal |
| 4 | Responsável do aluno 2 abre "Avisos" | Não vê o aviso do aluno 1 | RN-002 |
| 5 | Embarque do aluno 3 | Embarque salvo, nenhuma notificação criada | UC-I02 A1 |
| 6 | Tentar embarcar o aluno 1 de novo | Mensagem de que já embarcou | `409` |
| 7 | Motorista sem vínculo tenta abrir a rota | Acesso negado | RN-012 |
| 8 | Modo avião, embarcar o aluno 2 | Aceito, ícone "Pendente de sincronização" | UC-S05 A1, UC-R02 E1 |
| 9 | Fechar e abrir o app ainda offline | Pendente continua lá | RNF-006 |
| 10 | Reconectar | Sincroniza em até 5 min, horário salvo é o do toque, responsável recebe o aviso | UC-S05 A1, RNF-006 |

---

## 8. Riscos e plano B

| Risco | Plano B |
|---|---|
| Configurar push (FCM/APNs) consome a semana | Notificação in-app com polling (já é o plano principal) |
| Stack nova para parte da equipe | Escolher no Dia 1 a stack que a maioria já usou |
| Integração deixada para o fim | Integrações fixas nos Dias 3 e 5; contrato da API fechado no Dia 1 |
| GPS não funciona no navegador/emulador | Localização é opcional; enviar sem ela |
| Detecção de rede inconsistente na Web | Tratar falha de envio (timeout/erro de rede) como "offline" e mandar para a fila |
| Alguém trava na sua frente | O A fica livre a partir do Dia 3 para ajudar |
| Flutter Web bloqueado por CORS ao chamar a API | Middleware de CORS no backend desde o Dia 1 (Membro A) |
| App no emulador Android não acha `localhost` | Usar `--dart-define=API_URL=http://10.0.2.2:8080` |
| Um membro roda o seed e apaga os dados do outro | Cada um usa o próprio projeto gratuito no Supabase; um projeto compartilhado só para integração e demo |
| Senha do banco vazar no GitHub | `backend/.env` no `.gitignore`, só o `.env.example` vai para o repositório |
| Hora errada na mensagem (servidor em UTC) | Formatar HH:MM sempre em horário de Brasília (UTC-3) |

---

## 9. Bônus, se sobrar tempo

**UC-S06 — Registrar Desembarque.** Reaproveita quase tudo: mesma tela (botão "Desceu" na
seção "Na van"), mesmo service, mesma fila offline e o mesmo UC-I02 com tipo `DESEMBARQUE`.
A única regra nova é a RN-011 (só desembarca quem embarcou na mesma rota).

---

## 10. Interface do usuário

São 3 telas: login, "Rota do dia" (motorista) e "Avisos" (responsável). Todas precisam
funcionar em celular e no navegador (RNF-004).

### Princípios

- **O motorista está dirigindo.** Botões grandes (no mínimo 56 px de altura), texto grande,
  alto contraste, nenhuma navegação para registrar um embarque e **nenhum modal de
  confirmação**: um toque registra (RNF-005).
- **A cor diz o status**, sempre acompanhada de ícone e texto (não depender só da cor):

| Status do aluno | Cor | Ícone | Texto |
|---|---|---|---|
| Aguardando embarque | Neutro (cinza) | — | botão "Embarcou" |
| Embarcado e enviado | Verde | check | "Embarcou às 06:42" |
| Embarcado, pendente de envio | Âmbar | nuvem riscada | "Pendente de sincronização" |

- **Sem conexão é sempre visível**: faixa no topo da tela, nunca escondida (RNF-003).

### Tela 1 — Login

Lista dos usuários do seed, cada um com nome e papel (motorista ou responsável).
Um toque entra. O app abre a "Rota do dia" para motorista e "Avisos" para responsável.

### Tela 2 — Rota do dia (motorista, UC-R02)

```text
┌──────────────────────────────────┐
│ Rota do dia · Ida · 06:30        │
│ Van ABC-1D23        2 de 3 na van│
├──────────────────────────────────┤
│ [faixa âmbar, só sem conexão]    │
│ Sem conexão. Os embarques serão  │
│ enviados quando o sinal voltar.  │
├──────────────────────────────────┤
│ PRÓXIMA PARADA                   │
│ ┌──────────────────────────────┐ │
│ │ 3  Carlos Lima               │ │
│ │    Rua das Flores, 210       │ │
│ │ ┌──────────────────────────┐ │ │
│ │ │        EMBARCOU          │ │ │  <- botão principal, largura total
│ │ └──────────────────────────┘ │ │
│ └──────────────────────────────┘ │
│ DEPOIS                           │
│ (demais paradas, botão menor)    │
├──────────────────────────────────┤
│ NA VAN (2)                       │
│ ✓ Ana Souza     Embarcou às 06:42│  <- verde
│ ☁ Beatriz Reis  Pendente de      │  <- âmbar
│                 sincronização    │
└──────────────────────────────────┘
```

Comportamento:

- A "Próxima parada" é o primeiro aluno da ordem que ainda não embarcou.
- Ao tocar "Embarcou": o aluno vai na hora para "Na van" (verde ou âmbar, conforme o
  módulo devolver `StatusEnvio.enviado` ou `StatusEnvio.pendente`) e a próxima parada passa a ser destacada.
- Quando todos embarcam: mensagem "Todos os alunos embarcaram".
- Quando um pendente sincroniza, o ícone muda de âmbar para verde sem recarregar a tela.
- Os outros alunos da lista também têm o botão "Embarcou" (o aluno pode embarcar fora
  da ordem), só que menor.

Mensagens:

| Situação | Mensagem |
|---|---|
| Carregando | "Carregando a rota…" |
| `403` | "Você não é o motorista ativo desta van." (tela inteira, sem lista) |
| `409` | "Ana Souza já embarcou." (aviso rápido no rodapé) |
| Lista vazia | "Nenhum aluno confirmado para esta rota." |
| Erro inesperado | "Não foi possível registrar. Tente de novo." |

### Tela 3 — Avisos (responsável, UC-I02)

```text
┌──────────────────────────────────┐
│ Avisos                           │
│ Atualizado há 5 s                │
├──────────────────────────────────┤
│ ┌──────────────────────────────┐ │
│ │ Ana Souza                    │ │
│ │ ● Na van desde 06:42         │ │  <- verde
│ └──────────────────────────────┘ │
├──────────────────────────────────┤
│ HOJE                             │
│ • Ana Souza embarcou na van      │  <- não lido: ponto azul
│   às 06:42.           há 2 min   │
└──────────────────────────────────┘
```

Comportamento:

- Um card por aluno do responsável, com o status atual derivado dos avisos:
  "● Na van desde 06:42" (verde) ou "○ Aguardando embarque" (cinza).
- Lista dos avisos do dia, do mais novo para o mais antigo; não lidos com um ponto.
- Atualiza sozinha a cada ~10 s; "Atualizado há X s" mostra quando foi a última vez.
- Sem conexão: faixa "Sem conexão. Os avisos podem estar desatualizados. Última
  atualização às 06:40." (RNF-003).
- Sem avisos: "Nenhum aviso hoje. Você será avisado quando o aluno embarcar."

---

## 11. Exigências da disciplina

Fonte: README do repositório da disciplina e a atividade "Lista Master Class — Diagrama de
Classes UML e Organização da Arquitetura de Software" (2º bimestre).

| Exigência do professor | Onde é atendida |
|---|---|
| Entrega até **02/12 às 19:31** | Esta sprint + dias de folga |
| 1 caso de uso, que não seja login nem relatório | UC-S05 Registrar Embarque (o login é só um apoio simplificado) |
| Regras de negócio, requisitos (RF e RNF), definição do UC e diagrama de sequência do UC | Já feitos no 1º bimestre (atividades 02, 03 e 04); revisar o que mudar na implementação |
| **Diagrama de classes** do UC | `03-arquitetura.md`, feito pelo Membro B no Dia 1 |
| Interface gráfica, back-end (API REST) e banco de dados | App Flutter, API em Dart Frog, PostgreSQL no Supabase |
| Arquitetura em camadas (apresentação, aplicação, domínio, infraestrutura) e estrutura de diretórios justificada | `03-arquitetura.md` e regras do "Contexto do projeto" em `02-prompts-llm.md` |
| Contrato do repositório separado da implementação na infraestrutura | Repositórios como classe abstrata no domínio + implementação Postgres na infraestrutura |
| Entidades com comportamento (evitar classes anêmicas) | Ex.: `Presenca.registrarEmbarque()` valida o próprio status (RN-010), como no diagrama de sequência |
| Rastreabilidade RN → RF → UC → classes | Comentário de documentação em cada classe principal + tabela em `03-arquitetura.md` |
| Jira em ciclos de 7 dias com epic, story, task e bug | Seção 2, item 2 |
| Cada task do Jira vira uma branch no GitHub | Seção 2, item 2 (`task-<número>-<descricao-curta>`) |
| "Melhorias em todo o projeto" | Revisar os documentos do 1º bimestre que a implementação mudar (ex.: mapa de dados, sequência) |
