"""Gera os artefatos de entrega do 1º bimestre a partir dos documentos em Markdown.

Saída: pasta `entrega-1-bimestre/` com os PDFs e imagens pedidos pelo professor.

Requisitos:
  - Python 3 com o pacote `markdown`  (pip install markdown)
  - Microsoft Edge ou Google Chrome instalado (usado em modo headless para gerar PDF/PNG)
  - Opcional: PlantUML (.jar) + Java para regenerar os diagramas de sequência:
        set PLANTUML_JAR=C:\\caminho\\plantuml.jar

Uso (na raiz do repositório):
  python ferramentas/gerar_artefatos.py
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import markdown

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "documentos"
SAIDA = RAIZ / "entrega-1-bimestre"

INTEGRANTES = [
    "Luís Gustavo Ribeiro de Freitas (RA143379)",
    "Pedro Augusto dos Santos Watermann (RA145121)",
    "Gustavo Bragada Cavalcanti (RA145116)",
    "Amanda da Silva Palacio (RA133649)",
    "Vinicius Garcia Del Cielo (RA143653)",
]

CSS = """
@page { size: A4; margin: 16mm 14mm 16mm 14mm; }
body { font-family: "Segoe UI", Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1d1d1f; }
h1 { font-size: 20pt; border-bottom: 2px solid #2E4A7A; padding-bottom: 4px; color: #1F3459; }
h2 { font-size: 15pt; color: #1F3459; margin-top: 22px; page-break-after: avoid; }
h3 { font-size: 12.5pt; color: #1F3459; page-break-after: avoid; }
h4 { font-size: 11pt; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 9.3pt; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #b9c3d3; padding: 4px 6px; vertical-align: top; text-align: left; }
th { background: #EEF3FA; }
code { font-family: Consolas, monospace; font-size: 9pt; background: #f3f4f6; padding: 0 3px; }
pre { background: #f3f4f6; padding: 8px; font-size: 9pt; white-space: pre-wrap; }
blockquote { border-left: 3px solid #b9c3d3; margin: 8px 0; padding: 2px 10px; color: #444; }
img { max-width: 100%; page-break-inside: avoid; display: block; margin: 6px auto; }
hr { border: none; border-top: 1px solid #d0d6e0; margin: 18px 0; }
.capa { border: 1px solid #b9c3d3; background: #F6F8FC; padding: 10px 14px; margin-bottom: 18px; font-size: 9.8pt; }
.capa b { color: #1F3459; }
.quebra { page-break-before: always; }
"""


def navegador():
    candidatos = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        shutil.which("msedge") or "",
        shutil.which("google-chrome") or "",
        shutil.which("chromium") or "",
    ]
    for c in candidatos:
        if c and Path(c).exists():
            return c
    sys.exit("Edge/Chrome não encontrado.")


def rebaixar_titulos(texto, niveis=1):
    """Aumenta o nível dos títulos (# → ##) para inserir um documento dentro de outro."""
    fora_de_codigo = []
    em_codigo = False
    for linha in texto.splitlines():
        if linha.startswith("```"):
            em_codigo = not em_codigo
        if not em_codigo and re.match(r"^#{1,5} ", linha):
            linha = "#" * niveis + linha
        fora_de_codigo.append(linha)
    return "\n".join(fora_de_codigo)


def capa(titulo_documento):
    nomes = "<br>".join(INTEGRANTES)
    return (f'<div class="capa"><b>VanTrack</b> — {titulo_documento}<br>'
            f'<b>Disciplina:</b> 9899/32 — Análise e Projeto de Software (2026)<br>'
            f'<b>Integrantes:</b><br>{nomes}<br>'
            f'<b>Gerado em:</b> {date.today().strftime("%d/%m/%Y")}</div>')


def md_para_pdf(partes, titulo_documento, destino, base_dir, browser, tmp, css_extra=""):
    """partes: lista de (texto_markdown, quebra_de_pagina_antes)."""
    corpo = [capa(titulo_documento)]
    for texto, quebra in partes:
        html = markdown.markdown(texto, extensions=["tables", "fenced_code", "sane_lists"])
        corpo.append(f'<div class="{"quebra" if quebra else ""}">{html}</div>')
    base = base_dir.resolve().as_uri() + "/"
    pagina = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
              f'<base href="{base}"><title>{titulo_documento}</title><style>{CSS}{css_extra}</style></head>'
              f'<body>{"".join(corpo)}</body></html>')
    arquivo_html = Path(tmp) / (destino.stem + ".html")
    arquivo_html.write_text(pagina, encoding="utf-8")
    subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--user-data-dir={Path(tmp) / 'perfil'}",
                    "--allow-file-access-from-files",
                    f"--print-to-pdf={destino}", arquivo_html.resolve().as_uri()],
                   check=True, capture_output=True)
    print("  ✔", destino.relative_to(RAIZ))


def ler(caminho):
    return (DOCS / caminho).read_text(encoding="utf-8")


def gerar_sequencias():
    jar = os.environ.get("PLANTUML_JAR")
    if not jar:
        print("  (PLANTUML_JAR não definido — usando as imagens já existentes dos diagramas de sequência)")
        return
    scripts = DOCS / "atividade-04" / "scripts"
    subprocess.run(["java", "-Dfile.encoding=UTF-8", "-jar", jar, "-charset", "UTF-8", "-Sdpi=170", "-tpng",
                    "-o", str((DOCS / "atividade-04" / "imagens").resolve()), *sorted(str(p) for p in scripts.glob("*.puml"))],
                   check=True)
    print("  ✔ diagramas de sequência regenerados")


def gerar_diagrama_casos_de_uso(browser, tmp):
    pasta = DOCS / "atividade-03"
    subprocess.run([sys.executable, str(pasta / "scripts" / "gerar_diagrama_casos_de_uso.py")], check=True,
                   capture_output=True)
    svg = pasta / "diagrama-casos-de-uso.svg"
    w, h = re.search(r'width="(\d+)" height="(\d+)"', svg.read_text(encoding="utf-8")).groups()
    png = pasta / "diagrama-casos-de-uso.png"
    subprocess.run([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={w},{h}",
                    f"--user-data-dir={Path(tmp) / 'perfil-png'}",
                    f"--screenshot={png}", svg.resolve().as_uri()], check=True, capture_output=True)
    print("  ✔", png.relative_to(RAIZ))
    return png


def main():
    browser = navegador()
    SAIDA.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        print("Diagramas:")
        gerar_sequencias()
        png_uc = gerar_diagrama_casos_de_uso(browser, tmp)

        print("Documentos:")
        md_para_pdf([(ler("atividade-02/01-regras-negocio.md"), False)],
                    "Documento de Regras de Negócio", SAIDA / "01-regras-de-negocio.pdf",
                    DOCS / "atividade-02", browser, tmp)

        requisitos = ("# Documento de Requisitos — VanTrack\n\n"
                      "Este documento reúne os requisitos funcionais, os requisitos não funcionais "
                      "e a matriz de rastreabilidade entre regras de negócio, requisitos e casos de uso.\n\n"
                      "1. Requisitos Funcionais (RF-001 a RF-016)\n"
                      "2. Requisitos Não Funcionais (RNF-001 a RNF-006)\n"
                      "3. Rastreabilidade (RN ↔ RF/RNF ↔ UC)\n")
        md_para_pdf([(requisitos, False),
                     (rebaixar_titulos(ler("atividade-02/02-requisitos-funcionais.md")), True),
                     (rebaixar_titulos(ler("atividade-02/03-requisitos-nao-funcionais.md")), True),
                     (rebaixar_titulos(ler("atividade-02/04-rastreabilidade.md")), True)],
                    "Documento de Requisitos", SAIDA / "02-documento-de-requisitos.pdf",
                    DOCS / "atividade-02", browser, tmp)

        md_para_pdf([(ler("atividade-03/01-casos-de-uso.md"), False)],
                    "Documento de Casos de Uso", SAIDA / "03-documento-de-casos-de-uso.pdf",
                    DOCS / "atividade-03", browser, tmp)

        shutil.copyfile(png_uc, SAIDA / "04-diagrama-de-casos-de-uso.png")
        print("  ✔", (SAIDA / "04-diagrama-de-casos-de-uso.png").relative_to(RAIZ))

        md_para_pdf([(ler("atividade-04/01-diagramas-de-sequencia.md"), False)],
                    "Diagramas de Sequência", SAIDA / "05-diagramas-de-sequencia.pdf",
                    DOCS / "atividade-04", browser, tmp,
                    css_extra="h3 { page-break-before: always; } img { max-height: 235mm; object-fit: contain; }")


if __name__ == "__main__":
    main()
