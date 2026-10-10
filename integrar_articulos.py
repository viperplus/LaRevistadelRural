# -*- coding: utf-8 -*-
"""Integra los tres articulos de Lengua (Carla Lopardo) en la revista.

Uso (desde la carpeta revista/):
    python integrar_articulos.py          # vista previa (no escribe nada)
    python integrar_articulos.py --write  # copia fotos + agrega a ediciones.json
"""
import os
import re
import sys
import json
import shutil
import unicodedata

BASE = os.path.join(r"C:\Users\black\Desktop\opencode archivos", "clase n°4", "revista")
SRC = os.path.join(BASE, "ARTICULOS")
EDIT = os.path.join(BASE, "ediciones", "01")
DATOS = os.path.join(BASE, "datos", "ediciones.json")
EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif")
WRITE = "--write" in sys.argv

# ---------------------------------------------------------------- utilidades
def sin_acentos(s):
    return "".join(unicodedata.normalize("NFD", c)[0] for c in s)


def quitar(texto, sub):
    """Quita `sub` de `texto` ignorando acentos/mayusculas, preservando indices."""
    if not sub:
        return texto
    nt = sin_acentos(texto).lower()
    ns = sin_acentos(sub).lower()
    i = nt.find(ns)
    while i != -1:
        texto = texto[:i] + texto[i + len(sub):]
        nt = nt[:i] + nt[i + len(ns):]
        i = nt.find(ns)
    return texto


def limpiar(stem):
    s = re.sub(r"\s*\(\d+\)\s*$", "", stem)
    s = re.sub(r"\s+_$", "", s)
    s = re.sub(r"\s+", " ", s).strip(" -_")
    return s


def romper(stem, separador):
    return [p.strip() for p in re.split(separador, limpiar(stem)) if p.strip()]


def capitalizar(s):
    s = re.sub(r"\s+", " ", s).strip()
    if s and (s.isupper() or s.islower()):
        return s.title()
    return s


def carpeta(nombre_prefijo):
    for d in sorted(os.listdir(SRC)):
        if os.path.isdir(os.path.join(SRC, d)) and d.startswith(nombre_prefijo):
            return d
    raise SystemExit("No encuentro la carpeta %r" % nombre_prefijo)


def imagenes(folder):
    raiz = os.path.join(SRC, folder)
    out = []
    for root, dirs, files in os.walk(raiz):
        dirs.sort()
        for f in sorted(files):
            if os.path.splitext(f)[1].lower() in EXTS:
                out.append(os.path.relpath(os.path.join(root, f), raiz))
    return out


# ------------------------------------------------------------ epigrafes
def epi_malvinas(rel):
    stem = limpiar(os.path.splitext(os.path.basename(rel))[0])
    p = romper(stem, r"\s+-\s*")
    nombre = capitalizar(p[0])
    sede = capitalizar(p[1]) if len(p) > 1 else ""
    return "La carta de %s%s" % (nombre, (" · " + sede) if sede else "")


