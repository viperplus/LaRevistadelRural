# -*- coding: utf-8 -*-
"""verificar_final.py — Solo LECTURA en disco, sin heredoc.

Resuelve cada href css de cada html generado (normpath) contra el disco
y dice OK/FALTA. Imprime también fotos totales. Nada más.
"""
import os, io, sys, glob, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E = r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista\ediciones\01"
rotos = 0
tot = 0

paginas = [os.path.join(E, "index.html")] \
        + sorted(glob.glob(os.path.join(E, "secciones", "*.html"))) \
        + sorted(glob.glob(os.path.join(E, "articulos", "*.html")))
tot = len(paginas)

for p in paginas:
    h = open(p, encoding="utf-8").read()
    base = os.path.dirname(p)
    refs = re.findall(r'''href=["']([^"']*\.css)["']''', h)
    for r in refs:
        absr = os.path.normpath(os.path.join(base, r))
        ok = os.path.exists(absr)
        if not ok:
            rotos += 1
        tag = os.path.relpath(p, E)
        print("  %-46s %-32s %s" % (tag, r, "OK" if ok else "FALTA"))

fotos = 0
for raiz, _, archs in os.walk(os.path.join(E, "imagenes")):
    fotos += sum(1 for f in archs
                 if os.path.splitext(f)[1].lower() in (".jpg", ".jpeg", ".png", ".webp", ".gif"))

print("\n== RESULTADO FINAL ==")
print("  paginas: %d   |   css rotos: %d   |   fotos en disco: %d"
      % (tot, rotos, fotos))
