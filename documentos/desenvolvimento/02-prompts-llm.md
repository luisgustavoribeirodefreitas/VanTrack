# Prompts para implementar o UC-S05 com uma LLM

Um prompt por membro, para usar junto com o [backlog do UC-S05](01-backlog-uc-s05.md).
Os prompts seguem as exigências do professor (seção 11 do backlog): diagrama de classes,
arquitetura em camadas, branch por task do Jira e rastreabilidade até as classes.

## Como usar

1. **Ordem:** no Dia 1 o Membro B roda primeiro o **Prompt 0** (diagrama de classes e
   arquitetura) e a equipe revisa. O código de todos segue esse diagrama.
2. **Uma task do Jira = uma branch = uma conversa com a LLM.** Crie a branch no padrão do
   professor (`task-<número>-<descricao-curta>`) e monte a mensagem assim:

   ```text
   [Contexto do projeto]
   [Prompt do seu membro]
   Task desta conversa: <CHAVE-DO-JIRA> — <título da task>
   ```

   O prompt do membro dá a visão da sua frente inteira; a última linha limita o que a LLM
   faz agora.
3. **De preferência, usem um agente de código dentro do repositório** (Claude Code, Cursor,
   Copilot em modo agente). Ele lê os arquivos citados sozinho. Se usarem um chat no
   navegador, anexem os arquivos da lista "Arquivos para anexar" do seu prompt.
4. Revisem o código gerado antes de abrir o PR. Vocês vão precisar explicá-lo na apresentação,
   e o professor cobra a relação entre o diagrama de classes e o código.
5. Problema achado em teste vira **Bug** no Jira, com branch própria, e é corrigido do mesmo jeito.

### Antes de começar (uma vez por pessoa)

- Instalar o Flutter (já traz o Dart) e o Dart Frog: `dart pub global activate dart_frog_cli`.
- Criar um projeto gratuito no Supabase **para desenvolvimento próprio**. Cada membro usa o seu,
  para que um não apague os dados do outro ao rodar o seed. A equipe cria mais um projeto
  compartilhado para a integração e a demo.
- Copiar a string de conexão do banco (Supabase → Project Settings → Database → Connection
  string, modo "Session pooler") para `backend/.env`. **Nunca commitar o `.env`.**

---

## Contexto do projeto (igual para todos)

