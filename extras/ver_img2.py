#!/usr/bin/env python3
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\ediciones\01\el-partido-por-el-ambiente\index.html', encoding='utf-8') as f:
    html = f.read()
imgs = re.findall(r'<img src="([^"]+)"', html)
print('Imagenes:', imgs)