def epi_panuelos(rel):
    sede_dir = os.path.dirname(rel)
    stem = limpiar(os.path.splitext(os.path.basename(rel))[0])
    sede = capitalizar(sede_dir.split(os.sep)[0]) if sede_dir else ""
    t = quitar(stem, sede_dir.split(os.sep)[0] if sede_dir else "")
    t = re.sub(r"(?i)^whatsapp image.*$", "", t)
    t = re.sub(r"(?i)\banexo\s*\d+", "", t)
    t = re.sub(r"(?i)\bmi\s+pa[ñn]uelo\b", "", t)
    t = re.sub(r"(?i)\bpa[ñn]uelos?\b", "", t)
    t = re.sub(r"(?i)\bsede\b", "", t)
    t = re.sub(r"(?i)\b\d+(er|ro|do|to)\s+a[ñn]o\b", "", t)
    t = re.sub(r"(?i)\blengua\b", "", t)
    t = re.sub(r"(?i)\bclase\s*\d+", "", t)
    t = re.sub(r"[-\u2013\u2014_]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip(" .,")
    if len(t) < 3 or t.lower().startswith("whatsapp"):
        return ("Pañuelos · " + sede) if sede else "Pañuelos"
    n = capitalizar(t)
    return "El pañuelo de %s%s" % (n, (" · " + sede) if sede else "")


def epi_fantastica(rel):
    stem = limpiar(os.path.splitext(os.path.basename(rel))[0])
    p = romper(stem, r"\s+-\s+")
    if len(p) > 1:
        sede, nombre = capitalizar(p[0]), capitalizar(p[1])
    else:
        sede, nombre = "", capitalizar(p[0])
    return "%s%s" % (nombre, (" · " + sede) if sede else "")


# ------------------------------------------------------------ articulos
ART = [
    dict(
        folder_prefijo="2 DE ABRIL",
        uid="2-de-abril-mujeres-en-malvinas",
        seccion="territorio",
        titulo="Mujeres en Malvinas: cartas para quienes estuvieron",
        bajada=("Por el 2 de abril escribimos a las mujeres que formaron parte de la "
                "Guerra de Malvinas —enfermeras, instrumentadoras, comunicadoras y "
                "colaboradoras— para hacerles llegar las cartas que preparamos."),
        fecha="Abril 2026",
        fecha_iso="2026-04-02",
        sede="Todas las sedes",
        epi=epi_malvinas,
        cuerpo=[
            {"t": "p", "v": ("Para continuar practicando la memoria identitaria y seguir "
                             "construyendo sentidos propios sobre la Guerra de Malvinas, "
                             "concientizamos sobre la invisibilización de las mujeres que "
                             "formaron parte de la guerra.")},
            {"t": "p", "v": ("La propuesta era escribirle a una mujer que participó en la "
                             "Guerra de Malvinas (como enfermera, instrumentadora, "
                             "comunicadora o colaboradora) con el fin de hacerle llegar las "
                             "cartas que están prontas a ser recibidas por dos de ellas en el "
                             "mes de octubre.")},
        ],
    ),
    dict(
        folder_prefijo="24 MARZO",
        uid="24-marzo-floreceran-panuelos",
        seccion="estudiantes",
        titulo="Florecerán pañuelos",
        bajada=("En vísperas del 50 aniversario del golpe militar, tomamos la consigna de "
                "los organismos de derechos humanos y hicimos florecer historias con "
                "pañuelos blancos."),
        fecha="Marzo 2026",
        fecha_iso="2026-03-24",
        sede="Todas las sedes",
        epi=epi_panuelos,
        cuerpo=[
            {"t": "p", "v": ("En vísperas del 50 aniversario del golpe militar, los organismos "
                             "de derechos humanos convocaron a la sociedad, instituciones, "
                             "sindicatos, comunidad educativa y organizaciones de la sociedad "
                             "civil a sumarse a la campaña “Florecerán pañuelos”.")},
            {"t": "p", "v": ("Es por esto que desde la escuela, reafirmamos nuestro compromiso "
                             "con los derechos humanos y la democracia desde la construcción "
                             "de una ciudadanía crítica.")},
            {"t": "p", "v": ("Realizamos pañuelos blancos con materiales a mano para "
                             "intervenirlos con frases, símbolos, dibujos y flores dibujadas "
                             "para que florezcan historias en todos los rincones del país. "
                             "Esos pañuelos podían compartirlo en alguna parte de la escuela, "
                             "la plaza, negocios o cualquier espacio visible.")},
        ],
    ),
    dict(
        folder_prefijo="ESCRITURA FANT",
        uid="escritura-fantastica",
        seccion="cultura",
        titulo="Escritura fantástica",
        bajada=("De la mano de Mariana Enríquez y su cuento “El desentierro de la "
                "Angelita”, nos adentramos en el género fantástico."),
        fecha="Noviembre 2026",
        fecha_iso="2026-11-01",
        sede="Todas las sedes",
        epi=epi_fantastica,
        cuerpo=[
            {"t": "p", "v": ("Desde la antología de escritoras latinoamericanas seleccionadas "
                             "por la docente, realizamos una introducción al género fantástico "
                             "de la mano de la escritora Mariana Enríquez con su cuento “El "
                             "desentierro de la Angelita”.")},
            {"t": "p", "v": ("El propósito es aprender, a través de producciones escritas, a "
                             "profundizar en la importancia de lo fantástico en el mundo de la "
                             "literatura.")},
        ],
    ),
]


def construir(a):
    folder = carpeta(a["folder_prefijo"])
    rels = imagenes(folder)
    fotos, epigrafes = [], []
    for i, rel in enumerate(rels, 1):
        ext = os.path.splitext(rel)[1].lower()
        nombre = "foto-%02d%s" % (i, ext)
        fotos.append(nombre)
        epigrafes.append(a["epi"](rel))
    disp = ["portada"] + ["galeria"] * (len(fotos) - 1)
    art = {
        "id": a["uid"],
        "seccion": a["seccion"],
        "clase": "",
        "titulo": a["titulo"],
        "bajada": a["bajada"],
        "autor": "Carla Lopardo",
        "rol": "Docente de Lengua y Literatura",
        "sede": a["sede"],
        "fecha": a["fecha"],
        "fecha_iso": a["fecha_iso"],
        "foto_principal": "%s/%s/%s" % (a["seccion"], a["uid"], fotos[0]),
        "fotos": fotos,
        "fotos_disposicion": disp,
        "epigrafes": epigrafes,
        "cuerpo": a["cuerpo"],
        "anio": "",
    }
    return art, folder, rels


nuevos = []
for a in ART:
    art, folder, rels = construir(a)
    nuevos.append((art, folder, rels))
    print("=" * 78)
    print("%s  ->  %d fotos" % (art["titulo"], len(art["fotos"])))
    print("  uid: %s | seccion: %s | carpeta: %s" % (art["id"], art["seccion"], folder))
    for o, f, e in zip(rels, art["fotos"], art["epigrafes"]):
        print("   %-46s -> %-13s %s" % (o, f, e))

if not WRITE:
    print("\nVista previa solamente. Corre con --write para aplicar.")
else:
    for art, folder, rels in nuevos:
        dst = os.path.join(EDIT, art["id"])
        os.makedirs(dst, exist_ok=True)
        for rel, nombre in zip(rels, art["fotos"]):
            shutil.copy2(os.path.join(SRC, folder, rel), os.path.join(dst, nombre))
        print("copiadas %d fotos -> %s" % (len(rels), dst))

    datos = json.load(open(DATOS, encoding="utf-8"))
    ids = {x["id"] for x in datos["articulos"]}
    for art, folder, rels in nuevos:
        if art["id"] in ids:
            print("ya existia, salto:", art["id"])
            continue
        datos["articulos"].append(art)
    with open(DATOS, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("ediciones.json -> %d articulos" % len(datos["articulos"]))
