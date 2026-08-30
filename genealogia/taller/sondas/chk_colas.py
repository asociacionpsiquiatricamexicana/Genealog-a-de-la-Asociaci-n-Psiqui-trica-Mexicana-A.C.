"""Comprueba si el desajuste de conteo de palabras hace perder texto en el PDF.

wordCount() cuenta sobre el texto concatenado del bloque; sliceBlock() indexa
palabra por palabra dentro de cada fragmento. Una palabra repartida entre dos
fragmentos (una versalita o una cursiva pegada a su puntuacion) cuenta una vez
en el primero y dos en el segundo. Si el paginador corta justo en ese tope, la
cola del bloque queda fuera de la pagina y no se compone en ninguna otra.
"""
import json, re, unicodedata
import os
import sys
import pypdfium2 as pdfium

BLANDOS = "­​�‍"
d = json.load(open("assets/08fffc00-d395-438c-88b0-a0545e4c4793.bin", encoding="utf-8"))
B = d["blocks"]


def texto(b):
    return "".join((" " if p.get("br") else (p.get("x") or "")) for p in (b.get("parts") or []))


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c) and c not in BLANDOS)
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def n_concatenado(b):
    return len([w for w in texto(b).strip().split() if w])


def n_por_fragmento(b):
    n = 0
    for p in (b.get("parts") or []):
        if p.get("br"):
            continue
        n += len([w for w in re.split(r"(\s+)", p.get("x") or "")
                  if w and not re.fullmatch(r"\s+", w)])
    return n


pdf = pdfium.PdfDocument(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir,
                   "APM60_Genealogia__corregido.pdf"))
todo = norm(" ".join(pdf[i].get_textpage().get_text_bounded() for i in range(len(pdf))))

malos = [i for i, b in enumerate(B)
         if b.get("parts") and n_concatenado(b) != n_por_fragmento(b)]
print(f"bloques con conteo discrepante: {len(malos)} de {len(B)}")

perdidos = []
for i in malos:
    cola = " ".join(texto(B[i]).split()[-7:])
    cola = re.sub(r"\d+$", "", cola)  # la llamada de nota va volada, fuera del bloque
    if norm(cola) and norm(cola) not in todo:
        perdidos.append((i, cola))
print(f"bloques cuya cola NO aparece en el PDF: {len(perdidos)}")
for i, c in perdidos:
    print(f"   bloque {i} ({B[i]['t']}): {c!r}")
