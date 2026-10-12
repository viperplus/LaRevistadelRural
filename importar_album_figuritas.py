# -*- coding: utf-8 -*-
"""Importa las figuritas al album estilo Panini del articulo `album-figuritas`.

Lee FIGUSAS, separa figuritas de fotos de escenarios, las agrupa por sede,
las achica a ~700 px y las deja en ediciones/01/album-figuritas/. Despues
escribe (o actualiza) la entrada del articulo en datos/ediciones.json.
"""
import colorsys
import hashlib
import json
import os
import re
import shutil
import sys
import unicodedata

from PIL import Image, ImageOps

BASE = os.path.join(r"C:\Users\black\Desktop\opencode archivos", "clase n" + "\u00b04", "revista")
SRC = os.path.join(r"C:\Users\black\Desktop\opencode archivos", "FIGUSAS")
DATOS = os.path.join(BASE, "datos", "ediciones.json")
UID = "album-figuritas"
ANCHO = 700
CALIDAD = 82
MIN_PESO = 12000          # si el jpg ya existe y pesa mas que esto, no lo regenero
ID_ART = UID

# Fotos de estadios, paisajes y potreros: no son figuritas, quedan afuera.
ESCENARIOS = {
    "CONA NIYEU.jpeg",
    "LAGO PELLEGRINI.jpeg", "LAGO PELLEGRINI1.jpeg", "LAGO PELLEGRINI2.jpeg",
    "NAHUPA HUEN.jpeg",
    "Potrero sede Aguada de Guerra.jpeg",
    "VILLA LLANQU\u00cdN.jpeg",
    "estadio comico.jpeg", "estadio el cain.jpeg", "estadio laguna blanca.jpeg",
    "pe\u00f1as blancas.jpeg", "pe\u00f1as blancas 1.jpeg", "pe\u00f1as blancas 2.jpeg",
}
# S\u00f3lo el marco, sin dibujo: plantilla en blanco que no aporta al \u00e1lbum.
EN_BLANCO = {"S__SDA.png"}
# Sedes escritas distinto por error: se agrupan todas bajo el mismo nombre.
SEDE_DISPLAY = {
    "COMICO": "C\u00f3mico", "COMIC\u00d3": "C\u00f3mico",
    "CERRO_POLICIA": "Cerro Polic\u00eda",
}
# ...pero si son figuritas escritas con " - " en vez de "__"
FIGU_SIN_GUIONES = {
    "LAGO PELLEGRINI - DAMARIS_AMAYA.jpeg": ("LAGO PELLEGRINI", "DAMARIS_AMAYA"),
    "LUCRECIA - LAGO PELLEGRINI.jpeg": ("LAGO PELLEGRINI", "LUCRECIA"),
    "MENCU\u00c9.jpeg": ("MENCU\u00c9", ""),
}

RE_SUFIJO = re.compile(r"\s*\((\d+)\)\s*$")


def palabra(w):
    w = w.strip()
    if not w:
        return ""
    return w[0].upper() + w[1:].lower()


def nombre_legible(raw):
    """ERNESTO_MILLAQUEO -> Ernesto Millaqueo"""
    raw = RE_SUFIJO.sub("", raw).strip()
    return " ".join(palabra(p) for p in re.split(r"[\s_]+", raw) if p)


def sede_legible(raw):
    """AGUADA_CECILIO / VALLE_ VERDE -> Aguada Cecilio / Valle Verde"""
    if raw in SEDE_DISPLAY:
        return SEDE_DISPLAY[raw]
    partes = [palabra(p) for p in re.split(r"[\s_]+", raw.strip()) if p.strip()]
    # Articulos cortos se escriben en minuscula salvo que abran la frase.
    minus = {"de", "del", "la", "el", "los", "las", "y", "en"}
    out = []
    for i, p in enumerate(partes):
        low = p.lower()
        out.append(palabra(p) if (i == 0 or low not in minus) else low)
    return " ".join(out)


# ---------- color de cada sede ---------------------------------------------
PAPEL = (250.0, 246.0, 238.0)   # --papel de revista.css
GOLDEN = 0.6180339887498949


def _luminancia(rgb):
    def f(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(rgb[0]) + 0.7152 * f(rgb[1]) + 0.0722 * f(rgb[2])


def _contraste(a, b):
    la, lb = _luminancia(a), _luminancia(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(c)))) for c in rgb)


