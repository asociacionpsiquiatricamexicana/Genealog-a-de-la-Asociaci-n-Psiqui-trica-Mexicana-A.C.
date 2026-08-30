# -*- coding: utf-8 -*-
"""Sincroniza los dos flipbooks con el estado vivo del libro:
  * Standalone: reinyecta en el manifiesto el JSON del libro Y el modulo de
    estilo (ambos gzip+base64), de modo que composicion y contenido igualen
    al PDF.
  * Plano: regenera via flatten.py (lee assets/*.bin y el modulo de estilo).
"""
import json, base64, gzip, re, io, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# El flipbook autonomo se construye reinyectando el libro y el modulo de estilo
# en el manifiesto de una plantilla: el visor con su codigo, sus tipografias y
# su andamiaje. Esa plantilla es un archivo grande que no vive en el repositorio;
# se indica con FLIPBOOK_SRC. A falta de ella se puede partir del flipbook ya
# publicado, que sirve de plantilla de si mismo.
OUT = 'Genealogia_APM_Flipbook__Standalone__corregido.html'
SRC = os.environ.get('FLIPBOOK_SRC') or os.path.join(HERE, os.pardir, OUT)
if not os.path.exists(SRC):
    raise SystemExit(
        f'no se encuentra la plantilla del flipbook autonomo: {SRC}\n'
        'Indica su ruta en la variable FLIPBOOK_SRC, o deja en '
        f'genealogia/{OUT} el flipbook publicado, que sirve de plantilla.')
UUID_BOOK = '08fffc00-d395-438c-88b0-a0545e4c4793'
UUID_STYLE = 'a4d0e564-9e95-4331-9b24-990858d9e4e7'

def gz64(raw: bytes) -> str:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb', mtime=0) as gz:
        gz.write(raw)
    return base64.b64encode(buf.getvalue()).decode('ascii')

# El componente que pinta cada cara del libro y el cajon del Indice arman su
# estilo como objetos de JavaScript aplicados directamente, sin pasar por el
# ayudante css(): quedaban fuera de toda compensacion del seguimiento. La
# cornisa del visor baja ademas al mismo techo que la del impreso.
OBJETOS_VISOR = [
    ("letterSpacing: '0.12em', textTransform: 'uppercase', color: '#767070',",
     "letterSpacing: '0.1em', wordSpacing: '-0.1em', textTransform: 'uppercase', color: '#767070',"),
    ("fontSize: px(6.6), letterSpacing: '0.1em',",
     "fontSize: px(6.6), letterSpacing: '0.1em', wordSpacing: '-0.1em',"),
    ("fontSize: '13px', letterSpacing: '0.1em', textTransform: 'uppercase', color: '#7D4343' }",
     "fontSize: '13px', letterSpacing: '0.1em', wordSpacing: '-0.1em', textTransform: 'uppercase', color: '#7D4343' }"),
]


def compensar_seguimiento(html: str) -> str:
    """Cancela el doble conteo del espacio entre palabras en la interfaz del visor.

    El seguimiento tipografico (letter-spacing) tambien se suma despues del
    caracter de espacio, de modo que el hueco entre palabras crece el doble que
    el hueco entre letras y se lee como un espacio de mas. El modulo de estilo
    del libro ya lo compensa en su ayudante css(); los rotulos de la interfaz
    del visor —cabecera, cajon de busqueda, aviso de carga, botones— se
    escriben como CSS plano y quedaban fuera. Se les anade aqui el
    word-spacing negativo equivalente, sin tocar los que ya lo declaran.
    """
    puestos = 0

    def arregla(cuerpo: str) -> str:
        nonlocal puestos
        if "word-spacing" in cuerpo:
            return cuerpo
        m = re.search(r"letter-spacing:\s*(-?[\d.]+)em", cuerpo)
        if not m or float(m.group(1)) <= 0:
            return cuerpo
        puestos += 1
        return cuerpo[:m.end()] + f";word-spacing:-{m.group(1)}em" + cuerpo[m.end():]

    # el visor lleva parte de su plantilla dentro de cadenas de JavaScript,
    # donde las comillas del atributo van escapadas
    html = re.sub(r'style=(\\?)"([^"]*)"',
                  lambda m: 'style=' + m.group(1) + '"' + arregla(m.group(2)) + '"', html)
    html = re.sub(r"\{([^{}]*)\}", lambda m: "{" + arregla(m.group(1)) + "}", html)

    # El componente que pinta cada cara del libro y el cajon del Indice arman su
    # estilo como objetos de JavaScript aplicados directamente, sin pasar por el
    # ayudante css(): quedaban fuera de toda compensacion. Se les pone aqui, y
    # la cornisa del visor baja al mismo techo que la del impreso.
    for viejo, reemplazo in OBJETOS_VISOR:
        n = html.count(viejo)
        assert n <= 1, (n, viejo[:50])
        if n:
            html = html.replace(viejo, reemplazo)
            puestos += 1

    print(f"  interfaz: {puestos} rotulos con seguimiento compensado")
    return html


