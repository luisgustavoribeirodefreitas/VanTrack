# Tasks do Jira — UC-S05 Registrar Embarque

Plano de todas as tasks da sprint, por membro, pronto para cadastrar no Jira. Detalhes de cada frente no [backlog](01-backlog-uc-s05.md) e os prompts em [02-prompts-llm.md](02-prompts-llm.md).

> Arquivo gerado junto com [04-tasks-jira.csv](04-tasks-jira.csv), que importa tudo de uma vez no Jira.

---

## 1. Como montar no Jira

**Hierarquia.** O professor pede *Epic > Story > (Task == Bug)*. No Jira, uma Task comum fica no mesmo nível da Story e não pode ficar dentro dela; o que fica dentro de uma Story é a **Subtarefa**. Então:

| Professor | Tipo no Jira | Quantidade |
|---|---|---|
| Epic | Epic | 1 (UC-S05) |
| Story | História (Story) | 7 (S0 a S6) |
| Task | Subtarefa, dentro da Story | 47 |
| Bug | Bug (ou Subtarefa com o rótulo `bug`), criado durante os testes | conforme aparecer |

**Importar pelo CSV** (Jira Cloud: Configurações → Sistema → Importação externa → CSV, ou no projeto: ⋯ → Importar itens):

1. Envie o `04-tasks-jira.csv` (codificação UTF-8).
2. Mapeie as colunas: `Issue ID` → *ID do item*, `Parent ID` → *ID do pai* (ou *Parent*), `Issue Type` → *Tipo de item*, `Summary` → *Resumo*, `Description` → *Descrição*, `Labels` → *Rótulos*.
3. Se o Jira estiver em português, mapeie os valores do tipo: `Epic` → Epic, `Story` → História, `Subtask` → Subtarefa.
4. Depois da importação, atribua cada subtarefa ao membro pelo rótulo (`membro-a` a `membro-e`) e coloque tudo na sprint.

Se a importação der problema, cadastre à mão a partir das tabelas abaixo: o resumo de cada task começa com o código (ex.: `[A-01]`), e a descrição completa está na seção 5.

**Sprint.** Os ciclos do professor são de 7 dias, começando em 04/11. Sugestão: esta sprint de **18/11 a 24/11**, deixando 25/11 a 01/12 para bugs e documentação antes da entrega de **02/12 às 19:31**. "Dia 1" nas tabelas é o primeiro dia da sprint.

**Branch.** Cada subtarefa (e cada bug) vira uma branch no padrão do professor: `task-<número do Jira>-<descrição>`. A coluna "Branch sugerida" já traz a descrição; troque `<nº>` pelo número que o Jira gerar (ex.: `task-18-cors`).

**Prompt.** Para cada task, mande para a LLM: contexto do projeto + prompt do seu membro + `Task desta conversa: <CHAVE> — <resumo>`.

---

## 2. Definição de pronto (vale para todas as tasks)

- Código segue o diagrama de classes e as camadas de 03-arquitetura.md
- Testes da task escritos e passando
- Classes principais com comentário de responsabilidade e RN/RF/UC
- PR da branch revisado e aprovado por outro membro antes do merge na main
- Critérios de aceite conferidos por quem revisou

---

## 3. Resumo por membro

| Membro | Frente | Tasks | Horas estimadas |
|---|---|---|---|
| A | Backend base, seed e integração | 12 | 27 h |
| B | Diagrama de classes e backend do embarque | 12 | 27 h |
| C | Login e notificação ponta a ponta (UC-I02) | 8 | 23 h |
| D | App do motorista (UC-R02) | 8 | 23 h |
| E | Modo offline e sincronização (A1, RNF-006) | 7 | 23 h |
| **Total** | | **47** | **123 h** |

As horas são uma estimativa para equilibrar a divisão, contando o tempo de revisar o código gerado pela LLM.

### Tasks de cada membro, em ordem

**Membro A — Backend base, seed e integração**

| Dia | Código | Task | Depende de |
|---|---|---|---|
| 1 | A-01 | Criar o projeto Dart Frog conectado ao Supabase | — |
| 1 | A-02 | Liberar CORS para o Flutter Web | A-01 |
| 1 | A-03 | Criar as tabelas do banco (migration 001_base.sql) | — |
| 1–2 | A-04 | Criar os dados de teste (seed.sql) | A-03 |
| 2 | A-05 | Criar o comando de reset do banco | A-03, A-04 |
| 2 | A-06 | Implementar as entidades de domínio do diagrama de classes | B-01, A-01 |
| 2 | A-07 | Implementar PresencaRepository e VinculoRepository | A-06, A-03 |
| 3 | A-08 | Listar os alunos da rota (GET /rotas/{rotaId}/alunos) | A-07, C-02 |
| 3 | A-09 | Escrever o README do backend | A-05 |
| 4–5 | A-10 | Integrar na main e preparar o ambiente da demo | — |
| 5 | A-11 | Executar os testes de aceitação e registrar os bugs | A-10 |
| 7 | A-12 | Conferir as exigências da disciplina para a entrega | B-12, E-07, C-08 |

**Membro B — Diagrama de classes e backend do embarque**

| Dia | Código | Task | Depende de |
|---|---|---|---|
| 1 | B-01 | Identificar as classes e montar o diagrama de classes do UC-S05 | — |
| 1 | B-02 | Definir a arquitetura em camadas e a estrutura de diretórios | B-01 |
| 1 | B-03 | Documentar as classes principais e a rastreabilidade até as classes | B-01 |
| 2 | B-04 | Implementar Presenca.registrarEmbarque (RN-010) | A-06 |
| 2 | B-05 | Criar o contrato NotificacaoService e a versão vazia | B-01 |
| 2–3 | B-06 | Implementar EmbarqueService.registrarEmbarque | B-04, B-05, A-07 |
| 3 | B-07 | Garantir a idempotência pelo registroId | B-06 |
| 3 | B-08 | Criar a rota POST /rotas/{rotaId}/embarques e o EmbarqueController | B-06, C-02 |
| 3 | B-09 | Criar a rota de sincronização em lote | B-08 |
| 4 | B-10 | Testes unitários do EmbarqueService | B-07 |
| 4 | B-11 | Trocar a notificação vazia pela implementação real | C-04 |
| 6 | B-12 | Atualizar o diagrama de classes e a arquitetura com o código real | A-10 |

