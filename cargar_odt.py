import sys, os, re, shutil, zipfile, argparse
import xml.etree.ElementTree as ET

OFFICE = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
TEXT   = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
DRAW   = "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
XLINK  = "http://www.w3.org/1999/xlink"

W  = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
A  = "http://schemas.openxmlformats.org/drawingml/2006/main"
A_EMBED = "{%s}embed" % "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

EXTRAIDOS = "enviar_aqui"
EXTRAIDOS_IMG = os.path.join(EXTRAIDOS, "imagenes_odt")

def slug_articulo(archivo):
    base = os.path.splitext(os.path.basename(archivo))[0].lower()
    slug = re.sub(r"[^a-z0-9_]+", "_", base).strip("_")[:40] or "articulo"
    return slug

def subcarpeta_articulo(archivo, carpeta_base):
    return os.path.join(carpeta_base, slug_articulo(archivo))

def texto_simple(el, t):
    partes = []
    def rec(nodo):
        if nodo.tag == t["frame"] or nodo.tag == t["image"]:
            return
        if nodo.text:
            partes.append(nodo.text)
        for hijo in nodo:
            rec(hijo)
        if nodo.tail:
            partes.append(nodo.tail)
    rec(el)
    return "".join(partes)

def texto_runs(el, t):
    partes = []
    for nodo in el.iter():
        if nodo.tag == "{%s}t" % W:
            partes.append(nodo.text or "")
    return "".join(partes)

def parrafo_segmentos(el, t):
    res = []
    buff = []
    def flush():
        if buff:
            res.append(("p", "".join(buff)))
            buff.clear()
    def walk(nodo):
        if nodo.tag == t["frame"] or nodo.tag == t["image"]:
            flush()
            res.append(("img", ruta_imagen(nodo, t)))
            return
        if nodo.text:
            buff.append(nodo.text)
        for hijo in nodo:
            walk(hijo)
        if nodo.tail:
            buff.append(nodo.tail)
    walk(el)
    flush()
    return res

def ruta_imagen(nodo, t):
    img = nodo if nodo.tag == t["image"] else None
    if img is None:
        img = nodo.find(".//" + t["image"])
    if img is None:
        return ""
    return img.get(t["href"]) or ""

def segmentos_odt(el, t):
    res = []
    for nodo in el:
        tag = nodo.tag
        if tag == t["frame"] or tag == t["image"]:
            res.append(("img", ruta_imagen(nodo, t)))
        elif tag == t["p"]:
            res.extend(parrafo_segmentos(nodo, t))
        elif tag == t["h"]:
            nivel = nodo.get(t["nivel"]) or "1"
            res.append(("h", (nivel, texto_simple(nodo, t))))
        else:
            seg = segmentos_odt(nodo, t)
            if seg:
                res.extend(seg)
    return res

def segmentos_docx(el_n, rels):
    res = []
    buff = []
    def flush():
        if buff:
            res.append(("p", "".join(buff)))
            buff.clear()
    for nodo in el_n.iter():
        if nodo.tag == "{%s}t" % W:
            buff.append(nodo.text or "")
        elif nodo.tag == "{%s}blip" % A:
            embed = nodo.get(A_EMBED)
            if embed and embed in rels:
                flush()
                res.append(("img", rels[embed]))
    flush()
    return res

def bloque_a_texto(bloques, mapa, salida):
    i = 0
    primero = True
    while i < len(bloques):
        tipo, valor = bloques[i]
        if tipo == "img":
            destino = mapa.get(valor)
            salida.append("[FOTO:%s]" % (destino or "faltante"))
            if i + 1 < len(bloques) and bloques[i + 1][0] in ("p",):
                prox = bloques[i + 1][1].strip()
                if 0 < len(prox) <= 160 and not prox.upper().startswith(("AUTOR", "POR ", "FIRMA")):
                    salida.append("[LEYENDA]%s[/LEYENDA]" % prox)
                    i += 1
            i += 1
            continue
        texto = valor[1].strip() if tipo == "h" else valor.strip()
        if not texto:
            i += 1
            continue
        if texto.startswith("http://") or texto.startswith("https://"):
            i += 1
            continue
        if tipo == "h":
            nivel = int(valor[0])
            salida.append("[TITULO]%s" % texto if primero else "[SUBTITULO]%s" % texto)
            primero = False
        elif primero:
            salida.append("[TITULO]%s" % texto)
            primero = False
        else:
            mayus = texto.upper()
            if texto.startswith("Autor") or texto.startswith("Por ") or mayus.startswith("FIRMA"):
                salida.append("[FIRMA]%s" % texto)
            else:
                salida.append("[PARRAFO]%s" % texto)
        i += 1

