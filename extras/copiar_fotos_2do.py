#!/usr/bin/env python3
"""Copiar fotos de ARTICULOS 2DO AÑO a las carpetas de artículos."""
import json, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')
EDIT = os.path.join(BASE, 'ediciones', '01')
SRC = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTICULOS 2DO AÑO'

# Mapeo artículo -> carpeta origen
MAPEO = {
    'nueva_carpeta_10': 'Nueva carpeta (10)',
    'nueva_carpeta_12': 'Nueva carpeta (12)',
    'nueva_carpeta_2': 'Nueva carpeta (2)',
    'nueva_carpeta_3': 'Nueva carpeta (3)',
    'nueva_carpeta_8': 'Nueva carpeta (8)',
    'clase_n_10_cient_fica_y_tecnol_gica': 'Nueva carpeta (9)',
    'clase_n_10_cient_fica_y_tecnol_gicaintegrantes_agu': 'Nueva carpeta (7)',
    'clase_n_10_espacio_curricular_ed_cient_fica_y_tecn': 'Nueva carpeta (4)',
    'arroyo_los_berros': 'Nueva carpeta',
    'latido_del_equilibrio_ambiental_en_naupa_huen': None,  # ODT
    'acciones_peque_as_para_un_mundo_grande': None,  # ODT
    'los_festejos_de_una_localidad': None,  # ODT
}

with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    uid = art['id']
    if uid not in MAPEO:
        continue
    
    carpeta = MAPEO[uid]
    if carpeta is None:
        continue
    
    src_dir = os.path.join(SRC, carpeta)
    dst_dir = os.path.join(EDIT, uid)
    
    if not os.path.isdir(src_dir):
        print(f'{uid}: No existe {src_dir}')
        continue
    
    # Buscar fotos
    imgs = sorted([f for f in os.listdir(src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    if not imgs:
        print(f'{uid}: Sin fotos en {carpeta}')
        continue
    
    os.makedirs(dst_dir, exist_ok=True)
    
    fotos = []
    for i, img in enumerate(imgs, 1):
        ext = os.path.splitext(img)[1]
        dst = os.path.join(dst_dir, f'foto-{i:02d}{ext}')
        shutil.copy2(os.path.join(src_dir, img), dst)
        fotos.append(f'foto-{i:02d}{ext}')
    
    art['fotos'] = fotos
    art['epigrafes'] = [''] * len(fotos)
    print(f'{uid}: {len(fotos)} fotos copiadas')

with open(DATOS, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Regenerar
sys.path.insert(0, BASE)
from construir_revista_v2 import main as generar
generar()
print('Listo!')
