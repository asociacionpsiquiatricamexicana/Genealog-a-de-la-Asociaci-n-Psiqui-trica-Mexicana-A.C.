# -*- coding: utf-8 -*-
"""Compone el volumen como libro: flujo natural, caja llena, aperturas mayores
en página propia, páginas a sangre, cornisa, folio, ornamentos y Contenido
derivado de su propia paginación.

La escala tipográfica ya no se ata al mapa de folios del flipbook: se elige la
que llena la caja con la fuente de esta edición. El Contenido se recalcula
sobre la paginación resultante hasta que deja de moverse.
"""
import json, os
from playwright.sync_api import sync_playwright
from componer import (TRIM_W, TRIM_H, M_TOP, M_SIDE, M_BOT, BOX_W, BOX_H, PX,
                      BOOK, roman)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'pdfs')
os.makedirs(OUT, exist_ok=True)
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
TS = 1.0
C_VINO, C_TINTA, C_GRIS = '#7D4343', '#1C1B1A', '#767070'

book = json.load(open(BOOK, encoding='utf-8'))
blocks = book['blocks']
TOC = book['toc']

def normalizar_aparato():
    """Un párrafo embutido en una relación de referencias se componía al cuerpo
    de lectura (10,9 pt) mientras las entradas que lo rodean van al cuerpo de
    consulta (8,6 pt): en la página se leía como un cuerpo extraño y quedaba
    pegado a la entrada siguiente. Se homogeneiza solo cuando el párrafo toca de
    veras una entrada de aparato, no por vivir en una sección que tenga muchas.
    """
    INVIS = {'anchor', 'cardEnd', 'pb', 'rule'}
    APARATO = {'ref', 'note'}

    def vecino(i, paso):
        j = i + paso
        while 0 <= j < len(blocks) and blocks[j].get('t') in INVIS:
            j += paso
        return blocks[j] if 0 <= j < len(blocks) else None

    ajustados = 0
    for i, b in enumerate(blocks):
        if b.get('t') != 'p' or b.get('s'):
            continue
        ant, sig = vecino(i, -1), vecino(i, 1)
        toca = ((ant and ant.get('t') in APARATO and ant.get('h') == b.get('h')) or
                (sig and sig.get('t') in APARATO and sig.get('h') == b.get('h')))
        if not toca:
            continue
        b['s'] = 8.6
        b['ni'] = 1
        ajustados += 1

    # Los titulos mayores traian saltos de linea rigidos heredados de otra
    # medida, que partian el subtitulo en puntos arbitrarios («Glosario, siglas
    # / y definiciones operativas», «Ruta de / recuperacion documental»). Se
    # conserva unicamente el salto que separa el ordinal («Apendice II.») de su
    # subtitulo —estructural y comun a todos— y el resto se deja fluir con
    # reparto equilibrado.
    import re as _re
    titulos = 0
    for b in blocks:
        if b.get('t') != 'major':
            continue
        parts = b.get('parts') or []
        if not any(p.get('br') for p in parts):
            continue
        ordinal = bool(_re.match(r'^(Capítulo|Apéndice)\s', (parts[0].get('x') or '')))
        nuevas, visto = [], False
        for p in parts:
            if p.get('br'):
                if ordinal and not visto:
                    nuevas.append(p); visto = True
                continue          # los demas saltos se retiran
            if nuevas and not nuevas[-1].get('br') and 'x' in nuevas[-1] and 'x' in p:
                nuevas[-1] = {**nuevas[-1], 'x': nuevas[-1]['x'] + ' ' + p['x']}
            else:
                nuevas.append(p)
        if nuevas != parts:
            b['parts'] = nuevas
            titulos += 1
    print(f'titulos: {titulos} con saltos rigidos normalizados')

    # una nota al pie que sigue a otra continua su grupo: no repite el filete
    grupo = 0
    for i, b in enumerate(blocks):
        if b.get('t') != 'fnote':
            continue
        j = i - 1
        while j >= 0 and blocks[j].get('t') in INVIS:
            j -= 1
        if j >= 0 and blocks[j].get('t') == 'fnote':
            b['noRule'] = True
            grupo += 1
    print(f'aparato: {grupo} notas al pie continuan grupo (sin filete propio)')

    aire = 0
    for i, b in enumerate(blocks[:-1]):
        sig = vecino(i, 1)
        if sig is None:
            continue
        if b.get('t') in ('p', 'field', 'auth') and sig.get('t') in APARATO:
            b['mb'] = 7
            aire += 1
    print(f'aparato: {ajustados} párrafos al cuerpo de consulta, {aire} con aire añadido')