```text
Você vai me ajudar a implementar parte do VanTrack, um app de acompanhamento de vans
escolares, feito como trabalho da disciplina Análise e Projeto de Software por uma equipe
de 5 pessoas em uma sprint de 7 dias. A equipe implementa um único caso de uso:
UC-S05 Registrar Embarque, com o include UC-I02 Notificar Responsável e o fluxo
alternativo A1 (sem conectividade). O professor avalia se o código segue o que foi
modelado: regras de negócio -> requisitos -> caso de uso -> diagrama de sequência ->
diagrama de classes -> arquitetura -> diretórios -> implementação.

Stack combinada pela equipe:
- Backend: Dart, com o framework Dart Frog. Ele expõe a API REST da seção 3 do backlog.
- Banco: Supabase, usado SOMENTE como banco PostgreSQL. O backend conecta direto no
  Postgres com o pacote `postgres`. O app NÃO acessa o Supabase: tudo passa pela API em
  Dart. Não usar Supabase Auth, Realtime, Storage, Edge Functions nem o pacote
  supabase_flutter.
- App (Android e Web obrigatórios; iOS se alguém puder testar): Flutter.
- Testes: `dart test` (package:test + mocktail) no backend e `flutter test`
  (flutter_test + mocktail) no app.

Bibliotecas combinadas (não adicione outras sem me perguntar, porque a equipe precisa
combinar):
- backend: dart_frog, postgres, dotenv, uuid, test, mocktail
- app: http, shared_preferences, connectivity_plus, geolocator, uuid, intl, mocktail
- estado no app: setState e ChangeNotifier do próprio Flutter. NÃO usar Riverpod, Bloc,
  GetX nem Provider.
- navegação no app: Navigator padrão do Flutter (sem go_router).

Arquitetura (definida em documentos/desenvolvimento/03-arquitetura.md, com o diagrama de
classes do UC-S05):
- Camadas: apresentação (rotas HTTP e controllers no backend; telas no app), aplicação
  (services que coordenam o caso de uso), domínio (entidades com comportamento e os
  CONTRATOS dos repositórios) e infraestrutura (implementação Postgres dos repositórios,
  conexão, cliente HTTP, armazenamento local).
- Diretórios por funcionalidade, com as camadas dentro de cada módulo
  (ex.: backend/lib/embarque/aplicacao/embarque_service.dart). Use os módulos e pastas
  definidos em 03-arquitetura.md.
- Dependências permitidas: apresentação -> aplicação -> domínio; infraestrutura implementa
  os contratos do domínio. O domínio não importa nada de Dart Frog, postgres, http nem
  Flutter. Controllers não acessam repositórios nem contêm regra de negócio.
- Entidades não são anêmicas: a regra que depende só do estado da entidade fica nela
  (ex.: Presenca.registrarEmbarque valida o status, RN-010). Services coordenam.
- No Dart Frog, os arquivos de backend/routes/ só leem a requisição e chamam o Controller.

Estrutura do repositório:
- backend/   -> servidor Dart Frog (rotas em backend/routes/, módulos em backend/lib/)
- app/       -> aplicativo Flutter (módulos em app/lib/)
- supabase/  -> migrations/ (arquivos .sql numerados) e seed.sql (dados de teste)

Configuração:
- Backend: a string de conexão vem de backend/.env (variável DATABASE_URL). O .env NÃO é
  commitado; mantenha um backend/.env.example sem a senha. O servidor roda na porta 8080.
- App: a URL da API vem de --dart-define=API_URL (padrão http://localhost:8080; no emulador
  Android é http://10.0.2.2:8080). Dados mockados com --dart-define=USE_MOCK=true.
- Datas: colunas timestamptz no banco e ISO 8601 com fuso no JSON. Ao mostrar HH:MM (na
  tela ou em mensagens geradas pelo servidor), use o horário de Brasília (UTC-3, sem horário
  de verão). Cuidado: o servidor pode estar em UTC.
- IDs: bigint (int no Dart). O registroId do embarque é UUID (String).

Fontes da verdade:
- documentos/desenvolvimento/01-backlog-uc-s05.md — leia inteiro, principalmente a seção 3
  (contrato da API e do módulo de embarque), 6 (seed), 7 (testes de aceitação),
  10 (interface) e 11 (exigências do professor);
- documentos/desenvolvimento/03-arquitetura.md — diagrama de classes, camadas e pastas;
- documentos/atividade-03/01-casos-de-uso.md (UC-S05, UC-R02 e UC-I02);
- documentos/atividade-04/scripts/UC-S05.puml, UC-R02.puml e UC-I02.puml (sequência);
- documentos/atividade-02/ (regras de negócio e requisitos).

Regras para você:
1. Implemente SOMENTE a task indicada na última linha da mensagem, dentro da parte do
   membro descrita abaixo. As outras partes estão sendo feitas por outras pessoas ao
   mesmo tempo.
2. Não altere o contrato da API nem o contrato do módulo de embarque (seção 3 do backlog).
   Se achar que ele precisa mudar, pare e me explique o motivo, porque a equipe precisa
   combinar.
3. Use as classes, atributos, operações e pastas do diagrama de classes (03-arquitetura.md),
   com os mesmos nomes. Se precisar de uma classe ou operação que não está no diagrama,
   não invente em silêncio: me avise, para atualizarmos o diagrama e manter a
   rastreabilidade.
4. Repositórios: contrato (classe abstrata) no domínio e implementação Postgres na
   infraestrutura, para os services serem testados com mocks, sem banco.
5. Cada classe principal tem um comentário de documentação (///) com: responsabilidade,
   e as RN, RF e UC relacionados. Quando um trecho implementar uma regra, cite-a em um
   comentário curto (ex.: // RN-012: só o motorista ativo da van).
6. Antes de escrever código, me mostre um plano curto (arquivos que vai criar ou alterar)
   e espere eu aprovar.
7. Prefira a solução mais simples que cumpra os critérios de aceite. Nada de
   funcionalidades fora do backlog.
8. Escreva os testes pedidos. No fim, me diga: como rodar, como testar manualmente, o que
   ficou faltando, o que depende de outro membro e uma sugestão de mensagem de commit
   começando pela chave da task do Jira.
9. Textos da interface e mensagens de erro em português, iguais aos do backlog.
10. Nunca coloque senha, string de conexão ou chave do Supabase no código ou em arquivo
    commitado. Não faça commit na main, merge nem push: isso é comigo.
```

