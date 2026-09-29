# -*- coding: utf-8 -*-
"""construir_revista_v2.py — Generador con estructura: cada artículo en su carpeta."""
import os, shutil, json, html as H, re

BASE = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(BASE, "datos", "ediciones.json")
ODT = os.path.abspath(os.path.join(BASE, "..", "enviar_aqui", "imagenes_odt"))
EDIT = os.path.join(BASE, "ediciones", "01")

REV = "La Revista del Rural"
SUBNOMBRE = "Revista digital de la ESRN Rural Virtual"

ODT_POR_ID = {
    "el-chip-en-la-cancha": "clase_9_art_culo_para_la_revista_milton_",
    "la-primera-ley-de-newton": "la_ley_de_la_incercia",
    "el-partido-por-el-ambiente": "el_partido_por_el_ambiente",
    "la-fiesta-del-paraje-treneta": "fiestas_y_tradiciones_mundialistas",
    "próxima-parada-atractivos-mundialistas": "pr_xima_parada__atractivos_mundialistas_",
}

# ---- Egresadas y egresados de la promoción 2026 --------------------------
# Tuplas: (apellido, nombre, orientación, sede). Todas las personas cursaron
# 5.º año, ciclo orientado en Ciencias Naturales o en Turismo.
EGRESADOS = [
    ("Cañumil", "Milagros Alejandra", "Ciencias Naturales", "Aguada Cecilio"),
    ("Contrera", "Sol Antonella", "Ciencias Naturales", "Aguada Cecilio"),
    ("Catalán", "Rocío Noemí", "Ciencias Naturales", "Aguada de Guerra"),
    ("Echegoy", "Marcos Agustín", "Ciencias Naturales", "Aguada de Guerra"),
    ("Pintos", "Yaqueline Mayra", "Ciencias Naturales", "Aguada de Guerra"),
    ("Vera", "Matías Alejandro", "Ciencias Naturales", "Aguada de Guerra"),
    ("Zapata", "Daiana", "Turismo", "Aguada Guzmán"),
    ("Cayul", "Cristian Nahuel", "Ciencias Naturales", "Arroyo los Berros"),
    ("Criban", "Agustín", "Ciencias Naturales", "Cerro Policía"),
    ("Faría", "Lázaro", "Ciencias Naturales", "Cerro Policía"),
    ("Andres Martiarena", "Milagros", "Ciencias Naturales", "Cerro Policía"),
    ("Pelliza", "Keila", "Ciencias Naturales", "Cerro Policía"),
    ("Pelliza", "Lucila", "Ciencias Naturales", "Cerro Policía"),
    ("López Amacio", "Cecilia Marilí", "Ciencias Naturales", "Colan Conhué"),
    ("Cañehuán", "Alexis Isaías", "Ciencias Naturales", "Comicó"),
    ("Vergara Mayer", "Fautino Manuel", "Turismo", "Corralito"),
    ("Llancafil", "Dalma Yanina", "Ciencias Naturales", "El Caín"),
    ("Lleiful", "Denis Nahuel", "Ciencias Naturales", "El Caín"),
    ("Florentino", "Martín Ignacio", "Ciencias Naturales", "El Cóndor"),
    ("Aguirre", "Agustina De Jesús", "Ciencias Naturales", "El Cóndor"),
    ("Vargas", "Ariana Joselin", "Ciencias Naturales", "El Cóndor"),
    ("Fernández", "Luz", "Turismo", "El Cóndor"),
    ("Monsalve", "Mateo Valentín", "Turismo", "El Cóndor"),
    ("Romero", "Cristian Tomás", "Turismo", "El Cóndor"),
    ("Deluchi", "Sofía", "Turismo", "El Cóndor"),
    ("García", "Sofía", "Turismo", "El Cóndor"),
    ("Miranda Rodríguez", "Jeremías Leonardo", "Turismo", "El Manso"),
    ("Monsalbe", "Leonel Uriel", "Turismo", "El Manso"),
    ("Ulloa", "Sol Antonella", "Turismo", "El Manso"),
    ("Soria", "Mario Enrique", "Turismo", "El Manso"),
    ("Paredes", "Luzmila Jazzmín Andrea", "Turismo", "Lago Pellegrini"),
    ("Rubilar", "Lautaro Gabriel", "Turismo", "Lago Pellegrini"),
    ("Aravena", "Alexis Joaquín", "Turismo", "Lago Pellegrini"),
    ("Aravena", "Sahiara Ayelén", "Turismo", "Lago Pellegrini"),
    ("Gueladi", "Benjamín Daniel", "Turismo", "Lago Pellegrini"),
    ("Iriarte Condori", "Brenda Gisella", "Turismo", "Lago Pellegrini"),
    ("Sarmiento", "Lara Macarena", "Turismo", "Lago Pellegrini"),
    ("Moreira", "Alejandro David", "Turismo", "Lago Pellegrini"),
    ("Cabezas", "Antonella Esther", "Ciencias Naturales", "Lago Pellegrini"),
    ("Lagos", "Jonás Daniel", "Ciencias Naturales", "Lago Pellegrini"),
    ("Medrano", "Catalina Antonella", "Ciencias Naturales", "Lago Pellegrini"),
    ("Muñoz Guerrero", "Daira Sarai", "Ciencias Naturales", "Lago Pellegrini"),
    ("Nuñez", "Sofía Abigaíl", "Ciencias Naturales", "Lago Pellegrini"),
    ("Pardo", "Jeremías Samuel", "Ciencias Naturales", "Lago Pellegrini"),
    ("Pardo", "José Antonio", "Ciencias Naturales", "Lago Pellegrini"),
    ("Pablo", "Dylan Aaron", "Ciencias Naturales", "Lago Pellegrini"),
    ("Zúñiga Olave", "Bautista Alejandro", "Ciencias Naturales", "Lago Pellegrini"),
    ("Morel", "Tobías", "Ciencias Naturales", "Lago Pellegrini"),
    ("Varnes", "Selene Mery", "Ciencias Naturales", "Laguna Blanca"),
    ("Maliqueo", "Alexander Leonel", "Ciencias Naturales", "Laguna Blanca"),
    ("Montecinos", "Yordan Cleofás", "Ciencias Naturales", "Laguna Blanca"),
    ("Lincopan", "Abigail Rocío", "Ciencias Naturales", "Mencué"),
    ("Montre Arias", "Ludmila Agostina", "Ciencias Naturales", "Mencué"),
    ("Ñanco", "Isaías Daniel Atahualpa", "Turismo", "Mencué"),
    ("Calle Torrez", "Zaida Camila", "Ciencias Naturales", "Peñas Blancas"),
    ("Gauna", "Fernando", "Ciencias Naturales", "Peñas Blancas"),
    ("Lebeau", "José Luis", "Ciencias Naturales", "Rincón Treneta"),
    ("Cahuimpan", "Milagros Noemí", "Ciencias Naturales", "Río Chico"),
    ("Osuna", "Gonzalo Ezequiel", "Ciencias Naturales", "Río Chico"),
    ("Mancilla", "Kiara Yael", "Ciencias Naturales", "Valle Verde"),
    ("Godoy", "Lautaro Elías", "Ciencias Naturales", "Valle Verde"),
    ("Paillalef Parra", "Benjamín Gonzalo", "Turismo", "Villa Llanquín"),
    ("Calluhuequi", "Enzo Leonel", "Ciencias Naturales", "Yaminué"),
    ("Quichan", "Carlos Lisandro", "Ciencias Naturales", "Yaminué"),
    ("Quichan", "Lautaro Ismael", "Ciencias Naturales", "Yaminué"),
    ("Yanca Pazos", "Milena Ludmila", "Turismo", "Cona Niyeu"),
]


