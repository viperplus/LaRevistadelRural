#!/usr/bin/env python3
"""Extrae texto e imágenes de un PDF y lo agrega a importados.json."""

import json, os, sys, fitz  # PyMuPDF

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "datos")
ODT = os.path.join(BASE, "odt")

def slug(nombre):
    s = nombre.lower().strip()
    for c in "áéíóúñü .,;:!?¡¿()[]{}\"'/-":
        s = s.replace(c, "_")
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_")[:60]

def extraer_pdf(ruta):
    doc = fitz.open(ruta)
    nombre = os.path.splitext(os.path.basename(ruta))[0]
    slug_nombre = slug(nombre)

    # Crear carpeta de imágenes
    img_dir = os.path.join(ODT, slug_nombre)
    os.makedirs(img_dir, exist_ok=True)

    parrafos = []
    fotos = []
    n_foto = 0

    for i, pagina in enumerate(doc):
        # Extraer texto
        texto = pagina.get_text("text")
        for linea in texto.split("\n"):
            linea = linea.strip()
            if linea:
                parrafos.append(linea)

        # Extraer imágenes
        imgs = pagina.get_images(full=True)
        for img in imgs:
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n > 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            n_foto += 1
            nombre_img = f"foto_{n_foto:02d}.png"
            pix.save(os.path.join(img_dir, nombre_img))
            fotos.append(nombre_img)

    doc.close()

    return {
        "archivo": os.path.basename(ruta),
        "slug": slug_nombre,
        "titulo": parrafos[0] if parrafos else nombre,
        "firma": "",
        "n_parrafos": len(parrafos),
        "n_fotos": len(fotos),
        "parrafos": parrafos,
        "fotos_extraidas": fotos
    }

def main():
    if len(sys.argv) < 2:
        print("Uso: python extraer_pdf.py archivo1.pdf [archivo2.pdf ...]")
        print("    O:  python extraer_pdf.py carpeta_con_pdfs/")
        sys.exit(1)

    importados_path = os.path.join(DATOS, "importados.json")
    with open(importados_path, encoding="utf-8") as f:
        importados = json.load(f)

    existentes = {a["slug"] for a in importados}

    rutas = []
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            for f in os.listdir(arg):
                if f.lower().endswith(".pdf"):
                    rutas.append(os.path.join(arg, f))
        elif os.path.isfile(arg) and arg.lower().endswith(".pdf"):
            rutas.append(arg)

    print(f"PDFs encontrados: {len(rutas)}\n")

    agregados = 0
    for ruta in rutas:
        print(f"Procesando: {os.path.basename(ruta)}")
        try:
            datos = extraer_pdf(ruta)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

        if datos["slug"] in existentes:
            print(f"  Saltado (ya existe)")
            continue

        # Quitar campo auxiliar
        fotos = datos.pop("fotos_extraidas", [])
        importados.append(datos)
        existentes.add(datos["slug"])
        agregados += 1
        print(f"  OK: {datos['n_parrafos']} párrafos, {datos['n_fotos']} fotos")

    # Guardar
    with open(importados_path, "w", encoding="utf-8") as f:
        json.dump(importados, f, ensure_ascii=False, indent=2)

    print(f"\nTotal agregados: {agregados}")
    print(f"Total en importados.json: {len(importados)}")

if __name__ == "__main__":
    main()