---

## Prompt 0 — Diagrama de classes e arquitetura (Membro B, Dia 1)

**Arquivos para anexar (chat no navegador):** backlog, `01-casos-de-uso.md`,
`03-mapa-dados.md`, `01-regras-negocio.md`, `02-requisitos-funcionais.md`, `UC-S05.puml`,
`UC-R02.puml`, `UC-I02.puml`.

```text
Eu sou o Membro B. Antes de alguém programar, preciso entregar o projeto da solução do
UC-S05: diagrama de classes, arquitetura e estrutura de diretórios. É exigência do
professor e é a base que os outros 4 membros vão seguir. NÃO escreva código de
implementação nesta conversa, só a documentação.

Siga o caminho que o professor pede: regras de negócio -> requisitos -> caso de uso ->
diagrama de sequência -> identificação de classes -> responsabilidades -> diagrama de
classes -> arquitetura -> diretórios.

Crie documentos/desenvolvimento/03-arquitetura.md com:

1. Identificação das classes, a partir das mensagens dos diagramas de sequência UC-S05,
   UC-R02 e UC-I02, do mapa de dados e do backlog (seções 3 e 4). Tabela com
   Classe | Camada | Responsabilidade | Atributos | Operações. Inclua o backend e o app
   (TelaRotaDoDia, ModuloEmbarque e suas implementações, ArmazenamentoLocal). Explique
   quais participantes da sequência viraram classes e quais não (ex.: atores, banco).
2. Diagrama de classes em PlantUML, salvo em
   documentos/desenvolvimento/scripts/diagrama-classes-uc-s05.puml e referenciado no .md.
   - Atributos com visibilidade e tipo; operações com parâmetros e retorno.
   - Relacionamentos corretos (associação, agregação, composição, generalização,
     realização, dependência), com multiplicidades, escolhidos pela identidade, posse e
     ciclo de vida dos objetos. Justifique as composições.
   - Contratos de repositório (interfaces) separados das implementações Postgres.
   - Pacotes para as camadas/módulos.
   - Entidades com comportamento, não anêmicas. Partindo da sequência, por exemplo:
     Presenca.registrarEmbarque(dataHora, localizacao): Embarque, que valida o status
     (RN-010); VinculoMotoristaVan.estaAtivo(); Notificacao.deEmbarque(...) que monta a
     mensagem; Notificacao.marcarComoLida().
   - Se o diagrama ficar grande, faça um de domínio e um da aplicação/infraestrutura.
3. Arquitetura em camadas: apresentação, aplicação, domínio e infraestrutura; quais classes
   ficam em cada uma; dependências permitidas e dependências a evitar (ex.: controller não
   acessa repositório; domínio não depende de Dart Frog, postgres nem Flutter). Explique
   que camada lógica não é o mesmo que diretório físico.
4. Estrutura de diretórios do backend (Dart Frog) e do app (Flutter), em árvore comentada,
   organizada por funcionalidade com as camadas dentro de cada módulo. Proposta inicial
   para você avaliar e justificar (pode mudar, explicando o motivo):
   - backend/lib/: compartilhado/ (conexão, autenticação, erros HTTP), cadastro/ (Aluno,
     Responsavel, Motorista, Van, vínculos), rota/ (Rota, PontoParada, Presenca, Embarque),
     embarque/ (EmbarqueController, EmbarqueService), notificacao/ (Notificacao,
     NotificacaoRepository, NotificacaoService); backend/routes/ só com as rotas HTTP.
   - app/lib/: compartilhado/ (cliente da API, sessão, cores), login/, embarque/
     (apresentacao, aplicacao, dominio, infraestrutura), avisos/.
   Evite dependência circular entre módulos.
5. Documentação das classes principais (EmbarqueService, Presenca, NotificacaoService,
   ModuloEmbarque): Classe | Responsabilidade | Operações | Dependências | RN | RF | UC.
6. Rastreabilidade RN -> RF -> UC -> classes e operações, para RN-002, RN-009, RN-010,
   RN-012, RF-009, RF-011, RNF-005 e RNF-006 (ex.: RN-010 -> RF-009 -> UC-S05 passo 3 ->
   Presenca.registrarEmbarque).
7. Decisões arquiteturais com justificativa: API REST em Dart Frog, Supabase só como
   Postgres, idempotência pelo registroId, fila offline no app, notificação por polling.

Mantenha o contrato da API e o contrato do módulo de embarque do backlog (seção 3)
exatamente como estão. Se o diagrama mostrar que algo do backlog está errado ou
incompleto, liste no fim do documento, em "Pontos para a equipe decidir", em vez de mudar.
Se o PlantUML estiver instalado, gere também a imagem PNG.
```

