#!/usr/bin/env python3
"""Copiar TODAS las fotos disponibles a artículos sin fotos."""
import json, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')
EDIT = os.path.join(BASE, 'ediciones', '01')
SRC_BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4'

with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

# Buscar todas las fotos disponibles en el proyecto
todas_las_fotos = []
for root, dirs, files in os.walk(SRC_BASE):
    # Saltar carpetas de edición y css
    if 'ediciones' in root or 'css' in root:
        continue
    for f in files:
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            todas_las_fotos.append(os.path.join(root, f))

print(f'Total fotos encontradas: {len(todas_las_fotos)}')

# Mapeo de carpetas fuente para cada artículo
MAPEO_FOTOS = {
    # Artículos originales (de carpetas ODT/PDF)
    'la-primera-ley-de-newton': 'la-primera-ley-de-newton',
    'próxima-parada-atractivos-mundialistas': 'próxima-parada-atractivos-mundialistas',
    'los-festejos-de-una-localidad': 'los-festejos-de-una-localidad',
    'el-cuidado-del-agua': 'el-cuidado-del-agua',
    'tecnologia-mundialista': 'tecnologia-mundialista',
    'no-a-la-basura': 'no-a-la-basura',
    
    # Artículos 2do año (de ARTICULOS 2DO AÑO)
    '1_reflexi_n_a_trav_s_de_fotograf_a': 'ARTICULOS 2DO AÑO\\Nueva carpeta (11)',
    'la_primera_ley_de_newton': 'ARTICULOS 2DO AÑO\\Nueva carpeta (8)',
    'latido_del_equilibrio_ambiental_en_naupa_huen': 'ARTICULOS 2DO AÑO\\Nueva carpeta (5)',
    'acciones_peque_as_para_un_mundo_grande': 'ARTICULOS 2DO AÑO\\Nueva carpeta (6)',
    'reflexi_n_a_trav_s_de_fotograf_a': 'ARTICULOS 2DO AÑO\\Nueva carpeta (11)',
    'los_festejos_de_una_localidad': 'ARTICULOS 2DO AÑO\\Nueva carpeta (13)',
    'arroyo_los_berros': 'ARTICULOS 2DO AÑO\\Nueva carpeta',
    'nueva_carpeta_10': 'ARTICULOS 2DO AÑO\\Nueva carpeta (10)',
    'clase_n_10_cient_fica_y_tecnol_gica': 'ARTICULOS 2DO AÑO\\Nueva carpeta (9)',
    'nueva_carpeta_12': 'ARTICULOS 2DO AÑO\\Nueva carpeta (12)',
    'nueva_carpeta_2': 'ARTICULOS 2DO AÑO\\Nueva carpeta (2)',
    'nueva_carpeta_3': 'ARTICULOS 2DO AÑO\\Nueva carpeta (3)',
    'clase_n_10_espacio_curricular_ed_cient_fica_y_tecn': 'ARTICULOS 2DO AÑO\\Nueva carpeta (4)',
    'clase_n_10_cient_fica_y_tecnol_gicaintegrantes_agu': 'ARTICULOS 2DO AÑO\\Nueva carpeta (7)',
    'nueva_carpeta_8': 'ARTICULOS 2DO AÑO\\Nueva carpeta (8)',
}

for art in data['articulos']:
    uid = art['id']
    
    # Solo procesar artículos sin fotos
    if art.get('fotos'):
        continue
    
    if uid not in MAPEO_FOTOS:
        print(f'{uid}: SIN MAPEO')
        continue
    
    carpeta = MAPEO_FOTOS[uid]
    
    # Buscar carpeta fuente
    if carpeta.startswith('ARTICULOS'):
        src_dir = os.path.join(SRC_BASE, carpeta)
    else:
        # Buscar en carpetas ODT y PDF
        src_dir = None
        for search_dir in ['revista\\odt', 'ARTÍCULOS PDF']:
            candidate = os.path.join(SRC_BASE, search_dir, carpeta)
            if os.path.isdir(candidate):
                src_dir = candidate
                break
    
    if src_dir and os.path.isdir(src_dir):
        imgs = sorted([f for f in os.listdir(src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        
        if imgs:
            os.makedirs(os.path.join(EDIT, uid), exist_ok=True)
            fotos = []
            for i, img in enumerate(imgs, 1):
                ext = os.path.splitext(img)[1]
                dst = os.path.join(EDIT, uid, f'foto-{i:02d}{ext}')
                shutil.copy2(os.path.join(src_dir, img), dst)
                fotos.append(f'foto-{i:02d}{ext}')
            
            art['fotos'] = fotos
            art['epigrafes'] = [''] * len(fotos)
            print(f'{uid}: {len(fotos)} fotos copiadas desde {carpeta}')
        else:
            print(f'{uid}: Sin fotos en {carpeta}')
    else:
        print(f'{uid}: Carpeta no encontrada: {carpeta}')

# Guardar
with open(DATOS, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Regenerar
sys.path.insert(0, BASE)
from construir_revista_v2 import main as generar
generar()
print('Listo!')
