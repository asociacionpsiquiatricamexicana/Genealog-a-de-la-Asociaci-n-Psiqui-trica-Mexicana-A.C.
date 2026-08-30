#!/usr/bin/env python3
"""Aplica parches de texto sobre la fuente de verdad del libro, o ninguno.

Cada parche dice en qué bloque va, qué texto reemplaza y por cuál. Antes de
escribir nada se comprueba que **cada** `viejo` aparece exactamente una vez, en
un solo fragmento del bloque: si alguno casa dos veces o ninguna, no se escribe
ni un parche. Un reemplazo que casa donde no debía es el error más caro de este
proyecto, porque no se ve hasta que alguien lee el PDF impreso.

    python3 parche.py parches.json            # comprueba y aplica
    python3 parche.py parches.json --ensayo   # solo comprueba

Formato de parches.json — una lista de objetos:

    [{"id": "nota 4 del cuarto episodio",
      "bloque": 876,
      "viejo": "texto exacto que se reemplaza",
      "nuevo": "texto que lo sustituye"}]

`bloque` puede omitirse si se pasa `"buscar"`: entonces se localiza el único
bloque que contiene ese texto, y se aborta si hay más de uno.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(AQUI, os.pardir, os.pardir, os.pardir, os.pardir,
                   "genealogia", "taller", "assets",
                   "08fffc00-d395-438c-88b0-a0545e4c4793.bin")


def cargar(ruta=None):
    ruta = ruta or os.path.normpath(BIN)
    if not os.path.exists(ruta):
        raise SystemExit(f"no encuentro la fuente del libro en {ruta}")
    return ruta, json.load(open(ruta, encoding="utf-8"))


def texto(bloque):
    return "".join((" " if p.get("br") else (p.get("x") or ""))
                   for p in (bloque.get("parts") or []))


def planear(bloques, parches):
    """Devuelve (plan, fallos). El plan solo se ejecuta si no hay fallos."""
    plan, fallos = [], []
    for p in parches:
        ident = p.get("id") or p["viejo"][:40]
        i = p.get("bloque")
        if i is None:
            cands = [k for k, b in enumerate(bloques) if p["viejo"] in texto(b)]
            if len(cands) != 1:
                fallos.append((ident, f"«buscar» halla {len(cands)} bloques; se necesita uno"))
                continue
            i = cands[0]
        if not (0 <= i < len(bloques)):
            fallos.append((ident, f"el bloque {i} está fuera de rango"))
            continue
        partes = bloques[i].get("parts") or []
        donde = [k for k, f in enumerate(partes) if p["viejo"] in (f.get("x") or "")]
        veces = sum((f.get("x") or "").count(p["viejo"]) for f in partes)
        if len(donde) != 1 or veces != 1:
            fallos.append((ident, f"aparece {veces} veces en {len(donde)} fragmentos del bloque {i}"))
            continue
        plan.append((ident, i, donde[0], p["viejo"], p["nuevo"]))
    return plan, fallos


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    parches = json.load(open(sys.argv[1], encoding="utf-8"))
    ensayo = "--ensayo" in sys.argv
    ruta, libro = cargar()
    plan, fallos = planear(libro["blocks"], parches)

    if fallos:
        print("PARCHES RECHAZADOS — no se escribió nada:")
        for ident, motivo in fallos:
            print(f"  · {ident}: {motivo}")
        raise SystemExit(1)

    for ident, i, k, viejo, nuevo in plan:
        print(f"  {'(ensayo) ' if ensayo else ''}bloque {i:>4} fragmento {k}: {ident}")
        if not ensayo:
            libro["blocks"][i]["parts"][k]["x"] = \
                libro["blocks"][i]["parts"][k]["x"].replace(viejo, nuevo)

    if ensayo:
        print(f"{len(plan)} parches comprobados, ninguno aplicado")
        return
    json.dump(libro, open(ruta, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"{len(plan)} parches aplicados sobre {os.path.basename(ruta)}")
    print("Recuerda: si además insertaste o borraste bloques, reancla el Contenido.")


if __name__ == "__main__":
    main()