---

## Membro A — Backend base, seed e integração

**Arquivos para anexar (chat no navegador):** backlog, `03-arquitetura.md`,
`01-casos-de-uso.md`, `03-mapa-dados.md`.

```text
Eu sou o Membro A. Minha parte: backend base, modelo de dados, seed e o endpoint que lista
os alunos da rota. Sou o primeiro a entregar, porque os Membros B e C dependem das minhas
tabelas, entidades e repositórios.

O login simplificado e o middleware de autenticação são do Membro C; o meu endpoint usa o
usuário logado que esse middleware disponibiliza.

Se documentos/desenvolvimento/03-arquitetura.md ainda não existir, faça só os itens 1 a 5
(projeto, CORS, SQL, seed e reset) e pare: as classes Dart dependem do diagrama.

Implemente:
1. backend/: projeto Dart Frog rodando na porta 8080, lendo DATABASE_URL do backend/.env,
   com backend/.env.example e o .env no .gitignore. Uma única conexão/pool com o Postgres,
   na infraestrutura do módulo compartilhado, usada pelos repositórios.
2. Middleware de CORS liberando qualquer origem em desenvolvimento (sem isso o Flutter Web
   não consegue chamar a API), incluindo resposta ao preflight OPTIONS.
3. supabase/migrations/001_base.sql com as tabelas, seguindo
   documentos/atividade-01/03-mapa-dados.md e o diagrama de classes: empresa, van,
   motorista, vinculo_motorista_van (início, fim; só um ativo por van), responsavel,
   aluno, aluno_responsavel (N:N), ponto_parada, rota (data, trajeto, horário previsto,
   situação), presenca (situação: CONFIRMADO, AUSENTE, EMBARCADO; ordem na rota; ponto de
   parada) e embarque (registro_id uuid único, data_hora timestamptz, latitude/longitude
   opcionais, sincronizado), e uma tabela sessao para os tokens de login.
   Ative RLS em todas as tabelas, sem policies: isso bloqueia o acesso público pela API
   automática do Supabase, e o backend continua acessando porque conecta como dono do banco.
   NÃO crie a tabela de notificação: ela é do Membro C (002_notificacao.sql).
4. supabase/seed.sql exatamente como a seção 6 do backlog, com a rota sempre na data de
   hoje (current_date). Deve poder rodar de novo do zero.
5. backend/bin/reset_db.dart: um comando (`dart run bin/reset_db.dart`) que apaga as
   tabelas, roda todos os arquivos de supabase/migrations/ em ordem e depois o seed.sql,
   usando o DATABASE_URL. Assim cada membro reseta o próprio projeto do Supabase.
6. Entidades de domínio do diagrama de classes (Aluno, Responsavel, Motorista, Van,
   VinculoMotoristaVan, Rota, PontoParada, Presenca, Embarque), com os atributos e as
   operações simples do próprio estado (ex.: VinculoMotoristaVan.estaAtivo()).
   Presenca.registrarEmbarque é do Membro B: deixe só a assinatura com um
   UnimplementedError.
7. Contratos PresencaRepository e VinculoRepository (buscar responsáveis de um aluno;
   motorista ativo de uma van) no domínio, e as implementações Postgres na
   infraestrutura. Os Membros B e C vão usá-los.
8. GET /rotas/{rotaId}/alunos conforme a seção 3: só presenças CONFIRMADO ou EMBARCADO,
   na ordem da rota; só o motorista ativo da van da rota pode chamar (RN-012, senão 403);
   aluno AUSENTE não aparece (exceção da RN-010). Rota HTTP -> Controller -> Service ->
   repositório, como nas camadas definidas. Testes: aluno ausente não aparece; motorista
   sem vínculo recebe 403; ordem correta.
9. backend/README.md curto: instalar, configurar o .env, resetar o banco, subir o servidor
   (`dart_frog dev`).

Testes também do que for criado nos itens 6 e 7 (ex.: VinculoMotoristaVan.estaAtivo()).

Critérios de aceite: os da seção 4 do backlog, Membro A.
```

---

## Membro B — Backend do embarque

