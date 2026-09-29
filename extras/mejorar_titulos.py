#!/usr/bin/env python3
"""Mejorar títulos de artículos genéricos."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')

with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

# Mapeo de títulos genéricos a mejores títulos
TITULOS = {
    'nueva_carpeta_10': 'Un problema que nos afecta a todos',
    'nueva_carpeta_2': 'Un pequeño descanso, una gran importancia',
    'nueva_carpeta_3': 'Las células',
    'nueva_carpeta_8': 'Los paisajes de Cerro Policia',
    'arroyo_los_berros': 'Nuestro paraje, nuestra responsabilidad',
    'clase_n_10_espacio_curricular_ed_cient_fica_y_tecn': 'Sembrando conciencia, cosechando un paraje limpio',
    'clase_n_10_cient_fica_y_tecnol_gicaintegrantes_agu': 'Nuestro Mundial 2026',
    'clase_n_10_cient_fica_y_tecnol_gica': 'La Copa del Mundo: mucho más que un trofeo',
}

# Mapeo de bajadas
BAJADAS = {
    'nueva_carpeta_10': 'El problema del basurero a cielo abierto en Cerro Policia y sus consecuencias para la salud y el ambiente.',
    'nueva_carpeta_2': 'La pausa de hidratación en el fútbol: por qué es importante y qué pasa si no existe.',
    'nueva_carpeta_3': 'Qué son las células, sus partes y funciones.',
    'nueva_carpeta_8': 'Análisis fotográfico de los paisajes de Cerro Policia.',
    'arroyo_los_berros': 'La contaminación en Arroyo Los Berros y propuestas para mejorar.',
    'clase_n_10_espacio_curricular_ed_cient_fica_y_tecn': 'Transformación de Arroyo Los Berros a través de la conciencia comunitaria.',
    'clase_n_10_cient_fica_y_tecnol_gicaintegrantes_agu': 'La experiencia del Mundial 2026 en la escuela.',
    'clase_n_10_cient_fica_y_tecnol_gica': 'Análisis científico del trofeo de la Copa del Mundo FIFA.',
}

# Mapeo de secciones
SECCIONES = {
    'nueva_carpeta_10': 'ciencia',
    'nueva_carpeta_2': 'ciencia',
    'nueva_carpeta_3': 'ciencia',
    'nueva_carpeta_8': 'cultura',
    'arroyo_los_berros': 'territorio',
    'clase_n_10_espacio_curricular_ed_cient_fica_y_tecn': 'territorio',
    'clase_n_10_cient_fica_y_tecnol_gicaintegrantes_agu': 'escuela',
    'clase_n_10_cient_fica_y_tecnol_gica': 'ciencia',
}

for art in data['articulos']:
    if art['id'] in TITULOS:
        art['titulo'] = TITULOS[art['id']]
        print(f'Actualizado: {art["id"]} -> {art["titulo"]}')
    if art['id'] in BAJADAS:
        art['bajada'] = BAJADAS[art['id']]
    if art['id'] in SECCIONES:
        art['seccion'] = SECCIONES[art['id']]

with open(DATOS, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Regenerar
sys.path.insert(0, BASE)
from construir_revista_v2 import main as generar
generar()
print('Listo!')
