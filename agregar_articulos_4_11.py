# -*- coding: utf-8 -*-
"""agregar_articulos_4_11.py — Incorpora los 2 artículos de "articulos 4-11".

1) "El Cóndor" (Balneario El Cóndor, 1.º año) -> sección Territorio.
   Las fotos salen del PDF original (se extrajeron con PyMuPDF).
2) "Hablamos con un veterano cerca de Kakel Huincul" (Sosa Torres Marcial,
   sede Colán Conhue) -> sección Voces.

Convención de fotos (la que usan los 540 casos que ya funcionan):
   archivo real en ediciones/01/<uid>/foto-NN.jpg
   JSON: fotos ["foto-01.jpg", ...] + fotos_disposicion [...]
Así resuelven tanto la tarjeta de la sección (../<uid>/fotos[0]) como el
<img> dentro del artículo.
"""
import json, io, sys, os
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista"
EDIT = os.path.join(BASE, "ediciones", "01")
TMP = r"C:\Users\black\AppData\Local\Temp\opencode\arts4_11"
PDFIMGS = os.path.join(TMP, "pdfimgs")
P_JSON = os.path.join(BASE, "datos", "ediciones.json")

MAX_LADO = 1400


def guardar_jpg(src, dst):
    """Convierte a JPEG RGB, achica si hace falta y guarda optimizado."""
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        fondo = Image.new("RGB", im.size, (255, 255, 255))
        fondo.paste(im, mask=im.split()[-1])
        im = fondo
    else:
        im = im.convert("RGB")
    w, h = im.size
    if max(w, h) > MAX_LADO:
        s = MAX_LADO / max(w, h)
        im = im.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "JPEG", quality=86, optimize=True, progressive=True)
    return os.path.getsize(dst)


# ---------------------------------------------------------------- artículo 1
UID1 = "el-condor-balneario-y-ecosistema"
FOTOS1 = [
    (os.path.join(PDFIMGS, "p1_05.png"), "foto-01.jpg"),
    (os.path.join(PDFIMGS, "p1_04.png"), "foto-02.jpg"),
    (os.path.join(PDFIMGS, "p1_03.png"), "foto-03.jpg"),
]

ART1 = {
    "id": UID1,
    "seccion": "territorio",
    "titulo": "El Cóndor: nuestro lugar mirado con los ojos de la ciencia",
    "bajada": "En Científica y Tecnológica estudiamos los ecosistemas y los niveles de organización de los seres vivos. Con eso en la cabeza, miramos el balneario donde vivimos.",
    "autor": "Francisco Casanoba, Mateo Lefinir y Randi Piccinini Ramos",
    "rol": "Estudiantes 1.º año",
    "sede": "El Cóndor",
    "anio": "1.º año",
    "fecha": "Diciembre 2026",
    "fecha_iso": "2026-12-01",
    "odt": None,
    "cuerpo": [
        {"t": "pregunta", "v": "¿Alguna vez miraste tu propio pueblo con los ojos de la ciencia?"},
        {"t": "p", "v": "En Científica y Tecnológica aprendimos sobre los ecosistemas y los niveles de organización de los seres vivos. Por eso miramos nuestro lugar usando lo que aprendimos, y esto es lo que encontramos."},
        {"t": "h3", "v": "El origen del nombre"},
        {"t": "p", "v": "El nombre «Cóndor» pertenecía a un buque danés que en 1881 encalló en nuestras costas. Los sobrevivientes del naufragio se asentaron en la zona junto a otra familia danesa que ya vivía en una estancia de aquí, y la población fue creciendo."},
        {"t": "h3", "v": "Dónde estamos"},
        {"t": "p", "v": "El Balneario El Cóndor se ubica a 30 km de Viedma, la capital de Río Negro, en la desembocadura del río Negro en el Mar Argentino."},
        {"t": "h3", "v": "Lo que mostramos a quien nos visita"},
        {"t": "p", "v": "El Cóndor es un destino turístico. Estamos orgullosos de nuestras playas, los acantilados, la desembocadura del río Negro, el faro más antiguo de la Patagonia, el monumento a Ceferino Namuncurá y nuestro Memorial de Malvinas."},
        {"t": "fig", "f": "foto-01.jpg", "clase": "fig--g8"},
        {"t": "h3", "v": "Un ecosistema de transición costero"},
        {"t": "p", "v": "El ecosistema de El Cóndor es único porque combina varios ambientes a la vez:"},
        {"t": "li", "b": "Estepa:", "v": "el paisaje abierto y seco de la Patagonia."},
        {"t": "li", "b": "Acantilados costeros:", "v": "las paredes altas que caen sobre el mar."},
        {"t": "li", "b": "Dunas:", "v": "la arena que el viento mueve y acumula."},
        {"t": "li", "b": "Marismas:", "v": "las zonas bajas que la marea cubre y descubre."},
        {"t": "fig", "f": "foto-02.jpg", "clase": "fig--g8"},
        {"t": "h3", "v": "La flora"},
        {"t": "p", "v": "La vegetación es típica de la estepa patagónica: pastizales halófilos (resistentes al suelo con sal), arbustos bajos adaptados al clima frío y plantas halófitas, que crecen donde hay mucha salinidad cerca de la costa."},
        {"t": "h3", "v": "La fauna"},
        {"t": "p", "v": "El Cóndor tiene más de 200 especies de aves y una buena variedad de fauna costera y esteparia: loros barranqueros, gaviotas, lobos marinos, delfines, orcas, maras, zorros, choiques, ovejas, tortugas terrestres y zorrinos."},
        {"t": "fig", "f": "foto-03.jpg", "clase": "fig--g8"},
        {"t": "h3", "v": "Dos espacios protegidos"},
        {"t": "p", "v": "En la zona tenemos dos espacios protegidos para resguardar la naturaleza y las especies:"},
        {"t": "li", "b": "Reserva Natural Municipal Acantilado de Los Loros:", "v": "resguarda los acantilados donde nidifican los loros barranqueros."},
        {"t": "li", "b": "Punta Bermeja («La Lobería»):", "v": "protege a los lobos marinos."},
        {"t": "h3", "v": "El loro barranquero, el ave emblemática"},
        {"t": "p", "v": "El loro barranquero (Cyanoliseus patagonus) es el ave típica y más emblemática del balneario. ¡El Cóndor tiene la colonia de loros barranqueros más grande del mundo!"},
        {"t": "h3", "v": "El artículo original"},
        {"t": "p", "v": "Así quedó armado el trabajo que presentamos en Científica y Tecnológica, con las fotos y el diseño que hicimos en clase."},
        {"t": "fig", "f": "articulo-original.png", "clase": "fig--mediana"},
        {"t": "firma", "v": "Francisco Casanoba, Mateo Lefinir y Randi Piccinini Ramos · 1.º año · Sede El Cóndor"},
    ],
    "fotos": [n for _s, n in FOTOS1],
    "fotos_disposicion": ["fig", "fig", "fig"],
    "epigrafes": ["", "", ""],
}