**Arquivos para anexar (chat no navegador):** backlog, `03-arquitetura.md`,
`01-casos-de-uso.md`, `UC-S05.puml`.

```text
Eu sou o Membro B. Minha parte: o registro do embarque no servidor (UC-S05, RF-009).
O diagrama de classes (03-arquitetura.md) foi feito por mim no Dia 1 e revisado pela
equipe; siga-o.

As tabelas, as entidades, os repositórios e a conexão com o banco são do Membro A; o login
e a autenticação são do Membro C. Use o que já existe em backend/ e supabase/. Se faltar alguma coisa de que você
precisa, NÃO crie uma tabela ou classe duplicada: pare e me diga o que falta para eu
combinar com o Membro A.

Implemente, seguindo o diagrama de sequência documentos/atividade-04/scripts/UC-S05.puml:
1. Domínio: o método Presenca.registrarEmbarque(dataHora, localizacao): Embarque, na classe
   Presenca do Membro A (hoje com UnimplementedError). A própria entidade valida que está
   CONFIRMADO (RN-010), muda o status para EMBARCADO e devolve o Embarque. Se não estiver
   CONFIRMADO, lança uma exceção de domínio (que vira 409 na apresentação).
2. Apresentação: rota do Dart Frog backend/routes/rotas/[rotaId]/embarques/index.dart (POST)
   que chama o EmbarqueController. O controller só converte JSON <-> objetos e exceções <->
   códigos HTTP; corpo e respostas exatamente como na seção 3 do backlog
   (201, 200, 403, 404, 409).
3. Aplicação: EmbarqueService.registrarEmbarque(rotaId, alunoId, registroId, dataHora,
   localizacao?, motoristaId), que coordena o caso de uso:
   - valida que o usuário logado é o motorista ativo da van da rota (RN-012) -> 403;
   - valida que a rota e o aluno existem -> 404;
   - idempotência: se o registroId já foi processado, devolve o mesmo resultado (200),
     sem salvar de novo e sem notificar de novo;
   - chama presenca.registrarEmbarque com a dataHora recebida (é a hora do toque no
     aparelho, NÃO a hora do servidor) e salva a presença e o embarque;
   - depois de salvar, chama NotificacaoService.notificarMovimentacao(presenca,
     TipoMovimentacao.embarque) (ponto do include UC-I02).
   Salvar o embarque e mudar o status devem acontecer na mesma transação do Postgres
   (runTx do pacote postgres). Se precisar de um método novo no repositório para isso,
   adicione-o no contrato e na implementação e me avise para eu alinhar com o Membro A.
   Proteja contra corrida: a coluna registro_id é única; se o insert violar a unicidade,
   trate como "já processado" (200).
4. Enquanto o Membro C não entrega o NotificacaoService, crie o contrato NotificacaoService
   com o método notificarMovimentacao e uma implementação vazia (NotificacaoServiceVazio),
   em arquivos separados, nas pastas do módulo notificacao definidas no diagrama. O
   Membro C só vai criar a implementação real.
5. Rota backend/routes/rotas/[rotaId]/embarques/sincronizar.dart (POST): recebe
   { registros: [...] }, processa cada um com o mesmo EmbarqueService e devolve o resultado
   por registroId. Um registro com erro não pode impedir os outros.
6. Testes:
   - da entidade Presenca: CONFIRMADO embarca; AUSENTE e EMBARCADO lançam a exceção;
   - do EmbarqueService com mocktail (sem banco): um teste para cada linha da tabela de
     respostas da seção 3, mais: mesmo registroId duas vezes gera um único embarque e uma
     única chamada ao NotificacaoService; a dataHora salva é a enviada.

Critérios de aceite: os da seção 4 do backlog, Membro B.
```

---

## Membro C — Notificação ponta a ponta (UC-I02)

**Arquivos para anexar (chat no navegador):** backlog, `03-arquitetura.md`,
`01-casos-de-uso.md`, `UC-I02.puml`.