BLEED = {'plate', 'display'}
HEADING = {'major', 'sec', 'ficha', 'rot', 'fclose', 'cardStart', 'thead'}
# no se deja un encabezado solo al pie de página
ATTACH_NEXT = {'major', 'sec', 'ficha', 'rot', 'fclose', 'cardStart', 'field', 'thead'}

SHELL = """<!doctype html><meta charset="utf-8"><style>%(fuentes)s
:root{--font-body:'Lora','Gentium Griego',Georgia,serif;--font-heading:'Cormorant Garamond','Gentium Griego',Georgia,serif}
html,body{margin:0;padding:0}
#probe{position:absolute;left:-99999px;top:0;width:%(bw)fpx}
</style><div id="probe"></div><script>%(style)s</script><script>
window.__blocks=%(blocks)s;
window.INVISIBLE=['anchor','cardEnd','pb'];
const S=window.__bookStyle;const probe=document.getElementById('probe');
window.__toc=[];                       // filas del Contenido, inyectadas por pase
window.K=%(px)f; window.TS=%(ts)f;
window.itemsOf=function(segs){
  const out=[];
  for(const [bi,f,t] of segs){
    const b=window.__blocks[bi];
    if(b.t==='autotoc'){ out.push({__toc:true, from:f||0, to:(t===null||t===undefined)?null:t}); continue; }
    if(f===0&&(t===null||t===undefined)){ out.push(b); continue; }
    const sl=S.sliceBlock(b,f,t===null?undefined:t);
    if(f>0){                 // es continuacion: no repite etiqueta ni filete
      delete sl.label;       // «1 ·» de la nota, rotulo del campo
      sl.contFrom=true;      // epigrafes y entradillas sin aire de cabeza
    }
    out.push(sl);
  }
  return out;
};
window.htmlOf=function(segs){
  let h='';
  for(const b of window.itemsOf(segs)){
    if(b.__toc){
      const desde=b.from||0, hasta=(b.to===null||b.to===undefined)?window.__tocRows.length:b.to;
      if(desde===0) h+=window.__tocHead;          // el titulo solo en la primera
      h+=window.__tocRows.slice(desde,hasta).join('');
      continue;
    }
    if(window.INVISIBLE.includes(b.t)) continue;      // no pintan nada
    if(['rule','orn','cardStart'].includes(b.t) || (b.parts&&b.parts.length)){
      let piece=S.blockHtml(b,window.K,window.TS);
      if(b.ragged)            // un renglon corto seguido de una direccion larga
        piece=piece.replace('text-align:justify',   // se estiraba de margen a
          'text-align:left;overflow-wrap:anywhere');// margen: se deja en bandera
      if(b.mb) piece='<div style="margin-bottom:'+(b.mb*window.K)+'px">'+piece+'</div>';
      h+=piece;
    }
  }
  return h;
};
window.measureOf=function(segs){ probe.innerHTML=window.htmlOf(segs); return probe.getBoundingClientRect().height; };
window.measureHtml=function(h){ probe.innerHTML=h; return probe.getBoundingClientRect().height; };
window.wc=function(i){
  const b=window.__blocks[i];
  if(b.t==='autotoc') return window.__tocRows.length;   // se mide en renglones
  return S.wordCount(b);
};
window.plateOf=function(i){ return S.plateHtml(window.__blocks[i],window.K,window.TS); };
window.coverOf=function(){ return S.coverHtml(window.K,window.TS); };
window.backOf=function(){ return S.backCoverHtml(window.K,window.TS); };
window.setToc=function(head,rows){ window.__tocHead=head; window.__tocRows=rows; };
</script>"""


def shell(fuentes, style_js):
    return SHELL % {'fuentes': fuentes, 'style': style_js,
                    'blocks': json.dumps(blocks, ensure_ascii=False),
                    'bw': BOX_W * PX, 'px': PX, 'ts': TS}


