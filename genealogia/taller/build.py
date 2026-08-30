# -*- coding: utf-8 -*-
"""Extrae de la fuente de verdad el texto que cada bloque debe llevar y lo deja
en exp.pkl, para que cmp.py lo coteje palabra por palabra contra el texto real
del PDF.

Solo necesita el .bin: la extraccion del PDF es asunto de cmp.py, que carga
mypages.json por su cuenta. Este archivo lo cargaba tambien —535 KB parseados
para nada, resto de haber copiado el encabezado de cmp.py— y eso ademas lo
ataba a que extraer_texto_pdf.py se hubiera ejecutado antes.
"""
import json, re, pickle

from componer import BOOK

libro = json.load(open(BOOK, encoding='utf-8'))
blocks = libro['blocks']; TOC = libro['toc']

def blocktext(b):
    if b.get('parts') is not None:
        return ''.join((' ' if p.get('br') else (p.get('x') or '')) for p in b['parts'])
    if b.get('lines'):
        return ' '.join(' '.join(p.get('x') or '' for p in l) for l in b['lines'])
    if b.get('rows'):
        return ' '.join(''.join((' ' if p.get('br') else (p.get('x') or '')) for p in r.get('parts',[])) for r in b['rows'])
    if b.get('title'):
        return b['title'] + (' ' + b['sub'] if b.get('sub') else '')
    return ''

INVIS = {'anchor','cardEnd','pb','rule','orn'}
exp = []   # list of (blockindex, text)
for i,b in enumerate(blocks):
    t = b.get('t')
    if t in INVIS: continue
    if t == 'autotoc':
        for r in TOC:
            exp.append((i, r['label']))
        continue
    s = ''
    if t == 'field':
        s = (b.get('label') or '') + ' ' + blocktext(b)
    elif t == 'fnote':
        lab = b.get('label') or ''
        if lab and not re.search('Nota', lab): lab = lab + ' ·'
        s = lab + ' ' + blocktext(b)
    elif t == 'cardStart':
        s = re.sub(r'\.$','', b.get('label') or 'Ficha de catalogación')
    else:
        s = blocktext(b)
    if s.strip():
        exp.append((i, s))

pickle.dump(exp, open('exp.pkl','wb'))
print('bloques con texto:', len(exp))
print('chars exp:', sum(len(s) for _,s in exp))
