#!/usr/bin/env python3
import json, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')
SRC = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTÍCULOS PDF\Nueva carpeta (3)'
DST = os.path.join(BASE, 'ediciones', '01', 'imagenes', 'que-pasaria-sin-agua')

os.makedirs(DST, exist_ok=True)

fotos = []
for i, f in enumerate(['2.png', '3.png'], 1):
    ext = os.path.splitext(f)[1]
    nombre = f'foto-{i:02d}{ext}'
    shutil.copy2(os.path.join(SRC, f), os.path.join(DST, nombre))
    fotos.append(f'imagenes/que-pasaria-sin-agua/{nombre}')

with open(os.path.join(DATOS, 'ediciones.json'), encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    if art['id'] == 'que-pasaria-sin-agua':
        art['fotos'] = fotos
        art['epigrafes'] = ['', '']
        print(f'Fotos agregadas: {fotos}')

with open(os.path.join(DATOS, 'ediciones.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
