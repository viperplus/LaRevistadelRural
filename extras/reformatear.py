#!/usr/bin/env python3
import json, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')
PDF_BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTÍCULOS PDF'

def limpiar(txt):
    txt = re.sub(r'PDF\+?\s*\d*', '', txt)
    txt = txt.replace('Aquí tienes la digitalización completa del texto del documento provisto:', '')
    return txt.strip()

def a_cuerpo(txt):
    paras = []
    for l in txt.split('\n'):
        l = l.strip()
        if not l or l == 'PDF':
            continue
        if re.match(r'^(SEDE:|TUTOR|CURSO:|NOMBRE|PARTICIPANTES:|TEMA:|4TO AÑO)', l):
            continue
        if len(l) < 60 and (l.endswith(':') or l.endswith('?')):
            paras.append({"t": "h3", "v": l})
        else:
            paras.append({"t": "p", "v": l})
    return paras

ediciones_path = os.path.join(DATOS, 'ediciones.json')
with open(ediciones_path, encoding='utf-8') as f:
    ediciones = json.load(f)

reemplazos = {
    'cuidemos-el-ambiente': os.path.join(PDF_BASE, 'Nueva carpeta', 'Nuevo documento de texto.txt'),
    'la-contaminacion': os.path.join(PDF_BASE, 'Nueva carpeta (6)', 'Nuevo documento de texto.txt'),
    'que-pasaria-sin-agua': os.path.join(PDF_BASE, 'Nueva carpeta (11)', 'Nuevo documento de texto.txt'),
}

for art in ediciones['articulos']:
    if art['id'] in reemplazos:
        txt_path = reemplazos[art['id']]
        with open(txt_path, encoding='utf-8') as f:
            raw = f.read()
        raw = limpiar(raw)
        
        # Quitar titulo del inicio si esta
        lineas = raw.split('\n')
        if lineas and art['titulo'].lower()[:15] in lineas[0].lower():
            raw = '\n'.join(lineas[1:])
        
        art['cuerpo'] = a_cuerpo(raw)
        print(f'Reformateado: {art["id"]} -> {len(art["cuerpo"])} bloques')

with open(ediciones_path, 'w', encoding='utf-8') as f:
    json.dump(ediciones, f, ensure_ascii=False, indent=2)

print('\nRegenerando HTML...')
sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
