#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\ediciones.json', encoding='utf-8') as f:
    data = json.load(f)
for i, a in enumerate(data['articulos'], 1):
    cuerp = a.get('cuerpo', [])
    shorts = sum(1 for c in cuerp if c.get('t')=='p' and len(c.get('v',''))<50)
    total = sum(1 for c in cuerp if c.get('t')=='p')
    aid = a['id']
    if shorts > total * 0.5 and total > 5:
        print(f'{i:2}. {aid:45} ({total}p, {shorts} cortos) -> REFORMATEAR')
    else:
        print(f'{i:2}. {aid:45} ({total}p) OK')