**Membro C — Login e notificação ponta a ponta (UC-I02)**

| Dia | Código | Task | Depende de |
|---|---|---|---|
| 1 | C-01 | Criar a tabela de notificação (migration 002) | A-03 |
| 1–2 | C-02 | Login simplificado: GET /usuarios, POST /login e autenticação | A-01, A-03 |
| 2 | C-03 | Implementar a entidade Notificacao e o NotificacaoRepository | B-01, C-01 |
| 2–3 | C-04 | Implementar o NotificacaoService real (UC-I02) | C-03, B-05, A-07 |
| 3 | C-05 | Criar GET /notificacoes e PATCH /notificacoes/{id}/lida | C-03, C-02 |
| 4 | C-06 | Criar a tela "Avisos" do responsável | D-02, C-05 |
| 4 | C-07 | Atualizar os avisos sozinho, tratar sem conexão e marcar como lido | C-06 |
| 6–7 | C-08 | Roteiro da demo e evidências do Jira | A-11 |

**Membro D — App do motorista (UC-R02)**

| Dia | Código | Task | Depende de |
|---|---|---|---|
| 1 | D-01 | Criar o projeto Flutter com os módulos | B-02 |
| 1–2 | D-02 | Cliente da API, sessão do usuário e modo mock | D-01 |
| 2 | D-03 | Criar a tela de login | D-02 |
| 2 | D-04 | Criar o contrato ModuloEmbarque e o ModuloEmbarqueOnline | D-02 |
| 2–3 | D-05 | Montar a tela "Rota do dia" | D-02 |
| 3 | D-06 | Registrar o embarque com um toque e tratar os estados | D-04, D-05 |
| 3 | D-07 | Ligar o app do motorista à API real | A-08, B-08, C-02 |
| 4 | D-08 | Testes de widget da tela "Rota do dia" | D-06 |

**Membro E — Modo offline e sincronização (A1, RNF-006)**

| Dia | Código | Task | Depende de |
|---|---|---|---|
| 1–2 | E-01 | Criar a fila persistente (ArmazenamentoLocal) | D-01 |
| 2 | E-02 | Detectar a conectividade | D-01 |
| 3 | E-03 | Criar o ModuloEmbarqueComFila | D-04, E-01, E-02 |
| 3–4 | E-04 | Sincronizar automaticamente ao reconectar | E-03, B-09 |
| 4 | E-05 | Ativar o modo offline no app e a faixa "Sem conexão" | E-04, D-05 |
| 4 | E-06 | Testes do módulo offline | E-04 |
| 6 | E-07 | Revisar os artefatos do 1º bimestre | B-12 |

### Dependências que travam outras pessoas (fazer primeiro)

| Task | Dono | Desbloqueia |
|---|---|---|
| B-01 — Identificar as classes e montar o diagrama de classes do UC-S05 | B | B-02, B-03, A-06, B-05, C-03 |
| A-03 — Criar as tabelas do banco (migration 001_base.sql) | A | A-04, A-05, A-07, C-01, C-02 |
| C-02 — Login simplificado: GET /usuarios, POST /login e autenticação | C | A-08, B-08, C-05, D-07 |
| D-02 — Cliente da API, sessão do usuário e modo mock | D | C-06, D-03, D-04, D-05 |
| A-01 — Criar o projeto Dart Frog conectado ao Supabase | A | A-02, A-06, C-02 |
| A-07 — Implementar PresencaRepository e VinculoRepository | A | A-08, B-06, C-04 |
| D-01 — Criar o projeto Flutter com os módulos | D | D-02, E-01, E-02 |
| A-06 — Implementar as entidades de domínio do diagrama de classes | A | A-07, B-04 |
| B-05 — Criar o contrato NotificacaoService e a versão vazia | B | B-06, C-04 |
| B-08 — Criar a rota POST /rotas/{rotaId}/embarques e o EmbarqueController | B | B-09, D-07 |
| D-04 — Criar o contrato ModuloEmbarque e o ModuloEmbarqueOnline | D | D-06, E-03 |
| D-05 — Montar a tela "Rota do dia" | D | D-06, E-05 |
| A-10 — Integrar na main e preparar o ambiente da demo | A | A-11, B-12 |
| B-12 — Atualizar o diagrama de classes e a arquitetura com o código real | B | E-07, A-12 |

---

## 4. Tasks por Story

**Epic: UC-S05 Registrar Embarque (com UC-I02 e fluxo A1)**

### S0 — Projeto da solução: diagrama de classes e arquitetura do UC-S05

*Como equipe, queremos o diagrama de classes, as camadas e a estrutura de diretórios definidos antes de programar, para que todo o código siga o mesmo projeto (exigência da disciplina).* Responsável: Membro B.

| Código | Task | Membro | Dia | Horas | Depende de | Branch sugerida |
|---|---|---|---|---|---|---|
| B-01 | Identificar as classes e montar o diagrama de classes do UC-S05 | B | 1 | 4 h | — | `task-<nº>-diagrama-classes-uc-s05` |
| B-02 | Definir a arquitetura em camadas e a estrutura de diretórios | B | 1 | 2 h | B-01 | `task-<nº>-arquitetura-camadas-diretorios` |
| B-03 | Documentar as classes principais e a rastreabilidade até as classes | B | 1 | 1 h | B-01 | `task-<nº>-rastreabilidade-classes` |

### S1 — Base do backend e dados de teste

*Como equipe, queremos o servidor, o banco e os dados de teste prontos, para que todas as frentes trabalhem sobre a mesma base.* Responsável: Membro A.

