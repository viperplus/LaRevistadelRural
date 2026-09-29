#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')
EDIT = os.path.join(BASE, 'ediciones', '01')

with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    uid = art['id']
    art_dir = os.path.join(EDIT, uid)
    if not os.path.isdir(art_dir):
        continue
    
    # Buscar fotos reales en la carpeta
    fotos_reales = sorted([f for f in os.listdir(art_dir) if f.startswith('foto-') and os.path.isfile(os.path.join(art_dir, f))])
    
    if fotos_reales:
        art['fotos'] = fotos_reales
        print(f'{uid}: {len(fotos_reales)} fotos actualizadas')
    else:
        art['fotos'] = []
        print(f'{uid}: sin fotos')

with open(DATOS, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('JSON actualizado. Regenerando...')
sys.path.insert(0, BASE)
from construir_revista_v2 import main as generar
generar()
print('Listo!')
