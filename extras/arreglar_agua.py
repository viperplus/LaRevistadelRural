#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')

with open(os.path.join(DATOS, 'ediciones.json'), encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    if art['id'] == 'el-cuidado-del-agua':
        art['cuerpo'] = [
            {"t": "p", "v": "¿Alguna vez pensaste cuánta agua usamos en nuestra vida cotidiana? El agua es un recurso vital, pero no siempre la cuidamos como debemos."},
            {"t": "h3", "v": "¿Por qué debemos cuidar el agua?"},
            {"t": "p", "v": "El agua es esencial para la vida. La usamos para beber, cocinar, bañarnos, lavar y muchas cosas más. Pero el agua no es infinita, y en muchas comunidades rurales es difícil de obtener. Por eso, debemos valorarla y cuidarla."},
            {"t": "h3", "v": "¿Qué podemos hacer desde casa?"},
            {"t": "p", "v": "Cerrar la canilla mientras nos lavamos los dientes o las manos. No dejar que el agua corra sin necesidad. Reparar las fugas de agua en las cañerías. Usar menos agua al lavar los platos o la ropa."},
            {"t": "h3", "v": "Cuidar el agua en la comunidad"},
            {"t": "p", "v": "No tirar basura ni productos químicos al río o al arroyo. Mantener limpios los lugares donde se encuentra el agua. Participar de campañas de cuidado del agua en la escuela y la comunidad."},
            {"t": "p", "v": "El agua es un recurso que debemos cuidar todos los días. Cada pequeña acción cuenta para que todos puedan acceder a agua limpia y segura."},
            {"t": "p", "v": "— Suazo Stefania. Sede: Valle Verde A32."},
        ]
        art['fotos'] = []
        art['epigrafes'] = []
        print(f'Arreglado: el-cuidado-del-agua')

with open(os.path.join(DATOS, 'ediciones.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
