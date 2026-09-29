#!/usr/bin/env python3
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\ediciones.json', encoding='utf-8') as f:
    data = json.load(f)

# Palabras clave de consignas de clase
keywords = [
    'Introducción', 'Transición', 'Cuerpo del artículo', 'El cuerpo del artículo',
    'El cierre', 'La autoría', 'La Autoría', '¿Qué elementos debe tener',
    '¿Qué formato deberá', 'Tamaño de hoja', 'Letra de tamaño', 'Extensión máxima',
    'Prestar especial atención', 'Recuerden que si el artículo',
    'En este tercer paso', 'Tercer paso', 'Primer paso', 'Segundo paso',
    'Las temáticas que podrán', 'La Revista del Rural es un proyecto',
    'Les proponemos redactar', 'La idea es trabajar',
    'Organicemos previamente', 'Cuidemos la ortografía',
    'Leamos el texto en voz alta', 'Incluyamos imágenes',
    'Pueden resumir el contenido', 'dejar una frase que invite',
    'Vivir cerca del monte', 'En los últimos años',
    '¿Alguna vez pensaste qué ocurre cuando un incendio',
]

problemas = []
for a in data['articulos']:
    aid = a['id']
    for c in a.get('cuerpo', []):
        v = c.get('v', '')
        for kw in keywords:
            if kw.lower() in v.lower():
                problemas.append((aid, kw, v[:100]))
                break

if problemas:
    print('ARTÍCULOS CON TEXTO DE CLASE:')
    for aid, kw, txt in problemas:
        print(f'  {aid}: "{kw}" en: {txt}')
else:
    print('No se encontraron problemas.')