def egresados_body():
    """Cuerpo de la página Egresados: saludo + tarjetas por sede."""
    total = len(EGRESADOS)
    por_sede = {}
    for apellido, nombre, orient, sede in EGRESADOS:
        por_sede.setdefault(sede, []).append((apellido, nombre, orient))
    tarjetas = []
    for sede in sorted(por_sede, key=str.lower):
        items = "".join(
            "<li><strong>%s</strong>, %s <span class='egr__or'>%s</span></li>"
            % (esc(apellido), esc(nombre), esc(orient))
            for apellido, nombre, orient
            in sorted(por_sede[sede], key=lambda r: (r[1].lower(), r[0].lower())))
        tarjetas.append(
            "<article class='tarjeta'><h3 class='tarjeta__t'>%s</h3>"
            "<ul class='egr__lista'>%s</ul></article>" % (esc(sede), items))
    intro = ("¡Felicitaciones a toda nuestra hermosa promoción! Este año, "
             "<strong>%d estudiantes</strong> de 5.º año de la ESRN Rural Virtual "
             "cerraron su Ciclo Orientado — en Ciencias Naturales o en Turismo — "
             "desde cada rincón de la provincia. Los y las reunimos sede por sede, "
             "para decirles bien fuerte: ¡estamos muy orgullosos de ustedes!"
             % total)
    return ('<div class="pres__bloque">\n'
            '<h2 class="pres__h2">Egresadas y egresados 2026</h2>\n'
            '<p class="pres__p pres__ancho">%s</p>\n'
            '<div class="egr__tarjetas">\n%s\n</div>\n</div>') % (intro, "".join(tarjetas))


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,600;0,700;0,800;1,400&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&amp;display=swap" rel="stylesheet">')


def esc(t):
    return H.escape((t or "").strip(), quote=True)


# **negrita** en medio del texto. Se escapa primero, asi que las etiquetas del
# dato no pueden colarse. El asterisco es la unica marca admitida.
RE_NEGRITA = re.compile(r"\*\*(.+?)\*\*", re.S)


