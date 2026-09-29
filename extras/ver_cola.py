#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\importados.json', encoding='utf-8') as f:
    data = json.load(f)

# Check class worksheets for appended articles
targets = [
    'clase_9_fatima_hernadez',
    'clase_n°9_cientifica_y_tecnologica_4°a_o_pame',
    'correcci_n_saul_catriel',
]
for slug_part in targets:
    for a in data:
        if slug_part in a['slug']:
            print(f'\n===== {a["slug"][:60]} =====')
            paras = a.get('parrafos', [])
            # Show last 15 paragraphs
            start = max(0, len(paras) - 15)
            for i in range(start, len(paras)):
                print(f'  [{i}] {paras[i][:120]}')
            break
