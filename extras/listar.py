#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\ediciones.json', encoding='utf-8') as f:
    data = json.load(f)
print(f'Total articulos: {len(data["articulos"])}\n')
for i, a in enumerate(data['articulos'], 1):
    sec = a.get('seccion','')[:12]
    titulo = a.get('titulo','')[:55]
    autor = a.get('autor','')[:35]
    print(f'{i:2}. [{sec:12}] {titulo:55} | {autor}')
