#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\ediciones.json', encoding='utf-8') as f:
    data = json.load(f)

for i, a in enumerate(data['articulos'], 1):
    aid = a['id']
    titulo = a.get('titulo', '')[:50]
    cuerp = a.get('cuerpo', [])
    
    total_p = sum(1 for c in cuerp if c.get('t') == 'p')
    total_h3 = sum(1 for c in cuerp if c.get('t') == 'h3')
    shorts = sum(1 for c in cuerp if c.get('t') == 'p' and len(c.get('v', '')) < 50)
    fotos = len(a.get('fotos', []))
    
    problems = []
    if total_h3 == 0 and total_p > 3:
        problems.append('SIN SUBTITULOS')
    if shorts > total_p * 0.5 and total_p > 5:
        problems.append('TEXTO FRAGMENTADO')
    if total_p < 3:
        problems.append('MUY CORTO')
    if fotos == 0:
        problems.append('SIN FOTOS')
    
    status = ' | '.join(problems) if problems else 'OK'
    print(f'{i:2}. {aid:45} | {total_p:2}p {total_h3:2}h3 {fotos:2}f | {status}')
