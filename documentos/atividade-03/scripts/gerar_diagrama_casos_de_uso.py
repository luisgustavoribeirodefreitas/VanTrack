"""Gera o diagrama de casos de uso do VanTrack em SVG (diagrama-casos-de-uso.svg).

Uso:  python gerar_diagrama_casos_de_uso.py
O PNG é exportado a partir do SVG (ver ferramentas/gerar_artefatos.py).
"""
from pathlib import Path

W, H = 2100, 1660
RX, RY = 178, 48
COL = {"A": 560, "B": 1000, "C": 1440}
BOX = (330, 80, 1700, 1300)  # x1, y1, x2, y2

AZUL, AMARELO = "#EEF3FA", "#FFF6E5"

# id: (coluna, y, título, inclusão/extensão?)
UCS = {
    "S01": ("A", 170, "Vincular Usuário à Empresa", False),
    "C01": ("A", 350, "Manter Aluno (CRUD)", False),
    "S02": ("A", 530, "Acompanhar Van em Tempo Real", False),
    "S03": ("A", 710, "Confirmar Presença", False),
    "S04": ("A", 890, "Cancelar Utilização do Transporte", False),
    "S08": ("A", 1070, "Trocar Mensagens pelo Chat", False),
    "X01": ("B", 260, "Registrar Autorização do|Responsável Legal", True),
    "I02": ("B", 440, "Notificar Responsável sobre|Embarque/Desembarque", True),
    "X02": ("B", 620, "Recalcular Rota", True),
    "S10": ("B", 800, "Notificar Proximidade da Van", False),
    "I03": ("B", 980, "Notificar Responsáveis|sobre Atraso", True),
    "I01": ("B", 1160, "Notificar Motorista sobre|Cancelamento", True),
    "ADM01": ("C", 170, "Vincular Motorista à Van", False),
    "S05": ("C", 350, "Registrar Embarque", False),
    "S06": ("C", 530, "Registrar Desembarque", False),
    "S07": ("C", 710, "Emitir Aviso de Atraso", False),
    "S09": ("C", 890, "Gerar Rota Otimizada", False),
    "S11": ("C", 1070, "Detectar Atraso Automaticamente", False),
}

ACTORS = {
    "Resp": (175, 330, ["Responsável"], False),
    "Aluno": (175, 840, ["Aluno"], False),
    "Emp": (1900, 150, ["Empresa de", "Transporte"], False),
    "Mot": (1900, 520, ["Motorista"], False),
    "Tempo": (1900, 960, ["Tempo", "(agendador)"], False),
    "Geo": (780, 1420, ["Serviço de", "Geolocalização"], True),
    "Push": (1205, 1420, ["Serviço de", "Notificação"], True),
}

out = []


def uc_xy(uc):
    c, y, *_ = UCS[uc]
    return COL[c], y


def left(uc):
    x, y = uc_xy(uc)
    return x - RX, y


def right(uc):
    x, y = uc_xy(uc)
    return x + RX, y


def line(points, dashed=False, arrow=False, width=1.6):
    d = " ".join(f"{x:.0f},{y:.0f}" for x, y in points)
    extra = ' stroke-dasharray="9 6"' if dashed else ""
    extra += ' marker-end="url(#seta)"' if arrow else ""
    out.append(f'<polyline points="{d}" fill="none" stroke="#3A3A3A" stroke-width="{width}"{extra}/>')


def text(x, y, s, size=19, weight="normal", style="normal", anchor="middle"):
    out.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" font-weight="{weight}" '
               f'font-style="{style}" text-anchor="{anchor}">{s}</text>')


def label(x, y, s):
    """Rótulo com fundo branco para não ser cortado pelas linhas."""
    w = 8.6 * len(s) + 10
    out.append(f'<rect x="{x - w / 2:.0f}" y="{y - 15:.0f}" width="{w:.0f}" height="21" fill="#FAFBFD"/>')
    text(x, y, s, size=16, style="italic")


def ellipse_point(uc, towards):
    """Ponto na borda da elipse na direção de outro ponto."""
    import math
    cx, cy = uc_xy(uc)
    dx, dy = towards[0] - cx, towards[1] - cy
    t = 1 / math.sqrt((dx / RX) ** 2 + (dy / RY) ** 2)
    return cx + dx * t, cy + dy * t


def dep(src, dst, kind, pos=0.5):
    """Seta tracejada de src para dst (include: base→incluído; extend: extensor→base)."""
    a = ellipse_point(src, uc_xy(dst))
    b = ellipse_point(dst, uc_xy(src))
    line([a, b], dashed=True, arrow=True)
    mx, my = a[0] + (b[0] - a[0]) * pos, a[1] + (b[1] - a[1]) * pos
    label(mx, my, f"«{kind}»")


