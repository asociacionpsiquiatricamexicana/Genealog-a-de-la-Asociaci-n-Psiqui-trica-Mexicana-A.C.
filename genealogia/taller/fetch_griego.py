"""Trae las caras griegas de las candidatas y comprueba que traen politonico."""
import re, subprocess, os
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0 Safari/537.36")
CAND = {
    'EB Garamond':   'family=EB+Garamond:ital,wght@0,400;0,600;1,400',
    'Cardo':         'family=Cardo:ital,wght@0,400;0,700;1,400',
    'Gentium Book Plus': 'family=Gentium+Book+Plus:ital,wght@0,400;0,700;1,400',
    'GFS Didot':     'family=GFS+Didot',
}
os.makedirs('griego', exist_ok=True)
for fam, q in CAND.items():
    r = subprocess.run(['curl', '-sS', '-A', UA,
                        f'https://fonts.googleapis.com/css2?{q}&display=swap'],
                       capture_output=True)
    css = r.stdout.decode('utf-8', 'replace')
    if '@font-face' not in css:
        print(f"  {fam}: sin respuesta util ({css[:70]!r})"); continue
    bloques = re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
    rangos = sorted({r for r, _ in bloques})
    guardados = 0
    for rng, blk in bloques:
        if rng not in ('greek', 'greek-ext'):
            continue
        m = re.search(r'url\((https://[^)]+\.woff2)\)', blk)
        if not m:
            continue
        d = subprocess.run(['curl', '-sS', '-A', UA, m.group(1)], capture_output=True).stdout
        est = re.search(r'font-style:\s*(\w+)', blk).group(1)
        peso = re.search(r'font-weight:\s*(\d+)', blk).group(1)
        open(f"griego/{fam.replace(' ','_')}-{rng}-{est}-{peso}.woff2", 'wb').write(d)
        guardados += 1
    print(f"  {fam}: subconjuntos {rangos} | caras griegas guardadas {guardados}")