def toc_html(folio_of_block, u, f):
    """Devuelve (cabecera, renglones). El Contenido se pagina renglon a renglon:
    como bloque unico se desbordaba de la caja y la caja lo recortaba en
    silencio, de modo que el indice perdia las dieciseis ultimas entradas."""
    rows = []
    for t in TOC:
        # las cubiertas son paginas ciegas: se listan sin folio
        folio = '' if t.get('key') in ('portada', 'contracubierta') \
            else folio_of_block.get(t['i'], '')
        pad = u(10) if t['lvl'] else '0'
        rows.append(
            f'<div style="display:flex;align-items:baseline;gap:{u(4)};'
            f'font-family:var(--font-body);font-size:{f(8.6)};line-height:1.85;'
            f'color:{C_TINTA}"><span style="padding-left:{pad}">{t["label"]}</span>'
            f'<span style="flex:1;border-bottom:1px dotted {C_GRIS};'
            f'transform:translateY(-0.25em);opacity:.55"></span>'
            f'<span style="font-variant-numeric:tabular-nums;color:{C_GRIS}">{folio}</span></div>')
    head = (f'<div style="font-family:var(--font-heading);font-size:{f(19)};'
            f'font-variant:small-caps;letter-spacing:.05em;color:{C_VINO};font-weight:400">'
            f'Contenido</div>'
            f'<div style="width:{u(79)};height:1px;background:{C_VINO};'
            f'margin:{u(7)} 0 {u(13)}"></div>')
    return head, rows


def destino_toc(e):
    """La entrada de una parte apuntaba a su primer capitulo y no a su propia
    portadilla, de modo que el Contenido y los marcadores del PDF mandaban una
    pagina mas alla del sitio donde la parte empieza. Si a pocos bloques por
    detras hay una portadilla, ella es el destino."""
    i = e['i']
    if e.get('lvl') == 0:
        for j in range(i, max(-1, i - 7), -1):
            if blocks[j].get('t') == 'plate':
                return j
    return i


def desjustificar_enlaces():
    """Un parrafo que termina en una direccion electronica larga se justificaba:
    la direccion no cabia en el renglon del rotulo, pasaba entera a la linea
    siguiente y dejaba el rotulo estirado de margen a margen («Identificador
    digital     de     objeto:»). Esos parrafos van en bandera, y la direccion
    puede partirse si hace falta. El aparato (ref, note) ya lo hacia."""
    n = 0
    # los asientos del aparato (ref, note) son parrafos plenos: conservan la
    # justificacion y la direccion se parte donde haga falta; alternar asientos
    # justificados y en bandera producia un ritmo visual irregular
    CUERPO = ('p', 'fnote', 'field', 'epi', 'auth')
    for b in blocks:
        if b.get('t') not in CUERPO:
            continue
        if any(p.get('url') for p in b.get('parts', []) or []):
            b['ragged'] = True
            n += 1
    print(f'  enlaces: {n} parrafos con direccion pasan a bandera')
    return n


def corregir_cornisas():
    """El campo h de un bloque da la cornisa de la pagina que lo contiene. El
    bloque del Contenido lo heredaba de la seccion anterior, de modo que el
    indice del volumen se encabezaba «CREDITOS DE LA EDICION»."""
    cambios = []
    for i, b in enumerate(blocks):
        if b.get('t') == 'autotoc' and b.get('h') != 'Contenido':
            cambios.append((i, b.get('h'), 'Contenido'))
            b['h'] = 'Contenido'
    for i, viejo, nuevo in cambios:
        print(f'  cornisa: bloque {i} «{viejo}» -> «{nuevo}»')
    return cambios