def _hsv(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
    return (r * 255.0, g * 255.0, b * 255.0)


def _tonos(h):
    """Devuelve tres tonos de la misma sede:
      color   — fuerte: títulos, bordes. Oscurecido hasta pasar AA sobre papel.
      fondo   — medio: banda de cabecera, fichas del índice.
      pagina  — muy tenue: tinte de fondo de la página."""
    v = 0.60
    fuerte = _hsv(h, 0.60, v)
    while v > 0.16 and _contraste(fuerte, PAPEL) < 4.6:
        v -= 0.02
        fuerte = _hsv(h, 0.60, v)
    return _hex(fuerte), _hex(_hsv(h, 0.34, 0.93)), _hex(_hsv(h, 0.20, 0.985))


def colores_por_sede(sedes):
    """Un tono por sede, repartido por la rueda y sin repetir vecinos.
    Sale del nombre, así que una sede conserva su color si se agregan otras."""
    tomados = []
    fuera = {}
    for s in sorted(sedes, key=lambda x: x.lower()):
        h = (sum((i + 1) * ord(c) for i, c in enumerate(s)) * GOLDEN) % 1.0
        vueltas = 0
        while any(abs(h - t) < 0.07 for t in tomados) and vueltas < 400:
            h = (h + GOLDEN) % 1.0
            vueltas += 1
        tomados.append(h)
        color, fondo, pagina = _tonos(h)
        assert _contraste(_hsv_from_hex(color), PAPEL) >= 4.6, s
        fuera[s] = {"color": color, "fondo": fondo, "pagina": pagina}
    return fuera


def _hsv_from_hex(hx):
    return tuple(int(hx[i:i + 2], 16) for i in (1, 3, 5))


def clasificar():
    """-> [(sede, persona, archivo_origen)] ya ordenado."""
    sedes_conocidas = set()
    items = []
    descartadas = []

    for f in sorted(os.listdir(SRC)):
        p = os.path.join(SRC, f)
        if not os.path.isfile(p) or f in EN_BLANCO:
            continue
        base = os.path.splitext(f)[0]
        if "__" in base:
            sede, persona = base.split("__", 1)
            sedes_conocidas.add(sede.strip().upper())
            items.append((sede, persona, f))
        elif f in FIGU_SIN_GUIONES:
            sede, persona = FIGU_SIN_GUIONES[f]
            sedes_conocidas.add(sede.strip().upper())
            items.append((sede, persona, f))
        elif f in ESCENARIOS:
            descartadas.append(f)
        else:
            # Sin "__" y no listada: es una figurita mal nombrada. Si la
            # primera parte coincide con una sede conocida, la uso.
            if " - " in base:
                a, b = base.split(" - ", 1)
                if b.strip().upper() in sedes_conocidas:
                    items.append((b, a, f))
                    continue
                if a.strip().upper() in sedes_conocidas:
                    items.append((a, b, f))
                    continue
            descartadas.append("?? " + f)

    filas = []
    for sede, persona, f in items:
        s = sede_legible(sede)
        n = nombre_legible(persona) if persona else ""
        filas.append((s, n, f))
    filas.sort(key=lambda x: (x[0].lower(), x[1].lower(), x[2].lower()))
    return filas, descartadas


# ---------- repetidas --------------------------------------------------------
def normalizar(s):
    """'Kiara Mamani' y 'Kiara Mamaní' -> la misma clave."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def clave_persona(nombre):
    """El orden no importa: 'Fonseca Tiziana' es 'Tiziana Fonseca'."""
    n = normalizar(nombre)
    if not n:
        return None
    return " ".join(sorted(n.split()))


def huella(p):
    """Huella barata del archivo: alcanza para detectar copias exactas."""
    tam = os.path.getsize(p)
    with open(p, "rb") as fh:
        cabeza = fh.read(2 << 20)
        fh.seek(max(0, tam - (1 << 20)))
        cola = fh.read()
    return tam, hashlib.sha1(cabeza).hexdigest(), hashlib.sha1(cola).hexdigest()


def depurar(filas):
    """Sobra la figurita repetida: misma sede y persona, o el mismo archivo.
    -> (las que quedan, las que se van)."""
    dentro, fuera = [], []
    personas, huellas = set(), []
    for fila in filas:
        s, n, f = fila
        k = clave_persona(n)
        h = huella(os.path.join(SRC, f))
        repetida = h in huellas or (k is not None and (normalizar(s), k) in personas)
        if repetida:
            fuera.append(fila)
            continue
        huellas.append(h)
        if k is not None:
            personas.add((normalizar(s), k))
        dentro.append(fila)
    return dentro, fuera


def optimizar(dst):
    """Redimensiona a ANCHO px y guarda JPEG. Devuelve True si escribio."""
    if os.path.isfile(dst) and os.path.getsize(dst) > MIN_PESO:
        return False
    return True


def convertir(origen, dst):
    im = Image.open(origen)
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        fondo = Image.new("RGB", im.size, (255, 255, 255))
        im = im.convert("RGBA")
        fondo.paste(im, mask=im.split()[-1])
        im = fondo
    else:
        im = im.convert("RGB")
    w, h = im.size
    if w > ANCHO:
        im = im.resize((ANCHO, max(1, round(ANCHO * h / w))), Image.LANCZOS)
    im.save(dst, "JPEG", quality=CALIDAD, optimize=True, progressive=True)
    return im.size


def main():
    write = "--write" in sys.argv
    filas, descartadas = clasificar()
    filas, repetidas = depurar(filas)

    print("figuritas: %d  (repetidas quitadas: %d)" % (len(filas), len(repetidas)))
    for s, n, f in repetidas:
        print("    - %-22s %-22s <- %s" % (s, n or "(sin nombre)", f))
    print("descartadas (escenarios u otras): %d" % len(descartadas))
    for d in descartadas:
        print("   ", d)

    grupos = {}
    for s, n, f in filas:
        grupos.setdefault(s, []).append(n)
    print("sedes: %d" % len(grupos))
    for s in sorted(grupos, key=lambda x: x.lower()):
        sin = sum(1 for n in grupos[s] if not n)
        print("   %-24s %3d%s" % (s, len(grupos[s]), "  (sin nombre: %d)" % sin if sin else ""))

    if not write:
        print("\nVista previa. Corre con --write para importar.")
        return

    dst_dir = os.path.join(BASE, "ediciones", "01", UID)
    os.makedirs(dst_dir, exist_ok=True)

    # La numeracion se corre: si cambio el listado, hay que rehacerlas todas,
    # si no un fig-NNN.jpg viejo quedaria con la imagen de otra persona.
    viejo = []
    if os.path.isfile(DATOS):
        datos_v = json.load(open(DATOS, encoding="utf-8"))
        for a in datos_v["articulos"]:
            if a["id"] == ID_ART:
                viejo = list(zip(a.get("epigrafes", []), a.get("fotos_grupos", [])))
                break
    nuevo = [(n, s) for s, n, _ in filas]
    rehacer = viejo != nuevo
    if rehacer:
        for f in os.listdir(dst_dir):
            if re.match(r"^fig-\d+\.jpg$", f):
                os.remove(os.path.join(dst_dir, f))
        print("numeracion cambiada: se rehacen todas")

    fotos, epigrafes, grupos_ord = [], [], []
    hechas = nuevas = 0
    for i, (s, n, f) in enumerate(filas, 1):
        nombre = "fig-%03d.jpg" % i
        origen = os.path.join(SRC, f)
        destino = os.path.join(dst_dir, nombre)
        if optimizar(destino):
            convertir(origen, destino)
            nuevas += 1
        hechas += 1
        fotos.append(nombre)
        epigrafes.append(n)
        grupos_ord.append(s)
        if nuevas and nuevas % 50 == 0:
            print("   ... %d/%d" % (nuevas, len(filas)))


    total = sum(os.path.getsize(os.path.join(dst_dir, x)) for x in fotos)
    print("convertidas %d (nuevas %d) -> %.1f MB" % (hechas, nuevas, total / 1048576.0))

    art = armar_articulo(fotos, epigrafes, grupos_ord, grupos,
                         colores_por_sede(grupos))

    datos = json.load(open(DATOS, encoding="utf-8"))
    ids = {a["id"] for a in datos["articulos"]}
    if ID_ART in ids:
        for a in datos["articulos"]:
            if a["id"] == ID_ART:
                a.update(art)
        print("actualizado el articulo existente")
    else:
        # Va al final: aparece abajo en la seccion Estudiantes.
        datos["articulos"].append(art)
        print("agregado el articulo")
    with open(DATOS, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("ediciones.json -> %d articulos" % len(datos["articulos"]))


def armar_articulo(fotos, epigrafes, grupos_ord, grupos, colores):
    sedes = sorted(grupos, key=lambda x: x.lower())
    n_figu = len(fotos)
    n_sede = len(sedes)
    bajada = ("%d figuritas de %d sedes: el \u00e1lbum que se fue armando "
              "ficha por ficha, como en los \u00e1lbumes de Panini." % (n_figu, n_sede))

    cuerpo = [
        {"t": "p", "v": "¿Te acordás de abrir el paquete y correr a mirar si te había tocado la que te faltaba? Ese gesto es el que armamos acá: un álbum para juntar fichas, completar lugares y mirar quiénes están."},
        {"t": "p", "v": "Cada sede mandó sus figuritas, cada estudiante y cada tutor dejó la suya, y de a poquito el álbum se fue llenando hasta llegar a **%d figuritas repartidas en %d sedes**." % (n_figu, n_sede)},
        {"t": "p", "v": "Están agrupadas por sede, como en cualquier álbum que se respete. Tocá cualquier ficha para verla en grande."},
        {"t": "dato", "v": "%d sedes · %d figuritas · 1 solo álbum" % (n_sede, n_figu)},
    ]

    return {
        "id": ID_ART,
        "seccion": "estudiantes",
        "titulo": "El álbum de figuritas del Rural",
        "bajada": bajada,
        "autor": "Estudiantes y tutores de las %d sedes" % n_sede,
        "sede": "Todas las sedes",
        "fecha": "Octubre 2026",
        "fecha_iso": "2026-10-10",
        "tipo": "album",
        "cuerpo": cuerpo,
        "fotos": fotos,
        "epigrafes": epigrafes,
        "fotos_grupos": grupos_ord,
        "album_colores": colores,
    }


if __name__ == "__main__":
    main()
