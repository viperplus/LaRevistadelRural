#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')

with open(os.path.join(DATOS, 'ediciones.json'), encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    fotos = art.get('fotos', [])
    nuevas = []
    for f in fotos:
        if f.startswith('imagenes/'):
            f = '../' + f
        nuevas.append(f)
    if nuevas != fotos:
        art['fotos'] = nuevas
        print(f'{art["id"]}: corregido')

with open(os.path.join(DATOS, 'ediciones.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
