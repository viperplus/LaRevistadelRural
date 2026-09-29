# -*- coding: utf-8 -*-
"""verificar_estado.py — (RE)escrito limpio, solo lecturas.
Sin heredoc, sin replace sobre el fuente: accede directo al disco y
resuelve cada href .css/.svg de cada página generada.
"""
import os, io, sys, re, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E = r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista\ediciones\01"

def analizar(pagina, nivel_rel):
    """nivel_rel: 'portada' | 'seccion' | 'articulo' (para mensaje)"""
    h = open(pagina, encoding="utf-8").read()
    base = os.path.dirname(pagina)
    refs = re.findall(r'''(?:href|src)="([^"]*(?:\.css|\.svg|favicon[^" ]*))"''', h)
    malos = []
    for r in refs:
        if r.startswith(("http://", "https://", "data:")):
            continue
        ab = os.path.normpath(os.path.join(base, r))
        if not os.path.exists(ab):
            malos.append(r)
    return len(refs), malos

print("== CSV de rutas resueltas (rel - OK/FALTA) ==")
tot_refs = 0
tot_mal = 0
paginas = []
for p in [os.path.join(E, "index.html")] + \
         sorted(glob.glob(os.path.join(E, "secciones", "*.html"))) + \
         sorted(glob.glob(os.path.join(E, "articulos", "*.html"))):
    paginas.append(p)

for p in paginas:
    rel = os.path.relpath(p, E)
    n, mal = analizar(p, rel)
    tot_refs += n
    tot_mal += len(mal)
    if mal:
        for m in mal:
            print("  MAL   %-55s -> %s" % (rel, m))
    else:
        print("  ok    %-55s (%d refs)" % (rel, n))

print("\n== fotos en ediciones/01/imagenes ==")
t = 0
for raiz, _, archs in os.walk(os.path.join(E, "imagenes")):
    for a in archs:
        if os.path.splitext(a)[1].lower() in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            t += 1
print("  %d foto(s) en disco" % t)

print("\n== RESUMEN ==")
print("  paginas=%d  refs=%d  rotas=%d  fotos=%d" %
      (len(paginas), tot_refs, tot_mal, t))