| Código | Task | Membro | Dia | Horas | Depende de | Branch sugerida |
|---|---|---|---|---|---|---|
| A-01 | Criar o projeto Dart Frog conectado ao Supabase | A | 1 | 2 h | — | `task-<nº>-projeto-backend` |
| A-02 | Liberar CORS para o Flutter Web | A | 1 | 1 h | A-01 | `task-<nº>-cors` |
| A-03 | Criar as tabelas do banco (migration 001_base.sql) | A | 1 | 3 h | — | `task-<nº>-migration-base` |
| A-04 | Criar os dados de teste (seed.sql) | A | 1–2 | 2 h | A-03 | `task-<nº>-seed` |
| A-05 | Criar o comando de reset do banco | A | 2 | 2 h | A-03, A-04 | `task-<nº>-reset-db` |
| A-06 | Implementar as entidades de domínio do diagrama de classes | A | 2 | 3 h | B-01, A-01 | `task-<nº>-entidades-dominio` |
| A-07 | Implementar PresencaRepository e VinculoRepository | A | 2 | 3 h | A-06, A-03 | `task-<nº>-repositorios-presenca-vinculo` |
| A-08 | Listar os alunos da rota (GET /rotas/{rotaId}/alunos) | A | 3 | 3 h | A-07, C-02 | `task-<nº>-listar-alunos-rota` |
| A-09 | Escrever o README do backend | A | 3 | 1 h | A-05 | `task-<nº>-readme-backend` |

### S2 — Registrar o embarque no servidor

*Como motorista, quero registrar que o aluno entrou na van, para que o embarque fique registrado com data, horário e local (RF-009, RN-010, RN-012).* Responsável: Membro B.

| Código | Task | Membro | Dia | Horas | Depende de | Branch sugerida |
|---|---|---|---|---|---|---|
| B-04 | Implementar Presenca.registrarEmbarque (RN-010) | B | 2 | 2 h | A-06 | `task-<nº>-presenca-registrar-embarque` |
| B-05 | Criar o contrato NotificacaoService e a versão vazia | B | 2 | 1 h | B-01 | `task-<nº>-contrato-notificacao-service` |
| B-06 | Implementar EmbarqueService.registrarEmbarque | B | 2–3 | 4 h | B-04, B-05, A-07 | `task-<nº>-embarque-service` |
| B-07 | Garantir a idempotência pelo registroId | B | 3 | 2 h | B-06 | `task-<nº>-idempotencia-registro-id` |
| B-08 | Criar a rota POST /rotas/{rotaId}/embarques e o EmbarqueController | B | 3 | 2 h | B-06, C-02 | `task-<nº>-rota-registrar-embarque` |
| B-09 | Criar a rota de sincronização em lote | B | 3 | 2 h | B-08 | `task-<nº>-rota-sincronizar-embarques` |
| B-10 | Testes unitários do EmbarqueService | B | 4 | 3 h | B-07 | `task-<nº>-testes-embarque-service` |
| B-11 | Trocar a notificação vazia pela implementação real | B | 4 | 1 h | C-04 | `task-<nº>-ligar-notificacao-real` |

### S3 — Notificar o responsável sobre o embarque (UC-I02)

*Como responsável, quero ser avisado quando meu filho embarcar, para saber que ele está a caminho (RF-011, RN-002, RN-009).* Responsável: Membro C.

| Código | Task | Membro | Dia | Horas | Depende de | Branch sugerida |
|---|---|---|---|---|---|---|
| C-01 | Criar a tabela de notificação (migration 002) | C | 1 | 1 h | A-03 | `task-<nº>-migration-notificacao` |
| C-02 | Login simplificado: GET /usuarios, POST /login e autenticação | C | 1–2 | 3 h | A-01, A-03 | `task-<nº>-login-simplificado` |
| C-03 | Implementar a entidade Notificacao e o NotificacaoRepository | C | 2 | 3 h | B-01, C-01 | `task-<nº>-entidade-notificacao` |
| C-04 | Implementar o NotificacaoService real (UC-I02) | C | 2–3 | 3 h | C-03, B-05, A-07 | `task-<nº>-notificacao-service` |
| C-05 | Criar GET /notificacoes e PATCH /notificacoes/{id}/lida | C | 3 | 3 h | C-03, C-02 | `task-<nº>-rotas-notificacoes` |
| C-06 | Criar a tela "Avisos" do responsável | C | 4 | 5 h | D-02, C-05 | `task-<nº>-tela-avisos` |
| C-07 | Atualizar os avisos sozinho, tratar sem conexão e marcar como lido | C | 4 | 3 h | C-06 | `task-<nº>-avisos-atualizacao` |

### S4 — Tela do motorista para registrar o embarque (UC-R02)

*Como motorista, quero registrar o embarque com um toque na tela da rota, sem navegar pelo app enquanto dirijo (RF-009, RNF-004, RNF-005).* Responsável: Membro D.

| Código | Task | Membro | Dia | Horas | Depende de | Branch sugerida |
|---|---|---|---|---|---|---|
| D-01 | Criar o projeto Flutter com os módulos | D | 1 | 2 h | B-02 | `task-<nº>-projeto-app` |
| D-02 | Cliente da API, sessão do usuário e modo mock | D | 1–2 | 3 h | D-01 | `task-<nº>-cliente-api-mock` |
| D-03 | Criar a tela de login | D | 2 | 2 h | D-02 | `task-<nº>-tela-login` |
| D-04 | Criar o contrato ModuloEmbarque e o ModuloEmbarqueOnline | D | 2 | 3 h | D-02 | `task-<nº>-modulo-embarque-online` |
| D-05 | Montar a tela "Rota do dia" | D | 2–3 | 5 h | D-02 | `task-<nº>-tela-rota-do-dia` |
| D-06 | Registrar o embarque com um toque e tratar os estados | D | 3 | 3 h | D-04, D-05 | `task-<nº>-toque-embarcou-estados` |
| D-07 | Ligar o app do motorista à API real | D | 3 | 2 h | A-08, B-08, C-02 | `task-<nº>-integracao-api-motorista` |
| D-08 | Testes de widget da tela "Rota do dia" | D | 4 | 3 h | D-06 | `task-<nº>-testes-tela-rota` |

