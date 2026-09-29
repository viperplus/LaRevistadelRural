#!/usr/bin/env python3
"""Copiar fotos desde enviar_aqui/imagenes_odt a artículos sin fotos."""
import json, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')
EDIT = os.path.join(BASE, 'ediciones', '01')
SRC = r'C:\Users\black\Desktop\opencode archivos\clase n°4\enviar_aqui\imagenes_odt'

# Mapeo: article_id -> carpeta en enviar_aqui/imagenes_odt
MAPEO = {
    'el-cuidado-del-agua': 'c_mo_es_la_potabilizaci_n_en_el_paraje_a',
    'tecnologia-mundialista': 'culturas_de_campeones',
    'no-a-la-basura': 'clase_n_9_taller_de_educaci_n_cient_fica',
    'latido_del_equilibrio_ambiental_en_naupa_huen': 'clase_9_braiton_rocha_valle_verde_a32_ci',
    'acciones_peque_as_para_un_mundo_grande': 'leonel_godoy_valle_verde_clase_9_cientif',
    'los_festejos_de_una_localidad': 'fiestas_y_tradiciones_mundialistas',
}

with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    uid = art['id']
    
    # Solo procesar artículos sin fotos
    if art.get('fotos'):
        continue
    
    if uid not in MAPEO:
        print(f'{uid}: SIN MAPEO')
        continue
    
    carpeta = MAPEO[uid]
    src_dir = os.path.join(SRC, carpeta)
    
    if not os.path.isdir(src_dir):
        print(f'{uid}: Carpeta no encontrada: {carpeta}')
        continue
    
    imgs = sorted([f for f in os.listdir(src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    if not imgs:
        print(f'{uid}: Sin fotos en {carpeta}')
        continue
    
    # Limitar a 6 fotos
    imgs = imgs[:6]
    
    os.makedirs(os.path.join(EDIT, uid), exist_ok=True)
    fotos = []
    for i, img in enumerate(imgs, 1):
        ext = os.path.splitext(img)[1]
        dst = os.path.join(EDIT, uid, f'foto-{i:02d}{ext}')
        shutil.copy2(os.path.join(src_dir, img), dst)
        fotos.append(f'foto-{i:02d}{ext}')
    
    art['fotos'] = fotos
    art['epigrafes'] = [''] * len(fotos)
    print(f'{uid}: {len(fotos)} fotos copiadas')

# Guardar
with open(DATOS, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Regenerar
sys.path.insert(0, BASE)
from construir_revista_v2 import main as generar
generar()
print('Listo!')
