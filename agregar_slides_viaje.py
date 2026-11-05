# -*- coding: utf-8 -*-
"""agregar_slides_viaje.py — Slideshow de fotos en el artículo del viaje.

Las fotos ya están en ediciones/01/viaje-bariloche-el-cain/galeria/
(slide-01.jpg ... slide-47.jpg, descargadas de la carpeta de Drive).
Este script:
  1. arma la lista "slides" en el JSON,
  2. inserta el bloque {"t": "slides"} después de la presentación.
"""
import json, io, sys, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista"
UID = "viaje-bariloche-el-cain"
P = os.path.join(BASE, "datos", "ediciones.json")
GAL = os.path.join(BASE, "ediciones", "01", UID, "galeria")

fotos = sorted(f for f in os.listdir(GAL) if f.lower().endswith(".jpg"))
slides = ["galeria/%s" % f for f in fotos]
print("fotos en galeria:", len(slides))

d = json.load(open(P, encoding="utf-8"))
for a in d["articulos"]:
    if a.get("id") != UID:
        continue

    a["slides"] = slides

    # Sacar cualquier bloque de slides previo (por si se corre dos veces)
    cuerpo = [b for b in a.get("cuerpo", []) if b.get("t") != "slides"]

    intro = "Compartimos algunas de las fotos que sacamos durante esos días: la salida, el camino, los paisajes y los momentos que vivimos juntos."
    nuevo = [
        {"t": "p", "v": intro},
        {"t": "slides", "v": "Fotos del viaje a Bariloche · pasá las imágenes con las flechas"},
    ]
    # Después del primer párrafo de presentación
    cuerpo = cuerpo[:1] + nuevo + cuerpo[1:]
    a["cuerpo"] = cuerpo
    print("bloques del cuerpo:", [b.get("t") for b in cuerpo])
    break
else:
    print("ERROR: no encontre", UID)
    sys.exit(1)

open(P, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
print("OK json guardado")
