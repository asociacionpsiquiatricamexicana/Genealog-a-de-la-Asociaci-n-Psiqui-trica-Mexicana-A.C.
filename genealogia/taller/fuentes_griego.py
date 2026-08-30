"""Incorpora a la edicion una tipografia griega compatible.

Ni Lora ni Cormorant Garamond traen griego politonico, de modo que las voces
«ἱστορία» e «ἵστωρ» del Prefacio caian en la serif por omision del navegador.
Se elige Gentium Book Plus: cubre los nueve signos que el libro necesita
—comprobado glifo a glifo—, es de construccion humanista, como Lora, y no de
contraste alto como un Didot ni de trazo claro como un Garamond antiguo. Su
altura de x queda a un nueve por ciento de la de Lora, diferencia que aqui se
anula con size-adjust, de modo que el griego case exactamente con el cuerpo.

No se regenera fuentes.css entero a proposito: volver a pedir Lora y Cormorant
podria traer versiones con otras metricas y repaginar el libro sin necesidad.
Solo se anaden las caras nuevas.
"""
import base64, glob, os, re
from fontTools.ttLib import TTFont

MARCA = "/* --- griego politonico: Gentium Book Plus --- */"
CSS = "fuentes/fuentes.css"
css = open(CSS, encoding="utf-8").read()
if MARCA in css:
    raise SystemExit("las caras griegas ya estan en fuentes.css")

# altura de x de la Lora del libro, para igualar
blk = next(b for b in re.findall(r"@font-face\s*\{.*?\}", css, re.S)
           if "'Lora'" in b and "font-style: normal" in b and "font-weight: 400" in b)
open("/tmp/lora.woff2", "wb").write(
    base64.b64decode(re.search(r"base64,([A-Za-z0-9+/=]+)\)", blk).group(1)))
t = TTFont("/tmp/lora.woff2")
x_lora = t["OS/2"].sxHeight / t["head"].unitsPerEm

caras = []
for f in sorted(glob.glob("griego/Gentium_Book_Plus-*.woff2")):
    nom = os.path.basename(f)[:-6]
    _, _, est, peso = nom.rsplit("-", 3)
    g = TTFont(f)
    x_g = g["OS/2"].sxHeight / g["head"].unitsPerEm
    ajuste = x_lora / x_g * 100
    b64 = base64.b64encode(open(f, "rb").read()).decode()
    caras.append(
        "@font-face {\n"
        "  font-family: 'Gentium Griego';\n"
        f"  font-style: {est};\n"
        f"  font-weight: {peso};\n"
        "  font-display: swap;\n"
        f"  size-adjust: {ajuste:.1f}%;\n"
        f"  src: url(data:font/woff2;base64,{b64}) format('woff2');\n"
        "}")
    print(f"  {nom}: altura de x {x_g:.3f} em -> size-adjust {ajuste:.1f} %")

open(CSS, "a", encoding="utf-8").write("\n" + MARCA + "\n" + "\n".join(caras) + "\n")
print(f"anadidas {len(caras)} caras · fuentes.css {os.path.getsize(CSS)/1024:.0f} KB")
