#!/usr/bin/env python3
"""Verificar mapeo completo de fotos: de dónde viene cada foto y a qué artículo pertenece."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')
EDIT = os.path.join(BASE, 'ediciones', '01')
ODT = os.path.join(BASE, 'odt')
PDF = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTÍCULOS PDF'
DO2 = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTICULOS 2DO AÑO'
ENVIAR = r'C:\Users\black\Desktop\opencode archivos\clase n°4\enviar_aqui\imagenes_odt'

with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

# Construir índice: qué fotos existen en cada carpeta fuente
def listar_fotos(carpeta):
    if not os.path.isdir(carpeta):
        return []
    return sorted([f for f in os.listdir(carpeta) if f.lower().endswith(('.png','.jpg','.jpeg'))])

# Verificar cada artículo
print("=" * 80)
print("VERIFICACIÓN COMPLETA: ARTÍCULO → FOTOS EN DISCO")
print("=" * 80)

total_con_fotos = 0
total_sin_fotos = 0

for art in data['articulos']:
    uid = art['id']
    titulo = art.get('titulo', uid)
    seccion = art.get('seccion', '?')
    fotos_json = art.get('fotos', [])
    epigrafes = art.get('epigrafes', [])
    
    art_dir = os.path.join(EDIT, uid)
    
    # Fotos en disco
    if os.path.isdir(art_dir):
        fotos_disco = sorted([f for f in os.listdir(art_dir) if f.lower().endswith(('.png','.jpg','.jpeg'))])
    else:
        fotos_disco = []
    
    # Verificar consistencia JSON vs disco
    json_ok = len(fotos_json) == len(fotos_disco)
    
    print(f"\n--- {uid} ---")
    print(f"  Titulo: {titulo}")
    print(f"  Seccion: {seccion}")
    print(f"  Fotos JSON: {len(fotos_json)} | Fotos disco: {len(fotos_disco)} | {'OK' if json_ok else 'MISMATCH!'}")
    
    if fotos_json:
        total_con_fotos += 1
    else:
        total_sin_fotos += 1
    
    if fotos_disco:
        for f in fotos_disco:
            tam = os.path.getsize(os.path.join(art_dir, f))
            print(f"    {f} ({tam:,} bytes)")
    
    if epigrafes and len(epigrafes) > 0:
        for i, e in enumerate(epigrafes):
            if e.strip():
                print(f"  Epígrafe {i+1}: {e[:60]}...")

print(f"\n{'=' * 80}")
print(f"RESUMEN: {total_con_fotos} artículos con fotos, {total_sin_fotos} sin fotos")
print(f"{'=' * 80}")
