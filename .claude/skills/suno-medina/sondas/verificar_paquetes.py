#!/usr/bin/env python3
"""Sonda: verifica los paquetes de entrega contra la normativa del propio paquete.

Mide el artefacto entregado, no el código que lo produjo, igual que las sondas
del taller del libro. Comprueba, por pista:

  §9   Style <=1000 caracteres; «Spanish lyrics» presente; negative presente;
       sin cumplidos vacíos; KEY y BPM según el mapa Camelot de §1 del álbum.
  §3.2 Lyrics solo con tags estructurales canónicos en inglés; ningún bracket
       descriptivo largo (la excepción quirúrgica es <=3 palabras).
  §2.2 Lyrics <=5000 caracteres. El conteo de versos se reporta como AVISO,
       no como fallo: el rango 60-80 orienta la redacción de una letra nueva,
       no invalida una pieza ya compuesta.
  checklist-pregeneracion regla 3: cero puntos, punto y coma y dos puntos.
  Limpieza: ninguna nota de la skill dentro de un bloque pegable.

Uso:  python3 sondas/verificar_paquetes.py [directorio_de_paquetes]
Sale con 1 si alguna pista falla.
"""
import re, sys, glob, os

CAMELOT = {1:("G minor",86), 2:("E minor",72), 3:("D# minor",120), 4:("D minor",129),
           5:("E minor",129), 6:("F minor",78), 7:("A minor",60), 8:("D# minor",92),
           9:("E minor",99), 10:("A minor",60), 11:("E major",144), 12:("B minor",129)}

CANON = {"intro","verse","pre-chorus","chorus","bridge","breakdown","interlude",
         "outro","end","instrumental break","guitar solo","piano solo","fade out",
         "ending","post-chorus","coda","final coda","main theme",
         "instrumental theme","instrumental build","instrumental outro",
         "instrumental variation","instrumental weighing"}

VERSOS_MIN, VERSOS_MAX = 60, 80   # orientativo (checklist-pregeneracion regla 5): avisa, no falla

def bloque(t, nombre):
    m = re.search(rf"═+\n{nombre}[^\n]*\n═+\n(.*?)(?=\n═+\n|\Z)", t, re.S)
    return m.group(1).strip() if m else ""

def revisar(path):
    num = int(os.path.basename(path)[:2])
    t = open(path, encoding="utf-8").read()
    style, exclude, lyrics = (bloque(t, x) for x in ("STYLE", "EXCLUDE", "LYRICS"))
    key, bpm = CAMELOT[num]
    fallos = []

    if len(style) > 1000: fallos.append(f"Style {len(style)}>1000 car.")
    if "Spanish lyrics" not in style and "instrumental" not in style.lower():
        fallos.append("falta «Spanish lyrics»")
    if not exclude.strip(): fallos.append("Exclude vacío")
    if re.search(r"\b(professional|high-quality|amazing)\b", style, re.I):
        fallos.append("cumplido vacío en Style")
    if not re.search(rf"\b{bpm} BPM\b", style): fallos.append(f"BPM != {bpm}")
    if key.lower() not in style.lower(): fallos.append(f"KEY != {key}")

    largos = []
    for b in re.findall(r"\[([^\]]+)\]", lyrics):
        base = re.sub(r"\s*\d+$", "", b.strip()).lower()
        if base in CANON: continue
        if len(b.split()) > 3: largos.append(len(b.split()))
    if largos: fallos.append(f"{len(largos)} bracket(s) largo(s), peor {max(largos)} palabras")

    if len(lyrics) > 5000: fallos.append(f"Lyrics {len(lyrics)}>5000 car.")
    versos = [l for l in lyrics.split("\n") if l.strip() and not l.strip().startswith("[")]
    avisos = []
    if versos and not (VERSOS_MIN <= len(versos) <= VERSOS_MAX):
        # Aviso, no fallo: el rango orienta la redacción de una letra nueva; una
        # pieza ya compuesta no se corrige añadiendo o quitando versos.
        avisos.append(f"{len(versos)} versos, fuera del rango orientativo {VERSOS_MIN}-{VERSOS_MAX}")

    prosc = len(re.findall(r"[.;:]", "\n".join(versos)))
    if prosc: fallos.append(f"{prosc} signo(s) proscrito(s)")

    for campo, b in (("STYLE",style),("EXCLUDE",exclude),("LYRICS",lyrics)):
        if "NÚCLEO ANTIGLOTAL" in b or "no pegar en Suno" in b:
            fallos.append(f"nota de la skill dentro de {campo}")
    return fallos, avisos

def main():
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "referencias", "paquetes")
    archivos = sorted(glob.glob(os.path.join(d, "*.txt")))
    if not archivos:
        print(f"sin paquetes en {d}"); return 1
    malas = 0
    for f in archivos:
        fallos, avisos = revisar(f)
        if fallos:
            malas += 1
            print(f"FALLA  {os.path.basename(f)}")
            for x in fallos: print(f"         · {x}")
        else:
            print(f"ok     {os.path.basename(f)}")
        for a in avisos: print(f"  aviso  {os.path.basename(f)}: {a}")
    print(f"\n{len(archivos)-malas}/{len(archivos)} pistas conformes")
    return 1 if malas else 0

if __name__ == "__main__":
    sys.exit(main())
