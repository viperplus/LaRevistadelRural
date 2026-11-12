# -*- coding: utf-8 -*-
"""Integra el articulo 'El patio de todos: Mencue' en la revista."""
import os, json, shutil, unicodedata

BASE = r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista"
SRC_DIR = r"C:\Users\black\Desktop\articulos nuevos\Luciana Calfupan- Mencué"
EDIT = os.path.join(BASE, "ediciones", "01")
DATOS = os.path.join(BASE, "datos", "ediciones.json")

UID = "el-patio-de-todos-mencue"
SECCION = "ciencia"

cuerpo_txt = [
 ("p", "Durante estos últimos años, la limpieza de nuestro pueblo ha mejorado muchísimo. No solo porque la cantidad de basura en las calles se redujo, sino porque entre los pobladores, la Escuela y la Comisión de Fomento nos propusimos tener un patio más limpio."),
 ("p", "Para que esto suceda, contamos con la ayuda de los trabajadores de la Comisión de Fomento, quienes pasan a retirar la basura de nuestros domicilios. En casa, vamos juntando los residuos en el tacho, con bolsas de consorcio, para luego llevarlos al basurero local. Además, algunos vecinos se ocupan de llevar su propia basura directamente al basurero."),
 ("p", "En este año, la Comisión de Fomento se propuso limpiar y mantener la plaza principal, así como los terrenos públicos e institucionales. También salieron a recorrer los cerros para juntar nylos y bolsas que estaban desparramados."),
 ("p", "Por su parte, la Escuela Primaria realizó una jornada sobre cómo cuidar nuestro medio ambiente y dejó a disposición cuatro cestos de basura en la plaza principal, donde se separan por sector: botellas, latas, tapitas."),
 ("pregunta", "Y si vinieras a nuestro pueblo, sabiendo cómo se maneja la limpieza... ¿Te sumarías a nuestras ideas, por el bien de tu localidad?"),
]

art = {
    "id": UID,
    "seccion": SECCION,
    "titulo": "El patio de todos: Mencué",
    "bajada": "¿Cómo nos organizamos con la limpieza de nuestro pueblo? Le invitamos a conocer cómo nos organizamos con la limpieza de nuestro pueblo.",
    "autor": "Luciana y Milagros Calfupan",
    "rol": "Estudiantes 4° año — Sede Mencué",
    "sede": "Mencué",
    "anio": "4° año",
    "fecha": "Noviembre 2026",
    "fecha_iso": "2026-11-12",
    "foto_principal": "%s/%s/%s" % (SECCION, UID, "foto-01.jpg"),
    "fotos": ["foto-01.jpg", "foto-02.jpg"],
    "fotos_disposicion": ["portada", "galeria"],
    "epigrafes": ["", ""],
    "cuerpo": [{"t": t, "v": v} for t, v in cuerpo_txt],
}

# copiar fotos
dst = os.path.join(EDIT, UID)
os.makedirs(dst, exist_ok=True)
src_fotos = [os.path.join(SRC_DIR, "1.jpg"), os.path.join(SRC_DIR, "2.jpg")]
for src, nom in zip(src_fotos, art["fotos"]):
    shutil.copy2(src, os.path.join(dst, nom))
    print("copiada", src, "->", os.path.join(dst, nom))

# agregar al json (evitar duplicado)
datos = json.load(open(DATOS, encoding="utf-8"))
ids = {x["id"] for x in datos["articulos"]}
if UID in ids:
    print("ya estaba, no se duplica")
else:
    datos["articulos"].append(art)
    with open(DATOS, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("agregado. total articulos:", len(datos["articulos"]))
print("id:", UID)
