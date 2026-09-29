#!/usr/bin/env python3
import json, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')
ODT = os.path.join(BASE, 'odt')
IMGDIR = os.path.join(BASE, 'ediciones', '01', 'imagenes')

# Mapeo artículo -> carpeta ODT
MAPEO_ODT = {
    'cuidemos-el-ambiente': 'cient_fica_y_tecnol_gica_clase_n°9_4to_a_o_saira_linares_lag',
    'cuidemos-nuestro-ambiente-maia': 'cientifica_y_tecnologica_clase_9_maia_oses_de_4°a_o_de_la_se',
    'la-contaminacion': 'clase_9_cientifica_y_tecnologica_guadalupe_centeno_lago_pell',
    'monoxido-de-carbono-aguada-cecilio': 'clase_9_fatima_hernadez_erika_pil_aguada_cecilio_4to_a_o',
    'monoxido-de-carbono-pame': 'clase_n°9_cientifica_y_tecnologica_4°a_o_pame_loncoman_mencu',
    'cuidar-el-ambiente-kral': 'kral_milena_4to_a_o_lago_pellegrini_educaci_n_cient_fica_y_t',
    'que-pasaria-sin-agua': 'medrano_julieta_4to_a_o_clase_9_cientifica_y_tecnologica_lag',
}

with open(os.path.join(DATOS, 'ediciones.json'), encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    aid = art['id']
    if aid in MAPEO_ODT:
        carpeta = MAPEO_ODT[aid]
        src = os.path.join(ODT, carpeta)
        if not os.path.isdir(src):
            print(f'No existe: {src}')
            continue
        
        imgs = sorted([f for f in os.listdir(src) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
        if not imgs:
            print(f'Sin fotos: {aid}')
            continue
        
        # Crear carpeta destino
        dst = os.path.join(IMGDIR, aid)
        os.makedirs(dst, exist_ok=True)
        
        fotos = []
        epigrafes = []
        for i, img in enumerate(imgs, 1):
            ext = os.path.splitext(img)[1].lower()
            nombre = f'foto-{i:02d}{ext}'
            shutil.copy2(os.path.join(src, img), os.path.join(dst, nombre))
            fotos.append(f'imagenes/{aid}/{nombre}')
            epigrafes.append('')
        
        art['fotos'] = fotos
        art['epigrafes'] = epigrafes
        print(f'{aid}: {len(fotos)} fotos')

with open(os.path.join(DATOS, 'ediciones.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Regenerar
sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
