# -*- coding: utf-8 -*-
"""verificacion_final.py — Estado consolidado al cierre de sesión.
Lee el disco tal cual está AHORA (sin regenerar) y comprueba:
  1. CSS: toda referencia .css en los 14 HTML de la edición 01 resuelve.
  2. Fotos: archivos reales en ediciones/01/imagenes/**.
  3. Portada <link> index.html (2 niveles) sigue intacta.
"""
import os, io, sys, re, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E = r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista\ediciones\01"

print("== 1) CSS resuelve en cada página (14 archivos) ==")
htmls = [os.path.join(E, "index.html")] \
      + sorted(glob.glob(os.path.join(E, "secciones", "*.html"))) \
      + sorted(glob.glob(os.path.join(E, "articulos", "*.html")))
rotos = 0
for p in htmls:
    h = open(p, encoding="utf-8").read()
    refs = re.findall(r'''href=["']([^"']*\.css)["']''', h)
    for r in refs:
        ab = os.path.normpath(os.path.join(os.path.dirname(p), r))
        if not os.path.exists(ab):
            rotos += 1
            print("  FALTA  %s -> %s" % (os.path.basename(p), r))
print("  -> %d páginas · rutas css rotas: %d" % (len(htmls), rotos))

print("\n== 2) Fotos reales en ediciones/01/imagenes ==")
tot = 0
for raiz, _, archs in os.walk(os.path.join(E, "imagenes")):
    imgs = [f for f in archs if os.path.splitext(f)[1].lower()
            in (".jpg", ".jpeg", ".png", ".webp", ".gif")]
    if imgs:
        rel = os.path.relpath(raiz, E)
        tot += len(imgs)
        print("  %-52s %d" % (rel, len(imgs)))
print("  -> fotos totales en la edición: %d" % tot)

print("\n== 3) Portada index.html (debe seguir en ../../css/) ==")
h = open(os.path.join(E, "index.html"), encoding="utf-8").read()
for r in sorted(set(re.findall(r'''href=["']([^"']*\.css)["']''', h))):
    ab = os.path.normpath(os.path.join(E, r))
    print("  %-28s %s" % (r, "OK" if os.path.exists(ab) else "FALTA"))

print("\n== RESULTADO: %s ==" %
      ("TODO OK — revista completa y con formato" if rotos == 0 and tot > 0
       else "REVISAR (rutas rotas=%d, fotos=%d)" % (rotos, tot)))