```text
Eu sou o Membro C. Minha parte: o login simplificado do backend (apoio para todos) e o
UC-I02 Notificar Responsável sobre Embarque, do servidor até a tela "Avisos" do
responsável no app.

As tabelas e entidades de aluno, responsável e vínculo, a tabela sessao e a conexão com o
banco são do Membro A. O contrato NotificacaoService foi criado pelo Membro B, e o
EmbarqueService dele chama notificarMovimentacao. A estrutura do app e a tela de login são
do Membro D. Não altere o que é deles; se precisar de algo, me avise.

Backend:
1. supabase/migrations/002_notificacao.sql com a tabela notificacao: tipo do evento
   (EMBARQUE), responsável destinatário, aluno, mensagem, data/hora do evento (timestamptz),
   lida. Com RLS ativado e sem policies, como as tabelas do Membro A.
2. Login simplificado (módulo compartilhado), conforme a seção 3 do backlog: GET /usuarios
   (motoristas e responsáveis do seed, com nome e papel) e POST /login, que recebe o id e o
   papel de um usuário do seed e devolve um token (UUID salvo na tabela sessao). Middleware
   que valida o token do header Authorization e deixa disponível no contexto do Dart Frog
   quem é o usuário e o papel (MOTORISTA ou RESPONSAVEL); sem token válido -> 401. O login
   é só apoio: não é o caso de uso avaliado. Os Membros A e B dependem dele, então é a
   primeira coisa a ir para a main.
Os itens 3 a 5 seguem o diagrama de sequência documentos/atividade-04/scripts/UC-I02.puml e
o módulo notificacao do diagrama de classes.
3. Domínio: entidade Notificacao com comportamento, como no diagrama: a fábrica
   Notificacao.deEmbarque(...) monta a mensagem "<nome do aluno> embarcou na van às
   HH:MM." com a hora do embarque convertida para o horário de Brasília (não a hora
   atual: o embarque pode ter vindo de sincronização offline), e marcarComoLida().
   Contrato NotificacaoRepository no domínio e implementação Postgres na infraestrutura.
   Teste: a hora da mensagem é a do embarque em horário de Brasília.
4. Aplicação: implementação real do NotificacaoService (mesmo contrato do Membro B),
   registrada no lugar da versão vazia:
   - busca os responsáveis do aluno pelo VinculoRepository (RN-002, RN-009);
   - cria uma Notificacao para cada responsável e registra o evento como comunicado;
   - A1: aluno sem responsável -> não cria nada e retorna normalmente, sem erro.
   Testes com mocktail: aluno com 2 responsáveis -> 2 notificações; aluno sem
   responsável -> 0.
5. Apresentação: rotas do Dart Frog GET /notificacoes?desde={dataHora} conforme a seção 3,
   só com notificações do usuário logado (RN-002); e PATCH /notificacoes/{id}/lida, que só
   deixa marcar notificações do próprio usuário. Rota HTTP -> Controller -> Service.
   Teste: responsável não recebe nem marca notificação de aluno de outra família.

App (módulo avisos/ em app/lib/, com as camadas do diagrama):
6. Tela "Avisos" exatamente como a seção 10 do backlog: card por aluno com status
   ("Na van desde HH:MM" ou "Aguardando embarque"), lista de avisos do dia (mais novo
   primeiro, não lidos com um ponto), "Atualizado há X s", faixa de sem conexão (RNF-003)
   e estado vazio.
7. Atualização a cada ~10 s com Timer.periodic, cancelado no dispose. Se a requisição
   falhar, manter os avisos na tela e mostrar a faixa de sem conexão.
8. Ao abrir a tela, marcar os avisos exibidos como lidos.
9. Use o cliente de API e o token de login do módulo compartilhado (do Membro D); não crie
   outro.

Push real (Firebase Cloud Messaging) NÃO faz parte desta entrega. Só implemente se eu
pedir depois.

Critérios de aceite: os da seção 4 do backlog, Membro C.
```

---

## Membro D — App do motorista (UC-R02)

**Arquivos para anexar (chat no navegador):** backlog, `03-arquitetura.md`,
`01-casos-de-uso.md`, `UC-R02.puml`.