### S5 — Registrar o embarque sem conexão (fluxo A1, RNF-006)

*Como motorista, quero registrar o embarque mesmo sem sinal, para não ficar travado em trechos sem cobertura.* Responsável: Membro E.

| Código | Task | Membro | Dia | Horas | Depende de | Branch sugerida |
|---|---|---|---|---|---|---|
| E-01 | Criar a fila persistente (ArmazenamentoLocal) | E | 1–2 | 3 h | D-01 | `task-<nº>-armazenamento-local` |
| E-02 | Detectar a conectividade | E | 2 | 3 h | D-01 | `task-<nº>-deteccao-conectividade` |
| E-03 | Criar o ModuloEmbarqueComFila | E | 3 | 4 h | D-04, E-01, E-02 | `task-<nº>-modulo-embarque-com-fila` |
| E-04 | Sincronizar automaticamente ao reconectar | E | 3–4 | 5 h | E-03, B-09 | `task-<nº>-sincronizacao-automatica` |
| E-05 | Ativar o modo offline no app e a faixa "Sem conexão" | E | 4 | 2 h | E-04, D-05 | `task-<nº>-ativar-modo-offline` |
| E-06 | Testes do módulo offline | E | 4 | 4 h | E-04 | `task-<nº>-testes-modo-offline` |

### S6 — Integração, testes de aceitação e documentação final

*Como equipe, queremos o UC-S05 integrado, testado de ponta a ponta e com a documentação igual ao código, para a entrega de 02/12.* Responsável: Membro A, B, C, E.

| Código | Task | Membro | Dia | Horas | Depende de | Branch sugerida |
|---|---|---|---|---|---|---|
| A-10 | Integrar na main e preparar o ambiente da demo | A | 4–5 | 3 h | — | `task-<nº>-integracao-ambiente-demo` |
| A-11 | Executar os testes de aceitação e registrar os bugs | A | 5 | 3 h | A-10 | `task-<nº>-testes-aceitacao` |
| B-12 | Atualizar o diagrama de classes e a arquitetura com o código real | B | 6 | 3 h | A-10 | `task-<nº>-diagrama-classes-final` |
| E-07 | Revisar os artefatos do 1º bimestre | E | 6 | 2 h | B-12 | `task-<nº>-revisao-artefatos-1-bim` |
| C-08 | Roteiro da demo e evidências do Jira | C | 6–7 | 2 h | A-11 | `task-<nº>-roteiro-demo` |
| A-12 | Conferir as exigências da disciplina para a entrega | A | 7 | 1 h | B-12, E-07, C-08 | `task-<nº>-checklist-entrega` |

---

## 5. Descrição de cada task

Texto para colar na descrição da subtarefa no Jira (o CSV já traz isso).

#### [B-01] Identificar as classes e montar o diagrama de classes do UC-S05

- **Story:** S0 · **Membro:** B · **Dia:** 1 · **Estimativa:** 4 h · **Depende de:** —
- **Branch:** `task-<nº>-diagrama-classes-uc-s05`

A partir dos diagramas de sequência UC-S05, UC-R02 e UC-I02, do mapa de dados e do backlog, identificar as classes (tabela Classe | Camada | Responsabilidade | Atributos | Operações) e desenhar o diagrama de classes em PlantUML. Prompt 0, itens 1 e 2.

Critérios de aceite:

- Diagrama em documentos/desenvolvimento/scripts/diagrama-classes-uc-s05.puml, referenciado em 03-arquitetura.md
- Atributos com visibilidade e tipo; operações com parâmetros e retorno
- Relacionamentos e multiplicidades corretos, com as composições justificadas
- Contratos de repositório separados das implementações Postgres
- Entidades com comportamento (ex.: Presenca.registrarEmbarque, VinculoMotoristaVan.estaAtivo, Notificacao.deEmbarque)

#### [B-02] Definir a arquitetura em camadas e a estrutura de diretórios

- **Story:** S0 · **Membro:** B · **Dia:** 1 · **Estimativa:** 2 h · **Depende de:** B-01
- **Branch:** `task-<nº>-arquitetura-camadas-diretorios`

Organizar as classes em apresentação, aplicação, domínio e infraestrutura, definir as dependências permitidas e a árvore de diretórios do backend e do app, e registrar as decisões arquiteturais. Prompt 0, itens 3, 4 e 7.

Critérios de aceite:

- Cada camada com suas classes e as dependências permitidas e proibidas
- Árvore de diretórios comentada do backend e do app, por funcionalidade com camadas internas, sem dependência circular entre módulos
- Decisões arquiteturais justificadas

#### [B-03] Documentar as classes principais e a rastreabilidade até as classes

- **Story:** S0 · **Membro:** B · **Dia:** 1 · **Estimativa:** 1 h · **Depende de:** B-01
- **Branch:** `task-<nº>-rastreabilidade-classes`

Documentar EmbarqueService, Presenca, NotificacaoService e ModuloEmbarque e montar a rastreabilidade RN -> RF -> UC -> classes e operações. Prompt 0, itens 5 e 6. Apresentar o diagrama para a equipe revisar no fim do Dia 1.

Critérios de aceite:

- Tabela Classe | Responsabilidade | Operações | Dependências | RN | RF | UC
- Rastreabilidade de RN-002, RN-009, RN-010, RN-012, RF-009, RF-011, RNF-005 e RNF-006
- Diagrama revisado e aprovado pela equipe

#### [A-01] Criar o projeto Dart Frog conectado ao Supabase

- **Story:** S1 · **Membro:** A · **Dia:** 1 · **Estimativa:** 2 h · **Depende de:** —
- **Branch:** `task-<nº>-projeto-backend`

Criar o projeto do servidor em backend/, na porta 8080, lendo DATABASE_URL de backend/.env, com a conexão com o Postgres na infraestrutura do módulo compartilhado. Prompt do Membro A, item 1.

Critérios de aceite:

- `dart_frog dev` sobe o servidor e uma rota simples responde
- backend/.env no .gitignore e backend/.env.example sem senha

