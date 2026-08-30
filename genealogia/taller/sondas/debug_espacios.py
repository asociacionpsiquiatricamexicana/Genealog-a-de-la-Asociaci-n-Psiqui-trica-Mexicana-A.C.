"""Censo de huecos anomalos entre palabras, medidos sobre el PDF.

Se recorre el flujo de caracteres en orden de lectura. Donde hay un espacio
entre dos glifos de la misma linea de base, el hueco real es la distancia entre
la caja de tinta del glifo anterior y la del siguiente. Cada hueco se compara
con la mediana de su propio renglon: un factor alto es lo que el ojo lee como
espacio doble. Se descartan los saltos de columna (hueco > 3 veces el alto).
"""
import sys, statistics, json, collections
import pypdfium2 as pdfium

ruta   = sys.argv[1] if len(sys.argv) > 1 else "pdfs/libro.pdf"
UMBRAL = float(sys.argv[2]) if len(sys.argv) > 2 else 1.70

pdf = pdfium.PdfDocument(ruta)
hallazgos, por_pag = [], collections.Counter()

for pno in range(len(pdf)):
    tp = pdf[pno].get_textpage()
    n = tp.count_chars()
    ch, tight, base, alto = [], [], [], []
    for i in range(n):
        c = tp.get_text_range(i, 1)
        tl, tb, tr, tt = tp.get_charbox(i, loose=False)
        ll, lb, lr, lt = tp.get_charbox(i, loose=True)
        ch.append(c); tight.append((tl, tr, tr - tl > 0))
        base.append(round(lb, 1)); alto.append(lt - lb)

    # renglones = tramos contiguos con la misma base de caja holgada
    lineas, ini = [], 0
    for i in range(1, n + 1):
        if i == n or (ch[i].strip() and base[i] != base[ini]):
            if i - ini > 1: lineas.append((ini, i))
            ini = i
    for a, b in lineas:
        h = statistics.median([alto[i] for i in range(a, b) if alto[i] > 0] or [1])
        huecos = []
        for i in range(a + 1, b - 1):
            if ch[i] != " " or not tight[i - 1][2] or not tight[i + 1][2]:
                continue
            d = tight[i + 1][0] - tight[i - 1][1]
            if 0 < d <= 3 * h:
                huecos.append((i, d))
        if len(huecos) < 4:
            continue
        med = statistics.median(d for _, d in huecos)
        if med <= 0.05:
            continue
        peor = max(huecos, key=lambda x: x[1])
        if peor[1] / med >= UMBRAL:
            txt = "".join(ch[a:b]).replace("\n", " ").replace("\r", " ")
            k = peor[0] - a
            hallazgos.append({
                "pag": pno + 1, "razon": round(peor[1] / med, 2),
                "hueco_pt": round(peor[1], 2), "mediana_pt": round(med, 2),
                "alto_pt": round(h, 2), "texto": txt[:130],
                "sitio": txt[max(0, k - 26):k + 28],
            })
            por_pag[pno + 1] += 1

hallazgos.sort(key=lambda x: -x["razon"])
print(f"{ruta}: {len(pdf)} pags | {len(hallazgos)} renglones con hueco >= {UMBRAL}x mediana | {len(por_pag)} pags")
for x in hallazgos[:30]:
    print(f"  p{x['pag']:>3} x{x['razon']:<5} {x['hueco_pt']}pt (med {x['mediana_pt']}, alto {x['alto_pt']})  ...{x['sitio']}...")
print("\npeores paginas:", por_pag.most_common(12))
json.dump(hallazgos, open("huecos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