def md(t):
    """Escapa y convierte **negrita** en <strong>."""
    return RE_NEGRITA.sub(r"<strong>\1</strong>", esc(t))


def md_plano(t):
    """Como md(), pero para metaetiquetas: sin HTML."""
    return RE_NEGRITA.sub(r"\1", (t or "").strip())


def copiar_imagenes_a_carpeta(uid, dst_dir, odt=None):
    """Copia fotos de la fuente al directorio del artículo."""
    src = os.path.join(ODT, odt or ODT_POR_ID.get(uid, uid))
    imgs = []
    if os.path.isdir(src):
        for f in sorted(os.listdir(src)):
            ext = os.path.splitext(f)[1].lower()
            if ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
                nombre = "foto-%02d%s" % (len(imgs) + 1, ext)
                try:
                    shutil.copy2(os.path.join(src, f), os.path.join(dst_dir, nombre))
                    imgs.append(nombre)
                except OSError:
                    pass
    return imgs


RE_PDF_MARCA = re.compile(r"^\s*pdf\s*\+\s*\d+\s*$", re.I)
# Encabezado de un apendice que describe el material visual (afiches, fotos,
# registros). No es articulo: se corta todo lo que viene desde ahi.
RE_APENDICE_VISUAL = re.compile(
    r"(adjunt|registro\s+visual|material\s+visual|frases\s+y\s+afiches|registros\s+visuales)",
    re.I)


