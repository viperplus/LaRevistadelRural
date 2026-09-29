#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\ediciones.json', encoding='utf-8') as f:
    data = json.load(f)
print('ARTICULOS EN LA REVISTA:')
for i, a in enumerate(data['articulos'], 1):
    aid = a['id']
    print(f'{i:2}. {aid}')
