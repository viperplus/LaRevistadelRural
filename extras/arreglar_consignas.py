#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')

with open(os.path.join(DATOS, 'ediciones.json'), encoding='utf-8') as f:
    data = json.load(f)

# 1. el-partido-por-el-ambiente - quitar "Transición" como subtítulo
for art in data['articulos']:
    if art['id'] == 'el-partido-por-el-ambiente':
        nuevo = []
        for c in art['cuerpo']:
            if c.get('v') == 'La transición: pensar la cancha como enseñanza':
                continue
            nuevo.append(c)
        art['cuerpo'] = nuevo
        print(f'Arreglado: el-partido-por-el-ambiente')

# 2. una-mirada-sobre-la-realidad - verificar y limpiar
for art in data['articulos']:
    if art['id'] == 'una-mirada-sobre-la-realidad':
        print(f'Verificando: una-mirada-sobre-la-realidad')
        # Show first 3 paragraphs
        for c in art['cuerpo'][:3]:
            print(f'  [{c["t"]}] {c["v"][:80]}')

# 3. cuidar-el-ambiente-kral - quitar "Introducción", "Transición", "Cuerpo del artículo"
for art in data['articulos']:
    if art['id'] == 'cuidar-el-ambiente-kral':
        nuevo = []
        skip = {'Introducción', 'Transición', 'Cuerpo del artículo'}
        for c in art['cuerpo']:
            if c.get('v') in skip:
                continue
            nuevo.append(c)
        art['cuerpo'] = nuevo
        print(f'Arreglado: cuidar-el-ambiente-kral')

with open(os.path.join(DATOS, 'ediciones.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
