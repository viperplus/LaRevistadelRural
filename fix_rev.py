# -*- coding: utf-8 -*-
"""fix_rev.py — Corta construir_revista.py desde la corrupcion del main()
y reinserta un main() NUEVO que respeta el contrato de plantillas REAL
(HEAD_RECUR/PIE_PAG/TEMPLATE_*) leido del propio archivo intacto (1-197)."""
import os, sys, io, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
P    = os.path.join(BASE, "construir_revista.py")

src = open(P, encoding="utf-8").read()
lines = src.splitlines()

MARCA = '        html = TEMPLATE_ARTICULO.format('
idx = next(i for i, l in enumerate(lines) if MARCA in l)
assert 220 < idx < 290, "marca fuera de rango: %d" % idx
head_lines = "\n".join(lines[:idx])

MAIN = '''        sec_nom = sec["titulo"] if sec else "Voces"
        s_url = "secciones/%s.html" % sec["id"] if sec else "secciones/voces.html"
        sec_tag_nav = esc(sec_nom)
        html = TEMPLATE_ARTICULO.format(
            TITULO=esc(art.get("titulo", sid)), REV=REV,
            BAJADA=esc(art.get("bajada", "")), ED_NOM=ED_NOM, NAV=nav,
            SUBNOMBRE=esc(SUBNOMBRE),
            SEC_ETIQUETA=esc(sec_nom.upper()),
            AUTOR=esc(art.get("autor", "Estudiantes")),
            FECHA=esc(art.get("fecha", ED_NOM)),
            FECHA_ISO=esc(art.get("fecha_iso", "2026-09-01")),
            CUERPO=cuerpo,
            SEC_URL=s_url,
            SEC_TITULO_NAV=esc(sec_nom))
        open(os.path.join(EDIT, "articulos", sid + ".html"), "w", encoding="utf-8").write(html)

    ar_por_sec = {}
    for a in articulos:
        ar_por_sec.setdefault(a.get("seccion", "voces"), []).append(a)

    for i, s in enumerate(secciones):
        sec_num = "%02d" % (i + 1)
        art_sec = ar_por_sec.get(s["id"], [])
        cards = "".join(
            "<article class='art_card grid-6'><h3><a href='%s'>%s</a></h3>"
            "<p>%s</p></article>" % ("articulos/%s.html" % a["id"],
                                     esc(a.get("titulo", a["id"])),
                                     esc(a.get("bajada", "")))
            for a in art_sec)
        html = TEMPLATE_SECCION.format(
            TITULO=esc("Rural · %s" % s["titulo"]), REV=REV,
            BAJADA=esc(s.get("bajada", "")), ED_NOM=ED_NOM, NAV=nav,
            SUBNOMBRE=esc(SUBNOMBRE),
            SEC_NUM=sec_num, SEC_TOTAL="%02d" % len(secciones),
            SEC_TITULO=esc(s["titulo"]), SEC_DESCRIP=esc(s.get("bajada", "")),
            LISTA_ARTICULOS=cards)
        open(os.path.join(EDIT, "secciones", s["id"] + ".html"), "w", encoding="utf-8").write(html)

    sumario = "".join(SUMARIO_ITEM.format(
        num="%02d" % (i + 1), sec_tag=esc(s["id"]),
        url="secciones/%s.html" % s["id"], titulo=esc(s["titulo"]))
        for i, s in enumerate(secciones))
    sec_cards = "".join(SECCION_ITEM.format(
        url="secciones/%s.html" % s["id"], T_TITULO=esc(s["titulo"]),
        T_BAJADA=esc(s.get("bajada", ""))) for s in secciones)
    html = TEMPLATE_INDEX.format(
        TITULO=esc("Rural · %s" % ED_NOM), REV=REV,
        BAJADA=esc(SUBNOMBRE), ED_NOM=ED_NOM, NAV=nav,
        SUBNOMBRE=esc(SUBNOMBRE),
        SUMARIO=sumario, SECCIONES=sec_cards)
    open(os.path.join(EDIT, "index.html"), "w", encoding="utf-8").write(html)

    print("OK  ediciones/01  -> %d articulo(s) + %d seccion(es) + portada"
          % (len(articulos), len(secciones)))


if __name__ == "__main__":
    main()
'''
# OJO: EL MAIN_SOBRANTE viene DESPUÉS de la marca; aquí head_lines YA
# incluye "def main():" y el inicio correcto hasta "cuerpo = ...".
# Pero head_lines termina en "cuerpo = render_texto(...)" y NO incluye
# "sec_nom =..." — reaprovecho el head completo (1..idx) que va hasta
# la línea ANTERIOR a la marca (el bucle for art sigue abierto).
# MAIN empieza con "sec_nom =" que es la línea 227 del original -> OK.

nuevo = head_lines + "\\n" + MAIN
open(P, "w", encoding="utf-8").write(nuevo)
print("== reescrito: %d lineas (head %d + main nuevo) =="
      % (nuevo.count("\\n") + 1, head_lines.count("\\n") + 1))

r = subprocess.run([sys.executable or "python", "construir_revista.py"],
                   cwd=BASE, capture_output=True, text=True, encoding="utf-8",
                   errors="replace", timeout=180)
print("== rc=%d ==" % r.returncode)
out = r.stdout or r.stderr
print(out.strip()[:1400])
