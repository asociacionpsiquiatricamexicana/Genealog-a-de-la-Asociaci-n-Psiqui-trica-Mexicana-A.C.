"""Bateria reparada: comprobaciones sobre el PDF construido.

Las sondas de la primera pasada fallaron por el instrumento, no por el libro:
las tipografias se leen del propio archivo, los tipos «invisibles» los compone
libro.py y no el modulo de estilo, y el Contenido no lleva puntos conductores
como caracteres —son un borde de CSS—, de modo que no se puede analizar por
texto. Aqui el Contenido se comprueba contra el mapa de bloques del propio
armado, que es donde estuvo el fallo real de una tanda anterior.
"""
import json, re, collections
import pypdfium2 as pdfium

BIN, PDF = "assets/08fffc00-d395-438c-88b0-a0545e4c4793.bin", "pdfs/APM60_Genealogia__final.pdf"
d = json.load(open(BIN, encoding="utf-8"))
B, TOC = d["blocks"], d.get("toc", [])
PAGS = json.load(open("pdfs/pages_debug.json", encoding="utf-8"))
pdf = pdfium.PdfDocument(PDF)
N = len(pdf)
avisos = []


def aviso(c, m):
    avisos.append((c, m)); print(f"  [!] {c}: {m}")


def texto(b):
    return "".join((" " if p.get("br") else (p.get("x") or "")) for p in (b.get("parts") or [])) \
        or (b.get("title") or "") + " " + (b.get("sub") or "")


def norm(s):
    return re.sub(r"[^a-záéíóúüñ0-9 ]", " ", s.lower())


print(f"PDF {N} paginas | {len(B)} bloques | {len(TOC)} entradas de Contenido\n")

# --- A. tipografias realmente incrustadas ------------------------------------
print("A. tipografias incrustadas")
crudo = open(PDF, "rb").read()
fuentes = sorted(set(re.findall(rb"/BaseFont\s*/([A-Za-z0-9+#\-,]+)", crudo)))
emb = set(re.findall(rb"/FontFile2?\d?", crudo))
for f in fuentes:
    nom = f.decode("latin-1")
    # Gentium Book Plus la incrusta la propia edicion para el griego
    # politonico del Prefacio (fuentes_griego.py): no es sustitucion del
    # navegador y no debe rotularse como ajena.
    ok = re.search(r"Lora|Cormorant|Gentium", nom)
    print(f"   {nom:<44}{'' if ok else '   <-- ajena a la edicion'}")
    if not ok:
        aviso("tipografia", f"aparece «{nom}», que no es de la edicion (sustitucion del navegador)")
print(f"   descriptores de fuente incrustada: {len(emb)}")

# --- B. paginas sin texto -----------------------------------------------------
print("\nB. paginas sin texto")
vac = [i + 1 for i in range(N) if pdf[i].get_textpage().count_chars() < 12]
print(f"   {len(vac)}: {vac}  (se esperan solo las de descanso o a sangre sin texto)")

# --- C. cobertura de tipos de bloque -----------------------------------------
print("\nC. tipos de bloque frente a los dos compositores")
js = open("bookstyle_extraido.js", encoding="utf-8").read()
py = open("libro.py", encoding="utf-8").read()
tipos = collections.Counter(b.get("t") for b in B)
huerfanos = [t for t in tipos if f"'{t}'" not in js and f'"{t}"' not in js
             and f"'{t}'" not in py and f'"{t}"' not in py]
for t in huerfanos:
    aviso("bloque sin compositor", f"«{t}» ({tipos[t]} veces) no lo nombra ni el modulo de estilo ni libro.py")
print(f"   {len(tipos)} tipos, {sum(tipos.values())} bloques, {len(huerfanos)} sin compositor")

# --- D. el Contenido apunta a donde dice -------------------------------------
print("\nD. anclaje del Contenido")
malas = 0
for t in TOC:
    i, lab = t.get("i"), t.get("label", "")
    if i is None or not (0 <= i < len(B)):
        aviso("Contenido", f"«{lab[:44]}» apunta al bloque {i}, fuera de rango"); malas += 1; continue
    zona = norm(" ".join(texto(B[j]) for j in range(i, min(i + 6, len(B)))))
    clave = [w for w in norm(lab).split() if len(w) > 3][:3]
    if clave and not any(w in zona for w in clave):
        aviso("Contenido", f"«{lab[:44]}» apunta al bloque {i}, cuyo texto no lo contiene: «{zona[:56]}…»")
        malas += 1
print(f"   entradas que no cuadran con su bloque: {malas} de {len(TOC)}")

# --- E. marcadores ------------------------------------------------------------
print("\nE. marcadores")
marcas, fuera = 0, 0
for m in pdf.get_toc():
    marcas += 1
    try:
        dest = m.get_dest()
        pi = dest.get_index() if dest else None
    except Exception:
        pi = None
    if pi is None or not (0 <= pi < N):
        fuera += 1
        aviso("marcador", f"«{m.get_title()[:40]}» sin destino valido")
print(f"   {marcas} marcadores | destinos invalidos: {fuera}")

# --- F. bloques compuestos dos veces -----------------------------------------
print("\nF. bloques compuestos en mas de una pagina")
donde = collections.defaultdict(list)
for pi, p in enumerate(PAGS):
    for bi, f, t in p["segs"]:
        donde[bi].append((pi, f, t))
sospechosos = 0
for bi, apar in donde.items():
    if len(apar) < 2:
        continue
    # legitimo: un bloque partido, cuyos tramos no se solapan y se encadenan
    tramos = sorted((f or 0, t) for _, f, t in apar)
    solapan = any(tramos[k][1] is not None and tramos[k + 1][0] < tramos[k][1] for k in range(len(tramos) - 1))
    repetido = len({(f, t) for _, f, t in apar}) < len(apar)
    if solapan or repetido:
        sospechosos += 1
        aviso("duplicado", f"bloque {bi} ({B[bi].get('t')}) en paginas {[p+1 for p,_,_ in apar]} con tramos {tramos}")
print(f"   bloques con tramos solapados o repetidos: {sospechosos}")

print(f"\n=== {len(avisos)} avisos ===")
