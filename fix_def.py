# -*- coding: utf-8 -*-
"""fix_def.py — Reparación DEFINITIVA de construir_revista.py.

Conserva tal cual las líneas 1-199 (docstring + imports + constantes +
funciones + plantillas TEMPLATE_*, que están íntegras en disco — verificadas
por lecturas repetidas) y reemplaza el main() corrupto (200+) por uno NUEVO
que respeta el contrato exacto de las plantillas:

  HEAD_RECUR -> TITULO REV BAJADA ED_NOM NAV
  PIE_PAG    -> REV SUBNOMBRE ED_NOM
  TEMPLATE_ARTICULO -> +SEC_ETIQUETA TITULO AUTOR FECHA FECHA_ISO CUERPO
                       SEC_URL SEC_TITULO_NAV
  TEMPLATE_SECCION  -> +SEC_NUM SEC_TOTAL SEC_TITULO SEC_DESCRIP LISTA_ARTICULOS
  TEMPLATE_INDEX    -> +ED_NOM SUBNOMBRE SUMARIO SECCIONES
  SUMARIO_ITEM -> sumario__num + sec_tag + url + titulo
  SECCION_ITEM -> url + T_TITULO + T_BAJADA
"""
import os, sys, io, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(BASE, "construir_revista.py")

src = open(TARGET, encoding="utf-8").read()
lines = src.splitlines()

# Punto de corte SEGURO: tras el bloque de plantillas (línea 199 = fin de
# SECCION_ITEM) — todo lo anterior está verificado íntegro en disco.
cabecera = "\n".join(lines[:199]) + "\n"

MAIN = r'''def main():
    datos = json.load(open(DATOS, encoding="utf-8"))
    secciones = datos.get("secciones") or []
    articulos = datos.get("articulos") or []

    os.makedirs(os.path.join(EDIT, "secciones"), exist_ok=True)
    os.makedirs(os.path.join(EDIT, "articulos"), exist_ok=True)
    os.makedirs(os.path.join(EDIT, "imagenes"), exist_ok=True)

    nav = "".join(
        "<li><a href='secciones/%s.html'>%s</a></li>" % (s["id"], esc(s["titulo"]))
        for s in secciones)
    nav = "<ul class='nav-ed__lista'>%s</ul>" % nav

    lista_sec = "".join(SECCION_ITEM.format(
        url="secciones/%s.html" % s["id"],
        T_TITULO=esc(s["titulo"]),
        T_BAJADA=esc(s.get("bajada", "")))
        for s in secciones)

    ar_por_sec = {}
    for art in articulos:
        ar_por_sec.setdefault(art.get("seccion", "voces"), []).append(art)

    for art in articulos:
        sid = art["id"]
        sec = next((s for s in secciones if s["id"] == art.get("seccion")), None)
        sec_nom = sec["titulo"] if sec else "Voces"
        fotos = copiar_imagenes(art.get("odt", sid), sid)
        texto = art.get("texto", "") or "\n".join(art.get("parrafos", []))
        cuerpo = render_texto(texto, fotos)
        if not cuerpo and art.get("parrafos"):
            cuerpo = "".join("<p class='txt-parrafo'>%s</p>" % esc(p)
                             for p in art["parrafos"])
        html = TEMPLATE_ARTICULO.format(
            TITULO=esc(art.get("titulo", sid)), REV=REV,
            BAJADA=esc(art.get("bajada", "")), ED_NOM=ED_NOM, NAV=nav,
            SUBNOMBRE=esc(SUBNOMBRE),
            SEC_ETIQUETA=esc(sec_nom.upper()),
            AUTOR=esc(art.get("autor", "Estudiantes")),
            FECHA=esc(art.get("fecha", ED_NOM)),
            FECHA_ISO=esc(art.get("fecha_iso", "2026-09-01")),
            CUERPO=cuerpo,
            SEC_URL=("secciones/%s.html" % sec["id"]) if sec else "secciones/voces.html",
            SEC_TITULO_NAV=esc(sec_nom))
        open(os.path.join(EDIT, "articulos", sid + ".html"),
             "w", encoding="utf-8").write(html)

    for i, s in enumerate(secciones):
        sec_num = "%02d" % (i + 1)
        lista_arts = "".join(
            "<article class='art_card grid-6'><h3>"
            "<a href='%s'>%s</a></h3><p>%s</p></article>" % (
                "articulos/%s.html" % a["id"],
                esc(a.get("titulo", a["id"])),
                esc(a.get("bajada", "")))
            for a in ar_por_sec.get(s["id"], []))
        html = TEMPLATE_SECCION.format(
            TITULO=esc("Rural · %s" % s["titulo"]), REV=REV,
            BAJADA=esc(s.get("bajada", "")), ED_NOM=ED_NOM, NAV=nav,
            SUBNOMBRE=esc(SUBNOMBRE),
            SEC_NUM=sec_num, SEC_TOTAL="%02d" % len(secciones),
            SEC_TITULO=esc(s["titulo"]),
            SEC_DESCRIP=esc(s.get("bajada", "")),
            LISTA_ARTICULOS=lista_arts)
        open(os.path.join(EDIT, "secciones", s["id"] + ".html"),
             "w", encoding="utf-8").write(html)

    sumario = "".join(SUMARIO_ITEM.format(
        num="%02d" % (i + 1),
        sec_tag=esc(s["titulo"]),
        url="secciones/%s.html" % s["id"],
        titulo=esc(s["titulo"]))
        for i, s in enumerate(secciones))
    html = TEMPLATE_INDEX.format(
        TITULO=esc("Rural · %s" % ED_NOM), REV=REV,
        BAJADA=esc(SUBNOMBRE), ED_NOM=ED_NOM, NAV=nav,
        SUBNOMBRE=esc(SUBNOMBRE),
        SUMARIO=sumario, SECCIONES=lista_sec)
    open(os.path.join(EDIT, "index.html"), "w", encoding="utf-8").write(html)

    print("OK  ediciones/01  -> %d artículo(s) + %d sección(es) + portada" %
          (len(articulos), len(secciones)))


if __name__ == "__main__":
    main()
'''

open(TARGET, "w", encoding="utf-8").write(cabecera + MAIN)
print("== reescrito: %d líneas (199 intactas + main nuevo) ==" %
      len(cabecera.splitlines()) + len(MAIN.splitlines()))

r = subprocess.run([sys.executable, TARGET], cwd=BASE, capture_output=True,
                   text=True, encoding="utf-8", errors="replace", timeout=180)
print("== rc=%s ==" % r.returncode)
print((r.stdout or r.stderr).strip()[:900])
