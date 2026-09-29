# -*- coding: utf-8 -*-
"""diag_rutas.py — Qué cargan REALMENTE los HTML generados y qué falta.

Lee los 3 niveles (portada, una sección, un artículo), extrae TODAS las
referencias (href de CSS, src de imágenes) y verifica contra disco si cada
recurso existe relativo a su ubicación. Responde de una vez "qué está roto".
"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E = r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista\ediciones\01"


def rutas_de(html):
    css = re.findall(r"""href=["']([^"']*\.css[^"']*)["']""", html)
    imgs = re.findall(r"""src=["']([^"']*\.(?:jpe?g|png|webp|gif|svg))["']""", html, re.I)
    links = re.findall(r"""href=["']([^"']*\.html)["']""", html)
    return css, imgs, links


def verificar(nivel, path_html, base_dir):
    html = open(path_html, encoding="utf-8", errors="replace").read()
    css, imgs, links = rutas_de(html)
    print("\n=== %s :: %s ===" % (nivel, os.path.relpath(path_html, E)))
    print("  CSS  (%d):" % len(css))
    for r in css:
        absr = os.path.normpath(os.path.join(base_dir, r))
        print("    [%s] %s" % ("OK " if os.path.exists(absr) else "FALTA", r))
    print("  IMÁGENES (%d):" % len(imgs))
    for r in imgs[:14]:
        absr = os.path.normpath(os.path.join(base_dir, r))
        print("    [%s] %s" % ("OK " if os.path.exists(absr) else "FALTA", r))
    if len(imgs) > 14:
        print("    ... y %d más" % (len(imgs) - 14))
    print("  LINKS internos (%d) — primeros 6:" % len(links))
    for r in links[:6]:
        absr = os.path.normpath(os.path.join(base_dir, r))
        print("    [%s] %s" % ("OK " if os.path.exists(absr) else "FALTA", r))
    return html


verificar("PORTADA", os.path.join(E, "index.html"), E)

# una sección (la primera que exista)
secc = [f for f in os.listdir(os.path.join(E, "secciones")) if f.endswith(".html")]
if secc:
    verificar("SECCIÓN", os.path.join(E, "secciones", secc[0]), os.path.join(E, "secciones"))

# un artículo (el primero que exista)
arts = [f for f in os.listdir(os.path.join(E, "articulos")) if f.endswith(".html")]
if arts:
    verificar("ARTÍCULO", os.path.join(E, "articulos", arts[0]), os.path.join(E, "articulos"))

print("\n== listo diag_rutas ==")
