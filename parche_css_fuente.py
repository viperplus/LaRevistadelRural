# -*- coding: utf-8 -*-
"""parche_css_fuente.py — Reparación PERMANENTE del generador.

Problema de fondo (verificado en disco):
  - index.html  (ediciones/01/)              usa ../../css/   -> 2 niveles, OK
  - secciones/*  y articulos/*  (3 niveles)  usa ../../css/   -> MAL (necesita ../../../)

El parche anterior sí arregló los HTML ya generados, pero al volver a correr
construir_revista.py el generador los SOBRESCRIBE con la ruta ../../css/ de
nuevo.  Así que el fix correcto es EN EL FUENTE: justo antes de escribir
cada página de sección y de artículo insertamos un .replace() global.

INSERTA (fácil de revertir, robusto a re-ejecución):
  html = html.replace("../../css/", "../../../css/")
antes de estas dos llamadas:
  open(os.path.join(EDIT, "articulos", sid + ".html",...
  open(os.path.join(EDIT, "secciones", s["id"] + ".html",...
"""
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "construir_revista.py")
c = open(P, encoding="utf-8").read()

ANCLAS = [
    'open(os.path.join(EDIT, "articulos", sid + ".html"',
    'open(os.path.join(EDIT, "secciones", s["id"] + ".html"',
]

# Recorremos de atrás hacia adelante para no invalidar índices
ediciones = []
for ancla in ANCLAS:
    idx = 0
    while True:
        i = c.find(ancla, idx)
        if i < 0:
            break
        inicio_lin = c.rfind("\n", 0, i) + 1
        ind = c[inicio_lin:i]
        indent = ind[: len(ind) - len(ind.lstrip())]
        repl = indent + 'html = html.replace("../../css/", "../../../css/")\n'
        ediciones.append((inicio_lin, repl))
        idx = i + 1

# Aplicar de atrás hacia delante para que los índices sigan siendo válidos
ediciones.sort(reverse=True)
for inicio_lin, repl in ediciones:
    c = c[:inicio_lin] + repl + c[inicio_lin:]

open(P, "w", encoding="utf-8").write(c)
print("== OK: %d páginas profundas parcheadas en el FUENTE del generador =="
      % len(ediciones))
