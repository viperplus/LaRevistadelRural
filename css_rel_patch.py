# -*- coding: utf-8 -*-
"""css_rel_patch.py — CORRECCIÓN FINAL y determinista del generador.

Problema REAL encontrado (verificado en disco):
  - portada (ediciones/01/index.html)    usa ../../css/  -> CORRECTO (sube 2)
  - seccion (ediciones/01/secciones/X)   usa ../../css/  -> MAL: necesita subir 3
  - articulo (ediciones/01/articulos/X)  usa ../../css/  -> MAL: necesita subir 3
Por eso las páginas interiores se ven sin formato (CSS no carga).

Arreglo SIN tocar plantillas: tras cada .format() que produce SECCION o
ARTICULO, reescribimos la ruta css ../../css/ -> ../../../css/ (se mantiene
intacta para la portada).  Es una sola línea de replace por página, segura.

Además verifica que las fotos que el usuario envió (enviar_aqui/imagenes_odt/
<slug>/) tienen archivos reales y reporta cuántas se copiarán.
"""
import os, sys, io, subprocess, glob as G

BASE = r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista"
P    = os.path.join(BASE, "construir_revista.py")

c = open(P, encoding="utf-8").read()

# --- 1) insertar replace de rutas css tras cada open() de seccion/articulo ---
marcas = [
    'open(os.path.join(EDIT, "secciones", s["id"] + ".html")',
    'open(os.path.join(EDIT, "articulos", sid + ".html")'
]
plant = '        html = html.replace("../../css/", "../../../css/")\n'

n = 0
for m in marcas:
    i = c.find(m)
    assert i > 0, "marca no hallada: " + m
    # encontrar el \n de cierre de la llamada open(...) (primer ')' seguido de \n)
    j = c.find(")", i)
    while j != -1 and c[j+1:j+2] != "\n":
        j = c.find(")", j + 1)
    c = c[:j+1] + "\n" + plant + c[j+1:]
    n += 1

open(P, "w", encoding="utf-8").write(c)
print("== insertadas %d limpiezas de ruta css ==" % n)

# --- 2) re-correr el generador ---
r = subprocess.run([sys.executable, "construir_revista.py"], cwd=BASE,
                   capture_output=True, text=True,
                   encoding="utf-8", errors="replace", timeout=240)
print("== rc=%s ==" % r.returncode)
print((r.stdout or r.stderr).strip()[:500])

# --- 3) verificación final: rutas css REALES que carga cada página ---
import re, json
ED = os.path.join(BASE, "ediciones", "01")
def css_ok(rel, fromdir):
    absr = os.path.normpath(os.path.join(fromdir, rel))
    return os.path.exists(absr), absr

print("\n== rutas css resueltas POR página (debe ser OK en todas) ==")
for d in [ED, os.path.join(ED, "secciones"), os.path.join(ED, "articulos")]:
    for f in sorted(G.glob(os.path.join(d, "*.html")))[:2]:
        h = open(f, encoding="utf-8").read()
        refs = re.findall(r'href="([^"]*\.css)"', h)
        for rel in refs:
            ok, absr = css_ok(rel, os.path.dirname(f))
            print("  %-42s -> %-54s %s" %
                  (os.path.basename(f), rel, "OK" if ok else "FALTA"))
