#!/usr/bin/env python3
import json, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')
EDIT = os.path.join(BASE, 'ediciones', '01')
ODT = os.path.join(BASE, 'odt')

# Fuente correcta para gol-de-ciencia
FUENTE = 'clase_n°9_cientifica_y_tecnologica_rio_chico_gaminao_aaron_e'

src_dir = os.path.join(ODT, FUENTE)
dst_dir = os.path.join(EDIT, 'gol-de-ciencia')

# Limpiar fotos viejas
for f in os.listdir(dst_dir):
    if f.startswith('foto-'):
        os.remove(os.path.join(dst_dir, f))

# Copiar fotos nuevas
imgs = sorted([f for f in os.listdir(src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
for i, img in enumerate(imgs[:5], 1):  # Max 5 fotos
    ext = os.path.splitext(img)[1]
    dst = os.path.join(dst_dir, f'foto-{i:02d}{ext}')
    shutil.copy2(os.path.join(src_dir, img), dst)
    print(f'Copiado: {img} -> foto-{i:02d}{ext}')

# Actualizar JSON
with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    if art['id'] == 'gol-de-ciencia':
        art['fotos'] = [f'foto-{i:02d}.png' for i in range(1, min(len(imgs), 5) + 1)]
        print(f'Actualizado JSON: {art["fotos"]}')

with open(DATOS, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Regenerar
sys.path.insert(0, BASE)
from construir_revista_v2 import main as generar
generar()
print('Listo!')