def render_cuerpo(art, fotos_paths):
    """Convierte bloques + fotos a HTML. fotos_paths son relativos al article folder."""
    cuerpo_html = []
    cuerpo = art.get("cuerpo") or []
    en_lista = None
    i = 0
    # Los bloques 'fig' colocan la siguiente foto de fotos_paths en una
    # posicion exacta del texto. Las fotos asi consumidas se excluyen del
    # reparto automatico de abajo, para no duplicar figuras.
    consumidas = set()

    def _fig(src, ep, clase="fig--g8"):
        return ('<figure class="fig %s"><img src="%s" alt="" loading="lazy" decoding="async">'
                '<figcaption>%s</figcaption></figure>') % (clase, src, ep)

    def _ep(i):
        return esc(epigs[i] if len(epigs) > i else "")

    epigs = art.get("epigrafes") or []
    fig_index = 0
    while i < len(cuerpo):
        b = cuerpo[i]
        t, v = b.get("t"), b.get("v", "")
        # 'tarjeta' -> rotulo + texto corto. Lo que se lee mejor en grilla
        # que como titulo+parrafo. Las consecutivas se agrupan.
        if t == "tarjeta":
            if en_lista:
                cuerpo_html.append("</%s>" % ("ul" if en_lista == "li" else "ol"))
                en_lista = None
            grupo = []
            while i < len(cuerpo) and cuerpo[i].get("t") == "tarjeta":
                grupo.append(cuerpo[i])
                i += 1
            tarjetas = "".join(
                '<article class="tarjeta"><h3 class="tarjeta__t">%s</h3><p class="tarjeta__p">%s</p></article>'
                % (md(g.get("titulo") or g.get("v") or ""), md(g.get("texto") or ""))
                for g in grupo)
            cuerpo_html.append('<div class="tarjetas">%s</div>' % tarjetas)
            continue
        i += 1
        # "PDF+ 1", "PDF+ 2"..." son anotaciones de los alumnos para señalar
        # "aca va la imagen de esa pagina del PDF". No son titulos ni texto:
        # se descartan. Las fotos se muestran aparte, en la galeria.
        if RE_PDF_MARCA.match(v or ""):
            continue
        # Apendice de material visual ("... Adjuntos:", "Registro Visual"):
        # se corta el articulo, porque lo que sigue son descripciones de
        # fotos y afiches, no texto del trabajo.
        if len(v or "") < 120 and RE_APENDICE_VISUAL.search(v or ""):
            break
        # 'li' -> <ul> con vineta ; 'ol' -> <ol> numerada. Los bloques
        # consecutivos del mismo tipo se agrupan en una sola lista.
        # Ojo: el tipo de bloque NO es el nombre de la etiqueta.
        if t == "fig":
            # Figura en posicion exacta dentro del texto: consume la
            # proxima foto de fotos_paths en orden.
            if fig_index < len(fotos_paths):
                cuerpo_html.append(_fig(fotos_paths[fig_index], _ep(fig_index)))
                consumidas.add(fig_index)
                fig_index += 1
            continue
        if t in ("li", "ol"):
            tag = "ul" if t == "li" else "ol"
            if en_lista != t:
                if en_lista:
                    cuerpo_html.append("</%s>" % ("ul" if en_lista == "li" else "ol"))
                cuerpo_html.append("<%s class='txt-lista'>" % tag)
                en_lista = t
            # 'b' opcional: texto en negrita al inicio del item ("Campañas de
            # concientización: informar y Patience...").
            lead = b.get("b")
            if lead:
                cuerpo_html.append("<li><strong>%s</strong> %s</li>" % (md(lead), md(v)))
            else:
                cuerpo_html.append("<li>%s</li>" % md(v))
            continue
        if en_lista:
            cuerpo_html.append("</%s>" % ("ul" if en_lista == "li" else "ol"))
            en_lista = None
        if t == "h3":
            cuerpo_html.append("<h3 class='txt-titulo'>%s</h3>" % md(v))
        elif t == "pregunta":
            # Pregunta de apertura: un poco mas de peso que un parrafo normal,
            # sin VOLVER a ser un bloquequote.
            cuerpo_html.append("<p class='txt-pregunta'>%s</p>" % md(v))
        elif t == "h4":
            # Subtitulo dentro de una seccion: para los items rotulados de
            # un bloque con encabezado ("Ejes principales", "Propuestas"...).
            cuerpo_html.append("<h4 class='txt-subtitulo'>%s</h4>" % md(v))
        elif t == "cita":
            cuerpo_html.append("<blockquote class='txt-cita'><p>%s</p></blockquote>" % md(v))
        elif t == "dato":
            cuerpo_html.append("<p class='txt-dato'><strong>%s</strong></p>" % md(v))
        elif t == "firma":
            # Firma de autor al pie de una seccion. Se usa cuando un mismo
            # articulo reune varias firmas (trabajo grupal por secciones).
            cuerpo_html.append("<p class='txt-firma'>%s</p>" % md(v))
        elif t == "video":
            # Video de Google Drive: se muestra con el reproductor de vista
            # previa (link /file/d/ID/view... -> /file/d/ID/preview).
            mid = v.replace("https://drive.google.com/file/d/", "").replace("http://drive.google.com/file/d/", "")
            mid = mid.split("/")[0] if "/" in mid else mid.split("?")[0] if "?" in mid else mid
            src = "https://drive.google.com/file/d/%s/preview" % mid
            cuerpo_html.append('<div class="video"><iframe src="%s" allow="autoplay" allowfullscreen loading="lazy" title="Video del experimento"></iframe></div>' % esc(src))
        else:
            cuerpo_html.append("<p class='txt-parrafo'>%s</p>" % md(v))
    if en_lista:
        cuerpo_html.append("</%s>" % ("ul" if en_lista == "li" else "ol"))
    epigs = art.get("epigrafes") or []
    # Disposicion opcional, una por foto: "portada" (arriba, grande),
    # "seccion" (corte de seccion) o "inline" (chica, dentro del texto).
    disp = art.get("fotos_disposicion") or []

    def _fig(src, ep, clase="fig--g8"):
        return ('<figure class="fig %s"><img src="%s" alt="" loading="lazy" decoding="async">'
                '<figcaption>%s</figcaption></figure>') % (clase, src, ep)

    def _ep(i):
        return esc(epigs[i] if len(epigs) > i else "")

    if not fotos_paths:
        vacio = '<div class="fig--vacio" aria-hidden="true"></div>'
        cuerpo_html.insert(min(1, len(cuerpo_html)), vacio)
        return "".join(cuerpo_html)

    def _cortes(prefijo):
        return [j for j, h in enumerate(cuerpo_html) if h.startswith(prefijo)]

    if len(disp) == len(fotos_paths):
        # Una foto por corte de seccion, en orden. Lo que sobra no se apila en
        # el ultimo h3: se va a la grilla del pie, a la par. El indice 0 se
        # descarta porque pondria la foto por encima del primer titulo.
        cortes = [j for j in _cortes("<h3") if j > 0]
        # Una foto por corte, pero nunca pegada a la anterior: el corte 0 es el
        # que cae junto a la portada, asi que se respeta la distancia minima.
        libres = [j for j in cortes if j > 1]
        galeria, colocar = [], []
        seccion_n = 0
        for i, f in enumerate(fotos_paths):
            if i in consumidas:
                continue
            d = disp[i]
            if d == "portada":
                colocar.append((0, _fig(f, _ep(i), "fig--portada"), True))
            elif d == "galeria":
                galeria.append(_fig(f, _ep(i), "fig--par"))
            elif d == "final":
                cuerpo_html.append(_fig(f, _ep(i)))
            elif d == "inline":
                objetivo = round((i + 1) * len(cuerpo_html) / (len(fotos_paths) + 1))
                anclas = _cortes("<p ") or list(range(len(cuerpo_html)))
                colocar.append((min(anclas, key=lambda j: abs(j - objetivo)),
                                _fig(f, _ep(i), "fig--inline"), False))
            elif d == "seccion-m" and seccion_n < len(libres):
                colocar.append((libres[seccion_n], _fig(f, _ep(i), "fig--mediana"), False))
                seccion_n += 1
            elif d == "seccion-m":
                cuerpo_html.append(_fig(f, _ep(i), "fig--mediana"))
            elif seccion_n < len(libres):
                colocar.append((libres[seccion_n], _fig(f, _ep(i)), False))
                seccion_n += 1
            else:
                galeria.append(_fig(f, _ep(i), "fig--par"))
        # De atras hacia adelante: al insertar en orden, cada figura correria
        # los indices de las que faltan y el reparto se desarma.
        for pos, html, al_frente in sorted(colocar, key=lambda x: x[0], reverse=not any(c[2] for c in colocar)):
            if al_frente:
                cuerpo_html.insert(0, html)
            else:
                cuerpo_html.insert(pos, html)
        if galeria:
            cuerpo_html.append('<div class="figs-par">%s</div>' % "".join(galeria))
        return "".join(cuerpo_html)

    # Sin disposicion explicita: la primera abre despues de la introduccion y
    # las demas, una por corte de seccion. El excedente va a la grilla del pie.
    if 0 not in consumidas:
        cuerpo_html.insert(1, _fig(fotos_paths[0], _ep(0)))
    # >2 y no >1: la primera foto ya esta en el indice 1, asi que un corte en
    # el 2 dejaría las dos pegadas. Entre foto y foto tiene que haber texto.
    cortes = [j for j in _cortes("<h3") if j > 2]
    colocar, galeria = [], []
    k = 1
    for f in fotos_paths[1:]:
        if k in consumidas:
            k += 1
            continue
        n = k - 1
        if n < len(cortes):
            colocar.append((cortes[n], _fig(f, _ep(k))))
        else:
            galeria.append(_fig(f, _ep(k), "fig--par"))
        k += 1
    for pos, html in sorted(colocar, key=lambda x: -x[0]):
        cuerpo_html.insert(pos, html)
    if galeria:
        cuerpo_html.append('<div class="figs-par">%s</div>' % "".join(galeria))
    return "".join(cuerpo_html)


