#!/usr/bin/env python3
import json, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')
PDF_BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTÍCULOS PDF'

def limpiar(txt):
    txt = re.sub(r'PDF\+?\s*\d*', '', txt)
    txt = txt.replace('Aquí tienes la digitalización completa del texto del documento provisto:', '')
    txt = txt.replace('Aquí tienes la transcripción completa y detallada del documento provisto, organizado para reflejar fielmente su contenido:', '')
    return txt.strip()

def a_cuerpo(txt):
    # Separar por 3 o mas espacios (párrafos en .txt de una sola línea)
    partes = re.split(r'\s{3,}', txt)
    paras = []
    for p in partes:
        p = p.strip()
        if not p or p == 'PDF':
            continue
        # Saltar metadata
        if re.match(r'^(SEDE:|TUTOR|CURSO:|NOMBRE|PARTICIPANTES:|TEMA:|4TO AÑO)', p):
            continue
        if re.match(r'^(CIENTÍFICA Y TECNOLÓGICA|CLASE 9)', p):
            continue
        # Detectar subtítulos
        lineas = p.split('\n')
        for l in lineas:
            l = l.strip()
            if not l or l == 'PDF':
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
        
        # Quitar header si existe
        for skip in ['CIENTÍFICA Y TECNOLÓGICA', 'CLASE 9', '11 DE AGOSTO']:
            if skip in raw[:200]:
                idx = raw.find(skip)
                # Buscar fin del header (doble espacio)
                fin = re.search(r'\s{3,}', raw[idx:])
                if fin:
                    raw = raw[idx + fin.start():]
        
        art['cuerpo'] = a_cuerpo(raw)
        print(f'{art["id"]}: {len(art["cuerpo"])} bloques')
        for b in art['cuerpo'][:3]:
            print(f'  [{b["t"]}] {b["v"][:80]}')

with open(ediciones_path, 'w', encoding='utf-8') as f:
    json.dump(ediciones, f, ensure_ascii=False, indent=2)

print('\nRegenerando...')
sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
