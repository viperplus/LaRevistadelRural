# -*- coding: utf-8 -*-
import os, io, sys, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
E = r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista\ediciones\01"
print("== Resolucion REAL css por nivel (href como quedó en el HTML) ==")
for p in glob.glob(os.path.join(E, "*.html")) + glob.glob(os.path.join(E, "secciones", "*.html")) + glob.glob(os.path.join(E, "articulos", "*.html")):
    rel = os.path.relpath(p, E)
    h = open(p, encoding="utf-8").read()
    refs = re.findall(r"""href=['"]([^'"]*\.css[^'"]*)['"]""", h)
    base = os.path.dirname(p)
    for r in refs:
        absr = os.path.normpath(os.path.join(base, r))
        print("  %-55s %-28s -> %s [%s]" %
              (rel, r, absr, "OK" if os.path.exists(absr) else "FALTA"))