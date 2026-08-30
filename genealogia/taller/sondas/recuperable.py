"""Comprueba que se puede recuperar del repositorio lo que hace falta para
volver a componer el libro, y dice que falta."""
import re, json, gzip, base64, os, subprocess
import sys

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir)
if not os.path.isdir(REPO):
    raise SystemExit(f"{REPO} no es un directorio: esta sonda recibe la carpeta de "
                     "publicacion (genealogia/), donde estan el PDF y los flipbooks.")
s = open(f"{REPO}/Genealogia_APM_Flipbook__Standalone__corregido.html", encoding="utf-8").read()
man = json.loads(re.search(r'<script type="__bundler/manifest">\n(.*?)\n  </script>', s, re.S).group(1))

libro = gzip.decompress(base64.b64decode(man["08fffc00-d395-438c-88b0-a0545e4c4793"]["data"]))
estilo = gzip.decompress(base64.b64decode(man["a4d0e564-9e95-4331-9b24-990858d9e4e7"]["data"]))

vivo_libro = open("assets/08fffc00-d395-438c-88b0-a0545e4c4793.bin", "rb").read()
vivo_estilo = open("assets/a4d0e564-9e95-4331-9b24-990858d9e4e7.js", "rb").read()

igual_libro = json.loads(libro) == json.loads(vivo_libro)
igual_estilo = estilo == vivo_estilo

print("lo publicado frente al taller:")
print(f"   contenido del libro: {'al dia' if igual_libro else 'DESFASADO'}  "
      f"({len(json.loads(libro)['blocks'])} bloques)")
print(f"   modulo de estilo:    {'al dia' if igual_estilo else 'DESFASADO'}  "
      f"({len(estilo)} bytes en el flipbook, {len(vivo_estilo)} en el taller)")
if not igual_estilo:
    print("   -> el flipbook lleva una version anterior del modulo de estilo;")
    print("      se pone al dia con sync_flipbooks.py.")

# Que el taller este versionado se le pregunta a git, no a una lista escrita a
# mano: la lista envejece en cuanto se confirma un archivo y sigue anunciando
# que falta lo que ya esta.
TALLER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
seguidos = subprocess.run(["git", "-C", TALLER, "ls-files"],
                          capture_output=True, text=True)
if seguidos.returncode != 0:
    raise SystemExit("\nno hay repositorio git aqui: no se puede decir que se recupera.")
versionados = set(seguidos.stdout.split())

necesarios = sorted(
    [f for f in os.listdir(".") if f.endswith(".py")]
    + [os.path.join("sondas", f) for f in os.listdir("sondas") if f.endswith(".py")]
    + ["assets/08fffc00-d395-438c-88b0-a0545e4c4793.bin",
       "assets/a4d0e564-9e95-4331-9b24-990858d9e4e7.js",
       "bookstyle_extraido.js", "fuentes/fuentes.css", "requisitos.txt", "LEEME.md"])

fuera = [f for f in necesarios if os.path.exists(f) and f not in versionados]
print(f"\ntaller versionado: {len(necesarios) - len(fuera)} de {len(necesarios)} archivos")
if not fuera:
    print("   se recompone el libro desde el repositorio, sin nada del entorno efimero.")
else:
    print("NO esta en el repositorio (solo en el taller efimero):")
    for f in fuera:
        print(f"   {f:<38} {os.path.getsize(f)/1024:>8.0f} KB")
