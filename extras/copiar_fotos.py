#!/usr/bin/env python3
import json, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')
PDF_BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTÍCULOS PDF'
IMG_BASE = os.path.join(BASE, 'ediciones', '01', 'imagenes')

# Mapeo: carpeta -> (articulo_id, prefijo fotos en ediciones)
mapeo = {
    'Nueva carpeta': 'cuidemos-el-ambiente',
    'Nueva carpeta (2)': 'cuidemos-nuestro-ambiente-maia',
    'Nueva carpeta (3)': 'no-solo-un-encuentro-de-sedes',
    'Nueva carpeta (4)': 'hay-algo-mas-en-las-fotos',
    'Nueva carpeta (5)': 'monoxido-de-carbono-aguada-cecilio',
    'Nueva carpeta (6)': 'la-contaminacion',
    'Nueva carpeta (7)': 'monoxido-de-carbono-pame',
    'Nueva carpeta (8)': 'no-a-la-basura',
    'Nueva carpeta (9)': 'cuidar-el-ambiente-kral',
    'Nueva carpeta (10)': 'yaminue-conexion-naturaleza',
    'Nueva carpeta (11)': 'que-pasaria-sin-agua',
    'Nueva carpeta (12)': 'cuidar-nuestro-ambiente-seco',
}

with open(os.path.join(DATOS, 'ediciones.json'), encoding='utf-8') as f:
    data = json.load(f)

for carpeta, art_id in mapeo.items():
    src_dir = os.path.join(PDF_BASE, carpeta)
    if not os.path.exists(src_dir):
        continue
    
    # Buscar imágenes
    imgs = sorted([f for f in os.listdir(src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    if not imgs:
        continue
    
    # Crear carpeta destino
    dst_dir = os.path.join(IMG_BASE, art_id)
    os.makedirs(dst_dir, exist_ok=True)
    
    # Copiar y renombrar
    fotos = []
    epigrafes = []
    for i, img in enumerate(imgs, 1):
        ext = os.path.splitext(img)[1].lower()
        dst_file = os.path.join(dst_dir, f'foto_{i:02d}{ext}')
        shutil.copy2(os.path.join(src_dir, img), dst_file)
        fotos.append(f'imagenes/{art_id}/foto_{i:02d}{ext}')
        epigrafes.append('')
        print(f'  {art_id}: foto_{i:02d}{ext}')
    
    # Actualizar artículo
    for art in data['articulos']:
        if art['id'] == art_id:
            art['fotos'] = fotos
            art['epigrafes'] = epigrafes
            break

with open(os.path.join(DATOS, 'ediciones.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Regenerar
sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
