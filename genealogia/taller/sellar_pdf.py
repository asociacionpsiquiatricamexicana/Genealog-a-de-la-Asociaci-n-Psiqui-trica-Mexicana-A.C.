# -*- coding: utf-8 -*-
"""Metadatos e índice de marcadores sobre el PDF compuesto."""
import json, os
import pikepdf
from pikepdf import Dictionary, Name, String, Array

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'pdfs', 'libro.pdf')
DST = os.path.join(HERE, 'pdfs', 'APM60_Genealogia__final.pdf')

idx = json.load(open(os.path.join(HERE, 'indice_final.json'), encoding='utf-8'))
marks, pages = idx['marks'], idx['pages']

TITLE = 'Genealogía de la Asociación Psiquiátrica Mexicana, A.C.'
SUBTITLE = 'Gran Proyecto Historiográfico'
AUTHOR = ('José Carlos Medina Rodríguez, compilador; '
          'David Eduardo Saucedo Martínez, editor')

pdf = pikepdf.open(SRC, allow_overwriting_input=True)

# El mapa pagina->folio y el PDF han de venir de la misma pasada. Si no, las
# etiquetas y los marcadores se sellan sobre una paginacion que ya cambio.
if len(pages) != len(pdf.pages):
    raise SystemExit(f'El indice tiene {len(pages)} paginas y el PDF {len(pdf.pages)}: '
                     'vuelve a componer antes de sellar.')

with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
    meta['dc:title'] = TITLE
    meta['dc:creator'] = [AUTHOR]
    meta['dc:publisher'] = ['Asociación Psiquiátrica Mexicana, A.C.']
    meta['dc:language'] = ['es-MX']
    meta['dc:description'] = (
        SUBTITLE + '. Obra conmemorativa del sexagésimo aniversario de la '
        'fundación de la Asociación Psiquiátrica Mexicana, A.C., 1966-2026. '
        'Primera edición digital, Ciudad de México, 2026.')
    meta['dc:rights'] = ['CC BY-NC-ND 4.0']
    meta['dc:identifier'] = 'DOI 10.5281/zenodo.22035217'
    meta['pdf:Keywords'] = ('Asociación Psiquiátrica Mexicana; psiquiatría; México; '
                            'historia; historia oral; prosopografía; salud mental')

pdf.docinfo['/Title'] = String(TITLE)
pdf.docinfo['/Author'] = String(AUTHOR)
pdf.docinfo['/Subject'] = String(SUBTITLE + ' · Sexagésimo aniversario, 1966-2026')
pdf.docinfo['/Keywords'] = String('Asociación Psiquiátrica Mexicana, A.C.; psiquiatría; '
                                  'México; historia; historia oral; prosopografía')

# el visor debe abrir mostrando el índice de marcadores y una página completa
pdf.Root[Name.PageMode] = Name.UseOutlines
pdf.Root[Name.PageLayout] = Name.SinglePage
pdf.Root[Name.Lang] = String('es-MX')

# Etiquetas de pagina: una sola serie continua, sin reinicios. Antes cada
# tramo de laminas abria su propio tramo con St=1 y prefijo «s/n », de modo que
# siete paginas distintas se rotulaban «s/n 1» en el visor. Las laminas
# consumen numero aunque no lo impriman: se les da el que les toca.
from componer import unroman as _unroman


def _serie(f):
    if not f:
        return None
    return 'D' if f.isdigit() else 'r'


def _valor(f):
    return int(f) if f.isdigit() else _unroman(f)


nums = Array()
i = 0
while i < len(pages):
    f = pages[i].get('folio')
    s = _serie(f)
    if s is None:
        # paginas fuera de toda serie (forros): se rotulan aparte
        j = i
        while j < len(pages) and _serie(pages[j].get('folio')) is None:
            j += 1
        nums.append(i)
        nums.append(Dictionary(P=String('forro')))
        i = j
        continue
    # tramo contiguo de la misma serie con numeracion consecutiva
    inicio = _valor(f)
    j, esperado = i + 1, inicio + 1
    while (j < len(pages) and _serie(pages[j].get('folio')) == s
           and _valor(pages[j]['folio']) == esperado):
        j += 1
        esperado += 1
    nums.append(i)
    nums.append(Dictionary(S=Name.D if s == 'D' else Name.r, St=inicio))
    i = j
pdf.Root[Name.PageLabels] = Dictionary(Nums=nums)

# marcadores
with pdf.open_outline() as outline:
    outline.root.clear()
    stack = []
    for m in marks:
        pagina = m['page']
        # las cubiertas no nacen de bloques: primera y ultima pagina reales
        if m['label'] == 'Portada':
            pagina = 0
        elif m['label'] == 'Contracubierta':
            pagina = len(pdf.pages) - 1
        if pagina is None:
            continue
        item = pikepdf.OutlineItem(m['label'], pagina)
        lvl = m['lvl']
        if lvl == 0 or not stack:
            outline.root.append(item)
            stack = [item]
        else:
            parent = stack[0]
            parent.children.append(item)
            stack = stack[:1] + [item]

pdf.save(DST, linearize=True)
pdf.close()

chk = pikepdf.open(DST)
print('páginas:', len(chk.pages))
print('título:', chk.docinfo.get('/Title'))
with chk.open_outline() as o:
    print('marcadores raíz:', len(o.root),
          '| hijos:', sum(len(x.children) for x in o.root))
print('bytes:', os.path.getsize(DST))