# ---------------------------------------------------------------- artículo 2
UID2 = "hablamos-con-un-veterano-kakel-huincul"
FOTOS2 = [
    (os.path.join(TMP, "img02.png"), "foto-01.jpg"),
    (os.path.join(TMP, "img03.png"), "foto-02.jpg"),
]

ART2 = {
    "id": UID2,
    "seccion": "voces",
    "titulo": "Hablamos con un veterano cerca de Kakel Huincul",
    "bajada": "Visitamos a don Marcial Torres, un gaucho de la Línea Sur que vive en Cerro Cura Uf: cómo se prepara para el invierno, cómo cuida a sus animales y qué les pide a las generaciones que vienen.",
    "autor": "Sosa Torres Marcial",
    "rol": "Estudiante · Clase 10",
    "sede": "Colán Conhue",
    "fecha": "Diciembre 2026",
    "fecha_iso": "2026-12-01",
    "odt": None,
    "cuerpo": [
        {"t": "pregunta", "v": "¿Conocías a gente de esta zona? Entérate de cómo sobrevive con sus animales y cómo se prepara antes del invierno."},
        {"t": "cita", "v": "Aprender de ellos es saber valorar sus trabajos de manera digna y sin rencores."},
        {"t": "p", "v": "Visitamos a don Marcial Torres, un gaucho como cualquiera pero no de cualquier lugar. Él está ubicado junto a su familia en la Línea Sur, específicamente en el 25 de Mayo, cerca de Kakel Huincul. Al presentarnos nos cuenta lo que le ha tocado vivir: empezó a trabajar a los 7 años y hoy tiene 77 años de experiencia, y nunca se fue de este paraje llamado Cerro Cura Uf. Ha vivido cosas que hoy ya no son las mismas, por suerte: dificultades climáticas, despoblación de animales, problemas de construcción a causa de los ventarrones."},
        {"t": "h3", "v": "Prepararse antes del invierno"},
        {"t": "p", "v": "Hasta el día de hoy lo sigue sobrellevando con estos fríos grandes. Nos cuenta cómo se preparan antes del invierno: traen los recursos necesarios como mercadería (harina, yerba, fideos, arroz), leña, gas y forraje para los animales. Además, sueltan los castrones y carneros en el mes de mayo, refuerzan los corrales y las ramadas para guardar a los caballos, las chivas y las ovejas, y se abastecen de ropa para las bajas temperaturas, iluminación para la casa y linternas para la noche."},
        {"t": "h3", "v": "La salud de los animales"},
        {"t": "p", "v": "Como están cerca de la época de parición, le preguntamos por las medidas de seguridad para los animales. Nos dice que solo usan bañaderas y vacunas en caso de garrapatas, boquera y sarna. No suelen aparecer otras enfermedades, así que solo compran esos remedios. Para la boquera usan remedios caseros como aceite comestible; y si les agarra a los corderos machos se les pela la cola, y a las corderas la panza, para que no se siga propagando. Solo si no tienen los remedios que se compran —pietín, pedero o pododermatitis— recurren a ellos."},
        {"t": "h3", "v": "Los chivos y los yeguarizos"},
        {"t": "p", "v": "Con los chivos no es común que se enfermen, a menos que les agarre colitis o se pulguen: solo usan agua dulce, porque no se compran remedios para ese tipo de enfermedades. Por eso nos dice que los animales cabríos son más llevaderos. Los yeguarizos solo se desparasitan con vacunas o inyectables, pero no más que eso."},
        {"t": "h3", "v": "La parición"},
        {"t": "p", "v": "En el tiempo de parición también se preparan, a fines de septiembre, más que nada con los chivos. Con estas lluvias viven situaciones malas, como que se les muera una cría de frío al no poder encontrar dónde nació. Lo que los ayuda es la ramada hecha con techo de chapas y bien forrada con nailon y maderas, dividida en tres partes: para apartar las chivas recién paridas, las que están por tener cría y las que ya tenían cría. Así se organizan mejor. Al sacarlas por la mañana uno tiene que salir a pastorearlas y traer uno o dos chivitos; si hay más que traer, tienen que salir tres, y así se hace más fácil."},
        {"t": "fig", "f": "foto-02.jpg", "clase": "fig--g8"},
        {"t": "h3", "v": "Convivir con los animales salvajes"},
        {"t": "p", "v": "Queremos saber si se puede sostener el equilibrio con los animales salvajes como zorros, pumas o zorrinos, y nos dice:"},
        {"t": "cita", "v": "«Por suerte no nos ha tocado eso de las plagas, porque este lugar es llano, por eso no paran acá esos animales. También es que se anda mucho en estos lugares, ya que es un cuadro (alambrado) chico y por eso no vienen acá.»"},
        {"t": "p", "v": "Fuera del diálogo nos cuenta también que usan métodos simples, como andar siempre con perras, y por eso no los atacan de manera fácil. Parece que la sufren mucho en estos casos, pero por eso no piden veterinarios ni cazadores: van acompañados de lo que les dejaron los mayores."},
        {"t": "h3", "v": "Su mensaje para los que vienen"},
        {"t": "cita", "v": "«Lo único que les voy a decir a los que vienen este año es que aprendan lo que les enseñan y valoren los trabajos que hacemos, pero nunca olviden lo que nos dejaron nuestros ancestros.»"},
        {"t": "firma", "v": "Sosa Torres Marcial · Sede Colán Conhue (Anexo ESRN N.º 36) · Tutor: Maicol Carballo"},
    ],
    "fotos": [n for _s, n in FOTOS2],
    "fotos_disposicion": ["portada", "fig"],
    "epigrafes": ["", ""],
}

