"""Estado final del PDF publicado, medido sobre el archivo."""
import collections
import os
import sys
import pikepdf, pypdfium2 as pdfium

R = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir,
                   "APM60_Genealogia__corregido.pdf")
px, pdf = pikepdf.open(R), pdfium.PdfDocument(R)
print(f"paginas: {len(pdf)}")

uso = collections.defaultdict(set)
for i, p in enumerate(px.pages):
    for _, f in ((p.get("/Resources", {}) or {}).get("/Font", {}) or {}).items():
        uso[str(f.get("/BaseFont", "?"))].add(i + 1)
print("tipografias:")
for b, ps in sorted(uso.items(), key=lambda x: -len(x[1])):
    print(f"   {b:<40} {len(ps)} pags")

rotas = []
for i in range(len(pdf)):
    for ln in pdf[i].get_textpage().get_text_bounded().split("\n"):
        tk = ln.split()
        if len(tk) >= 4 and sum(1 for x in tk if len(x) == 1) > len(tk) * 0.45:
            rotas.append((i + 1, ln.strip()[:60]))
print(f"renglones que se parten al copiar: {len(rotas)} {rotas}")

pruebas = ["Primera parte", "Segunda parte", "Tercera parte", "Sexagésimo Aniversario",
           "de la Asociación Psiquiátrica", "Historiador Compilador", "Síntesis",
           "Mesas Directivas", "DOI 10.5281/zenodo.22035217", "ἱστορία"]
todo = " ".join(" ".join(pdf[i].get_textpage().get_text_bounded().split()) for i in range(len(pdf)))
print("busqueda dentro del PDF:")
for q in pruebas:
    print(f"   «{q}»: {'la encuentra' if q.lower() in todo.lower() else 'NO LA ENCUENTRA'}")
