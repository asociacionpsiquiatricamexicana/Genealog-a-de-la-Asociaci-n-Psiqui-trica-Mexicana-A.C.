# -*- coding: utf-8 -*-
"""Compone el volumen desde el JSON del libro (contenido + secciones + anclas),
no desde la paginación en pantalla del flipbook.

El JSON trae `anchors`: para cada folio real del volumen impreso, en qué bloque
empieza. Esa es la paginación del libro, no la de la pantalla. Se construye una
página por cada tramo entre anclas, se mide en el navegador, y donde el tramo no
cabe en la caja se parte por frontera de bloque: esas particiones son justamente
los folios que las anclas no traen (el JSON no registra un ancla cuando el corte
cae dentro de un bloque). Nada se rellena para cuadrar un total: lo que salga,
sale medido.
"""
import os

TRIM_W, TRIM_H = 439.37, 651.97          # 15,5 × 23 cm, del propio módulo de estilo
M_TOP, M_SIDE, M_BOT = 56.7, 62.4, 82.2  # ídem
BOX_W = TRIM_W - 2 * M_SIDE              # 314,57 pt ≈ los 314,0 pt de la norma
BOX_H = TRIM_H - M_TOP - M_BOT
PX = 96.0 / 72.0                         # 1 pt en px CSS, para que page.pdf case

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(HERE, 'assets', '08fffc00-d395-438c-88b0-a0545e4c4793.bin')


def roman(n):
    vals = [(1000,'m'),(900,'cm'),(500,'d'),(400,'cd'),(100,'c'),(90,'xc'),
            (50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]
    out = []
    for v, s in vals:
        while n >= v:
            out.append(s); n -= v
    return ''.join(out)


def unroman(s):
    vals = {'i':1,'v':5,'x':10,'l':50,'c':100,'d':500,'m':1000}
    n = prev = 0
    for ch in reversed(s.lower()):
        v = vals[ch]
        n = n - v if v < prev else n + v
        prev = v
    return n


def plan_from_anchors(book):
    """Tramos [start, end) de bloques por página, con el folio que las anclas dan."""
    blocks = book['blocks']
    n = len(blocks)
    anchors = sorted(book['anchors'], key=lambda a: a['bi'])

    cut_at = {}
    for a in anchors:
        bi = a['bi']
        # frac dice en qué punto del bloque cae el folio; redondeo a frontera,
        # y la medición de después corrige lo que no quepa.
        cut = bi if a.get('frac', 0) < 0.5 else min(bi + 1, n)
        cut_at.setdefault(cut, a['folio'])

    bleed = {i for i, b in enumerate(blocks) if b.get('t') in ('plate', 'display')}

    pages, start, folio = [], 0, None
    for i in range(n):
        if i in bleed:
            if i > start:
                pages.append({'start': start, 'end': i, 'folio': folio, 'bleed': False})
            pages.append({'start': i, 'end': i + 1, 'folio': None, 'bleed': True})
            start, folio = i + 1, None
            continue
        if i in cut_at and i > 0:
            if i > start:
                pages.append({'start': start, 'end': i, 'folio': folio, 'bleed': False})
            start, folio = i, cut_at[i]
    if start < n:
        pages.append({'start': start, 'end': n, 'folio': folio, 'bleed': False})
    return [p for p in pages if p['end'] > p['start']]


def assign_missing_folios(pages):
    """Las páginas nacidas de una partición por desborde no traen folio. Se les
    da el folio que falta en la secuencia, si el hueco existe; si no, quedan sin
    numerar (que es lo que son: páginas a sangre o de cortesía)."""
    # recoge los folios conocidos en orden
    for idx, p in enumerate(pages):
        if p.get('bleed') or p.get('folio'):
            continue
        # busca el folio anterior y el siguiente conocidos
        prev_f = next_f = None
        for q in reversed(pages[:idx]):
            if q.get('folio'):
                prev_f = q['folio']; break
        for q in pages[idx+1:]:
            if q.get('folio'):
                next_f = q['folio']; break
        if not prev_f or not next_f:
            continue
        pr, nx = prev_f.isdigit(), next_f.isdigit()
        if pr != nx:
            continue
        pv = int(prev_f) if pr else unroman(prev_f)
        nv = int(next_f) if nx else unroman(next_f)
        if nv - pv >= 2:                       # hay hueco: este folio existe
            val = pv + 1
            p['folio'] = str(val) if pr else roman(val)
    return pages