# ------------------------------------------------------------------- ejecutar
d = json.load(open(P_JSON, encoding="utf-8"))
existentes = {a.get("id") for a in d["articulos"]}
d["articulos"] = [a for a in d["articulos"] if a.get("id") not in (UID1, UID2)]

for art, fotos in ((ART1, FOTOS1), (ART2, FOTOS2)):
    art_dir = os.path.join(EDIT, art["id"])
    os.makedirs(art_dir, exist_ok=True)
    for src, nombre in fotos:
        dst = os.path.join(art_dir, nombre)
        kb = guardar_jpg(src, dst)
        print("  foto -> %s/%s (%.0f KB)" % (art["id"], nombre, kb / 1024))
    d["articulos"].append(art)

# El artículo original tal como lo entregaron (imagen completa de la página),
# se muestra al final del artículo de El Cóndor.
PNG_ORIG = None
for entry in os.scandir(r"C:\Users\black\Desktop\opencode archivos\articulos 4-11"):
    if entry.is_dir() and entry.name.startswith("Artículo revista"):
        for e2 in os.scandir(entry.path):
            if e2.name.lower().endswith(".png"):
                PNG_ORIG = e2.path
if PNG_ORIG:
    import shutil
    dst = os.path.join(EDIT, UID1, "articulo-original.png")
    shutil.copy2("\\\\?\\" + os.path.abspath(PNG_ORIG), dst)
    print("  original -> %s (%.0f KB)" % (os.path.basename(dst), os.path.getsize(dst) / 1024))

open(P_JSON, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
print("== total articulos: %d ==" % len(d["articulos"]))
por_sec = {}
for a in d["articulos"]:
    por_sec[a.get("seccion")] = por_sec.get(a.get("seccion"), 0) + 1
print("== por seccion:", por_sec)