def pagina(titulo, bajada, ed, nav, body, pie_note, cssdir, faviq, sec_id=None):
    css = '<link rel="stylesheet" href="%srevista.css">' % cssdir
    body_class = ' class="sec-%s"' % sec_id if sec_id else ''
    return ('<!doctype html>\n<html lang="es" dir="ltr">\n<head>\n'
            '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            "<title>%s · %s</title>\n<meta name=\"description\" content=\"%s\">\n"
            "<link rel=\"icon\" href=\"%s\" type=\"image/svg+xml\">\n%s\n%s\n</head>\n<body%s>\n"
            '<a class="salto" href="#contenido">Salto al contenido</a>\n'
            '<header class="masthead contenedor" role="banner">\n  <p class="masthead__marca"><a href="%s">%s</a></p>\n'
            '  <nav aria-label="Secciones" class="nav-ed">%s</nav>\n</header>\n'
            '<main id="contenido" class="contenedor">\n%s\n</main>\n'
            '<footer class="pie" role="contentinfo">\n  <div class="pie__interior contenedor">\n'
            '    <p class="pie__credito">%s · %s · %s. Escrita, ilustrada y fotografiada por estudiantes de la ESRN Rural Virtual.</p>\n'
            '  </div>\n</footer>\n</body>\n</html>\n') % (
        md(titulo), esc(REV), md_plano(bajada), faviq, FONTS, css, body_class, pie_note,
        esc(REV), nav, body, esc(REV), esc(SUBNOMBRE), esc(ed))


