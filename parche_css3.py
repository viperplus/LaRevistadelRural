# -*- coding: utf-8 -*-
"""parche_css3.py — Corrige el GENERADOR para que las páginas de sección y
artículo emitan rutas CSS de 3 niveles (../../../css/), que resuelven
desde ediciones/01/secciones/ y ediciones/01/articulos/.

Esto reemplaza el arreglo-de-disco previo (que se perdía al regenerar):
ahora el fix vive en el fuente, así que cada regeneración queda bien.
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(BASE, "construir_revista.py")
c = open(P, encoding="utf-8").read()

# Anclas: las dos líneas open() que escriben dentro de ediciones/01/.../secciones y articulos
ANCLAS = [
    'open(os.path.join(EDIT, "articulos", sid + ".html"),',
    'open(os.path.join(EDIT, "secciones", s["id"] + ".html"),',
]

# Procesamos de atrás hacia adelante para no corromper índices
ediciones = []
for ancla in ANCLAS:
    idx = 0
    while True:
        i = c.find(ancla, idx)
        if i < 0:
            break
        inicio_lin = c.rfind("\n", 0, i) + 1
        ind = c[inicio_lin:i]
        indent = ind[: len(ind) - len(ind.lstrip())]  # espacios de indentación
        # línea con la misma indentación
        repl = indent + 'html = html.replace("../../css/", "../../../css/")\n'
        ediciones.append((inicio_lin, repl))
        idx = i + 1

# aplicar de atrás hacia adelante
ediciones.sort(reverse=True)
for inicio_lin, repl in ediciones:
    c = c[:inicio_lin] + repl + c[inicio_lin:]

open(P, "w", encoding="utf-8").write(c)
print("== parche aplicado: %d página(s) (sección+artículo) corregidas en el fuente ==" % len(ediciones))
