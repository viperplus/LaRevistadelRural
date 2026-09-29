#!/usr/bin/env python3
import json, os, sys, re, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')
PDF_BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTÍCULOS PDF'

def cargar_json(nombre):
    with open(os.path.join(DATOS, nombre), encoding='utf-8') as f:
        return json.load(f)

def guardar_json(nombre, data):
    with open(os.path.join(DATOS, nombre), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def limpiar(txt):
    txt = re.sub(r'PDF\+?\s*\d*', '', txt)
    txt = txt.replace('Aquí tienes la digitalización completa del texto del documento provisto:', '')
    txt = txt.replace('Aquí tienes la transcripción completa y detallada del documento provisto, organizado para reflejar fielmente su contenido:', '')
    return txt.strip()

def a_parrafos(txt):
    paras = []
    for l in txt.split('\n'):
        l = l.strip()
        if not l or l == 'PDF':
            continue
        if re.match(r'^(SEDE:|TUTOR|CURSO:|NOMBRE Y APELLIDO:|PARTICIPANTES:|TEMA:|4TO AÑO|PDF)', l):
            continue
        paras.append(l)
    return paras

def es_sub(p):
    p = p.strip()
    return len(p) < 80 and (p.endswith(':') or p.endswith('?'))

def de_shout(p):
    if p.isupper() and not any(c.isdigit() for c in p):
        return p[:1].upper() + p[1:].lower()
    return p

def cuerpo(paras, quitar=0):
    if quitar > 0:
        paras = paras[:-quitar]
    r = []
    for p in paras:
        p = de_shout(p.strip())
        if not p:
            continue
        if es_sub(p):
            r.append({"t": "h3", "v": p})
        else:
            r.append({"t": "p", "v": p})
    return r

def main():
    ediciones = cargar_json('ediciones.json')
    importados = cargar_json('importados.json')
    ids = {a['id'] for a in ediciones['articulos']}

    articulos_nuevos = [
        {
            'id': 'no-solo-un-encuentro-de-sedes',
            'carpeta': 'Nueva carpeta (3)',
            'seccion': 'escuela',
            'titulo': 'No solo un encuentro de sedes...',
            'bajada': 'Mas de 120 personas de todas las sedes se juntaron en Viedma y El Condor para convivir, compartir y demostrar que unidos somos una gran comunidad.',
            'autor': 'Milagros Martinez / Noe Palma Rama',
            'rol': 'Estudiantes 4. ano',
            'sede': 'El Condor',
            'quitar_final': 0,
        },
        {
            'id': 'hay-algo-mas-en-las-fotos',
            'carpeta': 'Nueva carpeta (4)',
            'seccion': 'cultura',
            'titulo': 'Hay algo mas en las fotos',
            'bajada': 'Una foto de un paisaje o un retrato va mas alla de un simple recuerdo. Que hay detras de cada imagen?',
            'autor': 'Bianca Guaiquian',
            'rol': 'Estudiante 4. ano',
            'sede': 'Yaminue',
            'quitar_final': 1,
        },
        {
            'id': 'no-a-la-basura',
            'carpeta': 'Nueva carpeta (8)',
            'seccion': 'ciencia',
            'titulo': 'No a la basura...!',
            'bajada': 'Las causas, consecuencias y soluciones del problema de la basura en la ruta.',
            'autor': 'Giuliano Prospitti, Sahira Contreras, Valentino Velazquez',
            'rol': 'Estudiantes 4. ano',
            'sede': 'Lago Pellegrini',
            'quitar_final': 5,
        },
        {
            'id': 'cuidar-el-ambiente-kral',
            'carpeta': 'Nueva carpeta (9)',
            'seccion': 'ciencia',
            'titulo': 'Cuidar el ambiente tambien esta en nuestras manos',
            'bajada': 'Contaminacion, reduccion de residuos, cuidado del agua y los espacios verdes: acciones sencillas para todos.',
            'autor': 'Kral Milena',
            'rol': 'Estudiante 4. ano',
            'sede': 'Lago Pellegrini',
            'quitar_final': 4,
        },
        {
            'id': 'cuidar-nuestro-ambiente-seco',
            'carpeta': 'Nueva carpeta (12)',
            'seccion': 'ciencia',
            'titulo': 'Cuidar nuestro ambiente tambien es cuidar nuestro futuro',
            'bajada': 'Cuidar el agua, el suelo, el aire y los seres vivos es importante para nuestra comunidad y para las generaciones futuras.',
            'autor': 'Seco Gabriela',
            'rol': 'Estudiante 4. ano',
            'sede': 'Aguada de Guerra',
            'quitar_final': 1,
        },
    ]

    nuevos = []
    for cfg in articulos_nuevos:
        if cfg['id'] in ids:
            print(f"  [SKIP] {cfg['id']}")
            continue

        txt_path = os.path.join(PDF_BASE, cfg['carpeta'], 'Nuevo documento de texto.txt')
        if not os.path.exists(txt_path):
            print(f"  [FALTA] {cfg['id']}: {txt_path}")
            continue

        with open(txt_path, encoding='utf-8') as f:
            raw = f.read()

        raw = limpiar(raw)
        paras = a_parrafos(raw)

        # Skip header line if it matches title
        if paras and cfg['titulo'].lower()[:20] in paras[0].lower():
            paras = paras[1:]

        art = {
            'id': cfg['id'],
            'seccion': cfg['seccion'],
            'titulo': cfg['titulo'],
            'bajada': cfg['bajada'],
            'autor': cfg['autor'],
            'rol': cfg['rol'],
            'sede': cfg['sede'],
            'fecha': 'Noviembre 2026',
            'odt': None,
            'cuerpo': cuerpo(paras, quitar=cfg.get('quitar_final', 0)),
            'epigrafes': [],
        }
        nuevos.append(art)
        ids.add(cfg['id'])

    print(f"\nNuevos para importar: {len(nuevos)}")
    for a in nuevos:
        ediciones['articulos'].append(a)
        print(f"  [OK] {a['id']} - {a['titulo']}")

    guardar_json('ediciones.json', ediciones)

    print("\nRegenerando HTML...")
    sys.path.insert(0, BASE)
    from construir_revista import main as generar
    generar()
    print("\nListo!")

if __name__ == '__main__':
    main()
