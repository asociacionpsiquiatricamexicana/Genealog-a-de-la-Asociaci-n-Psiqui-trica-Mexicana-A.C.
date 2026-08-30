import re, subprocess, base64
UA=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36")
SPECS={
 'Lora':'family=Lora:ital,wght@0,400;0,600;1,400;1,600',
 'Cormorant Garamond':'family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600',
}
def curl(url, out=None):
    cmd=['curl','-sS','-A',UA,url]
    if out: cmd+=['-o',out]
    r=subprocess.run(cmd,capture_output=True)
    return r.stdout if not out else open(out,'rb').read()

css_all=[]
for fam,q in SPECS.items():
    css=curl(f'https://fonts.googleapis.com/css2?{q}&display=swap').decode()
    # conservar solo latin y latin-ext
    blocks=re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
    for rng,blk in blocks:
        if rng not in ('latin','latin-ext'): continue
        m=re.search(r'url\((https://[^)]+\.woff2)\)', blk)
        if not m: continue
        data=curl(m.group(1))
        b64=base64.b64encode(data).decode()
        blk=blk.replace(m.group(1), f'data:font/woff2;base64,{b64}')
        css_all.append(blk)
    print(fam, 'caras latinas:', sum(1 for r,_ in blocks if r in ('latin','latin-ext')))
out='\n'.join(css_all)
open('fuentes/fuentes.css','w',encoding='utf-8').write(out)
print('css total %.0f KB'%(len(out)/1024))
