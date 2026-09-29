#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')

with open(os.path.join(DATOS, 'ediciones.json'), encoding='utf-8') as f:
    data = json.load(f)

# Limitar monoxido-de-carbono-pame a 5 fotos
for art in data['articulos']:
    if art['id'] == 'monoxido-de-carbono-pame':
        art['fotos'] = art['fotos'][:5]
        art['epigrafes'] = [''] * 5
        print(f'Limitado: {art["id"]} a 5 fotos')

with open(os.path.join(DATOS, 'ediciones.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