src = open(SRC, encoding='utf-8').read()
m = re.search(r'(<script type="__bundler/manifest">\n)(.*?)(\n  </script>)', src, re.S)
man = json.loads(m.group(2))

# libro
raw = json.dumps(json.load(open(f'assets/{UUID_BOOK}.bin', encoding='utf-8')),
                 ensure_ascii=False, separators=(', ', ': ')).encode('utf-8')
man[UUID_BOOK]['data'] = gz64(raw)
man[UUID_BOOK]['compressed'] = True
man[UUID_BOOK]['mime'] = 'application/json'

# estilo
style = open(f'assets/{UUID_STYLE}.js', encoding='utf-8').read().encode('utf-8')
man[UUID_STYLE]['data'] = gz64(style)
man[UUID_STYLE]['compressed'] = True
man[UUID_STYLE]['mime'] = 'application/javascript'

# el standalone guarda el componente de pagina comprimido en su manifiesto,
# fuera del alcance de un reemplazo sobre el texto del archivo
for _clave, _rec in man.items():
    if not _rec.get('compressed'):
        continue
    try:
        _txt = gzip.decompress(base64.b64decode(_rec['data'])).decode('utf-8')
    except Exception:
        continue
    if 'headStyle' not in _txt:
        continue
    _n = 0
    for _viejo, _nuevo in OBJETOS_VISOR:
        if _viejo in _txt:
            _txt = _txt.replace(_viejo, _nuevo); _n += 1
    if _n:
        _rec['data'] = gz64(_txt.encode('utf-8'))
        print(f'  manifiesto: {_n} rotulos compensados en el componente de pagina')

new_man = json.dumps(man, ensure_ascii=False, separators=(',', ':'))
out = src[:m.start(2)] + new_man + src[m.end(2):]
out = compensar_seguimiento(out)
open(OUT, 'w', encoding='utf-8').write(out)

# ida y vuelta
chk = json.loads(re.search(r'<script type="__bundler/manifest">\n(.*?)\n  </script>', out, re.S).group(1))
back = json.loads(gzip.decompress(base64.b64decode(chk[UUID_BOOK]['data'])))
orig = json.load(open(f'assets/{UUID_BOOK}.bin', encoding='utf-8'))
assert back == orig, 'libro: ida y vuelta no coincide'
back_style = gzip.decompress(base64.b64decode(chk[UUID_STYLE]['data'])).decode('utf-8')
assert back_style == style.decode('utf-8'), 'estilo: ida y vuelta no coincide'
print(f'standalone OK · {len(back["blocks"])} bloques · {os.path.getsize(OUT)/1024:.0f} KB')

# plano
# flatten.py rearma el plano desde assets/: ademas del libro y del modulo de
# estilo necesita la plantilla (template.html) y los recursos del visor —React,
# ReactDOM, el cargador y el componente de pagina—, que no viven en el
# repositorio. Sin ellos este ultimo paso no puede correr y el plano publicado
# se queda como esta.
r = subprocess.run(['python3', 'flatten.py'], capture_output=True, text=True)
print(r.stdout.strip())
if r.returncode != 0:
    print(r.stderr[-800:])
    raise SystemExit('flatten fallo: el standalone ya quedo actualizado, pero el '
                     'plano no se pudo rearmar. Comprueba que estan template.html '
                     'y los recursos del visor en assets/.')

PLANO = 'Genealogia_APM_Flipbook__plano.html'
plano = compensar_seguimiento(open(PLANO, encoding='utf-8').read())
open(PLANO, 'w', encoding='utf-8').write(plano)
