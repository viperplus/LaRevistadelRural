#!/usr/bin/env python3
import json, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')
TXT = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTÍCULOS PDF\Nueva carpeta (2)\Nuevo documento de texto.txt'

with open(TXT, encoding='utf-8') as f:
    raw = f.read()

# Limpiar
raw = re.sub(r'PDF\+?\s*\d*', '', raw)
raw = raw.replace('CIENTÍFICA Y TECNOLÓGICA - CLASE 9 - MAIA OSES DE 4° AÑO DE LA SEDE DEL LAGO PELLEGRINI - TUTORA LUCRECIA ANGELI', '')

# Parrafos
paras = []
for l in raw.split('\n'):
    l = l.strip()
    if not l or l == 'PDF':
        continue
    paras.append(l)

# Titulo: "CUIDEMOS NUESTRO AMBIENTE" esta en la linea 1
titulo_linea = paras[0] if paras else ''
# El titulo real es "Cuidemos Nuestro Ambiente"
if 'CUIDEMOS' in titulo_linea.upper():
    titulo = 'Cuidemos Nuestro Ambiente'
    paras = paras[1:]  # quitar la linea del titulo
else:
    titulo = titulo_linea

# Limpiar subtitulos rotos
cuerpo = []
for p in paras:
    p = p.strip()
    if not p:
        continue
    if p == 'PDF':
        continue
    # Detectar subtitulos
    if len(p) < 60 and (p.endswith(':') or p.endswith('?')):
        cuerpo.append({"t": "h3", "v": p})
    else:
        cuerpo.append({"t": "p", "v": p})

# Quitar ultima linea si es firma
if cuerpo and '¡Cuidar el planeta' in cuerpo[-1].get('v', ''):
    pass  # keep it

art = {
    "id": "cuidemos-nuestro-ambiente-maia",
    "seccion": "ciencia",
    "titulo": titulo,
    "bajada": "Pequenas acciones, grandes cambios. Cuidar nuestro planeta es responsabilidad de todos.",
    "autor": "Maia Oses",
    "rol": "Estudiante 4. ano",
    "sede": "Lago Pellegrini",
    "fecha": "Noviembre 2026",
    "odt": None,
    "cuerpo": cuerpo,
    "epigrafes": []
}

ediciones_path = os.path.join(DATOS, 'ediciones.json')
with open(ediciones_path, encoding='utf-8') as f:
    ediciones = json.load(f)

ids = {a['id'] for a in ediciones['articulos']}
if art['id'] in ids:
    print('Ya existe')
else:
    ediciones['articulos'].append(art)
    with open(ediciones_path, 'w', encoding='utf-8') as f:
        json.dump(ediciones, f, ensure_ascii=False, indent=2)
    print(f'Agregado: {art["id"]} - {art["titulo"]}')

    # Regenerar
    sys.path.insert(0, BASE)
    from construir_revista import main as generar
    generar()
