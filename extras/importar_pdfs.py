#!/usr/bin/env python3
"""Importa artículos de PDFs a ediciones.json."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "datos")

def cargar_json(nombre):
    with open(os.path.join(DATOS, nombre), encoding="utf-8") as f:
        return json.load(f)

def guardar_json(nombre, data):
    with open(os.path.join(DATOS, nombre), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def es_subtitulo(p):
    p = p.strip()
    if len(p) > 70:
        return False
    if p.endswith("?") or p.endswith(":"):
        return True
    return False

def de_shout(p):
    if p.isupper() and not any(c.isdigit() for c in p):
        return p[:1].upper() + p[1:].lower()
    return p

def construir_cuerpo(parrafos, subtitulos=None, desde=0, hasta=None, quitar_ultimas=0):
    if hasta is None:
        hasta = len(parrafos)
    paras = parrafos[desde:hasta]
    if quitar_ultimas > 0:
        paras = paras[:-quitar_ultimas]
    subtitulos = subtitulos or []
    result = []
    for p in paras:
        p = de_shout(p.strip())
        if not p:
            continue
        if p in subtitulos:
            result.append({"t": "h3", "v": p})
        elif es_subtitulo(p):
            result.append({"t": "h3", "v": p})
        else:
            result.append({"t": "p", "v": p})
    return result

def extraer_parrafos(art_slug, importados):
    for a in importados:
        if a["slug"] == art_slug:
            return a.get("parrafos", [])
    return []

def main():
    print("=== Importacion de articulos PDF ===\n")
    ediciones = cargar_json("ediciones.json")
    importados = cargar_json("importados.json")
    ids_existentes = {a["id"] for a in ediciones["articulos"]}

    nuevos = []

    # 1. CUIDEMOS - Saira Linares
    paras = extraer_parrafos("cient_fica_y_tecnol_gica_clase_n°9_4to_a_o_saira_linares_lag", importados)
    if paras:
        nuevos.append({
            "id": "cuidemos-el-ambiente",
            "seccion": "ciencia",
            "titulo": "Cuidemos el ambiente",
            "bajada": "Cuidar el ambiente es fundamental para lograr una vida mas saludable y un futuro mejor.",
            "autor": "Saira Linares",
            "rol": "Estudiante 4.° ano",
            "sede": "Lago Pellegrini",
            "fecha": "Noviembre 2026",
            "odt": None,
            "cuerpo": construir_cuerpo(paras),
            "epigrafes": []
        })

    # 2. TECNOLOGIA MUNDIALISTA - Leonel Chico, Adrian Mateo Lopez
    paras = extraer_parrafos("clase_9_educacion_cintifica_y_tecnologica_4to_a_o_leonel_chi", importados)
    if paras:
        nuevos.append({
            "id": "tecnologia-mundialista",
            "seccion": "ciencia",
            "titulo": "La tecnologia en el Mundial 2026",
            "bajada": "Camaras corporales, sensores, inteligencia artificial y GPS: la tecnologia que uso el arbitraje en el Mundial.",
            "autor": "Hector Leonel Chico - Adrian Mateo Lopez",
            "rol": "Estudiantes 4.° ano",
            "sede": "Aguada de Guerra",
            "fecha": "Noviembre 2026",
            "odt": None,
            "cuerpo": construir_cuerpo(paras, quitar_ultimas=1),
            "epigrafes": []
        })

    # 3. LA CONTAMINACION - Guadalupe Centeno
    paras = extraer_parrafos("clase_9_cientifica_y_tecnologica_guadalupe_centeno_lago_pell", importados)
    if paras:
        nuevos.append({
            "id": "la-contaminacion",
            "seccion": "ciencia",
            "titulo": "La contaminacion",
            "bajada": "Un problema que nos afecta a todos: como la contaminacion afecta el agua, el aire y el suelo.",
            "autor": "Guadalupe Centeno",
            "rol": "Estudiante 4.° ano",
            "sede": "Lago Pellegrini",
            "fecha": "Noviembre 2026",
            "odt": None,
            "cuerpo": construir_cuerpo(paras),
            "epigrafes": []
        })

    # 4. QUE PASARIA SI UN DIA NOS QUEDARAMOS SIN AGUA - Medrano Julieta
    paras = extraer_parrafos("medrano_julieta_4to_a_o_clase_9_cientifica_y_tecnologica_lag", importados)
    if paras:
        titulo_completo = " ".join(paras[:2])
        nuevos.append({
            "id": "que-pasaria-sin-agua",
            "seccion": "ciencia",
            "titulo": titulo_completo,
            "bajada": "El agua es muy importante para nuestra vida. ¿Que pasaria si un dia faltara?",
            "autor": "Medrano Julieta",
            "rol": "Estudiante 4.° ano",
            "sede": "Lago Pellegrini",
            "fecha": "Noviembre 2026",
            "odt": None,
            "cuerpo": construir_cuerpo(paras, desde=2),
            "epigrafes": []
        })

    # 5. MONOXIDO DE CARBONO - Fatima Hernandez, Erika Pil
    paras = extraer_parrafos("clase_9_fatima_hernadez_erika_pil_aguada_cecilio_4to_a_o_1", importados)
    if paras:
        # Article starts after class instructions, find the article start
        idx = 0
        for i, p in enumerate(paras):
            if "monoxido" in p.lower() or "monóxido" in p.lower() or "calefaccion" in p.lower():
                idx = i
                break
        nuevos.append({
            "id": "monoxido-de-carbono-aguada-cecilio",
            "seccion": "ciencia",
            "titulo": "El monoxido de carbono: un enemigo invisible",
            "bajada": "El monoxido de carbono es un gas peligroso que no tiene olor, sabor ni color. Como prevenirlo.",
            "autor": "Fatima Hernandez - Erika Pil",
            "rol": "Estudiantes 4.° ano",
            "sede": "Aguada Cecilio",
            "fecha": "Noviembre 2026",
            "odt": None,
            "cuerpo": construir_cuerpo(paras, desde=idx),
            "epigrafes": []
        })

    # 6. MONOXIDO DE CARBONO - Pame Loncoman (extracted from tail)
    paras = extraer_parrafos("clase_n°9_cientifica_y_tecnologica_4°a_o_pame_loncoman_mencu", importados)
    if paras:
        # Article is in the tail of the class worksheet
        idx = 0
        for i, p in enumerate(paras):
            if "monoxido" in p.lower() or "monóxido" in p.lower():
                idx = i
                break
        articulo_paras = paras[idx:]
        nuevos.append({
            "id": "monoxido-de-carbono-pame",
            "seccion": "ciencia",
            "titulo": "El monoxido de carbono es un peligro real",
            "bajada": "Como detectar y prevenir el monoxido de carbono en el hogar.",
            "autor": "Pame Loncoman",
            "rol": "Estudiante 4.° ano",
            "sede": "Mencue",
            "fecha": "Noviembre 2026",
            "odt": None,
            "cuerpo": construir_cuerpo(articulo_paras, quitar_ultimas=1),
            "epigrafes": []
        })

    # Agregar articulos
    print("Articulos a importar:")
    agregados = 0
    for art in nuevos:
        if art["id"] in ids_existentes:
            print(f"  [SKIP] {art['id']} (ya existe)")
            continue
        ediciones["articulos"].append(art)
        ids_existentes.add(art["id"])
        agregados += 1
        print(f"  [OK] {art['id']} - {art['titulo']}")

    print(f"\nTotal nuevos: {agregados}")
    guardar_json("ediciones.json", ediciones)

    # Regenerar HTML
    print("\nRegenerando HTML...")
    sys.path.insert(0, BASE)
    from construir_revista import main as generar
    generar()
    print("\n=== Listo ===")

if __name__ == "__main__":
    main()
