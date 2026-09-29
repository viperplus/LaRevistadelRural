#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')

with open(os.path.join(DATOS, 'ediciones.json'), encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    if art['id'] == 'que-pasaria-sin-agua':
        art['cuerpo'] = [
            {"t": "p", "v": "¿Alguna vez pensaste qué pasaría si un día abrimos la canilla y no sale agua? El agua es muy importante para nuestra vida, ya que la usamos todos los días para tomar, cocinar, bañarnos y muchas otras cosas. En este artículo vamos a hablar sobre por qué tenemos que cuidarla y qué pasaría si algún día faltara."},
            {"t": "p", "v": "A veces usamos el agua sin pensar que no es un recurso que nunca se termina. Por eso, es importante conocer para qué la necesitamos y aprender algunas formas sencillas de cuidarla."},
            {"t": "h3", "v": "El agua es vital"},
            {"t": "p", "v": "El agua es necesaria para todos los seres vivos. Las personas la necesitamos para hidratarnos, cocinar, bañarnos y mantener nuestra higiene. También es importante para los animales y las plantas, ya que sin agua no podrían vivir."},
            {"t": "h3", "v": "¿Qué pasaría si faltara?"},
            {"t": "p", "v": "Si algún día nos quedáramos sin agua, nuestra vida cambiaría mucho. No podríamos tomar agua, preparar alimentos ni realizar actividades que hacemos todos los días. Además, las plantas se secarían y muchos animales tendrían dificultades para sobrevivir."},
            {"t": "h3", "v": "¿Cómo podemos cuidarla?"},
            {"t": "p", "v": "Por eso, es importante no desperdiciarla. Podemos cuidarla cerrando la canilla mientras nos lavamos los dientes, tomando duchas más cortas y evitando dejar correr el agua sin necesidad. Aunque parezcan acciones pequeñas, entre todos podemos hacer una gran diferencia."},
            {"t": "h3", "v": "La contaminación del agua"},
            {"t": "p", "v": "Además, otro problema que afecta al agua es la contaminación. Cuando se tiran residuos, basura o sustancias contaminantes en los ríos, lagos y mares, el agua puede dejar de ser segura para las personas, los animales y las plantas. Por eso, también es importante no tirar basura en lugares donde pueda llegar al agua y cuidar los espacios naturales."},
            {"t": "p", "v": "El agua es un recurso muy importante para la vida y debemos cuidarla todos los días. Cada pequeña acción cuenta y, si todos ponemos de nuestra parte, podemos evitar desperdiciarla. Cuidar el agua es cuidar nuestro futuro."},
        ]
        print(f'Arreglado: {art["id"]}')

with open(os.path.join(DATOS, 'ediciones.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