def main():
    datos = json.load(open(DATOS, encoding="utf-8"))
    ed = datos["edicion"]
    ed_etiqueta = ed.get("edicion_etiqueta") or ("Edición N.º %s — %s" % (ed.get("numero"), ed.get("fecha")))
    secciones = datos.get("secciones") or []
    articulos = datos.get("articulos") or []

    os.makedirs(EDIT, exist_ok=True)

    def nav_html(pre=""):
        pre_link = "<li><a href='%spresentacion.html' data-sec='presentacion'>Presentación</a></li>" % pre
        lis = "".join("<li><a href='%ssecciones/%s.html' data-sec='%s'>%s</a></li>" %
                      (pre, s["id"], s["id"], esc(s["titulo"])) for s in secciones)
        egr = "<li><a href='%segresados.html' data-sec='egresados'>Egresados</a></li>" % pre
        return "<ul class='nav-ed__lista'>%s%s%s</ul>" % (pre_link, lis, egr)

    art_por_sec = {}
    for a in articulos:
        art_por_sec.setdefault(a.get("seccion", "voces"), []).append(a)

    # ---- artículos (cada uno en su carpeta) ------------------------------
    for art in articulos:
        uid = art["id"]
        art_dir = os.path.join(EDIT, uid)
        os.makedirs(art_dir, exist_ok=True)

        # Copiar fotos a la carpeta del artículo
        fotos_en_json = art.get("fotos", [])
        if fotos_en_json:
            # Las fotos vienen del JSON con paths como ../imagenes/uid/foto-01.png
            # Copiamos los archivos reales a la carpeta del artículo
            imgs_dst = []
            for i, fpath in enumerate(fotos_en_json, 1):
                # Buscar el archivo original
                src_file = None
                if fpath.startswith("../imagenes/"):
                    src_file = os.path.join(EDIT, "imagenes", uid, os.path.basename(fpath))
                elif fpath.startswith("imagenes/"):
                    src_file = os.path.join(EDIT, fpath)
                if src_file and os.path.isfile(src_file):
                    ext = os.path.splitext(src_file)[1]
                    nombre = "foto-%02d%s" % (i, ext)
                    shutil.copy2(src_file, os.path.join(art_dir, nombre))
                    imgs_dst.append(nombre)
                else:
                    # Si no existe, intentar con el nombre original
                    nombre = os.path.basename(fpath)
                    imgs_dst.append(nombre)
            fotos_relativas = imgs_dst
        else:
            # Copiar desde ODT
            imgs = copiar_imagenes_a_carpeta(uid, art_dir, art.get("odt"))
            fotos_relativas = imgs

        sec = next((s for s in secciones if s["id"] == art.get("seccion")), None)
        sec_nom = sec["titulo"] if sec else "Voces"
        cuerpo = render_cuerpo(art, fotos_relativas)

        # Paths relativos: desde ediciones/01/<articulo>/ hasta ediciones/01/
        sec_url = "../secciones/%s.html" % sec["id"] if sec else "../index.html"

        # Byline: autor + sede + tutora (solo si constan) + fecha + seccion.
        # Se arman por partes para que falte lo que falte sin dejar
        # separadores sueltos ni textos de relleno.
        def _dato(clave, etiqueta, prop=""):
            v = (art.get(clave) or "").strip().strip("-·:")
            if not v:
                return ""
            at = ' itemprop="%s"' % prop if prop else ""
            return '<span class="articulo__dato"%s><b>%s</b> %s</span>' % (at, etiqueta, esc(v))

        partes = [_dato("autor", "Por", "author"),
                  _dato("sede", "Sede:", "location"),
                  _dato("tutora", "Tutora:"),
                  '<time datetime="%s">%s</time>' % (esc(art.get("fecha_iso", "2026-09-01")),
                                                     esc(art.get("fecha", ed_etiqueta))),
                  '<a href="%s">%s</a>' % (sec_url, esc(sec_nom))]
        meta = ' · '.join(p for p in partes if p)

        body = ('<article class="articulo grid-12" itemscope itemtype="https://schema.org/Article">\n'
                '<header class="articulo__cabeza grid-12">\n'
                '<p class="articulo__sec">%s</p>\n'
                '<h1 itemprop="headline" class="articulo__h1">%s</h1>\n'
                '<p class="articulo__bajada">%s</p>\n'
                '<p class="articulo__meta">%s</p>\n</header>\n'
                '<div class="articulo__cuerpo" itemprop="articleBody">\n%s\n</div>\n'
                '<footer class="articulo__fin"><p><a class="volver" href="%s">← Volver a %s</a></p></footer>\n'
                '</article>') % (
            esc(sec_nom.upper()), md(art.get("titulo", uid)), md(art.get("bajada", "")),
            meta, cuerpo, sec_url, esc(sec_nom))

        # HTML del artículo: ediciones/01/<articulo>/index.html
        open(os.path.join(art_dir, "index.html"), "w", encoding="utf-8").write(
            pagina(art.get("titulo", uid), art.get("bajada", ""), ed_etiqueta,
                   nav_html("../"), body, "../index.html", "../css/", "../favicon.svg"))

    # ---- secciones -------------------------------------------------------
    for i, s in enumerate(secciones):
        cards = []
        for a in art_por_sec.get(s["id"], []):
            # Buscar primera foto del artículo
            fotos = a.get("fotos", [])
            foto_html = ""
            if fotos:
                foto_html = "<img src='../%s/%s' alt='' class='art_card__img'>" % (a["id"], fotos[0])
            else:
                foto_html = "<div class='art_card__img art_card__img--vacio' aria-hidden='true'></div>"
            
            cards.append(
                "<article class='art_card grid-6' data-sec='%s'>"
                "%s"
                "<div class='art_card__contenido'>"
                "<h3><a href='../%s/index.html'>%s</a></h3>"
                "<p>%s</p>"
                "</div></article>" % (
                    a.get("seccion", "voces"), foto_html, a["id"], esc(a.get("titulo", a["id"])), esc(a.get("bajada", ""))))
        cards = "".join(cards)
        if not cards:
            cards = "<p class='txt-parrafo'>Sección en construcción: sumá tu artículo.</p>"
        body = ('<header class="sec-portada" aria-labelledby="seccion-titulo">\n'
                '<p class="sec-portada__num">%s / %s</p>\n<h1 id="seccion-titulo" class="sec-portada__h1">%s</h1>\n'
                '<p class="sec-portada__descrip">%s</p>\n</header>\n'
                '<div class="sec-listado grid-12" aria-label="%s">\n%s\n</div>'
                % ("%02d" % (i + 1), "%02d" % len(secciones), esc(s["titulo"]),
                   esc(s.get("bajada", "")), esc(s["titulo"]), cards))
        open(os.path.join(EDIT, "secciones", s["id"] + ".html"), "w", encoding="utf-8").write(
            pagina("La Revista del Rural · %s" % s["titulo"], s.get("bajada", ""), ed_etiqueta,
                   nav_html("../"), body, "../index.html", "../css/", "../favicon.svg", sec_id=s["id"]))

    # ---- portada ---------------------------------------------------------
    sumario = "".join(
        "<li class='sumario__item' data-sec='%s'><a class='sumario__link' href='secciones/%s.html'>"
        "<span class='sumario__num'>%s</span>"
        "<span class='sumario__texto'><span class='sumario__nombre'>%s</span>"
        "<span class='sumario__desc'>%s</span></span></a></li>"
        % (s["id"], s["id"], "%02d" % (i + 1), esc(s["titulo"]), esc(s.get("bajada", "")))
        for i, s in enumerate(secciones))
    sec_cards = "".join(
        "<article class='sec_card grid-4' data-sec='%s'><h3 class='sec_card__titulo'>"
        "<a href='secciones/%s.html'>%s</a></h3>"
        "<p class='sec_card__bajada'>%s</p></article>" %
        (s["id"], s["id"], esc(s["titulo"]), esc(s.get("bajada", "")))
        for s in secciones)
    egr_num = "%02d" % (len(secciones) + 1)
    sumario += ("<li class='sumario__item' data-sec='egresados'>"
                "<a class='sumario__link' href='egresados.html'>"
                "<span class='sumario__num'>%s</span>"
                "<span class='sumario__texto'><span class='sumario__nombre'>Egresados</span>"
                "<span class='sumario__desc'>Promoción de 5.º año</span></span></a></li>"
                % egr_num)
    sec_cards += ("<article class='sec_card grid-4' data-sec='egresados'>"
                  "<h3 class='sec_card__titulo'><a href='egresados.html'>Egresados</a></h3>"
                  "<p class='sec_card__bajada'>Promoción de 5.º año</p></article>")
    body = ('<section class="portada" aria-labelledby="portada-titulo">\n'
            '<p class="portada__sec">%s</p>\n'
            '<h1 id="portada-titulo" class="portada__h1">%s</h1>\n'
            '<p class="portada__bajada">%s</p>\n</section>\n'
            '<nav class="sumario" aria-label="Sumario">\n'
            '<p class="sumario__cabecera">Sumario · %s</p>\n<ul class="sumario__lista">\n%s\n</ul>\n</nav>\n'
            '<p class="todos__enlace"><a href="articulos.html">Ver los %d artículos de esta edición</a></p>'
            % (esc(ed_etiqueta), esc(REV), esc(SUBNOMBRE), esc(ed_etiqueta), sumario, len(articulos)))
    open(os.path.join(EDIT, "index.html"), "w", encoding="utf-8").write(
        pagina("La Revista del Rural · %s" % ed_etiqueta, SUBNOMBRE, ed_etiqueta, nav_html(""),
               body, "index.html", "css/", "favicon.svg"))

    # ---- egresados ---------------------------------------------------------
    n_egr = len(EGRESADOS)
    open(os.path.join(EDIT, "egresados.html"), "w", encoding="utf-8").write(
        pagina("La Revista del Rural · Egresados",
               "Egresadas y egresados de la ESRN Rural Virtual · %d personas" % n_egr,
               ed_etiqueta, nav_html(""),
               ('<header class="sec-portada" aria-labelledby="egresados-titulo">\n'
                '<p class="sec-portada__num">%d personas</p>\n'
                '<h1 id="egresados-titulo" class="sec-portada__h1">Egresados</h1>\n'
                '<p class="sec-portada__descrip">Promoción 2026 · Ciclo Orientado</p>\n</header>\n'
                '%s') % (n_egr, egresados_body()),
               "index.html", "css/", "favicon.svg", sec_id="egresados"))

    # ---- todos los artículos ---------------------------------------------
    todos = []
    for a in articulos:
        sec = next((s for s in secciones if s["id"] == a.get("seccion")), None)
        sec_tit = sec["titulo"] if sec else "Voces"
        fotos = a.get("fotos") or []
        thumb = ("<img src='%s/%s' alt='' class='art_card__img' loading='lazy'>" % (a["id"], fotos[0])
                 if fotos else "<div class='art_card__img art_card__img--vacio' aria-hidden='true'></div>")
        todos.append(
            "<article class='art_card grid-6' data-sec='%s'>"
            "%s"
            "<div class='art_card__contenido'>"
            "<p class='art_card__sec'>%s</p>"
            "<h3><a href='%s/index.html'>%s</a></h3>"
            "<p>%s</p></div></article>" % (
                a.get("seccion", "voces"), thumb, esc(sec_tit), a["id"],
                esc(a.get("titulo", a["id"])), esc(a.get("bajada", ""))))

    body_todos = ('<header class="sec-portada" aria-labelledby="todos-titulo">\n'
                  '<p class="sec-portada__num">%d artículos</p>\n'
                  '<h1 id="todos-titulo" class="sec-portada__h1">Todos los artículos</h1>\n'
                  '<p class="sec-portada__descrip">Todo lo que publicó esta edición, ordenado por sección.</p>\n'
                  '</header>\n'
                  '<div class="sec-listado grid-12">\n%s\n</div>'
                  % (len(articulos), "".join(todos)))
    open(os.path.join(EDIT, "articulos.html"), "w", encoding="utf-8").write(
        pagina("La Revista del Rural · Todos los artículos", ed_etiqueta, ed_etiqueta,
               nav_html(""), body_todos, "index.html", "css/", "favicon.svg"))

    # ---- presentación ----------------------------------------------------
    from generar_mapa import mapa_sedes_svg
    PRES_INTRO = ("Una propuesta educativa presencial-virtual "
                  "destinada a egresados de Educación Primaria que residen en parajes rurales "
                  "que no disponen de una oferta de Educación Secundaria tradicional. "
                  "Actualmente nuestra escuela cuenta con veintiséis sedes en toda la provincia, "
                  "a la que asisten diariamente más de cuatrocientos estudiantes.")
    PRES_DONDE = ("Cada punto verde de este mapa de la Provincia de Río Negro "
                  "indica una localidad o paraje donde funciona una sede de la "
                  "ESRN Rural Virtual.")
    PRES_REV = [
        "Presentamos la Revista del Rural, "
        "una propuesta pedagógica que pretende sumar un nuevo medio de expresión para toda "
        "nuestra extensa comunidad educativa.",
        "La revista se encuentra organizada en diferentes secciones. Las mismas fueron diseñadas "
        "y elaboradas por las y los estudiantes en instancias de trabajo colaborativo, junto con "
        "el acompañamiento docente. A lo largo de la revista podrán encontrar historias, noticias, "
        "arte, además de la divulgación de producciones elaboradas durante el año en los distintos "
        "espacios curriculares.",
    ]
    body = ('<section class="pres" aria-labelledby="pres-titulo">\n'
            '<header class="sec-portada">\n'
            '<p class="sec-portada__num">Presentación</p>\n'
            '<h1 id="pres-titulo" class="sec-portada__h1">%s</h1>\n'
            '<p class="sec-portada__descrip">%s</p>\n</header>\n'
            '<div class="pres__bloque">\n'
            '<h2 class="pres__h2">Somos la ESRN RURAL VIRTUAL</h2>\n'
            '<p class="pres__p pres__lead">%s</p>\n'
            '<figure class="pres__foto">\n'
            '<img src="grupo.png" alt="" loading="lazy" decoding="async">\n'
            '</figure>\n'
            '</div>\n'
            '<div class="pres__bloque">\n'
            '<h2 class="pres__h2">¿Dónde estamos?</h2>\n'
            '<p class="pres__p pres__ancho">%s</p>\n'
            '<figure class="mapa__figura">\n%s\n'
            '<figcaption class="mapa__ep">Sedes de la ESRN Rural Virtual '
            'en la Provincia de Río Negro.</figcaption>\n</figure>\n</div>\n'
            '<div class="pres__bloque">\n'
            '<h2 class="pres__h2">La Revista del Rural</h2>\n'
            '<div class="pres__doble">\n'
            '<div>\n%s\n</div>\n'
            '<figure class="pres__foto">\n'
            '<img src="revistas.png" alt="" loading="lazy" decoding="async">\n'
            '</figure>\n'
            '</div>\n'
            '</div>\n'
            '</section>') % (
        esc("Presentación"), esc(SUBNOMBRE), esc(PRES_INTRO), esc(PRES_DONDE),
        mapa_sedes_svg(),
        "".join('<p class="pres__p">%s</p>\n' % esc(p) for p in PRES_REV))
    open(os.path.join(EDIT, "presentacion.html"), "w", encoding="utf-8").write(
        pagina("La Revista del Rural · Presentación", SUBNOMBRE, ed_etiqueta,
               nav_html(""), body, "index.html", "css/", "favicon.svg"))

    print("OK ediciones/01 -> %d artículos + %d secciones + portada + articulos.html + presentacion.html"
          % (len(articulos), len(secciones)))


if __name__ == "__main__":
    main()
