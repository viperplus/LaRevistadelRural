#!/usr/bin/env python3
"""Importa 7 artículos faltantes de importados.json a ediciones.json."""

import json, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "datos")

def cargar_json(nombre):
    with open(os.path.join(DATOS, nombre), encoding="utf-8") as f:
        return json.load(f)

def guardar_json(nombre, data):
    with open(os.path.join(DATOS, nombre), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Guardado: {nombre}")

def es_subtitulo(p):
    """Detecta si un párrafo es subtítulo (pregunta corta o frase breve)."""
    p = p.strip()
    if len(p) > 70:
        return False
    if p.endswith("?") or p.endswith(":"):
        return True
    return False

def de_shout(p):
    """Convierte mayúsculas a oración si no tiene dígitos (fórmulas)."""
    if p.isupper() and not any(c.isdigit() for c in p):
        return p[:1].upper() + p[1:].lower()
    return p

def construir_cuerpo(parrafos, subtitulos=None, desde=0, hasta=None, quitar_ultimas=0):
    """Construye cuerpo [{t, v}] desde una lista de párrafos."""
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
    """Busca un artículo por slug en importados y retorna sus párrafos."""
    for a in importados:
        if a["slug"] == art_slug:
            return a.get("parrafos", [])
    return []

def buscar_por_titulo_parcial(texto, importados):
    """Busca un artículo cuyo título contiene el texto dado."""
    for a in importados:
        if texto.lower() in a.get("titulo", "").lower():
            return a
    return None

def main():
    print("=== Importación de artículos faltantes ===\n")

    ediciones = cargar_json("ediciones.json")
    importados = cargar_json("importados.json")

    ids_existentes = {a["id"] for a in ediciones["articulos"]}
    print(f"Artículos existentes: {len(ids_existentes)}")
    print(f"Documentos importados: {len(importados)}\n")

    # ── Definición de los 7 artículos a importar ──
    nuevos = []

    # 1. Potabilización Aguada Guzmán
    paras = extraer_parrafos("c_mo_es_la_potabilizaci_n_en_el_paraje_a", importados)
    if paras:
        subtitulos = [p for p in paras if p.strip().endswith("?") and len(p.strip()) < 70]
        nuevos.append({
            "id": "potabilizacion-aguada-guzman",
            "seccion": "ciencia",
            "titulo": "¿Cómo es la potabilización en el paraje Aguada Guzmán?",
            "bajada": "Salimos al paraje para conocer de dónde viene el agua que consumimos todos los días y cómo funciona la planta de ósmosis inversa.",
            "autor": "Samira Curaqueo · Milagros Cruz Pérez",
            "rol": "Estudiantes — Taller de Educación Científica y Tecnológica",
            "sede": "Aguada Guzmán",
            "fecha": "Noviembre 2026",
            "odt": "c_mo_es_la_potabilizaci_n_en_el_paraje_a",
            "cuerpo": construir_cuerpo(paras, subtitulos),
            "epigrafes": []
        })

    # 2. Una mirada sobre la realidad
    paras = extraer_parrafos("clase_9_cientifica_4_a_o_matias_anco_joa", importados)
    if paras:
        subtitulos_detectados = [p.strip() for p in paras if p.strip() in ("Reflexión:",)]
        nuevos.append({
            "id": "una-mirada-sobre-la-realidad",
            "seccion": "cultura",
            "titulo": "Una mirada sobre la realidad",
            "bajada": "La reflexión a través de fotografías: detener el tiempo y observar lo que muchas veces pasa desapercibido.",
            "autor": "Matías Ñanco · Joaquín Bobadilla",
            "rol": "Estudiantes — Taller de Educación Científica y Tecnológica",
            "sede": "Río Chico",
            "fecha": "Noviembre 2026",
            "odt": "clase_9_cientifica_4_a_o_matias_anco_joa",
            "cuerpo": construir_cuerpo(paras, subtitulos_detectados, quitar_ultimas=2),
            "epigrafes": []
        })

    # 3. Los festejos de una localidad
    paras = extraer_parrafos("clase_9_cientifica_4_a_o_rodrigo_fhaile_", importados)
    if paras:
        nuevos.append({
            "id": "los-festejos-de-una-localidad",
            "seccion": "territorio",
            "titulo": "Los festejos de una localidad",
            "bajada": "El Mundial 2026 en Río Chico: nervios, alegría y un pueblo entero celebrando a la Scaloneta.",
            "autor": "Rodrigo Fhaile · Gonzalo Osuna · Aarón Gaminao · Enrique González",
            "rol": "Estudiantes de 1.º a 5.º año",
            "sede": "ESRN Rural — Río Chico",
            "fecha": "Noviembre 2026",
            "odt": "clase_9_cientifica_4_a_o_rodrigo_fhaile_",
            "cuerpo": construir_cuerpo(paras, quitar_ultimas=0),
            "epigrafes": []
        })

    # 4. Problemática del medio ambiente Sierra Pailemán
    paras = extraer_parrafos("kevin_nahuel_sierra_paileman_clase_9_cie", importados)
    if paras:
        subtitulos_detectados = [p.strip() for p in paras if "Problemas de inundación" in p]
        nuevos.append({
            "id": "medio-ambiente-sierra-paileman",
            "seccion": "territorio",
            "titulo": "La problemática del medio ambiente en mi pueblo",
            "bajada": "Inundaciones, minería y el cuidado del ambiente en Sierra Pailemán.",
            "autor": "Kevin Nahuel",
            "rol": "Estudiante — Taller de Educación Científica y Tecnológica",
            "sede": "Sierra Pailemán",
            "fecha": "Noviembre 2026",
            "odt": "kevin_nahuel_sierra_paileman_clase_9_cie",
            "cuerpo": construir_cuerpo(paras, subtitulos_detectados),
            "epigrafes": []
        })

    # 5. La llegada de la primavera
    paras = extraer_parrafos("la_llegada_de_la_primavera", importados)
    if paras:
        nuevos.append({
            "id": "la-llegada-de-la-primavera",
            "seccion": "cultura",
            "titulo": "La llegada de la primavera",
            "bajada": "Una obra colectiva: un árbol que se llena de vida y mariposas para anunciar nuevos comienzos.",
            "autor": "Fernanda Taquí · Jazmín Cardozo · Katerina Maggioni · Deysi Taquí · Agostina Schivndt · Aixa Cardozo · Noelia Gabriel · Kiara Mamaní",
            "rol": "Estudiantes — Taller de Educación Científica y Tecnológica",
            "sede": "ESRN Rural",
            "fecha": "Noviembre 2026",
            "odt": "la_llegada_de_la_primavera",
            "cuerpo": construir_cuerpo(paras, quitar_ultimas=1),
            "epigrafes": []
        })

    # 6. ¡Gol de ciencia!
    paras = extraer_parrafos("rio_chico_estefania_manuel_4_a_o_cientif", importados)
    if paras:
        nuevos.append({
            "id": "gol-de-ciencia",
            "seccion": "ciencia",
            "titulo": "¡Gol de ciencia!",
            "bajada": "La química detrás del Mundial: energía, sudor, polímeros y el oro de la copa.",
            "autor": "Estefanía Manuel",
            "rol": "Estudiante — Taller de Educación Científica y Tecnológica",
            "sede": "Río Chico",
            "fecha": "Noviembre 2026",
            "odt": "rio_chico_estefania_manuel_4_a_o_cientif",
            "cuerpo": construir_cuerpo(paras),
            "epigrafes": []
        })

    # 7. El cuidado del agua (extraído del尾 de Suazo Stefania)
    for imp in importados:
        if imp["slug"] == "clase_n_9__4to_a_o__taller_de_educaci_n_":
            paras = imp.get("parrafos", [])
            # Buscar desde donde empieza el artículo
            idx_inicio = None
            for i, p in enumerate(paras):
                if "cuánta agua usamos" in p.lower() or "¿Alguna vez pensaste" in p:
                    idx_inicio = i
                    break
            if idx_inicio is not None:
                paras_art = paras[idx_inicio:]
                # Quitar líneas AUTOR/SEDE al final
                paras_art = [p for p in paras_art if not p.strip().startswith("AUTOR:") and not p.strip().startswith("SEDE:")]
                nuevos.append({
                    "id": "el-cuidado-del-agua",
                    "seccion": "ciencia",
                    "titulo": "El cuidado del agua",
                    "bajada": "Por qué debemos cuidarla y qué podemos hacer desde nuestras casas para evitar su desperdicio.",
                    "autor": "Suazo Stefania",
                    "rol": "Estudiante — Taller de Educación Científica y Tecnológica",
                    "sede": "Valle Verde A32",
                    "fecha": "Noviembre 2026",
                    "odt": None,
                    "cuerpo": construir_cuerpo(paras_art),
                    "epigrafes": []
                })
            break

    # ── Agregar artículos ──
    print("Artículos a importar:")
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

    # ── Regenerar HTML ──
    print("\nRegenerando HTML...")
    sys.path.insert(0, BASE)
    from construir_revista import main as generar
    generar()

    print("\n=== Listo ===")

if __name__ == "__main__":
    main()