# ---------------- moldura
out.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="white"/>')
x1, y1, x2, y2 = BOX
out.append(f'<rect x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" rx="8" fill="#FAFBFD" stroke="#333" stroke-width="2"/>')
text((x1 + x2) / 2, y1 + 34, "VanTrack", size=28, weight="bold")

# legenda
out.append(f'<ellipse cx="380" cy="40" rx="26" ry="12" fill="{AZUL}" stroke="#2E4A7A" stroke-width="1.5"/>')
text(418, 46, "caso de uso acionado por ator", size=18, anchor="start")
out.append(f'<ellipse cx="720" cy="40" rx="26" ry="12" fill="{AMARELO}" stroke="#2E4A7A" stroke-width="1.5"/>')
text(758, 46, "caso de uso de inclusão/extensão", size=18, anchor="start")
text(1080, 46, "«sistema externo»: ator secundário (outro sistema)", size=18, anchor="start")

# ---------------- comunicação (atores principais)
for uc in ["S01", "C01", "S02", "S03", "S04", "S08"]:
    line([(ACTORS["Resp"][0] + 30, ACTORS["Resp"][1] + 40), left(uc)])
    line([(ACTORS["Aluno"][0] + 30, ACTORS["Aluno"][1] + 40), left(uc)])
line([(ACTORS["Emp"][0] - 30, ACTORS["Emp"][1] + 40), right("ADM01")])
for uc in ["S05", "S06", "S07", "S09"]:
    line([(ACTORS["Mot"][0] - 30, ACTORS["Mot"][1] + 40), right(uc)])
for uc in ["S09", "S11"]:
    line([(ACTORS["Tempo"][0] - 30, ACTORS["Tempo"][1] + 40), right(uc)])
# Motorista ↔ chat (UC-S08): roteado pelo corredor inferior
mx = ACTORS["Mot"][0] - 30
line([(mx, ACTORS["Mot"][1] + 40), (1665, 610), (1665, 1255), (560, 1255), (560, 1070 + RY)])

# ---------------- atores secundários externos (barramentos nos corredores)
gx = ACTORS["Geo"][0]
line([(gx, ACTORS["Geo"][1] - 10), (gx, 530)])          # corredor A|B
line([(gx, 530), right("S02")])
line([(gx, 620), left("X02")])
line([(gx, 800), left("S10")])
line([(gx, 1340), (1240, 1340), (1240, 890)])           # corredor B|C
line([(1240, 890), left("S09")])
line([(1240, 1070), left("S11")])
px = ACTORS["Push"][0]
line([(px, ACTORS["Push"][1] - 10), (px, 440)])
for uc in ["I02", "S10", "I03", "I01"]:
    line([(px, uc_xy(uc)[1]), right(uc)])

# ---------------- elipses
for uc, (c, y, title, special) in UCS.items():
    x = COL[c]
    fill = AMARELO if special else AZUL
    out.append(f'<ellipse cx="{x}" cy="{y}" rx="{RX}" ry="{RY}" fill="{fill}" stroke="#2E4A7A" stroke-width="2"/>')
    lines = title.split("|")
    top = y - 10 * len(lines) - 4
    text(x, top + 8, f"UC-{uc}", size=19, weight="bold")
    for i, t in enumerate(lines):
        text(x, top + 32 + 22 * i, t, size=18)

# ---------------- include / extend
dep("S04", "I01", "include", pos=0.3)
dep("S05", "I02", "include")
dep("S06", "I02", "include")
dep("S07", "I03", "include")
dep("S11", "I03", "include")
dep("X01", "C01", "extend")
dep("X02", "S04", "extend", pos=0.72)

# ---------------- atores
for key, (x, y, names, external) in ACTORS.items():
    out.append(f'<g stroke="#222" stroke-width="3" fill="none">'
               f'<circle cx="{x}" cy="{y - 18}" r="18" fill="white"/>'
               f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + 50}"/>'
               f'<line x1="{x - 28}" y1="{y + 18}" x2="{x + 28}" y2="{y + 18}"/>'
               f'<line x1="{x}" y1="{y + 50}" x2="{x - 24}" y2="{y + 88}"/>'
               f'<line x1="{x}" y1="{y + 50}" x2="{x + 24}" y2="{y + 88}"/></g>')
    for i, n in enumerate(names):
        text(x, y + 118 + 24 * i, n, size=21, weight="bold")
    if external:
        text(x, y + 118 + 24 * len(names), "«sistema externo»", size=16, style="italic")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'font-family="Segoe UI, DejaVu Sans, Arial, sans-serif">'
       '<defs><marker id="seta" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" '
       'orient="auto-start-reverse"><path d="M1,1 L11,6 L1,11" fill="none" stroke="#3A3A3A" stroke-width="1.8"/></marker></defs>'
       + "".join(out) + "</svg>")

destino = Path(__file__).resolve().parent.parent / "diagrama-casos-de-uso.svg"
destino.write_text(svg, encoding="utf-8")
print(destino)
