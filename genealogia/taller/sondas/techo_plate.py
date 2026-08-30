"""El ordinal de portadilla: se barre con los tres textos reales, porque el
umbral depende del par de letras concreto y «PRIMERA» cede antes que «TERCERA»."""
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
TEXTOS = ["Primera Parte", "Segunda Parte", "Tercera Parte"]
VAL = [0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14]

pags, clave = [], []
for v in VAL:
    for txt in TEXTOS:
        pags.append(f'<div class="pg" style="font-family:{HEAD};font-size:7.2pt;font-weight:600;'
                    f'text-transform:uppercase;letter-spacing:{v}em;word-spacing:{-v}em">{txt}</div>')
        clave.append((v, txt))
html = ('<!doctype html><meta charset="utf-8"><style>' + fuentes +
        '@page{size:200mm 24mm;margin:5mm}body{margin:0}.pg{page-break-after:always;white-space:nowrap}'
        '</style><body>' + "".join(pags))
with sync_playwright() as p:
    b = p.chromium.launch(**({'executable_path': CHROME} if CHROME else {}))
    pg = b.new_page(); pg.set_content(html, wait_until='load')
    pg.pdf(path='techo3.pdf', width='200mm', height='24mm',
           margin={'top':'5mm','bottom':'5mm','left':'5mm','right':'5mm'}); b.close()
pdf = pdfium.PdfDocument('techo3.pdf')
res = {}
for i, (v, txt) in enumerate(clave):
    got = " ".join(pdf[i].get_textpage().get_text_bounded().split())
    res.setdefault(v, []).append((txt, got == txt.upper()))
for v in VAL:
    est = res[v]
    print(f"  {v:<6}{'TODOS LIMPIOS' if all(o for _, o in est) else 'rompe: ' + ', '.join(t for t, o in est if not o)}")