#### [A-02] Liberar CORS para o Flutter Web

- **Story:** S1 · **Membro:** A · **Dia:** 1 · **Estimativa:** 1 h · **Depende de:** A-01
- **Branch:** `task-<nº>-cors`

Middleware de CORS que libera qualquer origem em desenvolvimento e responde ao preflight OPTIONS. Prompt do Membro A, item 2.

Critérios de aceite:

- O app Flutter rodando no navegador chama a API sem erro de CORS

#### [A-03] Criar as tabelas do banco (migration 001_base.sql)

- **Story:** S1 · **Membro:** A · **Dia:** 1 · **Estimativa:** 3 h · **Depende de:** —
- **Branch:** `task-<nº>-migration-base`

Criar supabase/migrations/001_base.sql com as tabelas do mapa de dados usadas pelo UC-S05, mais a tabela sessao, com RLS ativado. Prompt do Membro A, item 3.

Critérios de aceite:

- Roda sem erro em um projeto Supabase vazio
- RLS ativado em todas as tabelas
- registro_id do embarque é único; só um vínculo motorista–van ativo por van

#### [A-04] Criar os dados de teste (seed.sql)

- **Story:** S1 · **Membro:** A · **Dia:** 1–2 · **Estimativa:** 2 h · **Depende de:** A-03
- **Branch:** `task-<nº>-seed`

Criar supabase/seed.sql exatamente como a seção 6 do backlog, com a rota sempre na data de hoje. Prompt do Membro A, item 4.

Critérios de aceite:

- Ana, Beatriz e Carlos confirmados; Bruno ausente
- Ana com 2 responsáveis; Carlos maior de idade sem responsável
- Um motorista ativo na van e outro sem vínculo

#### [A-05] Criar o comando de reset do banco

- **Story:** S1 · **Membro:** A · **Dia:** 2 · **Estimativa:** 2 h · **Depende de:** A-03, A-04
- **Branch:** `task-<nº>-reset-db`

Criar backend/bin/reset_db.dart, que apaga as tabelas, roda as migrations em ordem e o seed. Prompt do Membro A, item 5.

Critérios de aceite:

- `dart run bin/reset_db.dart` funciona duas vezes seguidas sem erro
- Roda todas as migrations da pasta, inclusive as dos outros membros

#### [A-06] Implementar as entidades de domínio do diagrama de classes

- **Story:** S1 · **Membro:** A · **Dia:** 2 · **Estimativa:** 3 h · **Depende de:** B-01, A-01
- **Branch:** `task-<nº>-entidades-dominio`

Criar as entidades Aluno, Responsavel, Motorista, Van, VinculoMotoristaVan, Rota, PontoParada, Presenca e Embarque com os atributos e operações do diagrama. Presenca.registrarEmbarque fica com UnimplementedError (é a task B-04). Prompt do Membro A, item 6.

Critérios de aceite:

- Nomes, atributos e operações iguais ao diagrama de classes
- O domínio não importa dart_frog nem postgres
- Teste de VinculoMotoristaVan.estaAtivo()

#### [A-07] Implementar PresencaRepository e VinculoRepository

- **Story:** S1 · **Membro:** A · **Dia:** 2 · **Estimativa:** 3 h · **Depende de:** A-06, A-03
- **Branch:** `task-<nº>-repositorios-presenca-vinculo`

Contratos no domínio e implementações Postgres na infraestrutura: presenças da rota em ordem, responsáveis de um aluno e motorista ativo de uma van. Prompt do Membro A, item 7.

Critérios de aceite:

- Contrato (classe abstrata) separado da implementação
- Consultas testadas manualmente contra o seed

#### [A-08] Listar os alunos da rota (GET /rotas/{rotaId}/alunos)

- **Story:** S1 · **Membro:** A · **Dia:** 3 · **Estimativa:** 3 h · **Depende de:** A-07, C-02
- **Branch:** `task-<nº>-listar-alunos-rota`

Endpoint da seção 3 do backlog: rota HTTP -> Controller -> Service -> repositório. Prompt do Membro A, item 8.

Critérios de aceite:

- Só alunos CONFIRMADO ou EMBARCADO, na ordem da rota; Bruno (ausente) não aparece
- Motorista sem vínculo com a van recebe 403 (RN-012)
- Resposta no formato exato da seção 3; testes automatizados desses casos

#### [A-09] Escrever o README do backend

- **Story:** S1 · **Membro:** A · **Dia:** 3 · **Estimativa:** 1 h · **Depende de:** A-05
- **Branch:** `task-<nº>-readme-backend`

backend/README.md com instalação, configuração do .env, reset do banco e como subir o servidor. Prompt do Membro A, item 9.

Critérios de aceite:

- Outro membro consegue subir o backend do zero só seguindo o README

#### [B-04] Implementar Presenca.registrarEmbarque (RN-010)

- **Story:** S2 · **Membro:** B · **Dia:** 2 · **Estimativa:** 2 h · **Depende de:** A-06
- **Branch:** `task-<nº>-presenca-registrar-embarque`

Comportamento de domínio: a presença valida que está CONFIRMADO, muda para EMBARCADO e devolve o Embarque; senão lança exceção de domínio. Prompt do Membro B, item 1.

Critérios de aceite:

- Testes: CONFIRMADO embarca; AUSENTE e EMBARCADO lançam a exceção

#### [B-05] Criar o contrato NotificacaoService e a versão vazia

- **Story:** S2 · **Membro:** B · **Dia:** 2 · **Estimativa:** 1 h · **Depende de:** B-01
- **Branch:** `task-<nº>-contrato-notificacao-service`

Contrato NotificacaoService com notificarMovimentacao e uma implementação vazia, para o EmbarqueService não esperar o UC-I02. Prompt do Membro B, item 4.

Critérios de aceite:

- Arquivos separados no módulo notificacao, como no diagrama
- Avisar o Membro C que o contrato está na main

#### [B-06] Implementar EmbarqueService.registrarEmbarque

- **Story:** S2 · **Membro:** B · **Dia:** 2–3 · **Estimativa:** 4 h · **Depende de:** B-04, B-05, A-07
- **Branch:** `task-<nº>-embarque-service`