def paginate(page, limit):
    """Flujo natural con reglas de apertura y de encabezado no huérfano.

    Los cortes de bloque caen SIEMPRE en frontera natural de línea: la busqueda
    binaria maximiza palabras dentro del presupuesto de altura, y como la altura
    solo crece por líneas enteras, el máximo llena su última línea. El antiguo
    retroceso por palabras dejaba renglones-muñón («…porque el Consejo es,») al
    pie de página. Además ningún fragmento queda en una sola línea: ni huérfana
    al pie ni viuda en cabeza; si no se puede, el bloque pasa entero."""
    pages = []
    cur = []          # segmentos [bi, from, to] de la página en curso
    n = len(blocks)

    def flush(hard=False):
        """hard=True cuando el corte es estructural (pb, portadilla, apertura
        mayor, ficha): tras esa frontera no se reequilibra contenido."""
        nonlocal cur
        if cur:
            pages.append({'bleed': False, 'segs': cur, 'hard_after': hard})
            cur = []
        elif pages:
            pages[-1]['hard_after'] = pages[-1].get('hard_after') or hard

    def ev(segs):
        return page.evaluate('s => window.measureOf(s)', segs)

    def line_h(bi, frm=0):
        """Altura de un fragmento de dos palabras: una línea con sus márgenes."""
        return ev([[bi, frm, min(frm + 2, page.evaluate('i => window.wc(i)', bi))]])

    def natural_cut(prefix, bi, frm, budget):
        """Máximo de palabras cuyo fragmento cabe en budget; el máximo cae en
        frontera de línea (una palabra más habría abierto línea nueva)."""
        wc = page.evaluate('i => window.wc(i)', bi)
        lo, hi, best = frm + 1, wc, None
        while lo <= hi:
            mid = (lo + hi) // 2
            hh = ev(prefix + [[bi, frm, mid]])
            if hh <= budget:
                best = mid; lo = mid + 1
            else:
                hi = mid - 1
        return best, wc

    MIN2 = 1.55       # umbral «al menos dos líneas»: alto > 1.55 × una línea

    i = 0
    while i < n:
        b = blocks[i]
        t = b.get('t')
        if cur and blocks[cur[-1][0]].get('t') == 'autotoc':
            flush(hard=True)   # el Contenido cierra su pagina, partido o no
        if t in BLEED:
            flush(hard=True)
            pages.append({'bleed': True, 'segs': [[i, 0, None]], 'hard_after': True})
            i += 1
            continue
        if t == 'pb':
            flush(hard=True); i += 1; continue
        if t == 'major':
            # abre página; si viene precedido de su rótulo, éste ya abrió
            if not (cur and len(cur) == 1 and blocks[cur[0][0]].get('t') == 'rot'):
                flush(hard=True)
        if t == 'ficha':
            # cada Mesa Directiva abre su propia página; pero la primera del
            # periodo comparte página con la cabecera de su sección, que si no
            # quedaba sola («Mesas Directivas del primer periodo» y nada más)
            resto = [blocks[s[0]].get('t') for s in cur
                     if blocks[s[0]].get('t') not in INVISIBLES]
            if any(v not in ('sec', 'major', 'rot') for v in resto):
                flush(hard=True)
        if t == 'rot' and i + 1 < n and blocks[i + 1].get('t') == 'major':
            flush(hard=True)

        trial = cur + [[i, 0, None]]
        h = ev(trial)
        if h <= limit + 0.5:
            cur = trial
            i += 1
            continue

        if not cur:
            # el bloque solo no cabe en página vacía: partir por líneas
            L1 = line_h(i)
            best, wc = natural_cut([], i, 0, limit)
            best = best or 1
            pages.append({'bleed': False, 'segs': [[i, 0, best]]})
            rest_from = best
            while rest_from < wc:
                rem_h = ev([[i, rest_from, None]])
                if rem_h <= limit:
                    # el resto cabe: si quedó en una sola línea, retrocede el
                    # corte anterior una línea para que no viaje viuda
                    if rem_h < MIN2 * L1 and pages and pages[-1]['segs'][-1][0] == i:
                        pf = pages[-1]['segs'][-1][1]
                        h_prev = ev([[i, pf, rest_from]])
                        nb, _ = natural_cut([], i, pf, h_prev - 0.55 * L1)
                        if nb and nb > pf:
                            pages[-1]['segs'][-1][2] = nb
                            rest_from = nb
                    cur = [[i, rest_from, None]]
                    break
                b2, _ = natural_cut([], i, rest_from, limit)
                b2 = b2 or (rest_from + 1)
                pages.append({'bleed': False, 'segs': [[i, rest_from, b2]]})
                rest_from = b2
            i += 1
            continue

        # cabe parte del bloque en lo que resta de página
        L1 = line_h(i)
        best, wc = natural_cut(cur, i, 0, limit)

        def push_whole():
            nonlocal cur
            # un encabezado al pie arrastra consigo TODA la cadena de rótulos
            # que lo precede («Ficha» + campo, rótulo + sección…): desmontar
            # solo el último dejaba al anterior huérfano al pie
            moved = []
            while cur and blocks[cur[-1][0]].get('t') in ATTACH_NEXT and len(cur) > 1:
                moved.insert(0, cur.pop())
            flush()
            cur = moved

        if t in ATTACH_NEXT or best is None or ev([[i, 0, best]]) < MIN2 * L1:
            push_whole()   # no cabe ni con dos líneas dignas: pasa entero
            continue

        # la cola que viaja a la página siguiente tampoco puede ser una línea
        tail_h = ev([[i, best, None]])
        guard = 0
        while tail_h < MIN2 * L1 and guard < 3:
            used = ev(cur + [[i, 0, best]])
            nb, _ = natural_cut(cur, i, 0, used - 0.55 * L1)
            if not nb or nb >= best:
                break
            best = nb
            tail_h = ev([[i, best, None]])
            guard += 1
        if ev([[i, 0, best]]) < MIN2 * L1:
            push_whole()   # el retroceso dejó huérfana la cabeza: pasa entero
            continue
        cur = cur + [[i, 0, best]]
        flush()
        # La cola puede ser mas alta que la caja entera (el Contenido, una
        # relacion larga): se sigue partiendo aqui, como el bloque que no cabe
        # en pagina vacia. Antes viajaba entera a la pagina siguiente y, cuando
        # el bloque posterior la cerraba, lo que rebasaba lo recortaba la caja
        # en silencio.
        rest_from = best
        while rest_from < wc and ev([[i, rest_from, None]]) > limit:
            nb, _ = natural_cut([], i, rest_from, limit)
            if not nb or nb <= rest_from or nb >= wc:
                break
            pages.append({'bleed': False, 'segs': [[i, rest_from, nb]]})
            rest_from = nb
        cur = [[i, rest_from, None]]
        i += 1
    flush()

    # Reequilibrio: una pagina de continuacion casi vacia (el residuo de una
    # ficha que rebasa por poco, una nota suelta) se rellena moviendo bloques
    # enteros desde la pagina anterior, solo a traves de fronteras blandas
    # (nunca sobre un pb, una portadilla o la apertura de una ficha).
    reeq = 0
    for k in range(1, len(pages)):
        p, prev = pages[k], pages[k - 1]
        if p['bleed'] or prev['bleed'] or prev.get('hard_after'):
            continue
        hp = ev(p['segs'])
        if hp >= 0.28 * limit:
            continue
        for _ in range(6):
            if not prev['segs'] or len(prev['segs']) <= 1:
                break
            last = prev['segs'][-1]
            if last[1] != 0 or last[2] is not None:
                break              # fragmento partido: no se traslada
            nueva_prev = prev['segs'][:-1]
            nueva_p = [last] + p['segs']
            if ev(nueva_prev) < ev(nueva_p):
                break              # no invertir el desequilibrio
            prev['segs'], p['segs'] = nueva_prev, nueva_p
            reeq += 1
            if ev(p['segs']) >= 0.28 * limit:
                break
        # un rotulo no queda suelto al pie tras el traslado
        while (len(prev['segs']) > 1 and prev['segs'][-1][1] == 0
               and prev['segs'][-1][2] is None
               and blocks[prev['segs'][-1][0]].get('t') in ATTACH_NEXT):
            p['segs'] = [prev['segs'].pop()] + p['segs']
            reeq += 1
    if reeq:
        print(f'  reequilibrio: {reeq} bloques movidos a paginas de continuacion cortas')

    # Reparto del corte: si la pagina corta es el residuo de un bloque partido
    # (dos lineas de nota antes de un salto duro), mover bloques enteros no
    # ayuda. Primero se intenta reunir el bloque entero en la pagina residuo;
    # si no cabe, se recoloca el corte hacia atras, linea a linea, sin dejar
    # nunca la cabeza en menos de dos lineas y solo si el residuo mejora.
    resplit = 0
    for k in range(1, len(pages)):
        p, prev = pages[k], pages[k - 1]
        if p['bleed'] or prev['bleed']:
            continue
        if ev(p['segs']) >= 0.22 * limit:
            continue
        head = prev['segs'][-1] if prev['segs'] else None
        tail = p['segs'][0] if p['segs'] else None
        if not head or not tail or head[0] != tail[0]:
            continue
        if head[2] is None or tail[1] != head[2]:
            continue               # no son las dos mitades del mismo corte
        bi, pf = head[0], head[1]
        entero = [[bi, pf, None]] + p['segs'][1:]
        if len(prev['segs']) > 1 and ev(entero) <= limit:
            # el bloque completo cabe en la pagina residuo: se reune alli y la
            # pagina anterior cierra limpia en el bloque previo. El rotulo (u
            # ornamento) que anunciaba al bloque reunido viaja con el: dejarlo
            # seria estrenar la pagina siguiente con su encabezado huerfano
            # al pie de la anterior.
            prev['segs'] = prev['segs'][:-1]
            p['segs'] = entero
            while (len(prev['segs']) > 1 and prev['segs'][-1][1] == 0
                   and prev['segs'][-1][2] is None
                   and blocks[prev['segs'][-1][0]].get('t') in
                       (ATTACH_NEXT | {'orn'})):
                p['segs'] = [prev['segs'].pop()] + p['segs']
            resplit += 1
            continue
        L1 = line_h(bi, pf)
        respaldo = (head[2], tail[1])
        guard = 0
        while ev(p['segs']) < 0.22 * limit and guard < 14:
            h_head = ev([[bi, pf, head[2]]])
            if h_head - 0.55 * L1 < MIN2 * L1:
                break              # la cabeza no puede bajar de dos lineas
            nb, _ = natural_cut([], bi, pf, h_head - 0.55 * L1)
            if not nb or nb >= head[2] or nb <= pf + 1:
                break
            head[2] = nb
            tail[1] = nb
            resplit += 1
            guard += 1
        if guard and ev([[bi, pf, head[2]]]) < MIN2 * L1:
            head[2], tail[1] = respaldo   # nunca dejar la cabeza huerfana
    if resplit:
        print(f'  reparto de corte: {resplit} ajustes hacia paginas residuo')

    # una página cuyos bloques no pintan nada (anclas, cierres de ficha) queda
    # en blanco: se funde con la siguiente en vez de imprimirse vacía
    def visible(segs):
        for bi, fr, to in segs:
            b = blocks[bi]
            t = b.get('t')
            if t in ('anchor', 'cardEnd', 'pb'):
                continue
            if t in ('rule', 'orn', 'cardStart', 'autotoc'):
                return True
            if b.get('parts') or b.get('rows'):
                return True
        return False

    merged = []
    for p in pages:
        if not p['bleed'] and not visible(p['segs']):
            if merged and not merged[-1]['bleed']:
                merged[-1]['segs'] = merged[-1]['segs'] + p['segs']
            else:
                p['carry'] = True
                merged.append(p)
            continue
        if merged and merged[-1].get('carry'):
            carried = merged.pop()
            # En una pagina a sangre manda el primer segmento: es el bloque que
            # se pinta a plana entera. Los bloques ciegos arrastrados van
            # detras, o la lamina se compondria a partir de un ancla y saldria
            # en blanco.
            p['segs'] = (p['segs'] + carried['segs'] if p['bleed']
                         else carried['segs'] + p['segs'])
        merged.append(p)
    return [p for p in merged if p['bleed'] or visible(p['segs'])]


