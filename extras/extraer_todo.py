# -*- coding: utf-8 -*-
"""extraer_todo.py — Vuelca el contenido de TODOS los .odt/.docx de enviar_aqui
usando la lógica de cargar_odt.py, y escribe datos/importados.json para revisar.
No toca ediciones.json todavía.
"""
import os, sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

AQUI = os.path.dirname(os.path.abspath(__file__))
REVISTA = os.path.abspath(os.path.join(AQUI, ".."))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, RAIZ)

import cargar_odt as C  # noqa: E402

ENV = os.path.join(RAIZ, "enviar_aqui")
C.EXTRAIDOS = ENV
C.EXTRAIDOS_IMG = os.path.join(ENV, "imagenes_odt")

salida = []
for nombre in sorted(os.listdir(ENV)):
    ext = os.path.splitext(nombre)[1].lower()
    if ext not in (".odt", ".docx"):
        continue
    ruta = os.path.join(ENV, nombre)
    try:
        lineas = C.cargar_odt(ruta, C.EXTRAIDOS_IMG) if ext == ".odt" else C.cargar_docx(ruta, C.EXTRAIDOS_IMG)
    except Exception as e:
        print("ERR", nombre, e)
        continue
    titulo = ""
    firma = ""
    parrafos = []
    fotos = 0
    for l in lineas:
        if l.startswith("[TITULO]"):
            if not titulo:
                titulo = l[8:].strip()
        elif l.startswith("[FIRMA]"):
            if not firma:
                firma = l[7:].strip()
        elif l.startswith("[PARRAFO]"):
            parrafos.append(l[9:].strip())
        elif l.startswith("[FOTO"):
            fotos += 1
    slug = C.slug_articulo(nombre)
    salida.append({
        "archivo": nombre,
        "slug": slug,
        "titulo": titulo,
        "firma": firma,
        "n_parrafos": len(parrafos),
        "n_fotos": fotos,
        "parrafos": parrafos,
    })

dest = os.path.join(AQUI, "..", "datos", "importados.json")
dest = os.path.abspath(dest)
with open(dest, "w", encoding="utf-8") as f:
    json.dump(salida, f, ensure_ascii=False, indent=2)

print("OK ->", os.path.relpath(dest, RAIZ))
print("documentos extraídos:", len(salida))
for s in salida:
    print("  %-42s parr=%-3d fotos=%-2d | %s" % (s["slug"][:42], s["n_parrafos"], s["n_fotos"], (s["titulo"] or "(sin título)")[:60]))
