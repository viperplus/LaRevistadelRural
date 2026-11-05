# -*- coding: utf-8 -*-
"""agregar_video_voces.py — Agrega UN artículo a la sección Voces.

Contenido: estudiantes de El Caín viajaron a Bariloche y cuentan su
experiencia. Incluye el video de Drive.
"""
import json, io, sys, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\ediciones.json"
d = json.load(open(P, encoding="utf-8"))

NUEVO_ID = "viaje-bariloche-el-cain"

# evitar duplicado si se corre dos veces
d["articulos"] = [a for a in d["articulos"] if a.get("id") != NUEVO_ID]

articulo = {
    "id": NUEVO_ID,
    "seccion": "voces",
    "titulo": "El viaje de El Caín a Bariloche: una experiencia para contar",
    "bajada": "Los estudiantes de la sede El Caín viajaron a Bariloche y comparten lo que vivieron.",
    "autor": "Estudiantes de El Caín",
    "rol": "Estudiantes 4.º año",
    "sede": "El Caín",
    "fecha": "Diciembre 2026",
    "fecha_iso": "2026-12-01",
    "odt": None,
    "cuerpo": [
        {
            "t": "p",
            "v": "Los estudiantes de la sede El Caín emprendieron un viaje a Bariloche y nos cuentan su experiencia. En este video comparten lo que significó para ellos recorrer nuevos paisajes, compartir días juntos y vivir una salida que quedará en la memoria de todo el grupo."
        },
        {
            "t": "video",
            "v": "https://drive.google.com/file/d/1jWi-RDJaz6Z2M1N7eHyiUa9dnT5urPvu/preview",
            "clase": "video--destacado",
            "cap": "Viaje de los estudiantes de El Caín a Bariloche."
        }
    ],
    "epigrafes": [],
    "fotos": [],
    "anio": "4.º año",
    "tutora": "Fernanda Ranileo"
}

d["articulos"].append(articulo)
open(P, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))

print("== agregado: %s (seccion=voces) ==" % NUEVO_ID)
print("== total articulos ahora: %d ==" % len(d["articulos"]))
