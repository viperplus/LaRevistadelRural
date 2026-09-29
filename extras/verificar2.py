#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\ediciones.json', encoding='utf-8') as f:
    data = json.load(f)

for a in data['articulos']:
    if a['id'] in ['el-partido-por-el-ambiente', 'cuidar-el-ambiente-kral']:
        print(f'=== {a["id"]} ===')
        for c in a['cuerpo'][:6]:
            t = c['t']
            v = c['v'][:100]
            print(f'[{t}] {v}')
        print()
