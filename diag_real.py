# -*- coding: utf-8 -*-
"""diag_real.py — Estado REAL del proyecto: qué datos hay, qué CSS existe,
qué artículos, y qué referencias carga el HTML generado."""
import os, sys, io, json, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = os.path.dirname(os.path.abspath(__file__))

print("=== 1) datos/ediciones.json ===")
dp = os.path.join(BASE, "datos", "ediciones.json")
try:
    d = json.load(open(dp, encoding="utf-8"))
except Exception as e:
    print("  ERROR leyendo: %r" % e)
    d = None

if d:
    secs = d.get("secciones") or []
    arts = d.get("articulos") or []
    print("  secciones=%d  articulos=%d" % (len(secs), len(arts)))
    print("  secciones ids:", [s.get("id") for s in secs])
    for a in arts[:8]:
        print("   - [%s] %s  | seccion=%s | titulo=%s" % (
            a.get("id"), a.get("odt") or a.get("odt") or "?", 
            a.get("seccion"), (a.get("titulo") or "")[:40]))

print("\n=== 2) CSS en revista/css/ ===")
cdir = os.path.join(BASE, "css")
if os.path.isdir(cdir):
    for f in sorted(os.listdir(cdir)):
        print("  css/%s  (%d B)" % (f, os.path.getsize(os.path.join(cdir, f))))
else:
    print("  !! NO existe la carpeta css/")

print("\n=== 3) HTML generado (portada) — referencias reales ===")
h = os.path.join(BASE, "ediciones", "01", "index.html")
if os.path.exists(h):
    html = open(h, encoding="utf-8").read()
    css_refs = re.findall(r"""rel=["']stylesheet["'][^>]*href=["']([^"']+)["']""", html)
    print("  CSS que carga la portada (%d):" % len(css_refs))
    for r in css_refs:
        # resuelve relativo al archivo
        absr = os.path.normpath(os.path.join(os.path.dirname(h), r))
        print("    %-40s -> %s [%s]" % (r, absr, "OK" if os.path.exists(absr) else "FALTA"))
    imgs = re.findall(r"""src=["']([^"']+)["']""", html)
    print("  imagenes en portada (%d):" % len(imgs))
    for r in imgs[:6]:
        absr = os.path.normpath(os.path.join(os.path.dirname(h), r))
        print("    %-40s -> %s [%s]" % (r, absr, "OK" if os.path.exists(absr) else "FALTA"))
else:
    print("  !! NO existe ediciones/01/index.html")

print("\n=== 4) contenido del JSON (primeros 900 caracteres) ===")
if d:
    print(json.dumps(d, ensure_ascii=False, indent=1)[:900])
