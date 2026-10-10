# -*- coding: utf-8 -*-
"""Optimiza para web las fotos de los tres articulos nuevos de Lengua.

- aplica la orientacion EXIF (para no depender del navegador)
- redimensiona a 1600 px de lado maximo
- re-guarda JPEG en calidad 85, optimizado y progresivo

Los originales siguen intactos en revista/ARTICULOS/.
"""
import os
import sys
from PIL import Image, ImageOps

MAX = 1600
BASE = os.path.join(r"C:\Users\black\Desktop\opencode archivos",
                    "clase n" + "\u00b04", "revista", "ediciones", "01")
UIDS = ["2-de-abril-mujeres-en-malvinas",
        "24-marzo-floreceran-panuelos",
        "escritura-fantastica"]
APLICAR = "--write" in sys.argv

tot_antes = tot_despues = 0
for u in UIDS:
    d = os.path.join(BASE, u)
    for f in sorted(os.listdir(d)):
        if not f.lower().endswith((".jpg", ".jpeg")):
            continue
        p = os.path.join(d, f)
        antes = os.path.getsize(p)
        im = Image.open(p)
        w, h = im.size
        im = ImageOps.exif_transpose(im)
        necesita = antes > 900 * 1024 or max(im.size) > MAX
        if not necesita:
            im.close()
            continue
        if max(im.size) > MAX:
            im.thumbnail((MAX, MAX), Image.LANCZOS)
        if not APLICAR:
            print("  %s/%s  %dx%d -> %dx%d  %.1f MB" % (
                u, f, w, h, im.size[0], im.size[1], antes / 1048576.0))
            im.close()
            continue
        if im.mode != "RGB":
            im = im.convert("RGB")
        tmp = p + ".tmp"
        im.save(tmp, "JPEG", quality=85, optimize=True, progressive=True)
        im.close()
        os.replace(tmp, p)
        despues = os.path.getsize(p)
        tot_antes += antes
        tot_despues += despues
        print("  %-14s %6.1f MB -> %6.2f MB" % (f, antes / 1048576.0, despues / 1048576.0))

if APLICAR:
    print("TOTAL  %.1f MB -> %.2f MB" % (tot_antes / 1048576.0, tot_despues / 1048576.0))
else:
    print("Vista previa. Corre con --write para aplicar.")
