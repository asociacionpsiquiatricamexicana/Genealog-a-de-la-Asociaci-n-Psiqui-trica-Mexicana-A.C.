"""Sigue cada entrada del Contenido hasta la pagina cuyo folio anuncia.

El folio se toma de las etiquetas de pagina del propio PDF —las que fija el
sellado y las que usa el visor—, no de leer el numero impreso, que puede caer
en cualquier sitio del flujo de texto extraido.
"""
import re
import os
import sys
import pikepdf
import pypdfium2 as pdfium

RUTA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir,
                   "APM60_Genealogia__corregido.pdf")
px = pikepdf.open(RUTA)
pdf = pdfium.PdfDocument(RUTA)
N = len(pdf)
pag = [pdf[i].get_textpage().get_text_bounded() for i in range(N)]

# etiquetas de pagina -> folio de cada indice
ROM = [(1000,'m'),(900,'cm'),(500,'d'),(400,'cd'),(100,'c'),(90,'xc'),
       (50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]
def romano(n):
    s = ''
    for v, r in ROM:
        while n >= v: s += r; n -= v
    return s

if "/PageLabels" not in px.Root:
    raise SystemExit(f"{RUTA} no lleva etiquetas de pagina: esta sonda necesita el PDF "
                     "ya sellado (sellar_pdf.py), no el recien compuesto.")
labels = px.Root.PageLabels.Nums
reglas = [(int(labels[i]), labels[i + 1]) for i in range(0, len(labels), 2)]
folio_de = {}
for k, (ini, d) in enumerate(reglas):
    fin = reglas[k + 1][0] if k + 1 < len(reglas) else N
    estilo = str(d.get("/S", ""))
    st = int(d.get("/St", 1))
    pref = str(d.get("/P", "")) if "/P" in d else ""
    for j in range(ini, fin):
        n = st + (j - ini)
        folio_de[j] = pref + (romano(n) if estilo == "/r" else str(n) if estilo == "/D" else "")
pagina_de = {}
for i, f in folio_de.items():
    if f: pagina_de.setdefault(f, i)
print(f"etiquetas de pagina: {len(reglas)} reglas, {len(pagina_de)} folios distintos")

filas = []
for i in range(20):
    for l in pag[i].split("\n"):
        m = re.match(r"\s*(.+?)\s+(\d{1,3}|[ivxl]{1,6})\s*$", l.strip())
        if m and len(m.group(1)) > 5 and m.group(1)[0].isupper() and "," not in m.group(1)[-14:]:
            filas.append((m.group(1).strip(), m.group(2)))
print(f"{len(filas)} filas de Contenido leidas\n")

bien = mal = sin = 0
for etq, fol in filas:
    p = pagina_de.get(fol)
    if p is None:
        sin += 1; print(f"  ??   «{etq[:50]}» -> folio {fol}: no hay pagina con ese folio"); continue
    clave = [w for w in re.sub(r"[^\wáéíóúñÁÉÍÓÚÑ ]", " ", etq).split() if len(w) > 3][:3]
    zona = " ".join(pag[max(0, p - 1):p + 2]).lower()
    if all(w.lower() in zona for w in clave):
        bien += 1
    else:
        mal += 1
        print(f"  MAL  «{etq[:50]}» -> folio {fol} (pagina {p+1} del PDF): no aparece ahi")
print(f"\n  cuadran {bien} · no cuadran {mal} · sin folio {sin}")
