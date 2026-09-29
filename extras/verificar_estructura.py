#!/usr/bin/env python3
import re, sys, os
sys.stdout.reconfigure(encoding='utf-8')
base = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\ediciones\01'

# Check index.html
with open(os.path.join(base, 'index.html'), encoding='utf-8') as f:
    html = f.read()
print('=== index.html ===')
print('CSS:', re.findall(r'href="([^"]*revista\.css)"', html))
print('Nav links:', re.findall(r"href='([^']*secciones/[^']*)'", html)[:3])

# Check secciones
sec_dir = os.path.join(base, 'secciones')
for sec in os.listdir(sec_dir):
    if sec.endswith('.html'):
        with open(os.path.join(sec_dir, sec), encoding='utf-8') as f:
            html = f.read()
        css = re.findall(r'href="([^"]*revista\.css)"', html)
        links = re.findall(r"href='([^']*articulos/[^']*)'", html)[:2]
        print(f'\n=== {sec} ===')
        print('CSS:', css)
        print('Art links:', links)
        break

# Check one article
art_dir = os.path.join(base, 'la-contaminacion')
with open(os.path.join(art_dir, 'index.html'), encoding='utf-8') as f:
    html = f.read()
print('\n=== la-contaminacion/index.html ===')
print('CSS:', re.findall(r'href="([^"]*revista\.css)"', html))
print('Volver:', re.findall(r'href="([^"]*)".*Volver', html))
print('Images:', re.findall(r'<img src="([^"]+)"', html)[:2])
