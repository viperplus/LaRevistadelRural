#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\importados.json', encoding='utf-8') as f:
    data = json.load(f)
for a in data[-18:]:
    slug = a.get('slug','')[:55]
    paras = a.get('n_parrafos', 0)
    fotos = a.get('n_fotos', 0)
    titulo = a.get('titulo','')[:70]
    print(f'{slug:55} | {paras:3}p {fotos:3}f | {titulo}')