Coordenar o caso de uso: motorista ativo (RN-012, 403), rota e aluno existem (404), presenca.registrarEmbarque com a hora do toque, salvar embarque e presença na mesma transação e chamar a notificação. Prompt do Membro B, item 3.

Critérios de aceite:

- Embarque salvo com a dataHora enviada pelo aparelho
- Embarque e status salvos na mesma transação
- NotificacaoService chamado depois de salvar

#### [B-07] Garantir a idempotência pelo registroId

- **Story:** S2 · **Membro:** B · **Dia:** 3 · **Estimativa:** 2 h · **Depende de:** B-06
- **Branch:** `task-<nº>-idempotencia-registro-id`

Mesmo registroId recebido de novo devolve o resultado anterior (200) sem salvar nem notificar de novo, inclusive em requisições simultâneas. Prompt do Membro B, item 3.

Critérios de aceite:

- Mesmo registroId duas vezes gera um único embarque e uma única notificação
- Violação de unicidade do registro_id tratada como já processado

#### [B-08] Criar a rota POST /rotas/{rotaId}/embarques e o EmbarqueController

- **Story:** S2 · **Membro:** B · **Dia:** 3 · **Estimativa:** 2 h · **Depende de:** B-06, C-02
- **Branch:** `task-<nº>-rota-registrar-embarque`

Rota do Dart Frog que chama o EmbarqueController; ele só converte JSON e exceções em códigos HTTP. Prompt do Membro B, item 2.

Critérios de aceite:

- Respostas 201, 200, 403, 404 e 409 como na seção 3 do backlog
- Controller sem regra de negócio e sem acesso a repositório

#### [B-09] Criar a rota de sincronização em lote

- **Story:** S2 · **Membro:** B · **Dia:** 3 · **Estimativa:** 2 h · **Depende de:** B-08
- **Branch:** `task-<nº>-rota-sincronizar-embarques`

POST /rotas/{rotaId}/embarques/sincronizar processa cada registro com o mesmo EmbarqueService e devolve o resultado por registroId. Prompt do Membro B, item 5.

Critérios de aceite:

- Um registro com erro não impede os outros
- Resposta com o código de cada registroId

#### [B-10] Testes unitários do EmbarqueService

- **Story:** S2 · **Membro:** B · **Dia:** 4 · **Estimativa:** 3 h · **Depende de:** B-07
- **Branch:** `task-<nº>-testes-embarque-service`

Testes com mocktail, sem banco: uma linha da tabela de respostas da seção 3 por teste, idempotência e hora do toque. Prompt do Membro B, item 6.

Critérios de aceite:

- Todos os testes passam com `dart test`

#### [B-11] Trocar a notificação vazia pela implementação real

- **Story:** S2 · **Membro:** B · **Dia:** 4 · **Estimativa:** 1 h · **Depende de:** C-04
- **Branch:** `task-<nº>-ligar-notificacao-real`

Registrar o NotificacaoService real do Membro C no lugar do NotificacaoServiceVazio.

Critérios de aceite:

- Embarque pela API cria as notificações dos responsáveis no banco

#### [C-01] Criar a tabela de notificação (migration 002)

- **Story:** S3 · **Membro:** C · **Dia:** 1 · **Estimativa:** 1 h · **Depende de:** A-03
- **Branch:** `task-<nº>-migration-notificacao`

supabase/migrations/002_notificacao.sql com RLS ativado. Prompt do Membro C, item 1.

Critérios de aceite:

- Roda depois da 001 pelo comando de reset

#### [C-02] Login simplificado: GET /usuarios, POST /login e autenticação

- **Story:** S3 · **Membro:** C · **Dia:** 1–2 · **Estimativa:** 3 h · **Depende de:** A-01, A-03
- **Branch:** `task-<nº>-login-simplificado`

Listar os usuários do seed, login pelo id e papel devolvendo um token salvo na tabela sessao, e middleware que identifica o usuário e o papel. O login é só apoio: não é o caso de uso avaliado. Prompt do Membro C, item 2.

Critérios de aceite:

- Sem token válido -> 401
- As rotas conseguem saber quem é o usuário logado e se é MOTORISTA ou RESPONSAVEL

#### [C-03] Implementar a entidade Notificacao e o NotificacaoRepository

- **Story:** S3 · **Membro:** C · **Dia:** 2 · **Estimativa:** 3 h · **Depende de:** B-01, C-01
- **Branch:** `task-<nº>-entidade-notificacao`

Notificacao.deEmbarque monta a mensagem com a hora do embarque em horário de Brasília; marcarComoLida. Contrato no domínio e implementação Postgres. Prompt do Membro C, item 3.

Critérios de aceite:

- Mensagem "<aluno> embarcou na van às HH:MM." com a hora do embarque (UTC-3)
- Teste da fábrica deEmbarque

#### [C-04] Implementar o NotificacaoService real (UC-I02)

- **Story:** S3 · **Membro:** C · **Dia:** 2–3 · **Estimativa:** 3 h · **Depende de:** C-03, B-05, A-07
- **Branch:** `task-<nº>-notificacao-service`

Buscar os responsáveis do aluno, criar uma notificação por responsável e tratar o fluxo A1 (aluno sem responsável). Prompt do Membro C, item 4.

Critérios de aceite:

- Ana -> 2 notificações; Carlos -> 0, sem erro
- Testes com mocktail

#### [C-05] Criar GET /notificacoes e PATCH /notificacoes/{id}/lida

- **Story:** S3 · **Membro:** C · **Dia:** 3 · **Estimativa:** 3 h · **Depende de:** C-03, C-02
- **Branch:** `task-<nº>-rotas-notificacoes`

Rotas HTTP -> Controller -> Service, só com notificações do usuário logado (RN-002). Prompt do Membro C, item 5.

Critérios de aceite:

- Responsável não vê nem marca notificação de outra família
- Filtro desde={dataHora} funcionando

#### [C-06] Criar a tela "Avisos" do responsável

