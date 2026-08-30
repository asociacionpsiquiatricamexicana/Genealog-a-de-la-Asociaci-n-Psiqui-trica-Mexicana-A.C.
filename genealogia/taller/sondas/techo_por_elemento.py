"""Halla, para cada rotulo de seguimiento ancho, el maximo que no rompe la copia.

Se compone cada uno con su tipografia, su cuerpo y su texto reales, uno por
pagina para que la extraccion no pueda desalinearse, y se extrae con el mismo
lector que usan los visores.
"""
import os
from playwright.sync_api import sync_playwright
import pypdfium2 as pdfium

HERE = os.path.dirname(os.path.abspath(__file__))
TALLER = os.path.dirname(HERE)          # las sondas viven un piso mas abajo
def _chromium():
    """El navegador que compone las paginas.

    Se toma de la variable CHROME si esta definida; si no, del directorio de
    navegadores de Playwright, y en ultimo termino se deja que Playwright
    resuelva el suyo. Antes iba una ruta fija, valida solo en la maquina donde
    se compuso el libro.
    """
    import glob
    ruta = os.environ.get('CHROME')
    if ruta and os.path.exists(ruta):
        return ruta
    base = os.environ.get('PLAYWRIGHT_BROWSERS_PATH', '')
    for patron in (os.path.join(base, 'chromium*', 'chrome-linux', 'chrome'),
                   os.path.join(base, 'chromium*', 'chrome-*', 'chrome'),
                   os.path.join(base, 'chromium')):
        hallado = sorted(glob.glob(patron))
        if hallado:
            return hallado[-1]
    return None


CHROME = _chromium()
fuentes = open(os.path.join(TALLER, 'fuentes', 'fuentes.css'), encoding='utf-8').read()
HEAD = "'Cormorant Garamond','Gentium Griego',Georgia,serif"

# nombre, cuerpo en puntos, extras de estilo, texto, seguimiento actual
CASOS = [
    ("portadilla de parte", 7.2, "text-transform:uppercase", "Primera Parte", 0.30),
    ("cubierta · aniversario", 7.2, "text-transform:uppercase", "Sexagésimo Aniversario · 1966–2026", 0.28),
    ("cubierta · titulo", 12.5, "font-variant:small-caps", "de la Asociación Psiquiátrica Mexicana, A.C.", 0.11),
    ("cubierta · cargos", 6.4, "text-transform:uppercase", "Historiador Compilador", 0.24),
    ("cubierta · sede", 6.4, "text-transform:uppercase", "Expo Santa Fe, Ciudad de México · 10 a 12 de septiembre de 2026", 0.16),
    ("cubierta · sello", 6.6, "text-transform:uppercase", "Asociación Psiquiátrica Mexicana, A.C.", 0.20),
    ("contracubierta · sello", 6.6, "text-transform:uppercase", "Asociación Psiquiátrica Mexicana, A.C.", 0.14),
    ("contracubierta · pie", 6.4, "text-transform:uppercase", "Ciudad de México, 2026 · Acceso abierto · CC BY-NC-ND 4.0", 0.14),
    ("contracubierta · doi", 6.4, "text-transform:uppercase", "DOI 10.5281/zenodo.22035217", 0.14),
]
VAL = [round(0.10 + 0.01 * i, 2) for i in range(21)]   # de 0,10 a 0,30

pags, clave = [], []
for nom, pt, extra, txt, act in CASOS:
    for v in VAL:
        pags.append(f'<div class="pg" style="font-family:{HEAD};font-size:{pt}pt;font-weight:600;'
                    f'{extra};letter-spacing:{v}em;word-spacing:{-v}em">{txt}</div>')
        clave.append((nom, v, txt, extra, act))
html = ('<!doctype html><meta charset="utf-8"><style>' + fuentes +
        '@page{size:320mm 30mm;margin:6mm}body{margin:0}'
        '.pg{page-break-after:always;white-space:nowrap}</style><body>' + "".join(pags))

with sync_playwright() as p:
    b = p.chromium.launch(**({'executable_path': CHROME} if CHROME else {}))
    pg = b.new_page()
    pg.set_content(html, wait_until='load')
    pg.pdf(path='techo.pdf', width='320mm', height='30mm',
           margin={'top': '6mm', 'bottom': '6mm', 'left': '6mm', 'right': '6mm'})
    b.close()

pdf = pdfium.PdfDocument('techo.pdf')
techo, ultimo = {}, None
for i, (nom, v, txt, extra, act) in enumerate(clave):
    got = " ".join(pdf[i].get_textpage().get_text_bounded().split())
    esp = " ".join((txt.upper() if "uppercase" in extra else txt).split())
    if got.replace(" ", "") == esp.replace(" ", "") and got.count(" ") == esp.count(" "):
        techo[nom] = v
print(f"{'elemento':<26}{'ahora':<9}{'techo limpio':<14}{'cambio'}")
for nom, pt, extra, txt, act in CASOS:
    t = techo.get(nom)
    est = "sin cambio" if t and t >= act else (f"{act} -> {t}" if t else "ninguno limpio")
    print(f"  {nom:<26}{act:<9}{str(t):<14}{est}")
