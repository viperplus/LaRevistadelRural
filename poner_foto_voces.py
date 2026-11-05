# -*- coding: utf-8 -*-
"""poner_foto_voces.py — Coloca la foto del viaje siguiendo la convención
de los artículos que ya funcionan (p. ej. el-chip-en-la-cancha):
   - archivo real en ediciones/01/<uid>/foto-01.jpg
   - JSON fotos: ["foto-01.jpg"]
   - JSON fotos_disposicion: ["portada"]
Así la tarjeta de la sección (usa ../<uid>/fotos[0]) y el artículo
(usa foto-01.jpg en su propia carpeta) resuelven ambos.
"""
import json, io, sys, os, shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista"
UID = "viaje-bariloche-el-cain"
SRC = r"C:\Users\black\AppData\Local\Temp\opencode\foto_cain.jpg"

# 1) copiar la foto DIRECTAMENTE a la carpeta del artículo
art_dir = os.path.join(BASE, "ediciones", "01", UID)
os.makedirs(art_dir, exist_ok=True)
dst = os.path.join(art_dir, "foto-01.jpg")
shutil.copy2(SRC, dst)
print("foto -> %s (%d bytes)" % (dst, os.path.getsize(dst)))

# 2) limpiar la copia previa en imagenes/ (ya no se usa)
prev = os.path.join(BASE, "ediciones", "01", "imagenes", UID)
if os.path.isdir(prev):
    shutil.rmtree(prev, ignore_errors=True)
    print("limpiado:", prev)

# 3) actualizar JSON con la convención correcta
P = os.path.join(BASE, "datos", "ediciones.json")
d = json.load(open(P, encoding="utf-8"))
for a in d["articulos"]:
    if a.get("id") == UID:
        a["fotos"] = ["foto-01.jpg"]
        a["fotos_disposicion"] = ["portada"]
        a["epigrafes"] = ["Estudiantes de El Caín durante el viaje a Bariloche."]
        print("JSON: fotos=%s disp=%s" % (a["fotos"], a["fotos_disposicion"]))
        break
else:
    print("ERROR: no encontre", UID); sys.exit(1)

open(P, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
print("OK json guardado")