- **Story:** S3 · **Membro:** C · **Dia:** 4 · **Estimativa:** 5 h · **Depende de:** D-02, C-05
- **Branch:** `task-<nº>-tela-avisos`

Tela do módulo avisos conforme a seção 10 do backlog: card por aluno com status e lista de avisos do dia. Prompt do Membro C, item 6.

Critérios de aceite:

- Layout e textos iguais à seção 10
- Estado vazio com a mensagem do backlog

#### [C-07] Atualizar os avisos sozinho, tratar sem conexão e marcar como lido

- **Story:** S3 · **Membro:** C · **Dia:** 4 · **Estimativa:** 3 h · **Depende de:** C-06
- **Branch:** `task-<nº>-avisos-atualizacao`

Timer.periodic a cada ~10 s, "Atualizado há X s", faixa de sem conexão mantendo os últimos avisos (RNF-003) e marcar como lidos ao exibir. Prompt do Membro C, itens 7 e 8.

Critérios de aceite:

- Aviso aparece em até ~10 s depois do embarque
- Sem rede, a tela mostra a faixa e não apaga os avisos

#### [D-01] Criar o projeto Flutter com os módulos

- **Story:** S4 · **Membro:** D · **Dia:** 1 · **Estimativa:** 2 h · **Depende de:** B-02
- **Branch:** `task-<nº>-projeto-app`

Projeto Flutter em app/ rodando no Android e na Web, com as pastas compartilhado/, login/, embarque/ e avisos/ do documento de arquitetura. Pode começar antes da B-02 e ajustar as pastas depois. Prompt do Membro D, item 1.

Critérios de aceite:

- `flutter run` funciona no Android (ou emulador) e no Chrome

#### [D-02] Cliente da API, sessão do usuário e modo mock

- **Story:** S4 · **Membro:** D · **Dia:** 1–2 · **Estimativa:** 3 h · **Depende de:** D-01
- **Branch:** `task-<nº>-cliente-api-mock`

Cliente HTTP com API_URL e token, sessão do usuário logado, cores do app e dados mockados com USE_MOCK=true. Prompt do Membro D, item 2.

Critérios de aceite:

- Com USE_MOCK=true o app funciona sem backend
- Mocks no formato da seção 3 com os alunos do seed

#### [D-03] Criar a tela de login

- **Story:** S4 · **Membro:** D · **Dia:** 2 · **Estimativa:** 2 h · **Depende de:** D-02
- **Branch:** `task-<nº>-tela-login`

Lista os usuários e entra com um toque; motorista vai para a Rota do dia e responsável para Avisos. Prompt do Membro D, item 3.

Critérios de aceite:

- Login funciona com mock e com a API (C-02)

#### [D-04] Criar o contrato ModuloEmbarque e o ModuloEmbarqueOnline

- **Story:** S4 · **Membro:** D · **Dia:** 2 · **Estimativa:** 3 h · **Depende de:** D-02
- **Branch:** `task-<nº>-modulo-embarque-online`

Classe abstrata e tipos exatamente como a seção 3 do backlog, e a implementação só online (GPS com limite de 2 s). Desbloqueia o Membro E. Prompt do Membro D, item 4.

Critérios de aceite:

- Contrato idêntico ao do backlog
- O toque nunca espera mais de 2 s pelo GPS
- Implementação escolhida em um único lugar no main.dart

#### [D-05] Montar a tela "Rota do dia"

- **Story:** S4 · **Membro:** D · **Dia:** 2–3 · **Estimativa:** 5 h · **Depende de:** D-02
- **Branch:** `task-<nº>-tela-rota-do-dia`

Layout da seção 10: cabeçalho, próxima parada com botão grande, Depois, Na van e o widget FaixaSemConexao (pronto e escondido). Prompt do Membro D, item 5.

Critérios de aceite:

- Botão "Embarcou" de largura total e no mínimo 56 de altura (RNF-005)
- Status sempre com cor, ícone e texto

#### [D-06] Registrar o embarque com um toque e tratar os estados

- **Story:** S4 · **Membro:** D · **Dia:** 3 · **Estimativa:** 3 h · **Depende de:** D-04, D-05
- **Branch:** `task-<nº>-toque-embarcou-estados`

Um toque registra sem diálogo; o aluno muda de seção na hora e a próxima parada é destacada; pendente em âmbar; mensagens de carregando, 403, 409, vazia e erro; escutar aoMudarPendentes. Prompt do Membro D, item 5.

Critérios de aceite:

- Testes de aceitação 1, 2 e 6 da seção 7 passam com mock
- Textos iguais aos da seção 10

#### [D-07] Ligar o app do motorista à API real

- **Story:** S4 · **Membro:** D · **Dia:** 3 · **Estimativa:** 2 h · **Depende de:** A-08, B-08, C-02
- **Branch:** `task-<nº>-integracao-api-motorista`

Trocar os mocks pela API real no fluxo do motorista e acertar as diferenças.

Critérios de aceite:

- Login, lista da rota e embarque funcionando contra o backend local

#### [D-08] Testes de widget da tela "Rota do dia"

- **Story:** S4 · **Membro:** D · **Dia:** 4 · **Estimativa:** 3 h · **Depende de:** D-06
- **Branch:** `task-<nº>-testes-tela-rota`

Testes com um ModuloEmbarque falso. Prompt do Membro D, item 7.

Critérios de aceite:

- Tocar "Embarcou" move o aluno e destaca a próxima parada
- Status pendente mostra o ícone âmbar; `flutter test` passa

#### [E-01] Criar a fila persistente (ArmazenamentoLocal)

- **Story:** S5 · **Membro:** E · **Dia:** 1–2 · **Estimativa:** 3 h · **Depende de:** D-01
- **Branch:** `task-<nº>-armazenamento-local`

Fila de registros em JSON no shared_preferences, que funciona no Android e na Web. Prompt do Membro E, item 1.

Critérios de aceite:

- A fila sobrevive a fechar e abrir o app
- Testes com SharedPreferences.setMockInitialValues

#### [E-02] Detectar a conectividade