def exportar_imagenes(archivo, carpeta_imgs, prefijos):
    subcarpeta = subcarpeta_articulo(archivo, carpeta_imgs)
    os.makedirs(subcarpeta, exist_ok=True)
    mapa = {}
    with zipfile.ZipFile(archivo) as z:
        nombres = [n for n in z.namelist()
                   if any(n.startswith(p) for p in prefijos)
                   and n.lower().split(".")[-1] in
                   ("jpg", "jpeg", "png", "gif", "svg", "bmp", "webp")]
        contador = 0
        for n in sorted(nombres):
            ext = os.path.splitext(n)[1].lower()
            contador += 1
            destino = "foto_%02d%s" % (contador, ext)
            with z.open(n) as f, open(os.path.join(subcarpeta, destino), "wb") as out:
                shutil.copyfileobj(f, out)
            mapa[n] = destino
    return mapa

def bloques_a_texto(bloques, mapa, salida):
    bloque_a_texto(bloques, mapa, salida)

def cargar_odt(ruta, carpeta_imgs):
    t = {
        "p": "{%s}p" % TEXT,
        "h": "{%s}h" % TEXT,
        "body": "{%s}body" % OFFICE,
        "frame": "{%s}frame" % DRAW,
        "image": "{%s}image" % DRAW,
        "href": "{%s}href" % XLINK,
        "nivel": "{%s}outline-level" % TEXT,
    }
    with zipfile.ZipFile(ruta) as z:
        contenido = z.read("content.xml")
    root = ET.fromstring(contenido)
    cuerpo = root.find(".//" + t["body"])
    bloques = segmentos_odt(cuerpo, t)
    mapa = exportar_imagenes(ruta, carpeta_imgs, ("media/", "Pictures/"))
    salida = []
    bloques_a_texto(bloques, mapa, salida)
    return salida

def cargar_docx(ruta, carpeta_imgs):
    with zipfile.ZipFile(ruta) as z:
        contenido = z.read("word/document.xml")
        rels = rels_docx(z)
    root = ET.fromstring(contenido)
    cuerpo = root.find(".//{%s}body" % W)
    mapa = exportar_imagenes(ruta, carpeta_imgs, ("word/media/",))
    bloques = []
    for p in cuerpo.iter("{%s}p" % W):
        estilo = ""
        ppr = p.find("{%s}pPr" % W)
        if ppr is not None:
            ps = ppr.find("{%s}pStyle" % W)
            if ps is not None:
                estilo = (ps.get("{%s}val" % W) or "").replace(" ", "")
        textos, imgs = [], []
        for nodo in p.iter():
            if nodo.tag == "{%s}t" % W:
                textos.append(nodo.text or "")
            elif nodo.tag == "{%s}blip" % A:
                embed = nodo.get(A_EMBED)
                if embed and embed in rels:
                    imgs.append(rels[embed])
        texto = "".join(textos).strip()
        es_titulo = (estilo in ("Title", "Subtitle", "Heading1", "Heading2", "Heading3")
                     or estilo.startswith(("Ttulo", "Título", "Heading", "Title")))
        if texto:
            if es_titulo:
                nivel = "1" if (estilo in ("Title", "Subtitle") or estilo.startswith(("Ttulo", "Título"))) else "2"
                bloques.append(("h", (nivel, texto)))
            else:
                bloques.append(("p", texto))
        for im in imgs:
            bloques.append(("img", im))
    salida = []
    bloque_a_texto(bloques, mapa, salida)
    return salida

def rels_docx(z):
    mapa = {}
    try:
        xml = z.read("word/_rels/document.xml.rels")
    except Exception:
        return mapa
    try:
        root = ET.fromstring(xml)
    except Exception:
        return mapa
    for r in root:
        target = (r.get("Target") or "").rstrip("/")
        if target.startswith("/"):
            target = target[1:]
        elif not target.startswith("word/media/"):
            if target.startswith("media/"):
                target = "word/media/" + target
        mapa[r.get("Id")] = target
    return mapa

def principal(ruta):
    if not os.path.exists(ruta):
        print("ERROR: no existe el archivo", ruta)
        sys.exit(1)
    ext = os.path.splitext(ruta)[1].lower()
    if ext == ".odt":
        salida = cargar_odt(ruta, EXTRAIDOS_IMG)
    elif ext == ".docx":
        salida = cargar_docx(ruta, EXTRAIDOS_IMG)
    else:
        print("ERROR: formato no soportado. Se aceptan .odt y .docx")
        sys.exit(1)

    n_fotos = len([l for l in salida if l.startswith("[FOTO")])
    texto = "\n".join(salida)
    destino_txt = os.path.join(EXTRAIDOS, "articulo_extraido.txt")
    with open(destino_txt, "w", encoding="utf-8") as f:
        f.write(texto)

    print("OK - articulo extraido de", os.path.basename(ruta))
    print("  Fotos :", n_fotos, "-> enviar_aqui/imagenes_odt/%s/" % slug_articulo(ruta))
    print("  Texto :", destino_txt)
    print("=" * 60)
    print(texto)

if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 2:
        print("Uso: python cargar_odt.py [ruta/al/articulo.odt]")
        print("     Se aceptan archivos .odt y .docx")
        sys.exit(1)
    principal(sys.argv[1])