```text
Eu sou o Membro D. Minha parte: o projeto Flutter, a tela de login e a tela "Rota do dia" do
motorista (UC-R02). Sou dono da estrutura do app; o Membro C vai adicionar o módulo avisos
e o Membro E vai criar a versão offline do módulo de embarque.

Implemente, em app/, com os módulos e camadas do diagrama de classes (03-arquitetura.md):
1. Projeto Flutter rodando no Android e na Web (RNF-004), com as pastas dos módulos
   compartilhado/, login/, embarque/ e avisos/ como definido no documento de arquitetura.
2. Módulo compartilhado: cliente HTTP (pacote http) com a URL de --dart-define=API_URL e o
   token de login no header Authorization; sessão do usuário logado; cores do app (um
   único verde e um único âmbar). Com --dart-define=USE_MOCK=true, devolve dados
   mockados no formato da seção 3, com os alunos do seed da seção 6 (Ana Souza, Beatriz
   Reis, Carlos Lima).
3. Módulo login: lista os usuários (GET /usuarios), um toque entra (POST /login).
   Motorista vai para "Rota do dia"; responsável vai para "Avisos" (crie a tela só com um
   texto provisório: ela é do Membro C).
4. Módulo embarque, camada de aplicação: a classe abstrata ModuloEmbarque e os tipos do
   contrato interno da seção 3 do backlog, EXATAMENTE como estão lá, e a primeira
   implementação, ModuloEmbarqueOnline. registrarEmbarque gera o registroId (pacote uuid),
   pega DateTime.now() e tenta a localização com o geolocator com limite de 2 s (sem
   permissão ou sem resposta, envia sem localização: o toque nunca pode ficar esperando o
   GPS), chama POST /rotas/{rotaId}/embarques (pela infraestrutura do módulo) e devolve
   StatusEnvio.enviado. Erros 403/404/409 viram EmbarqueException. listarPendentes devolve
   lista vazia e aoMudarPendentes é um Stream vazio. A implementação usada é escolhida em
   um único lugar (main.dart), para o Membro E trocar com uma linha.
5. Módulo embarque, camada de apresentação: TelaRotaDoDia exatamente como a seção 10 do
   backlog:
   - cabeçalho com trajeto, horário, placa e "X de Y na van";
   - "Próxima parada" em destaque com botão "Embarcou" grande, de largura total
     (no mínimo 56 de altura);
   - "Depois" com as demais paradas e botão menor (o aluno pode embarcar fora de ordem);
   - "Na van" com Icons.check_circle verde e "Embarcou às HH:MM", ou Icons.cloud_off âmbar e
     "Pendente de sincronização" quando o módulo devolver StatusEnvio.pendente;
   - um toque registra, SEM diálogo de confirmação (RNF-005);
   - após o toque o aluno muda de seção na hora e a próxima parada é destacada;
   - escutar aoMudarPendentes para trocar âmbar por verde sem recarregar (e mostrar o erro
     se o registro for rejeitado);
   - widget FaixaSemConexao (âmbar, Icons.wifi_off) no topo, recebendo um bool. Deixe-o
     pronto e escondido; o Membro E vai ligá-lo à detecção de rede;
   - mensagens de carregando, 403, 409, lista vazia e erro, com os textos da seção 10
     (409 em SnackBar).
   A tela só conversa com o ModuloEmbarque (e um serviço para listar os alunos da rota),
   nunca direto com o cliente HTTP.
6. Status sempre com cor + ícone + texto, nunca só cor.
7. Testes de widget da TelaRotaDoDia com um ModuloEmbarque falso: tocar "Embarcou" move o
   aluno para "Na van" e destaca a próxima parada; status pendente mostra o ícone âmbar.

Critérios de aceite: os da seção 4 do backlog, Membro D.
```

---

## Membro E — Modo offline e sincronização (A1, RNF-006)

**Arquivos para anexar (chat no navegador):** backlog, `03-arquitetura.md`,
`01-casos-de-uso.md`, `UC-S05.puml`, e os arquivos do módulo `app/lib/embarque/` criados
pelo Membro D.