def folio_labels(pages):
    """Romanos en los preliminares y arabigos desde la primera parte numerada.
    El cambio de serie se detecta por la primera portadilla que no es la del
    umbral —dato del propio libro— y no por el titulo, que no dice «primera
    parte» y hacia que la deteccion fallara y todo el volumen saliera arabigo.
    Las paginas a sangre consumen numero pero no lo imprimen, como es de uso."""
    primera_parte = None
    for bi, b in enumerate(blocks):
        if b.get('t') == 'plate' and bi > 0:
            primera_parte = bi
            break
    corte = len(pages)
    if primera_parte is not None:
        for idx, p in enumerate(pages):
            if any(seg[0] == primera_parte for seg in p['segs']):
                corte = idx
                break
    r = a = 0
    for idx, p in enumerate(pages):
        if idx < corte:
            r += 1
            p['folio'] = roman(r)
        else:
            a += 1
            p['folio'] = str(a)
        p['show'] = not p['bleed']
    print(f'  folios: {corte} paginas en romano, {len(pages) - corte} en arabigo'
          f' (corte en la portadilla del bloque {primera_parte})')
    return pages


INVISIBLES = {'anchor', 'cardEnd', 'pb', 'rule'}


def cornisa_of(p):
    """La cornisa la da el campo h del primer bloque VISIBLE de la pagina. Los
    bloques que no pintan nada —sobre todo las anclas del indice— declaran la
    seccion que termina, no la que empieza: el ancla 85 dice «Contacto y
    presencia digital» y va justo delante de «Quienes hacen este volumen». Si se
    tomaba el primer bloque a secas, cinco secciones abrian con la cornisa de la
    anterior."""
    if p['bleed']:
        return ''
    for bi, _, _ in p['segs']:
        if blocks[bi].get('t') in INVISIBLES:
            continue
        h = blocks[bi].get('h')
        if h:
            return h
    for i in range(p['segs'][0][0], -1, -1):
        if blocks[i].get('t') in INVISIBLES:
            continue
        h = blocks[i].get('h')
        if h:
            return h
    return ''


