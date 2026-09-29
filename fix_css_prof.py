# -*- coding: utf-8 -*-
"""fix_css_prof.py — Corrección de PROFUNDIDAD de CSS en páginas interiores.

Bug confirmado en disco (2026-09-19, rutas resueltas con normpath):
  portada  ediciones/01/index.html            -> ../../css/  [OK, 2 niveles]
  seccion  ediciones/01/secciones/<id>.html   -> ../../css/  [MAL: necesita 3]
  articulo ediciones/01/articulos/<id>.html   -> ../../css/  [MAL: necesita 3]

Estos archivos están a 3 niveles de revista/css/, así que su ruta correcta
es ../../../css/.  Este script lo corrige SOLO en disco (no regenera).
"""
import os, glob

E = r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista\ediciones\01"
cambios = 0

for sub in ("secciones", "articulos"):
    for p in glob.glob(os.path.join(E, sub, "*.html")):
        with open(p, encoding="utf-8") as f:
            t = f.read()
        n = t.count("../../css/")
        if n:
            t2 = t.replace("../../css/", "../../../css/")
            with open(p, "w", encoding="utf-8") as f:
                f.write(t2)
            cambios += n
            print("  FIX  %-42s -> %d css" % (os.path.basename(p), n))

print("== total rutas css corregidas a 3 niveles: %d ==" % cambios)

# verificación: resolver ahora la ruta real de una sección y un artículo
import re
for sub, ej in (("secciones", "escuela"), ("articulos", None)):
    import os as _o
    if ej:
        p = os.path.join(E, sub, ej + ".html")
    else:
        import glob as _g
        p = sorted(_g.glob(os.path.join(E, sub, "*.html")))[0]
    h = open(p, encoding="utf-8").read()
    refs = re.findall(r"""href=["']([^"']*\.css)["']""", h)
    for r in refs:
        absr = _o.path.normpath(_o.path.join(_o.path.dirname(p), r))
        print("  %-50s -> %s [%s]" % (os.path.relpath(p, E), r,
                                      "OK" if os.path.exists(absr) else "FALTA"))