```text
Eu sou o Membro E. Minha parte: o fluxo alternativo A1 do UC-S05 (sem conectividade) e o
RNF-006: embarques registrados sem sinal ficam no aparelho e são enviados sozinhos ao
reconectar.

A tela "Rota do dia" e a versão online do módulo são do Membro D. Eu crio uma NOVA
implementação da classe abstrata ModuloEmbarque (contrato interno da seção 3 do backlog),
sem mudar a classe abstrata, e troco a implementação usada no main.dart. Na tela, só posso
ligar o widget FaixaSemConexao à detecção de rede.

Implemente, no módulo embarque do app, nas camadas do diagrama de classes, seguindo o bloco
"A1 - Sem conectividade" de documentos/atividade-04/scripts/UC-S05.puml:
1. Infraestrutura: ArmazenamentoLocal, fila persistente com shared_preferences (lista de
   registros em JSON), que funciona no Android e na Web e sobrevive a fechar e abrir o app.
2. Infraestrutura: detecção de conectividade com connectivity_plus. Além disso, trate
   timeout (5 s) e erro de rede na chamada da API como "offline" (na Web o estado de rede
   não é confiável). Exponha o estado como um ValueNotifier<bool> para a FaixaSemConexao.
3. Aplicação: ModuloEmbarqueComFila implements ModuloEmbarque. registrarEmbarque:
   - gera registroId e captura data/hora e localização NO MOMENTO DO TOQUE (localização com
     limite de 2 s, como na versão do Membro D);
   - online: envia à API; se der erro de rede ou timeout, guarda na fila e devolve
     StatusEnvio.pendente;
   - offline: guarda na fila e devolve StatusEnvio.pendente na hora, sem travar a tela;
   - erros 403/404/409 da API NÃO vão para a fila: viram EmbarqueException para a tela.
4. Sincronização:
   - ao reconectar, envia a fila para POST /rotas/{rotaId}/embarques/sincronizar;
   - remove da fila só os registros confirmados pelo servidor (201 ou 200);
   - registro rejeitado (409 etc.) sai da fila e é avisado no stream aoMudarPendentes, para
     a tela mostrar o erro;
   - enquanto houver pendentes, tenta de novo a cada 30 s (meta do RNF-006: até 5 min após
     reconectar);
   - ao abrir o app com pendentes na fila, tenta sincronizar;
   - nunca dispare duas sincronizações ao mesmo tempo (use uma flag de "sincronizando").
5. listarPendentes e o stream aoMudarPendentes funcionando, para a tela mostrar e atualizar
   o ícone "Pendente de sincronização".
6. Trocar no main.dart a implementação para ModuloEmbarqueComFila e ligar a
   FaixaSemConexao da TelaRotaDoDia ao ValueNotifier de conectividade.
7. Testes com flutter_test (sem rede de verdade): use MockClient do package:http/testing,
   uma conectividade falsa injetada no construtor e
   SharedPreferences.setMockInitialValues. Casos: offline vai para a fila; reconectar
   sincroniza e esvazia a fila; falha no meio da sincronização não perde nem duplica
   registros; a dataHora enviada é a do toque; 409 não vai para a fila; a fila sobrevive a
   recriar o módulo.

Critérios de aceite: os da seção 4 do backlog, Membro E, e os testes 8, 9 e 10 da seção 7.
```

---

## Prompt final — Documento de arquitetura e revisão dos artefatos (Dias 6–7)

Usado por três tasks: **B-12** (itens 1 a 3, Membro B), **E-07** (item 4, Membro E) e
**A-12** (item 5, Membro A). Cada um manda o prompt inteiro e indica a sua task na última
linha.

**Arquivos para anexar (chat no navegador):** backlog, `03-arquitetura.md`, o diagrama de
classes, e a árvore de arquivos de `backend/lib`, `backend/routes` e `app/lib`.

```text
O código do UC-S05 está integrado na main. Preciso fechar a documentação que o professor
cobra na entrega: o diagrama de classes e a arquitetura têm que bater com o código. NÃO
altere código nesta conversa, só documentação; se achar diferença que exija mudar código,
liste para a equipe abrir um Bug no Jira. Faça só os itens da minha task:
B-12 -> itens 1 a 3; E-07 -> item 4; A-12 -> item 5.

1. Compare o código de backend/ e app/ com documentos/desenvolvimento/03-arquitetura.md e
   o diagrama de classes. Liste as diferenças (classe, atributo, operação, relacionamento ou
   pasta) e, para cada uma, proponha: atualizar o diagrama ou abrir Bug no código.
2. Depois que eu aprovar, atualize o diagrama de classes e o documento de arquitetura para
   ficarem iguais ao código, incluindo a árvore de diretórios real, comentada.
3. Complete a rastreabilidade RN -> RF -> UC -> classes e operações com os nomes reais.
4. Verifique se os artefatos do 1º bimestre ficaram desatualizados pela implementação e
   proponha as correções ("melhorias em todo o projeto", pedido pelo professor):
   documentos/atividade-01/03-mapa-dados.md (ex.: tabela de sessão, registro_id),
   documentos/atividade-04/scripts/UC-S05.puml e UC-I02.puml (nomes de operações), e os
   requisitos/regras que mudaram.
5. Confira a seção 11 do backlog (exigências do professor) e diga o que ainda falta para a
   entrega de 02/12 às 19:31.
```
