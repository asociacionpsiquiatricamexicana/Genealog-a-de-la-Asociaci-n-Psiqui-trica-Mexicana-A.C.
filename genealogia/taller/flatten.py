# -*- coding: utf-8 -*-
"""Aplana el flipbook: sin fase de desempaquetado, sin URL blob:, todo en línea."""
import json, base64, re, os

A='assets/'
def rd(u, mode='r'):
    for ext in ('.js','.html','.bin','.css'):
        p=A+u+ext
        if os.path.exists(p):
            return open(p,'rb').read() if mode=='rb' else open(p,encoding='utf-8').read()
    raise FileNotFoundError(u)

tpl=open('template.html',encoding='utf-8').read()
SUPPORT='845d96cb-bcd1-452b-9ad9-f4b66db8dac3'
DSB='afdd848e-d387-4d1f-b148-efb6b9e44158'
REACT='6175e48e-246a-490f-9202-8c8ece7c8c66'
REACTDOM='166d63ce-5078-4ba7-90ba-10e4675bb68e'
BOOKSTYLE='a4d0e564-9e95-4331-9b24-990858d9e4e7'
BOOK2='08fffc00-d395-438c-88b0-a0545e4c4793'

def safe(js):
    """Impide que el contenido cierre el <script> que lo envuelve."""
    return js.replace('</script','<\\/script').replace('<!--','<\\!--')

# --- 1. tipografías a data: URI -------------------------------------------
fonts=re.findall(r'url\("([0-9a-f-]{36})"\)', tpl)
for u in set(fonts):
    b64=base64.b64encode(rd(u,'rb')).decode('ascii')
    tpl=tpl.replace('url("%s")'%u, 'url("data:font/woff2;base64,%s")'%b64)
print('tipografías incrustadas:', len(set(fonts)))

# --- 2. bookStyle: de módulo ES a objeto global ----------------------------
mod=rd(BOOKSTYLE)
names=re.findall(r'^export\s+(?:const|let|var|function|class)\s+([A-Za-z_$][\w$]*)', mod, re.M)
assert names, 'no se hallaron exportaciones'
flat_mod=re.sub(r'^export\s+', '', mod, flags=re.M)
book_style_js = ('window.__bookStyle = (function(){\n%s\nreturn {%s};\n})();'
                 % (flat_mod, ', '.join(names)))
print('exportaciones de bookStyle:', len(names))

# --- 3. el volumen, ya corregido, como objeto global ----------------------
book=json.load(open(A+BOOK2+'.bin',encoding='utf-8'))
book_js='window.__book2 = ' + json.dumps(book, ensure_ascii=False).replace('<','\\u003c') + ';'

# --- 3b. el componente BookPage, como Blob ya resuelto ---------------------
BOOKPAGE='d3beda93-bfda-4edd-9417-416c012e5e89'
page=rd(BOOKPAGE)
# el sistema de diseño ya va en línea en la plantilla; estas dos referencias
# no existen como recursos y en el original devolvían 404
import re as _re
page=_re.sub(r'\s*<link rel="stylesheet" href="_ds/[^"]*">','',page)
page=_re.sub(r'\s*<script src="_ds/[^"]*"></script>','',page)
assert '_ds/' not in page
blob_js=('window.__resourceBlobs = {"./BookPage.dc.html": '
         'new Blob([%s], {type: "text/html"})};' % json.dumps(page, ensure_ascii=False))

# --- 4. sustituir import()/fetch() por los globales -----------------------
before=tpl
tpl=tpl.replace("import(/* @vite-ignore */ R.bookStyle || './book-style.js')",
                "Promise.resolve(window.__bookStyle)")
tpl=tpl.replace("fetch(R.book2 || 'book2.json').then((r) => r.json())",
                "Promise.resolve(window.__book2)")
assert tpl!=before and 'import(' not in tpl and "fetch(R.book2" not in tpl, 'no se pudo desviar import/fetch'

# --- 5. scripts externos en línea ----------------------------------------
head_inline = (
 '<script>window.__resources = {};</script>\n'
 '<script>' + safe(rd(REACT))     + '</script>\n'
 '<script>' + safe(rd(REACTDOM))  + '</script>\n'
 '<script>' + safe(book_style_js) + '</script>\n'
 '<script>' + safe(book_js)       + '</script>\n'
 '<script>' + safe(blob_js)       + '</script>\n')
tpl=tpl.replace('<script src="%s"></script>'%SUPPORT,
                head_inline + '<script>' + safe(rd(SUPPORT)) + '</script>')
tpl=tpl.replace('<script src="%s"></script>'%DSB,
                '<script>' + safe(rd(DSB)) + '</script>')
assert 'src="%s"'%SUPPORT not in tpl and 'src="%s"'%DSB not in tpl

# --- 6. comprobaciones finales -------------------------------------------
assert not re.search(r'src="[0-9a-f-]{36}"', tpl), 'quedan referencias por UUID'
# React y ReactDOM van en linea antes del cargador, de modo que las URL de
# unpkg que el visor conserva como respaldo no llegan a pedirse.
open('Genealogia_APM_Flipbook__plano.html','w',encoding='utf-8').write(tpl)
print('escrito · %.1f MB'%(len(tpl.encode())/1048576))
