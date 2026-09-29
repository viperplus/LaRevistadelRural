#!/usr/bin/env python3
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\ediciones\01\index.html', encoding='utf-8') as f:
    html = f.read()
print('CSS:', re.findall(r'href="([^"]*revista\.css)"', html))
print('Icon:', re.findall(r'href="([^"]*favicon[^"]*)"', html))
