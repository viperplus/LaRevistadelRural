#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\ediciones.json', encoding='utf-8') as f:
    data = json.load(f)
for art in data['articulos']:
    if 'gol' in art.get('id', '').lower() or 'ciencia' in art.get('id', '').lower():
        print(f'{art["id"]}: fuente={art.get("fuente", "?")}, fotos={art.get("fotos", [])}')
