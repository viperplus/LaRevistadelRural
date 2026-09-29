#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\importados.json', encoding='utf-8') as f:
    data = json.load(f)
for doc in data:
    if 'gol' in doc.get('id', '').lower() or 'ciencia' in doc.get('id', '').lower():
        print(f'{doc["id"]}: fuente={doc.get("fuente", "?")}')
