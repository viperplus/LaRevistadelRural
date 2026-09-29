#!/usr/bin/env python3
import json, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')
IMG_SRC = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTÍCULOS PDF\Nueva carpeta (10)'
IMG_DST = os.path.join(BASE, 'ediciones', '01', 'imagenes', 'yaminue-conexion-naturaleza')

os.makedirs(IMG_DST, exist_ok=True)

# Copiar imagenes PNG
fotos = []
for f in sorted(os.listdir(IMG_SRC)):
    if f.endswith('.png'):
        src = os.path.join(IMG_SRC, f)
        dst = os.path.join(IMG_DST, f'foto_{len(fotos)+1:02d}.png')
        shutil.copy2(src, dst)
        fotos.append(f'imagenes/yaminue-conexion-naturaleza/foto_{len(fotos)+1:02d}.png')
        print(f'  Copiada: {f}')

cuerpo = [
    {"t": "p", "v": "Yaminué es un lugar donde la naturaleza y la vida cotidiana se encuentran. En este articulo, podemos ver algunos de los espacios que hacen especial a este paraje."},
    {"t": "h3", "v": "Conexion con la naturaleza"},
    {"t": "p", "v": "Aca podemos ver como Yamine tiene conexion con la naturaleza."},
    {"t": "h3", "v": "Barrio local"},
    {"t": "p", "v": "Aca se localiza uno de los barrios de Yamine."},
    {"t": "h3", "v": "Viviendas de los habitantes"},
    {"t": "p", "v": "En esta foto se puede apreciar como algunas casas de sus habitantes se ven, tambien se alcanza a ver como estos humildes vecinos acceden a sus casas."},
    {"t": "h3", "v": "El puente"},
    {"t": "p", "v": "Este es el puente de Yamine, uno de los lugares mas destacados."},
    {"t": "h3", "v": "El arroyo"},
    {"t": "p", "v": "Este es el arroyo, pero aca le decimos catarata; es uno de los lugares donde en el verano mas se disfruta."},
]

art = {
    "id": "yaminue-conexion-naturaleza",
    "seccion": "territorio",
    "titulo": "Yamine: conexion con la naturaleza",
    "bajada": "Un recorrido por los espacios mas destacados de Yamine: el barrio, las viviendas, el puente y el arroyo.",
    "autor": "Marrone e Rosso",
    "rol": "Estudiantes 4. ano",
    "sede": "Yamine",
    "fecha": "Noviembre 2026",
    "odt": None,
    "cuerpo": cuerpo,
    "fotos": fotos,
    "epigrafes": [
        "Conexion con la naturaleza en Yamine.",
        "Barrio local de Yamine.",
        "Viviendas de los habitantes.",
        "El puente de Yamine.",
        "El arroyo, conocido como catarata."
    ]
}

ediciones_path = os.path.join(DATOS, 'ediciones.json')
with open(ediciones_path, encoding='utf-8') as f:
    ediciones = json.load(f)

# Agregar articulo
ediciones['articulos'].append(art)

with open(ediciones_path, 'w', encoding='utf-8') as f:
    json.dump(ediciones, f, ensure_ascii=False, indent=2)

print(f'Agregado: {art["id"]} - {art["titulo"]}')
print(f'Fotos: {len(fotos)}')

# Regenerar
sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