def run():
    normalizar_aparato()
    corregir_cornisas()
    desjustificar_enlaces()
    limit = BOX_H * PX
    fuentes = open(os.path.join(HERE, 'fuentes', 'fuentes.css'), encoding='utf-8').read()
    style_js = open(os.path.join(HERE, 'bookstyle_extraido.js'), encoding='utf-8').read()
    u = lambda pt: f'{pt * PX:.2f}px'
    f = lambda pt: f'{pt * PX * TS:.2f}px'

    with sync_playwright() as pw:
        br = pw.chromium.launch(**({'executable_path': CHROME} if CHROME else {}))
        page = br.new_page(viewport={'width': 1200, 'height': 900})
        page.set_content(shell(fuentes, style_js), wait_until='load')
        page.wait_for_timeout(1800)

        folio_of = {}
        pages = None
        for it in range(4):
            _head, _rows = toc_html(folio_of, u, f)
            page.evaluate('a => window.setToc(a[0], a[1])', [_head, _rows])
            pages = folio_labels(paginate(page, limit))
            import json as _json
            with open(os.path.join(OUT, 'pages_debug.json'), 'w', encoding='utf-8') as _f:
                _json.dump([{'folio': p.get('folio'), 'bleed': p['bleed'],
                             'segs': p['segs']} for p in pages], _f)
            new_map = {}
            for p in pages:
                for bi, _, _ in p['segs']:
                    new_map.setdefault(bi, p['folio'])
            # el folio de una entrada de índice es el de su bloque
            entry_map = {}
            for t in TOC:
                bi = destino_toc(t)
                fo = new_map.get(bi)
                if fo is None:
                    for bj in range(bi, len(blocks)):
                        if bj in new_map:
                            fo = new_map[bj]; break
                entry_map[t['i']] = fo or ''
            print(f'  pase {it + 1}: {len(pages)} páginas')
            if entry_map == folio_of:
                break
            folio_of = entry_map

        # verificacion: la caja recorta en silencio lo que la desborde. Un
        # bloque que no se puede partir (como era el Contenido) se perdia sin
        # aviso. Ninguna pagina debe medir mas que la caja.
        desbordes = []
        for n, p in enumerate(pages):
            if p['bleed']:
                continue
            hh = page.evaluate('s => window.measureOf(s)', p['segs'])
            if hh > limit + 1:
                desbordes.append((n, round(hh / limit, 3)))
        if desbordes:
            print(f'  !! {len(desbordes)} paginas desbordan la caja y se recortarian:')
            for n, r in desbordes[:12]:
                print(f'     pagina {n} x{r}')
        else:
            print('  caja: ninguna pagina desborda')

        htmls = []
        for p in pages:
            if p['bleed']:
                htmls.append(page.evaluate('i => window.plateOf(i)', p['segs'][0][0]))
            else:
                htmls.append(page.evaluate('s => window.htmlOf(s)', p['segs']))
        cover = page.evaluate('() => window.coverOf()')
        back = page.evaluate('() => window.backOf()')
        br.close()

    final = ([{'bleed': True, 'folio': '', 'show': False, 'html': cover, 'segs': [], 'cor': ''}] +
             [{'bleed': p['bleed'], 'folio': p['folio'], 'show': p['show'],
               'html': h, 'segs': p['segs'], 'cor': cornisa_of(p)}
              for p, h in zip(pages, htmls)] +
             [{'bleed': True, 'folio': '', 'show': False, 'html': back, 'segs': [], 'cor': ''}])
    return final, fuentes


