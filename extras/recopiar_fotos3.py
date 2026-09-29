#!/usr/bin/env python3
"""Recopiar fotos - MAPEO FINAL CORREGIDO."""
import json, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')
EDIT = os.path.join(BASE, 'ediciones', '01')
ODT = os.path.join(BASE, 'odt')
PDF = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTÍCULOS PDF'
ENVIAR = r'C:\Users\black\Desktop\opencode archivos\clase n°4\enviar_aqui\imagenes_odt'
DO2 = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTICULOS 2DO AÑO'

# =============================================
# MAPEO COMPLETO Y CORREGIDO
# =============================================

MAPEO = {
    # === ARTÍCULOS ORIGINALES - fotos desde enviar_aqui ===
    'el-chip-en-la-cancha': os.path.join(ENVIAR, 'culturas_de_campeones'),
    'la-primera-ley-de-newton': os.path.join(ENVIAR, 'la_ley_de_la_incercia'),
    'el-partido-por-el-ambiente': os.path.join(ENVIAR, 'el_partido_por_el_ambiente'),
    'la-fiesta-del-paraje-treneta': os.path.join(ENVIAR, 'fiestas_y_tradiciones_mundialistas'),
    'próxima-parada-atractivos-mundialistas': os.path.join(ENVIAR, 'pr_xima_parada__atractivos_mundialistas_'),
    'potabilizacion-aguada-guzman': os.path.join(ENVIAR, 'c_mo_es_la_potabilizaci_n_en_el_paraje_a'),
    'una-mirada-sobre-la-realidad': os.path.join(ODT, 'clase_9_cientifica_y_tecnologica_guadalupe_centeno_lago_pell'),
    'los-festejos-de-una-localidad': os.path.join(ENVIAR, 'clase_n_9_taller_de_educaci_n_cient_fica'),
    'medio-ambiente-sierra-paileman': os.path.join(ENVIAR, 'kevin_nahuel_sierra_paileman_clase_9_cie'),
    'la-llegada-de-la-primavera': os.path.join(ENVIAR, 'la_llegada_de_la_primavera'),
    'gol-de-ciencia': os.path.join(ENVIAR, 'rio_chico_estefania_manuel_4_a_o_cientif'),
    'el-cuidado-del-agua': os.path.join(ENVIAR, 'contreras_sahira_tegnologica_clase_9'),
    'cuidemos-el-ambiente': os.path.join(PDF, 'Nueva carpeta'),
    'tecnologia-mundialista': os.path.join(ENVIAR, 'clase_9_cientifica_4_a_o_rodrigo_fhaile_'),
    'la-contaminacion': os.path.join(ODT, 'clase_9_cientifica_y_tecnologica_guadalupe_centeno_lago_pell'),
    'que-pasaria-sin-agua': os.path.join(PDF, 'Nueva carpeta (11)'),
    'monoxido-de-carbono-aguada-cecilio': os.path.join(ODT, 'clase_9_fatima_hernadez_erika_pil_aguada_cecilio_4to_a_o'),
    'monoxido-de-carbono-pame': os.path.join(ODT, 'clase_n°9_cientifica_y_tecnologica_4°a_o_pame_loncoman_mencu'),
    'no-solo-un-encuentro-de-sedes': os.path.join(PDF, 'Nueva carpeta (3)'),
    'hay-algo-mas-en-las-fotos': os.path.join(PDF, 'Nueva carpeta (4)'),
    'no-a-la-basura': os.path.join(PDF, 'Nueva carpeta (8)'),
    'cuidar-el-ambiente-kral': os.path.join(PDF, 'Nueva carpeta (9)'),
    'cuidar-nuestro-ambiente-seco': os.path.join(PDF, 'Nueva carpeta (12)'),
    'cuidemos-nuestro-ambiente-maia': os.path.join(ODT, 'cientifica_y_tecnologica_clase_9_maia_oses_de_4°a_o_de_la_se'),
    'yaminue-conexion-naturaleza': os.path.join(PDF, 'Nueva carpeta (10)'),
    
    # === ARTÍCULOS 2DO AÑO - fotos desde ARTICULOS 2DO AÑO ===
    '1_reflexi_n_a_trav_s_de_fotograf_a': os.path.join(DO2, 'Nueva carpeta (11)'),
    'la_primera_ley_de_newton': os.path.join(DO2, 'Nueva carpeta (8)'),
    'latido_del_equilibrio_ambiental_en_naupa_huen': os.path.join(DO2, 'Nueva carpeta (5)'),
    'acciones_peque_as_para_un_mundo_grande': os.path.join(DO2, 'Nueva carpeta (6)'),
    'reflexi_n_a_trav_s_de_fotograf_a': os.path.join(DO2, 'Nueva carpeta (11)'),
    'los_festejos_de_una_localidad': os.path.join(DO2, 'Nueva carpeta (13)'),
    'arroyo_los_berros': os.path.join(DO2, 'Nueva carpeta'),
    'nueva_carpeta_10': os.path.join(DO2, 'Nueva carpeta (10)'),
    'clase_n_10_cient_fica_y_tecnol_gica': os.path.join(DO2, 'Nueva carpeta (9)'),
    'nueva_carpeta_12': os.path.join(DO2, 'Nueva carpeta (12)'),
    'nueva_carpeta_2': os.path.join(DO2, 'Nueva carpeta (2)'),
    'nueva_carpeta_3': os.path.join(DO2, 'Nueva carpeta (3)'),
    'clase_n_10_espacio_curricular_ed_cient_fica_y_tecn': os.path.join(DO2, 'Nueva carpeta (4)'),
    'clase_n_10_cient_fica_y_tecnol_gicaintegrantes_agu': os.path.join(DO2, 'Nueva carpeta (7)'),
    'nueva_carpeta_8': os.path.join(DO2, 'Nueva carpeta (8)'),
}

with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    uid = art['id']
    art_dir = os.path.join(EDIT, uid)
    os.makedirs(art_dir, exist_ok=True)
    
    # Limpiar fotos viejas
    for f in os.listdir(art_dir):
        if f.startswith('foto-'):
            os.remove(os.path.join(art_dir, f))
    
    if uid not in MAPEO:
        print(f'{uid}: SIN MAPEO')
        continue
    
    src_dir = MAPEO[uid]
    if not os.path.isdir(src_dir):
        print(f'{uid}: CARPETA NO EXISTE: {src_dir}')
        continue
    
    imgs = sorted([f for f in os.listdir(src_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
    imgs = imgs[:6]
    
    if not imgs:
        print(f'{uid}: sin fotos en {os.path.basename(src_dir)}')
        continue
    
    for i, img in enumerate(imgs, 1):
        ext = os.path.splitext(img)[1]
        dst = os.path.join(art_dir, f'foto-{i:02d}{ext}')
        shutil.copy2(os.path.join(src_dir, img), dst)
    
    art['fotos'] = [f'foto-{i:02d}{os.path.splitext(img)[1]}' for i, img in enumerate(imgs, 1)]
    art['epigrafes'] = [''] * len(imgs)
    print(f'{uid}: {len(imgs)} fotos OK')

with open(DATOS, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

sys.path.insert(0, BASE)
from construir_revista_v2 import main as generar
generar()
print('¡LISTO!')
