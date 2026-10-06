"""Extrai do guia os exemplos "Ruim:" e "Melhor:" (blocos de citação)."""
import re
from pathlib import Path

GUIA = Path(__file__).resolve().parent.parent / "anti-llmismo-ptbr" / "references" / "guia-completo.md"


def extract(path=GUIA):
    """Devolve lista de (tipo, item, texto). tipo é 'ruim' ou 'melhor'."""
    out = []
    kind = None
    item = ""
    buf = []

    def flush():
        if kind and buf:
            out.append((kind, item, "\n".join(buf).strip()))
        buf.clear()

    for line in Path(path).read_text(encoding="utf-8").splitlines():
        h = re.match(r"^###\s+(\d+)\.", line)
        if h:
            flush(); kind = None; item = h.group(1); continue
        if line.startswith("## "):
            flush(); kind = None; item = ""; continue
        s = line.strip()
        if s in ("Ruim:",):
            flush(); kind = "ruim"; continue
        if s in ("Melhor:",) or s.startswith("Quando pode ficar:"):
            flush(); kind = "melhor"; continue
        if line.startswith(">"):
            txt = line[1:].strip()
            if txt:
                buf.append(txt)
            elif buf and kind == "ruim":
                buf.append("")
            continue
        if s == "":
            # bloco de citação separado por linha vazia = outro exemplo
            if buf:
                flush()
            continue
        # qualquer outra linha encerra o grupo
        flush(); kind = None
    flush()
    return out
