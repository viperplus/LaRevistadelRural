#!/usr/bin/env python3
"""Importar artículos de ARTICULOS 2DO AÑO a ediciones.json"""
import os, sys, json, re, shutil, subprocess
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')
EDIT = os.path.join(BASE, 'ediciones', '01')
SRC = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTICULOS 2DO AÑO'
RAIZ = r'C:\Users\black\Desktop\opencode archivos\clase n°4'

sys.path.insert(0, RAIZ)
import cargar_odt as C

# Mapeo de secciones según el contenido
SECCIONES = {
    'ciencia': 'Ciencia y tecnología',
    'territorio': 'Territorio',
    'cultura': 'Cultura',
    'escuela': 'Escuela',
}

def slug(texto):
    s = re.sub(r'[^a-z0-9_]+', '_', texto.lower()).strip('_')[:50]
    return s or 'articulo'

def extraer_odt(ruta):
    """Extrae texto y fotos de un ODT."""
    try:
        lineas = C.cargar_odt(ruta, os.path.join(EDIT, 'imagenes_odt'))
        titulo = ''
        firma = ''
        parrafos = []
        fotos = []
        for l in lineas:
            if l.startswith('[TITULO]') and not titulo:
                titulo = l[8:].strip()
            elif l.startswith('[FIRMA]') and not firma:
                firma = l[7:].strip()
            elif l.startswith('[FOTO:'):
                fotos.append(l[6:].split(']')[0])
            elif l.startswith('[PARRAFO]'):
                parrafos.append(l[9:].strip())
            elif l.startswith('[SUBTITULO]'):
                parrafos.append(('h3', l[11:].strip()))
        return titulo, firma, parrafos, fotos
    except Exception as e:
        print(f'  ERR ODT: {e}')
        return '', '', [], []

def extraer_txt(carpeta):
    """Lee el archivo .txt de una carpeta Nueva carpeta."""
    txt_file = os.path.join(carpeta, 'Nuevo documento de texto.txt')
    if os.path.isfile(txt_file):
        with open(txt_file, encoding='utf-8') as f:
            return f.read()
    return ''

def parsear_articulo(texto, nombre_archivo=''):
    """Parsea un texto extraído en título, subtítulos, párrafos."""
    lineas = texto.strip().split('\n')
    titulo = ''
    parrafos = []
    subtitulo_actual = ''
    
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        
        # Detectar títulos (líneas en mayúsculas o que empiezan con "#")
        if linea.startswith('#'):
            titulo = linea.lstrip('#').strip()
        elif linea.isupper() and len(linea) > 5 and not titulo:
            titulo = linea
        elif linea.isupper() and len(linea) > 5:
            parrafos.append(('h3', linea.title()))
        else:
            parrafos.append(('p', linea))
    
    if not titulo:
        # Usar nombre del archivo como título
        titulo = os.path.splitext(nombre_archivo)[0]
        titulo = re.sub(r'[_-]', ' ', titulo).strip()
        titulo = titulo.title()
    
    return titulo, parrafos

def crear_articulo(titulo, parrafos, firma, fotos, seccion='ciencia'):
    """Crea un artículo para ediciones.json."""
    uid = slug(titulo)
    
    # Convertir párrafos al formato JSON
    cuerpo = []
    for p in parrafos:
        if isinstance(p, tuple):
            cuerpo.append({'t': p[0], 'v': p[1]})
        else:
            cuerpo.append({'t': 'p', 'v': p})
    
    return {
        'id': uid,
        'titulo': titulo,
        'bajada': parrafos[0][1] if parrafos and isinstance(parrafos[0], tuple) and parrafos[0][0] == 'p' else (parrafos[0] if parrafos else ''),
        'autor': firma or 'Estudiantes',
        'seccion': seccion,
        'fecha': 'Noviembre 2026',
        'fecha_iso': '2026-11-01',
        'cuerpo': cuerpo,
        'fotos': fotos,
        'epigrafes': [''] * len(fotos),
    }

# Cargar artículos existentes
with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

existentes = {a['id'] for a in data['articulos']}
nuevos = []

# 1. Procesar ODTs
print('=== ODTs ===')
for archivo in sorted(os.listdir(SRC)):
    ext = os.path.splitext(archivo)[1].lower()
    if ext not in ('.odt', '.docx'):
        continue
    
    ruta = os.path.join(SRC, archivo)
    print(f'Procesando: {archivo}')
    
    titulo, firma, parrafos, fotos_odt = extraer_odt(ruta)
    if titulo and parrafos:
        art = crear_articulo(titulo, parrafos, firma, [], 'ciencia')
        if art['id'] not in existentes:
            nuevos.append(art)
            existentes.add(art['id'])
            print(f'  -> {art["id"]}: {titulo[:50]}')
        else:
            print(f'  -> Ya existe: {art["id"]}')

# 2. Procesar carpetas Nueva carpeta
print('\n=== Nuevas carpetas ===')
for carpeta in sorted(os.listdir(SRC)):
    if not carpeta.startswith('Nueva carpeta'):
        continue
    
    ruta_carpeta = os.path.join(SRC, carpeta)
    if not os.path.isdir(ruta_carpeta):
        continue
    
    print(f'Procesando: {carpeta}')
    
    # Leer texto
    texto = extraer_txt(ruta_carpeta)
    if not texto:
        print('  -> Sin texto')
        continue
    
    # Parsear artículo
    titulo, parrafos = parsear_articulo(texto, carpeta)
    
    # Buscar fotos
    fotos = []
    for f in sorted(os.listdir(ruta_carpeta)):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            fotos.append(f)
    
    # Crear artículo
    art = crear_articulo(titulo, parrafos, '', fotos, 'ciencia')
    
    if art['id'] not in existentes:
        # Copiar fotos a la carpeta del artículo
        art_dir = os.path.join(EDIT, art['id'])
        os.makedirs(art_dir, exist_ok=True)
        
        fotos_copiadas = []
        for i, f in enumerate(fotos, 1):
            src = os.path.join(ruta_carpeta, f)
            ext = os.path.splitext(f)[1]
            dst = os.path.join(art_dir, f'foto-{i:02d}{ext}')
            shutil.copy2(src, dst)
            fotos_copiadas.append(f'foto-{i:02d}{ext}')
        
        art['fotos'] = fotos_copiadas
        art['epigrafes'] = [''] * len(fotos_copiadas)
        
        nuevos.append(art)
        existentes.add(art['id'])
        print(f'  -> {art["id"]}: {titulo[:50]} ({len(fotos_copiadas)} fotos)')
    else:
        print(f'  -> Ya existe: {art["id"]}')

# Guardar
if nuevos:
    data['articulos'].extend(nuevos)
    with open(DATOS, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'\n=== {len(nuevos)} artículos agregados ===')
    
    # Regenerar
    sys.path.insert(0, BASE)
    from construir_revista_v2 import main as generar
    generar()
else:
    print('\nNo hay artículos nuevos')
