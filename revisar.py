"""Revision conjunta de la revista, articulo por articulo.

Genera/actualiza control-revision.csv a partir de los 52 articulos
organizados en REVISTA ORDENADA, cruza cada uno con el articulo publicado
en la revista (revista/datos/ediciones.json) y conserva los veredictos
que ya se registraron.

Uso:
  python revisar.py                 -> regenera la tabla y la muestra
  python revisar.py 45 BIEN "nota"  -> anota el veredicto del articulo 045
  python revisar.py --ver 45        -> muestra el detalle del articulo 045
"""
import csv
import io
import json
import os
import re
import sys

BASE = r"C:\Users\black\Desktop\opencode archivos"
ORG = os.path.join(BASE, "REVISTA ORDENADA", "01-ARTICULOS")
INDICE = os.path.join(BASE, "REVISTA ORDENADA", "00-INDICE", "indice.csv")
EDICIONES = os.path.join(BASE, "clase n°4", "revista", "datos", "ediciones.json")
CSV_PATH = os.path.join(BASE, "clase n°4", "control-revision.csv")

COLS = ['orden', 'id_publicado', 'titulo', 'carpeta', 'anio', 'sede', 'autor',
        'fotos', 'parrafos', 'bajada', 'drive', 'duplicado_de', 'carpeta_origen',
        'estado', 'veredicto', 'notas']


def norm(s):
    s = (s or '').lower()
    s = re.sub(r'[^a-z0-9ñáéíóú ]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def articulos_publicados():
    if not os.path.isfile(EDICIONES):
        return {}
    datos = json.load(io.open(EDICIONES, encoding='utf-8'))
    arts = datos if isinstance(datos, list) else datos.get('articulos', [])
    return {a.get('id'): a for a in arts if isinstance(a, dict) and a.get('id')}


def cuerpo_texto(a):
    out = []
    for p in (a.get('cuerpo') or []):
        if isinstance(p, dict):
            out.append(p.get('v') or '')
    return '\n'.join(out)


def mejor_publicado(titulo, cuerpo, publicados, usados):
    """Cruza por titulo normalizado y, si no alcanza, por el texto comun."""
    t = norm(titulo)
    c = set(norm(cuerpo)[:600].split())
    mejor, puntaje = None, 0.0
    for pid, a in publicados.items():
        if pid in usados:
            continue
        pt = norm(a.get('titulo', ''))
        ts = pt and t
        sim_t = (len(set(t.split()) & set(pt.split()))
                 / max(len(set(t.split()) | set(pt.split())), 1)) if ts else 0.0
        pc = set(norm(cuerpo_texto(a))[:600].split())
        sim_c = (len(c & pc) / max(len(c | pc), 1)) if (c and pc) else 0.0
        punt = 0.6 * sim_t + 0.4 * sim_c
        if punt > puntaje:
            mejor, puntaje = pid, punt
    if mejor and puntaje >= 0.30:
        return mejor, round(puntaje, 2)
    return None, 0.0


def lee_articulo(carpeta):
    ruta = os.path.join(ORG, carpeta)
    txt = io.open(os.path.join(ruta, 'articulo.txt'), encoding='utf-8').read()
    fotos = len(os.listdir(os.path.join(ruta, '01-fotos'))) if os.path.isdir(
        os.path.join(ruta, '01-fotos')) else 0
    return txt, fotos


def carga_registro():
    reg = {}
    if os.path.isfile(CSV_PATH):
        for f in csv.DictReader(io.open(CSV_PATH, encoding='utf-8-sig'), delimiter=';'):
            if f.get('orden'):
                reg[f['orden']] = f
    return reg


def construye():
    publicados = articulos_publicados()
    usados = set()
    filas = []
    with io.open(INDICE, encoding='utf-8-sig') as f:
        for f in csv.DictReader(f, delimiter=';'):
            carpeta = f['carpeta']
            txt, fotos = lee_articulo(carpeta)
            pid, sim = mejor_publicado(f['titulo'], txt, publicados, usados)
            if pid:
                usados.add(pid)
            pub = publicados.get(pid) or {}
            cuerpo = cuerpo_texto(pub)
            parrafos = len([p for p in txt.split('\n') if p.strip()])
            filas.append({
                'orden': f['n'],
                'id_publicado': pid or '',
                'titulo': f['titulo'],
                'carpeta': carpeta,
                'anio': f['anio'],
                'sede': pub.get('sede', '') or f['sede'],
                'autor': pub.get('autor', ''),
                'fotos': fotos,
                'parrafos': parrafos,
                'bajada': 'si' if pub.get('bajada') else 'no',
                'drive': 'si' if 'drive.google.com' in txt else 'no',
                'duplicado_de': '',
                'carpeta_origen': f['carpeta_origen'],
                'estado': f['estado'],
                'veredicto': '',
                'notas': '',
            })
            if pid and sim < 0.8:
                filas[-1]['notas'] = f'cruce tenue ({sim})'
    return filas


def guarda(filas):
    with io.open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, delimiter=';', fieldnames=COLS)
        w.writeheader()
        for r in filas:
            w.writerow({c: r.get(c, '') for c in COLS})


def main():
    argv = sys.argv[1:]

    if argv and argv[0] == '--ver':
        n = argv[1].zfill(3)
        filas = {r['orden']: r for r in carga_registro().values()} or \
                {r['orden']: r for r in construye()}
        r = filas.get(n)
        if not r:
            print('no existe el articulo', n)
            return
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return

    filas = construye()
    # los veredictos ya anotados se conservan: primero por id publicado y
    # luego por titulo, porque el orden del inventario no coincide con el
    # de la revista (p.ej. el-chip-en-la-cancha era 1 y ahora es 009).
    previas = carga_registro()
    por_id = {p['id_publicado']: p for p in previas.values() if p.get('id_publicado')}
    por_tit = {norm(p.get('titulo')): p for p in previas.values() if p.get('titulo')}
    for r in filas:
        p = por_id.get(r['id_publicado']) or por_tit.get(norm(r['titulo']))
        if p:
            r['veredicto'] = p.get('veredicto', '') or r['veredicto']
            r['notas'] = p.get('notas', '') or r['notas']
    guarda(filas)

    if len(argv) >= 2:
        n = argv[0].zfill(3)
        ver = argv[1]
        nota = argv[2] if len(argv) > 2 else ''
        for r in filas:
            if r['orden'] == n:
                r['veredicto'] = ver
                if nota:
                    r['notas'] = (r['notas'] + ' | ' if r['notas'] else '') + nota
        guarda(filas)
        print(f'anotado {n}: {ver}')

    for r in filas:
        marca = {'BIEN': 'OK  '}.get(r['veredicto'], '    ')
        print(f"{marca}{r['orden']}  {r['titulo'][:52]:<52} "
              f"pub={r['id_publicado'][:22]:<22} drive={r['drive']} "
              f"fotos={r['fotos']} {r['notas'][:30]}")


if __name__ == '__main__':
    main()
