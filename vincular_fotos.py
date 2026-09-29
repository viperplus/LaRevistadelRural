# -*- coding: utf-8 -*-
"""vincula_fotos.py — Empareja fotos reales por CONTENIDO y regenera.

Ruldo determinista:
  1. Lee datos/ediciones.json (cánonico).
  2. Agrega a cada artículo el campo "odt" con la carpeta fuente real
     (verificada en disco: enviar_aqui/imagenes_odt/<carpeta>/), mapeando
     por tema + conteo + extensión de archivos.
  3. Re-escribe el JSON y vuelve a correr construir_revista.py.
  4. Verifica cuántas fotos quedaron en ediciones/01/imagenes/.
"""
import os, io, sys, json, subprocess, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# id de artículo (en JSON)  ->  carpeta fuente real en enviar_aqui/imagenes_odt/
MAPEO_ODT = {
    "el-chip-en-la-cancha":                "clase_9_art_culo_para_la_revista_milton_",
    "la-primera-ley-de-newton":            "la_ley_de_la_incercia",
    "el-partido-por-el-ambiente":          "el_partido_por_el_ambiente",
    "la-fiesta-del-paraje-treneta":        "fiestas_y_tradiciones_mundialistas",
    "proxima-parada-atractivos-mundialistas": "pr_xima_parada__atractivos_mundialistas_",
}

D = os.path.join(BASE, "datos", "ediciones.json")
datos = json.load(open(D, encoding="utf-8"))
fotos_antes = sum(len(a.get("fotos") or []) for a in datos.get("articulos", []))
cambios = 0

for a in datos.get("articulos", []):
    src = MAPEO_ODT.get(a.get("id"))
    if src:
        a["odt"] = src
        cambios += 1

# borrar el campo "odt" del artículo temporal/borrador (no tiene fotos)
for a in datos.get("articulos", []):
    if a.get("id") == "el-partido-por-el-ambiente-temporal":
        a.pop("odt", None)

open(D, "w", encoding="utf-8").write(json.dumps(datos, ensure_ascii=False, indent=2))

fotos_despues = sum(len(a.get("fotos") or []) for a in datos.get("articulos", []))
print("== JSON: %d artículos con 'odt' asignado == (fotos declaradas antes=%d)" %
      (cambios, fotos_antes))

# regenerar
r = subprocess.run([sys.executable, "construir_revista.py"], cwd=BASE,
                   capture_output=True, text=True, encoding="utf-8",
                   errors="replace", timeout=240)
print("== rc=%s ==" % r.returncode)
print((r.stdout or r.stderr).strip()[:900])

# verificación final de fotos en disco
E = os.path.join(BASE, "ediciones", "01", "imagenes")
total = 0
if os.path.isdir(E):
    for raiz, _, archs in os.walk(E):
        for f in archs:
            if os.path.splitext(f)[1].lower() in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
                total += 1
print("\n== fotos copiadas a ediciones/01/imagenes: %d ==" % total)
