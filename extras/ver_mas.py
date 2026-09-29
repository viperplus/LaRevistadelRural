#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\importados.json', encoding='utf-8') as f:
    data = json.load(f)

# Check YAMINUE and LA REVISTA RURAL more carefully
for slug_part in ['marrone_e_rosso', 'secogabriela']:
    for a in data:
        if slug_part in a['slug']:
            print(f'\n===== {a.get("titulo","")[:70]} =====')
            paras = a.get('parrafos', [])
            # Show paragraphs 15-25 to see middle content
            for i in range(15, min(25, len(paras))):
                print(f'  [{i}] {paras[i][:120]}')
            print(f'  ... total: {len(paras)} paragraphs')
            break
