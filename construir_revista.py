# -*- coding: utf-8 -*-
"""construir_revista.py — Generador del sitio de "Rural".

Lee datos/ediciones.json (canon), copia las fotos verbatim desde
enviar_aqui/imagenes_odt/<carpeta>/ y emite el sitio estático multi-página
en revista/ediciones/01/  (index + secciones + articulos).

Formato del cuerpo: bloques JSON  {t:"p"|"h3"|"cita"|"dato", v:"..."}.
"""
import os, shutil, json, html as H

BASE = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(BASE, "datos", "ediciones.json")
ODT = os.path.abspath(os.path.join(BASE, "..", "enviar_aqui", "imagenes_odt"))
EDIT = os.path.join(BASE, "ediciones", "01")
IMGDIR = os.path.join(EDIT, "imagenes")

REV = "Rural"
SUBNOMBRE = "Revista digital de la ESRN Rural Virtual"

# carpetas fuente reales por id de artículo (el JSON usa ids con tilde)
ODT_POR_ID = {
    "el-chip-en-la-cancha": "clase_9_art_culo_para_la_revista_milton_",
    "la-primera-ley-de-newton": "la_ley_de_la_incercia",
    "el-partido-por-el-ambiente": "el_partido_por_el_ambiente",
    "la-fiesta-del-paraje-treneta": "fiestas_y_tradiciones_mundialistas",
    "próxima-parada-atractivos-mundialistas": "pr_xima_parada__atractivos_mundialistas_",
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,600;0,700;0,800;1,400&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&amp;display=swap" rel="stylesheet">')


def esc(t):
    return H.escape((t or "").strip(), quote=True)


def copiar_imagenes(uid, odt=None):
    """Copia las fotos de la carpeta fuente a ediciones/01/imagenes/<uid>/."""
    src = os.path.join(ODT, odt or ODT_POR_ID.get(uid, uid))
    dst = os.path.join(IMGDIR, uid)
    imgs = []
    if os.path.isdir(src):
        os.makedirs(dst, exist_ok=True)
        for f in sorted(os.listdir(src)):
            ext = os.path.splitext(f)[1].lower()
            if ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
                nombre = "foto-%02d%s" % (len(imgs) + 1, ext)
                try:
                    shutil.copy2(os.path.join(src, f), os.path.join(dst, nombre))
                    imgs.append("../imagenes/%s/%s" % (uid, nombre))
                except OSError:
                    pass
    return imgs


def render_cuerpo(art):
    """Convierte los bloques {t,v} del cuerpo + fotos/epígrafes en HTML."""
    cuerpo_html = []
    cuerpo = art.get("cuerpo") or []
    for b in cuerpo:
        t, v = b.get("t"), b.get("v", "")
        if t == "h3":
            cuerpo_html.append("<h3 class='txt-titulo'>%s</h3>" % esc(v))
        elif t == "cita":
            cuerpo_html.append("<blockquote class='txt-cita'><p>%s</p></blockquote>" % esc(v))
        elif t == "dato":
            cuerpo_html.append("<p class='txt-dato'><strong>%s</strong></p>" % esc(v))
        else:
            cuerpo_html.append("<p class='txt-parrafo'>%s</p>" % esc(v))
    fotos = art.get("fotos") or copiar_imagenes(art["id"], art.get("odt"))
    epigs = art.get("epigrafes") or []
    if fotos and cuerpo_html:
        primera = '<figure class="fig fig--g8"><img src="%s" alt="" loading="lazy" decoding="async"><figcaption>%s</figcaption></figure>' % (
            fotos[0], esc(epigs[0] if epigs else ""))
        cuerpo_html.insert(1, primera)
        rest = fotos[1:]
    else:
        rest = []
    for i, f in enumerate(rest):
        ep = esc(epigs[i + 1] if len(epigs) > i + 1 else "")
        cuerpo_html.append('<figure class="fig fig--g8"><img src="%s" alt="" loading="lazy" decoding="async"><figcaption>%s</figcaption></figure>' % (f, ep))
    return "".join(cuerpo_html)


def pagina(titulo, bajada, ed, nav, body, pie_note, cssdir, faviq):
    css = '<link rel="stylesheet" href="%srevista.css">' % cssdir
    return ('<!doctype html>\n<html lang="es" dir="ltr">\n<head>\n'
            '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            "<title>%s · %s</title>\n<meta name=\"description\" content=\"%s\">\n"
            "<link rel=\"icon\" href=\"%s\" type=\"image/svg+xml\">\n%s\n%s\n</head>\n<body>\n"
            '<a class="salto" href="#contenido">Salto al contenido</a>\n'
            '<header class="masthead contenedor" role="banner">\n  <p class="masthead__marca"><a href="%s">%s</a></p>\n'
            '  <nav aria-label="Secciones" class="nav-ed">%s</nav>\n</header>\n'
            '<main id="contenido" class="contenedor">\n%s\n</main>\n'
            '<footer class="pie" role="contentinfo">\n  <div class="pie__interior contenedor">\n'
            '    <p class="pie__credito">%s · %s · %s. Escrita, ilustrada y fotografiada por estudiantes de la ESRN Rural Virtual.</p>\n'
            '  </div>\n</footer>\n</body>\n</html>\n') % (
        esc(titulo), esc(REV), esc(bajada), faviq, FONTS, css, pie_note,
        esc(REV), nav, body, esc(REV), esc(SUBNOMBRE), esc(ed))


def main():
    datos = json.load(open(DATOS, encoding="utf-8"))
    ed = datos["edicion"]
    ed_etiqueta = ed.get("edicion_etiqueta") or ("Edición N.º %s — %s" % (ed.get("numero"), ed.get("fecha")))
    secciones = datos.get("secciones") or []
    articulos = datos.get("articulos") or []

    for d in ("secciones", "articulos", "imagenes"):
        os.makedirs(os.path.join(EDIT, d), exist_ok=True)

    def nav_html(pre=""):
        lis = "".join("<li><a href='%ssecciones/%s.html'>%s</a></li>" %
                      (pre, s["id"], esc(s["titulo"])) for s in secciones)
        return "<ul class='nav-ed__lista'>%s</ul>" % lis

    art_por_sec = {}
    for a in articulos:
        art_por_sec.setdefault(a.get("seccion", "voces"), []).append(a)

    # ---- artículos -----------------------------------------------------
    for art in articulos:
        sec = next((s for s in secciones if s["id"] == art.get("seccion")), None)
        sec_nom = sec["titulo"] if sec else "Voces"
        cuerpo = render_cuerpo(art)
        sec_url = "../secciones/%s.html" % sec["id"] if sec else "../index.html"
        body = ('<article class="articulo grid-12" itemscope itemtype="https://schema.org/Article">\n'
                '<header class="articulo__cabeza grid-12">\n'
                '<p class="articulo__sec">%s</p>\n'
                '<h1 itemprop="headline" class="articulo__h1">%s</h1>\n'
                '<p class="articulo__bajada">%s</p>\n'
                '<p class="articulo__meta"><span itemprop="author">%s</span> · <time datetime="%s">%s</time>'
                ' · <a href="%s">%s</a></p>\n</header>\n'
                '<div class="articulo__cuerpo" itemprop="articleBody">\n%s\n</div>\n'
                '<footer class="articulo__fin"><p><a class="volver" href="%s">← Volver a %s</a></p></footer>\n'
                '</article>') % (
            esc(sec_nom.upper()), esc(art.get("titulo", art["id"])), esc(art.get("bajada", "")),
            esc(art.get("autor", "Estudiantes")), esc(art.get("fecha_iso", "2026-09-01")),
            esc(art.get("fecha", ed_etiqueta)), sec_url, esc(sec_nom), cuerpo, sec_url, esc(sec_nom))
        open(os.path.join(EDIT, "articulos", art["id"] + ".html"), "w", encoding="utf-8").write(
            pagina(art.get("titulo", art["id"]), art.get("bajada", ""), ed_etiqueta,
                   nav_html("../"), body, "../index.html", "../../../css/", "../../../favicon.svg"))

    # ---- secciones -----------------------------------------------------
    for i, s in enumerate(secciones):
        cards = "".join(
            "<article class='art_card grid-6'><h3><a href='%s'>%s</a></h3><p>%s</p></article>" % (
                "../articulos/%s.html" % a["id"], esc(a.get("titulo", a["id"])), esc(a.get("bajada", "")))
            for a in art_por_sec.get(s["id"], []))
        if not cards:
            cards = "<p class='txt-parrafo'>Sección en construcción: sumá tu artículo.</p>"
        body = ('<header class="sec-portada" aria-labelledby="seccion-titulo">\n'
                '<p class="sec-portada__num">%s / %s</p>\n<h1 id="seccion-titulo" class="sec-portada__h1">%s</h1>\n'
                '<p class="sec-portada__descrip">%s</p>\n</header>\n'
                '<div class="sec-listado grid-12" aria-label="%s">\n%s\n</div>'
                % ("%02d" % (i + 1), "%02d" % len(secciones), esc(s["titulo"]),
                   esc(s.get("bajada", "")), esc(s["titulo"]), cards))
        open(os.path.join(EDIT, "secciones", s["id"] + ".html"), "w", encoding="utf-8").write(
            pagina("Rural · %s" % s["titulo"], s.get("bajada", ""), ed_etiqueta,
                   nav_html("../"), body, "../index.html", "../../../css/", "../../../favicon.svg"))

    # ---- portada de la edición ------------------------------------------
    sumario = "".join(
        "<li class='sumario__item'><span class='sumario__num'>%s</span>"
        "<span class='sumario__sec'>%s</span>"
        "<a class='sumario__art' href='secciones/%s.html'>%s</a></li>"
        % ("%02d" % (i + 1), esc(s["titulo"]), s["id"], esc(s["titulo"]))
        for i, s in enumerate(secciones))
    sec_cards = "".join(
        "<article class='sec_card grid-12'><h3 class='sec_card__titulo'>"
        "<a href='secciones/%s.html'>%s</a></h3>"
        "<p class='sec_card__bajada'>%s</p></article>" %
        (s["id"], esc(s["titulo"]), esc(s.get("bajada", "")))
        for s in secciones)
    body = ('<section class="portada" aria-labelledby="portada-titulo">\n'
            '<p class="portada__sec">%s</p>\n'
            '<h1 id="portada-titulo" class="portada__h1">%s</h1>\n'
            '<p class="portada__bajada">%s</p>\n</section>\n'
            '<nav class="sumario" aria-label="Sumario">\n'
            '<p class="sumario__cabecera">Sumario · %s</p>\n<ul class="sumario__lista">\n%s\n</ul>\n</nav>\n'
            '<section class="secciones" aria-label="Secciones">\n'
            '<h2 class="secciones__titulo">Secciones</h2>\n<div class="secciones__lista grid-12">\n%s\n</div>\n</section>'
            % (esc(ed_etiqueta), esc(REV), esc(SUBNOMBRE), esc(ed_etiqueta), sumario, sec_cards))
    open(os.path.join(EDIT, "index.html"), "w", encoding="utf-8").write(
        pagina("Rural · %s" % ed_etiqueta, SUBNOMBRE, ed_etiqueta, nav_html(""),
               body, "index.html", "../../css/", "../../favicon.svg"))

    print("OK ediciones/01 -> %d artículos + %d secciones + portada" % (len(articulos), len(secciones)))


if __name__ == "__main__":
    main()