#!/usr/bin/env python3
"""Leer contenido de artículos que necesitan mejoras."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')

with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

# Artículos a mejorar
IDS_MEJORAR = [
    '1_reflexi_n_a_trav_s_de_fotograf_a',
    'la_primera_ley_de_newton',
    'latido_del_equilibrio_ambiental_en_naupa_huen',
    'acciones_peque_as_para_un_mundo_grande',
    'reflexi_n_a_trav_s_de_fotograf_a',
    'los_festejos_de_una_localidad',
    'arroyo_los_berros',
    'nueva_carpeta_10',
    'clase_n_10_cient_fica_y_tecnol_gica',
    'nueva_carpeta_12',
    'nueva_carpeta_2',
    'nueva_carpeta_3',
    'clase_n_10_espacio_curricular_ed_cient_fica_y_tecn',
    'clase_n_10_cient_fica_y_tecnol_gicaintegrantes_agu',
    'nueva_carpeta_8',
]

for art in data['articulos']:
    if art['id'] in IDS_MEJORAR:
        print(f'\n=== {art["id"]} ===')
        print(f'Título: {art.get("titulo", "?")}')
        print(f'Bajada: {art.get("bajada", "?")[:80]}')
        print(f'Sección: {art.get("seccion", "?")}')
        print(f'Párrafos: {len(art.get("cuerpo", []))}')
        print(f'Fotos: {len(art.get("fotos", []))}')
        print('Contenido:')
        for i, p in enumerate(art.get('cuerpo', [])[:5]):
            print(f'  [{p["t"]}] {p["v"][:80]}')
        if len(art.get('cuerpo', [])) > 5:
            print(f'  ... ({len(art["cuerpo"]) - 5} más)')