def emit(final, fuentes):
    css = f"""
{fuentes}
:root{{--font-body:'Lora','Gentium Griego',Georgia,serif;--font-heading:'Cormorant Garamond','Gentium Griego',Georgia,serif}}
@page{{size:{TRIM_W}pt {TRIM_H}pt;margin:0}}
html,body{{margin:0;padding:0;background:#fff;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{position:relative;width:{TRIM_W}pt;height:{TRIM_H}pt;overflow:hidden;
  page-break-after:always;break-after:page;background:#fff}}
.pg:last-child{{page-break-after:auto;break-after:auto}}
.caja{{position:absolute;left:{M_SIDE}pt;top:{M_TOP}pt;
  width:{BOX_W}pt;height:{BOX_H}pt;overflow:hidden}}
/* Una sola raya decorativa, y siempre la misma: bajo la cornisa y sobre el
   folio. El cuerpo no lleva ninguna otra. */
.filete{{position:absolute;left:{M_SIDE}pt;right:{M_SIDE}pt;top:{M_TOP - 13:.2f}pt;
  height:.4pt;background:{C_VINO};opacity:.42}}
.folio::before{{content:'';position:absolute;left:0;right:0;bottom:calc(100% + 7pt);
  height:.4pt;background:{C_VINO};opacity:.42}}
.cornisa{{position:absolute;left:{M_SIDE}pt;right:{M_SIDE}pt;top:{M_TOP - 26:.2f}pt;
  font-family:var(--font-heading);font-size:{6.8 * TS:.2f}pt;font-weight:600;
  letter-spacing:.10em;word-spacing:-.10em;text-transform:uppercase;color:{C_GRIS};
  text-align:right;white-space:nowrap;overflow:hidden}}
.folio{{position:absolute;left:{M_SIDE}pt;right:{M_SIDE}pt;bottom:{M_BOT - 34:.2f}pt;
  font-family:var(--font-body);font-size:{9.5 * TS:.2f}pt;color:{C_GRIS};
  text-align:center;font-variant-numeric:tabular-nums}}
"""
    parts = ['<!doctype html><html lang="es-MX"><meta charset="utf-8">',
             '<title>Genealogía de la Asociación Psiquiátrica Mexicana, A.C.</title>',
             f'<style>{css}</style><body>']
    for p in final:
        if p['bleed']:
            parts.append(f'<div class="pg">{p["html"]}</div>')
        else:
            filete = '<div class="filete"></div>' if p['cor'] else ''
            parts.append(f'<div class="pg"><div class="cornisa">{p["cor"]}</div>{filete}'
                         f'<div class="caja">{p["html"]}</div>'
                         f'<div class="folio">{p["folio"] if p["show"] else ""}</div></div>')
    parts.append('</body></html>')
    path = os.path.join(OUT, 'libro.html')
    open(path, 'w', encoding='utf-8').write(''.join(parts))
    with sync_playwright() as pw:
        br = pw.chromium.launch(**({'executable_path': CHROME} if CHROME else {}))
        pg = br.new_page()
        pg.goto('file://' + path, wait_until='load')
        pg.wait_for_timeout(3500)
        pg.pdf(path=os.path.join(OUT, 'libro.pdf'), prefer_css_page_size=True,
               print_background=True,
               margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        br.close()

    page_of = {}
    for pi, p in enumerate(final):
        for bi, _, _ in p['segs']:
            page_of.setdefault(bi, pi)
    marks = []
    for t in TOC:
        destino = destino_toc(t)
        pi = page_of.get(destino)
        if pi is None:
            for bj in range(destino, len(blocks)):
                if bj in page_of:
                    pi = page_of[bj]; break
        marks.append({'lvl': t['lvl'], 'label': t['label'], 'page': pi})
    # el folio se guarda SIEMPRE, tambien el de las paginas ciegas: consumen
    # numero aunque no lo impriman, y las etiquetas del PDF necesitan la serie
    # entera para no reiniciarse en cada lamina.
    json.dump({'pages': [{'folio': p['folio'] or None,
                          'impreso': bool(p['show'] and p['folio']),
                          'bleed': p['bleed']} for p in final], 'marks': marks},
              open(os.path.join(HERE, 'indice_final.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)


if __name__ == '__main__':
    final, fuentes = run()
    print('páginas totales:', len(final))
    emit(final, fuentes)
    print('PDF escrito')
