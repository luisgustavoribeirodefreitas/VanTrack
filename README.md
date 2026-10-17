# VanTrack

## Alunos
- RA143379: Luís Gustavo Ribeiro de Freitas
- RA145121: Pedro Augusto dos Santos Watermann
- RA145116: Gustavo Bragada Cavalcanti
- RA133649: Amanda da Silva Palacio
- RA143653: Vinicius Garcia Del Cielo

Aplicativo de gestão e acompanhamento de vans escolares.

O VanTrack tem como objetivo melhorar a comunicação entre motoristas,
alunos e responsáveis, oferecendo rastreamento da van em tempo real,
controle de presença e roteirização dinâmica.

## Entrega do 1º bimestre

Artefatos finais, na pasta [`entrega-1-bimestre/`](entrega-1-bimestre/):

| Artefato | Arquivo |
|---|---|
| Documento de regras de negócio | [01-regras-de-negocio.pdf](entrega-1-bimestre/01-regras-de-negocio.pdf) |
| Documento de requisitos (funcionais, não funcionais e rastreabilidade) | [02-documento-de-requisitos.pdf](entrega-1-bimestre/02-documento-de-requisitos.pdf) |
| Documento de casos de uso | [03-documento-de-casos-de-uso.pdf](entrega-1-bimestre/03-documento-de-casos-de-uso.pdf) |
| Diagrama de casos de uso | [04-diagrama-de-casos-de-uso.png](entrega-1-bimestre/04-diagrama-de-casos-de-uso.png) |
| Diagramas de sequência | [05-diagramas-de-sequencia.pdf](entrega-1-bimestre/05-diagramas-de-sequencia.pdf) (imagens individuais em [documentos/atividade-04/imagens](documentos/atividade-04/imagens/)) |
| Evidências do Jira (tarefas, histórias e sprints) | [06-evidencias-jira/](entrega-1-bimestre/06-evidencias-jira/) |

## Documentação (fontes em Markdown)

### Atividade 01 — Mapas de modelagem

- [Mapa de usuários e objetivos](documentos/atividade-01/01-mapa-usuarios.md)
- [Mapa de fluxos](documentos/atividade-01/02-mapa-fluxos.md)
- [Mapa de dados](documentos/atividade-01/03-mapa-dados.md)

### Atividade 02 — Regras e Requisitos

- [Regras de Negócio](documentos/atividade-02/01-regras-negocio.md)
- [Requisitos Funcionais](documentos/atividade-02/02-requisitos-funcionais.md)
- [Requisitos Não Funcionais](documentos/atividade-02/03-requisitos-nao-funcionais.md)
- [Rastreabilidade](documentos/atividade-02/04-rastreabilidade.md)

### Atividade 03 — Casos de Uso

- [Documento de casos de uso](documentos/atividade-03/01-casos-de-uso.md)
- [Diagrama de casos de uso](documentos/atividade-03/diagrama-casos-de-uso.png) (gerado por [script](documentos/atividade-03/scripts/gerar_diagrama_casos_de_uso.py))

### Atividade 04 — Diagramas de Sequência

- [Documento dos diagramas de sequência](documentos/atividade-04/01-diagramas-de-sequencia.md) (com a justificativa das responsabilidades dos participantes)
- [Scripts PlantUML](documentos/atividade-04/scripts/)
- [Imagens](documentos/atividade-04/imagens/)

## Como regenerar os PDFs

Requer Python 3 com o pacote `markdown` e o Microsoft Edge (ou Google Chrome).
Para regenerar também as imagens dos diagramas de sequência, defina `PLANTUML_JAR`
com o caminho do `plantuml.jar` (requer Java).

```bash
pip install markdown
python ferramentas/gerar_artefatos.py
```
