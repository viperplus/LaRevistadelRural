#!/usr/bin/env python3
import json, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')
IMG_SRC = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTÍCULOS PDF\Nueva carpeta (3)'
IMG_DST = os.path.join(BASE, 'ediciones', '01', 'imagenes', 'encuentro-de-sedes')

os.makedirs(IMG_DST, exist_ok=True)
print(f'Creando carpeta: {IMG_DST}')

# Copiar fotos
fotos = []
epigrafes = []
for i, f in enumerate(sorted(os.listdir(IMG_SRC))):
    if f.endswith('.png'):
        src = os.path.join(IMG_SRC, f)
        dst = os.path.join(IMG_DST, f'foto_{i+1:02d}.png')
        try:
            shutil.copy2(src, dst)
            fotos.append(f'imagenes/encuentro-de-sedes/foto_{i+1:02d}.png')
            epigrafes.append('Encuentro de sedes en Viedma y El Condor.')
            print(f'Copiada: {f}')
        except Exception as e:
            print(f'Error copiando {f}: {e}')

print(f'Fotos copiadas: {len(fotos)}')

cuerpo = [
    {"t": "p", "v": "Mas de 120 personas de todas las sedes de la ESRN Rural Virtual se reunieron en Viedma y el balneario El Condor para convivir, compartir experiencias y demostrar que la comunidad educativa esta mas unida que nunca."},
    {"t": "p", "v": "Durante cuatro dias, estudiantes, tutores y familias recorrieron la costa, participaron de actividades recreativas, disfrutaron del cine movil y vivieron momentos que quedaran en la memoria de todos."},
    {"t": "h3", "v": "Dia 1: Llegada y costanera"},
    {"t": "p", "v": "Un colectivo llevo a todas las sedes hasta la costa de Viedma. Lo primero fue un paseo por la costanera, donde el aire del mar y las primeras caras conocidas hicieron que la emocion comenzara a crecer. Despues, un chapuzon en la pileta compartido por todos."},
    {"t": "h3", "v": "Dia 2: Cine y escuela"},
    {"t": "p", "v": "El segundo dia fue para recorrer Viedma. Un paseo exhaustivo termino en la escuela Paulo Sexto, donde todos compartieron el almuerzo y pudimos ver la pelicula Yamka y el espiritu del volcan gracias al cine movil. Una experiencia que nos unio aun mas."},
    {"t": "h3", "v": "Dia 3: Playa y chorizada"},
    {"t": "p", "v": "Al tercer dia, todas las sedes convivimos en la playa de El Condor. Minijuegos, actividades y el sol de la costa hicieron que todos se divirtieran como nunca. Para cerrar la noche, una gran chorizada donde todos compartimos y nos despedimos antes del ultimo dia."},
    {"t": "h3", "v": "Dia 4: Centro Cultural y despedida"},
    {"t": "p", "v": "El cuarto y ultimo dia, la manana fue para el Centro Cultural de Viedma, donde presenciamos varios bailes y coros de ninos a temas populares. Luego, cada sede se fue a su lugar natal, llevando consigo recuerdos inolvidables."},
    {"t": "p", "v": "Mas de 120 personas demostraron que la convivencia, el respeto y la alegria son posibles cuando compartimos un mismo camino. Porque cada sede dejo un poco de si misma en Viedma y El Condor, este encuentro no fue solo un viaje, sino el recordatorio de que unidos somos una gran comunidad."},
]

art = {
    "id": "no-solo-un-encuentro-de-sedes",
    "seccion": "escuela",
    "titulo": "No solo un encuentro de sedes...",
    "bajada": "Mas de 120 personas de todas las sedes se juntaron en Viedma y El Condor para convivir, compartir y demostrar que unidos somos una gran comunidad.",
    "autor": "Milagros Martinez / Noe Palma Rama",
    "rol": "Estudiantes 4. ano",
    "sede": "El Condor",
    "fecha": "Noviembre 2026",
    "odt": None,
    "cuerpo": cuerpo,
    "fotos": fotos,
    "epigrafes": epigrafes
}

ediciones_path = os.path.join(DATOS, 'ediciones.json')
with open(ediciones_path, encoding='utf-8') as f:
    ediciones = json.load(f)

for i, a in enumerate(ediciones['articulos']):
    if a['id'] == 'no-solo-un-encuentro-de-sedes':
        ediciones['articulos'][i] = art
        print(f'Reemplazado: {art["id"]}')
        break

with open(ediciones_path, 'w', encoding='utf-8') as f:
    json.dump(ediciones, f, ensure_ascii=False, indent=2)

sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
