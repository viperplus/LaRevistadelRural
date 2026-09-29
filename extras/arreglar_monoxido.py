#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')

with open(os.path.join(DATOS, 'ediciones.json'), encoding='utf-8') as f:
    data = json.load(f)

for art in data['articulos']:
    if art['id'] == 'monoxido-de-carbono-pame':
        art['cuerpo'] = [
            {"t": "p", "v": "¿Te imaginas un peligro en tu casa que no lo puedas ver, ni oler, ni saborear pero puede ser muy peligroso para tu salud? ¡Ese peligro existe y se llama monóxido de carbono!"},
            {"t": "h3", "v": "¿Qué es el monóxido de carbono?"},
            {"t": "p", "v": "Es un gas incoloro (no tiene color), inoloro (no tiene olor) e insípido (no tiene sabor) por eso se dice que es el asesino invisible. Esto se forma cuando se queman cosas como por ejemplo: gas, leña, nafta o carbón sin que tengan suficiente oxígeno."},
            {"t": "p", "v": "Cuando lo respiramos entra a la sangre y evita que el oxígeno se transporte a nuestro cuerpo y esto puede dañar a nuestros órganos más importantes como el corazón y el cerebro."},
            {"t": "h3", "v": "¿Qué prácticas del hogar pueden ser peligrosas?"},
            {"t": "p", "v": "Dormir con brasas o llamas encendidas. Usar el horno o las hornallas para calefaccionarse. Colocar calefones en espacios cerrados. Encender motores de combustibles en garajes o en espacios sin ventilación."},
            {"t": "h3", "v": "¿Cómo nos damos cuenta?"},
            {"t": "p", "v": "Los síntomas son: dolor de cabeza, mareos, náuseas, cansancio, dolor de pecho, dificultad para respirar y vómito. Señales que nos avisan: las llamas de las cocinas de gas son amarillas o anaranjadas (deben estar celestes o azules) y la aparición de hollín o tiznado alrededor del artefacto."},
            {"t": "h3", "v": "¿Cómo protegernos?"},
            {"t": "p", "v": "Revisar los aparatos de gas una vez al año por un profesional. Mantener ventilación. No calefaccionarse con el horno ni las hornallas. No dejar el vehículo encendido en el garaje."},
            {"t": "p", "v": "El monóxido de carbono es un peligro real ¡pero se puede prevenir! — Pame Loncoman"},
        ]
        print(f'Arreglado: monoxido-de-carbono-pame')

with open(os.path.join(DATOS, 'ediciones.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
