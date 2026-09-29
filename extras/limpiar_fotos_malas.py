#!/usr/bin/env python3
"""Eliminar fotos de artículos donde las fotos no corresponden al contenido."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')
EDIT = os.path.join(BASE, 'ediciones', '01')

# Artículos donde las fotos NO corresponden al contenido
SIN_FOTOS = [
    'la-contaminacion',          # Fotos de una-mirada-sobre-la-realidad
    'una-mirada-sobre-la-realidad',  # Fotos de la-contaminacion
    'nueva_carpeta_8',           # Fotos de la_primera_ley_de_newton (debería ser paisajes)
    'tecnologia-mundialista',    # Fotos de fiestas mundialistas (debería ser tecnología)
    'no-a-la-basura',            # Solo 1 foto que no corresponde
    'el-cuidado-del-agua',       # Solo 1 foto que no corresponde
    'gol-de-ciencia',            # Solo 1 foto que no corresponde
    'la-llegada-de-la-primavera', # Solo 1 foto que no corresponde
]

with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    uid = art['id']
    
    if uid not in SIN_FOTOS:
        continue
    
    # Eliminar fotos del disco
    art_dir = os.path.join(EDIT, uid)
    if os.path.isdir(art_dir):
        for f in os.listdir(art_dir):
            if f.startswith('foto-'):
                os.remove(os.path.join(art_dir, f))
    
    # Limpiar JSON
    art['fotos'] = []
    art['epigrafes'] = []
    print(f'{uid}: fotos eliminadas')

# Guardar
with open(DATOS, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Regenerar
sys.path.insert(0, BASE)
from construir_revista_v2 import main as generar
generar()
print('¡LISTO!')