- **Story:** S5 · **Membro:** E · **Dia:** 2 · **Estimativa:** 3 h · **Depende de:** D-01
- **Branch:** `task-<nº>-deteccao-conectividade`

connectivity_plus + timeout de 5 s e erro de rede tratados como offline, expostos em um ValueNotifier<bool>. Prompt do Membro E, item 2.

Critérios de aceite:

- Modo avião é detectado no Android
- Na Web, falha de rede na chamada conta como offline

#### [E-03] Criar o ModuloEmbarqueComFila

- **Story:** S5 · **Membro:** E · **Dia:** 3 · **Estimativa:** 4 h · **Depende de:** D-04, E-01, E-02
- **Branch:** `task-<nº>-modulo-embarque-com-fila`

Nova implementação do contrato ModuloEmbarque: online envia, offline ou erro de rede vai para a fila e devolve pendente; 403/404/409 viram EmbarqueException. Prompt do Membro E, item 3.

Critérios de aceite:

- Contrato do backlog não foi alterado
- Hora e localização capturadas no momento do toque

#### [E-04] Sincronizar automaticamente ao reconectar

- **Story:** S5 · **Membro:** E · **Dia:** 3–4 · **Estimativa:** 5 h · **Depende de:** E-03, B-09
- **Branch:** `task-<nº>-sincronizacao-automatica`

Enviar a fila para a rota de sincronização, remover só o que o servidor confirmou, avisar rejeitados no aoMudarPendentes, tentar a cada 30 s e ao abrir o app, sem sincronizações simultâneas. Prompt do Membro E, itens 4 e 5.

Critérios de aceite:

- Pendentes sincronizados em até 5 min após reconectar (RNF-006)
- Falha no meio não perde nem duplica registros

#### [E-05] Ativar o modo offline no app e a faixa "Sem conexão"

- **Story:** S5 · **Membro:** E · **Dia:** 4 · **Estimativa:** 2 h · **Depende de:** E-04, D-05
- **Branch:** `task-<nº>-ativar-modo-offline`

Trocar no main.dart para ModuloEmbarqueComFila e ligar a FaixaSemConexao à detecção de rede. Prompt do Membro E, item 6.

Critérios de aceite:

- Testes de aceitação 8, 9 e 10 da seção 7 passam no Android

#### [E-06] Testes do módulo offline

- **Story:** S5 · **Membro:** E · **Dia:** 4 · **Estimativa:** 4 h · **Depende de:** E-04
- **Branch:** `task-<nº>-testes-modo-offline`

MockClient, conectividade falsa e SharedPreferences em memória. Prompt do Membro E, item 7.

Critérios de aceite:

- Todos os casos do item 7 do prompt cobertos; `flutter test` passa

#### [A-10] Integrar na main e preparar o ambiente da demo

- **Story:** S6 · **Membro:** A · **Dia:** 4–5 · **Estimativa:** 3 h · **Depende de:** —
- **Branch:** `task-<nº>-integracao-ambiente-demo`

Acompanhar os merges na main, configurar o projeto Supabase compartilhado com o reset e garantir que backend e app rodam juntos a partir da main.

Critérios de aceite:

- Main sobe do zero (reset do banco, backend e app) seguindo os READMEs
- Projeto Supabase da demo com o seed aplicado

#### [A-11] Executar os testes de aceitação e registrar os bugs

- **Story:** S6 · **Membro:** A · **Dia:** 5 · **Estimativa:** 3 h · **Depende de:** A-10
- **Branch:** `task-<nº>-testes-aceitacao`

Executar com a equipe os 10 testes da seção 7 do backlog e registrar o resultado em documentos/desenvolvimento/05-testes-aceitacao.md. Cada falha vira um Bug no Jira.

Critérios de aceite:

- Resultado dos 10 testes documentado
- Bugs abertos no Jira para cada falha

#### [B-12] Atualizar o diagrama de classes e a arquitetura com o código real

- **Story:** S6 · **Membro:** B · **Dia:** 6 · **Estimativa:** 3 h · **Depende de:** A-10
- **Branch:** `task-<nº>-diagrama-classes-final`

Comparar o código com 03-arquitetura.md, listar diferenças e atualizar diagrama, árvore de diretórios real e rastreabilidade. Prompt final, itens 1 a 3.

Critérios de aceite:

- Diagrama, árvore de diretórios e rastreabilidade iguais ao código da main
- Diferenças que exigem mudar código registradas como Bug

#### [E-07] Revisar os artefatos do 1º bimestre

- **Story:** S6 · **Membro:** E · **Dia:** 6 · **Estimativa:** 2 h · **Depende de:** B-12
- **Branch:** `task-<nº>-revisao-artefatos-1-bim`

Atualizar o que a implementação mudou: mapa de dados (sessão, registro_id), diagramas de sequência UC-S05 e UC-I02 e regras/requisitos afetados ("melhorias em todo o projeto"). Prompt final, item 4.

Critérios de aceite:

- Documentos do 1º bimestre coerentes com o código e o diagrama de classes

#### [C-08] Roteiro da demo e evidências do Jira

- **Story:** S6 · **Membro:** C · **Dia:** 6–7 · **Estimativa:** 2 h · **Depende de:** A-11
- **Branch:** `task-<nº>-roteiro-demo`

Roteiro da apresentação baseado nos testes de aceitação e prints do Jira (backlog, sprint, quadro, epic/stories) para a pasta de evidências.

Critérios de aceite:

- Roteiro em documentos/desenvolvimento/06-roteiro-demo.md
- Prints do Jira da sprint salvos

#### [A-12] Conferir as exigências da disciplina para a entrega

- **Story:** S6 · **Membro:** A · **Dia:** 7 · **Estimativa:** 1 h · **Depende de:** B-12, E-07, C-08
- **Branch:** `task-<nº>-checklist-entrega`

Conferir a seção 11 do backlog e o que falta para 02/12 às 19:31. Prompt final, item 5.

Critérios de aceite:

- Todas as linhas da seção 11 atendidas ou com responsável e prazo
