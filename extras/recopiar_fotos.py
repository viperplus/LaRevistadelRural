#!/usr/bin/env python3
"""Recopiar fotos desde fuentes originales a cada carpeta de artículo."""
import json, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')
EDIT = os.path.join(BASE, 'ediciones', '01')
ODT = os.path.join(BASE, 'odt')
PDF = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTÍCULOS PDF'

# Mapeo artículo -> carpeta ODT (solo las que existen)
MAPEO_ODT = {
    'cuidemos-el-ambiente': 'cient_fica_y_tecnol_gica_clase_n°9_4to_a_o_saira_linares_lag',
    'cuidemos-nuestro-ambiente-maia': 'cientifica_y_tecnologica_clase_9_maia_oses_de_4°a_o_de_la_se',
    'la-contaminacion': 'clase_9_cientifica_y_tecnologica_guadalupe_centeno_lago_pell',
    'monoxido-de-carbono-aguada-cecilio': 'clase_9_fatima_hernadez_erika_pil_aguada_cecilio_4to_a_o',
    'monoxido-de-carbono-pame': 'clase_n°9_cientifica_y_tecnologica_4°a_o_pame_loncoman_mencu',
    'cuidar-el-ambiente-kral': 'kral_milena_4to_a_o_lago_pellegrini_educaci_n_cient_fica_y_t',
    'que-pasaria-sin-agua': 'medrano_julieta_4to_a_o_clase_9_cientifica_y_tecnologica_lag',
}

# Mapeo artículo -> carpeta PDF
MAPEO_PDF = {
    'no-solo-un-encuentro-de-sedes': 'Nueva carpeta (3)',
    'yaminue-conexion-naturaleza': 'Nueva carpeta (11)',
    'la-fiesta-del-paraje-treneta': 'Nueva carpeta (1)',
    'próxima-parada-atractivos-mundialistas': 'Nueva carpeta (2)',
    'el-chip-en-la-cancha': 'Nueva carpeta (4)',
    'la-primera-ley-de-newton': 'Nueva carpeta (5)',
    'el-partido-por-el-ambiente': 'Nueva carpeta (6)',
    'los-festejos-de-una-localidad': 'Nueva carpeta (7)',
    'medio-ambiente-sierra-paileman': 'Nueva carpeta (8)',
    'la-llegada-de-la-primavera': 'Nueva carpeta (9)',
    'gol-de-ciencia': 'Nueva carpeta (10)',
    'potabilizacion-aguada-guzman': 'Nueva carpeta (12)',
    'una-mirada-sobre-la-realidad': 'Nueva carpeta (13)',
    'cuidar-nuestro-ambiente-seco': 'Nueva carpeta (14)',
    'no-a-la-basura': 'Nueva carpeta (15)',
    'hay-algo-mas-en-las-fotos': 'Nueva carpeta (16)',
    'el-cuidado-del-agua': 'Nueva carpeta (17)',
    'tecnologia-mundialista': 'Nueva carpeta (18)',
}

with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    uid = art['id']
    art_dir = os.path.join(EDIT, uid)
    os.makedirs(art_dir, exist_ok=True)
    
    fotos = art.get('fotos', [])
    if not fotos:
        print(f'{uid}: sin fotos en JSON, buscando en fuentes...')
        continue
    
    # Copiar cada foto
    for i, fpath in enumerate(fotos, 1):
        # Determinar fuente original
        basename = os.path.basename(fpath)
        
        # Buscar en ODT
        if uid in MAPEO_ODT:
            src = os.path.join(ODT, MAPEO_ODT[uid], basename)
            if os.path.isfile(src):
                ext = os.path.splitext(basename)[1]
                dst_name = f'foto-{i:02d}{ext}'
                shutil.copy2(src, os.path.join(art_dir, dst_name))
                print(f'{uid}: {dst_name} desde ODT')
                continue
        
        # Buscar en PDF folders
        if uid in MAPEO_PDF:
            src = os.path.join(PDF, MAPEO_PDF[uid], basename)
            if os.path.isfile(src):
                ext = os.path.splitext(basename)[1]
                dst_name = f'foto-{i:02d}{ext}'
                shutil.copy2(src, os.path.join(art_dir, dst_name))
                print(f'{uid}: {dst_name} desde PDF')
                continue
        
        print(f'{uid}: NO ENCONTRADO {basename}')

print('Listo!')
