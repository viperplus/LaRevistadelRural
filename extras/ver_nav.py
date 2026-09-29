#!/usr/bin/env python3
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\ediciones\01\gol-de-ciencia\index.html', encoding='utf-8') as f:
    html = f.read()
nav = re.findall(r"href='([^']*secciones[^']*)'", html)
print('Nav links:', nav)
volver = re.findall(r'href="([^"]*)".*Volver', html)
print('Volver:', volver)
