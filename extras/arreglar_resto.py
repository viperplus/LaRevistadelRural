#!/usr/bin/env python3
"""Arreglar artículos restantes sin subtítulos."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')

with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

# ========================================
# ARTÍCULOS A ARREGLAR
# ========================================

MEJORAS = {
    '1_reflexi_n_a_trav_s_de_fotograf_a': {
        'titulo': 'Reflexión a través de la fotografía',
        'bajada': 'Aguada Cecilio: un paraje para visitar y admirar.',
        'seccion': 'cultura',
        'cuerpo': [
            {'t': 'p', 'v': 'Aguada Cecilio es un paraje para visitar y admirar. Sus paisajes son únicos y muestran la belleza de nuestra región.'},
            {'t': 'h3', 'v': 'El Cerrito Amarillo'},
            {'t': 'p', 'v': 'Una de las mejores vistas es la del "Cerrito Amarillo", uno de los 5 cerritos amarillos de Argentina. Está compuesto principalmente por rocas sedimentarias con presencia de azufre o limonita.'},
            {'t': 'h3', 'v': 'La Aguadita'},
            {'t': 'p', 'v': 'La Aguadita es el manantial natural de agua dulce que dio origen al paraje. Es un lugar muy bonito para visitar.'},
            {'t': 'h3', 'v': 'El Puente Colorado'},
            {'t': 'p', 'v': 'El Puente Colorado es uno de los lugares más lindos del paraje. Es un punto de encuentro para los vecinos y visitantes.'},
            {'t': 'p', 'v': 'A través de la fotografía, podemos capturar la belleza de estos lugares y compartirla con otros.'},
        ],
    },
    'reflexi_n_a_trav_s_de_fotograf_a': {
        'titulo': 'Reflexión a través de la fotografía',
        'bajada': 'Aguada Cecilio: un paraje para visitar y admirar.',
        'seccion': 'cultura',
        'cuerpo': [
            {'t': 'p', 'v': 'Aguada Cecilio es un paraje para visitar y admirar. Sus paisajes son únicos y muestran la belleza de nuestra región.'},
            {'t': 'h3', 'v': 'El Cerrito Amarillo'},
            {'t': 'p', 'v': 'Una de las mejores vistas es la del "Cerrito Amarillo", uno de los 5 cerritos amarillos de Argentina. Está compuesto principalmente por rocas sedimentarias con presencia de azufre o limonita.'},
            {'t': 'h3', 'v': 'La Aguadita'},
            {'t': 'p', 'v': 'La Aguadita es el manantial natural de agua dulce que dio origen al paraje. Es un lugar muy bonito para visitar.'},
            {'t': 'h3', 'v': 'El Puente Colorado'},
            {'t': 'p', 'v': 'El Puente Colorado es uno de los lugares más lindos del paraje. Es un punto de encuentro para los vecinos y visitantes.'},
            {'t': 'p', 'v': 'A través de la fotografía, podemos capturar la belleza de estos lugares y compartirla con otros.'},
        ],
    },
    'la_primera_ley_de_newton': {
        'titulo': 'La primera ley de Newton',
        'bajada': 'Todo permanece quieto, salvo que una fuerza lo cambie.',
        'seccion': 'ciencia',
        'cuerpo': [
            {'t': 'p', 'v': 'Todo permanece quieto, salvo que una fuerza lo cambie. De esto tratará el siguiente artículo.'},
            {'t': 'h3', 'v': '¿Qué es la ley de inercia?'},
            {'t': 'p', 'v': 'Esta ley dice que si una fuerza actúa, el cuerpo cambia su velocidad o dirección. La ley de inercia es uno de los principios fundamentales de la física.'},
            {'t': 'p', 'v': 'Un objeto quieto se queda quieto y un objeto en movimiento sigue moviéndose en línea recta y a la misma velocidad. Esto pasa siempre, a menos que una fuerza de afuera actúe sobre él.'},
            {'t': 'h3', 'v': '¿Dónde se aplica?'},
            {'t': 'p', 'v': 'La inercia se observa en situaciones comunes como el frenado brusco de un auto, donde el cuerpo se va hacia adelante, o cuando un objeto quieto en una mesa no se mueve solo.'},
            {'t': 'h3', 'v': 'Importancia'},
            {'t': 'p', 'v': 'Esta ley es fundamental en la mecánica clásica y sienta las bases para comprender el comportamiento de los objetos bajo la influencia de fuerzas.'},
        ],
    },
    'los_festejos_de_una_localidad': {
        'titulo': 'Los festejos de una localidad',
        'bajada': '¿Alguna vez pensaste cómo un deporte puede unir tanto a una comunidad?',
        'seccion': 'territorio',
        'cuerpo': [
            {'t': 'p', 'v': '¿Alguna vez pensaste cómo un deporte puede unir tanto a una comunidad? A lo largo del tiempo podemos ver cómo los festejos argentinos han sido eufóricos y cargados de una pasión inexplicable.'},
            {'t': 'p', 'v': 'Esto ha sido trasladado a distintas zonas del país, algunas más eufóricas que otras, y otras un tanto calmadas.'},
            {'t': 'h3', 'v': 'La Scaloneta nos unió'},
            {'t': 'p', 'v': 'Durante el mundial de fútbol FIFA World Cup 2026, en Río Chico se vivió el fútbol con mucha emoción y entusiasmo. Cada partido de la selección Argentina se esperaba con muchas ganas.'},
            {'t': 'p', 'v': 'A medida que la Scaloneta avanzaba de ronda, aumentaba la emoción y las ganas de verla llegar a la final.'},
            {'t': 'h3', 'v': 'La final contra España'},
            {'t': 'p', 'v': 'Era todo perfecto hasta que llegó la final contra España. Se vivió con muchos nervios, ilusión y orgullo por todo el camino recorrido.'},
            {'t': 'h3', 'v': 'Recuerdos inolvidables'},
            {'t': 'p', 'v': 'El mundial dejó recuerdos inolvidables en toda la comunidad. Los festejos en las calles, los mates compartidos y la emoción de ver a la selección Argentina en la final.'},
        ],
    },
    'clase_n_10_cient_fica_y_tecnol_gicaintegrantes_agu': {
        'titulo': 'Nuestro Mundial 2026',
        'bajada': 'La experiencia del Mundial 2026 en la escuela.',
        'seccion': 'escuela',
        'cuerpo': [
            {'t': 'p', 'v': 'El Mundial 2026 fue una experiencia increíble para toda la comunidad de Peñas Blancas.'},
            {'t': 'h3', 'v': 'La preparación'},
            {'t': 'p', 'v': 'Decoramos la escuela con banderas argentinas y preparamos todo para ver los partidos juntos. Fue una experiencia muy emotiva.'},
            {'t': 'h3', 'v': 'El día del partido'},
            {'t': 'p', 'v': 'El 22 de junio vimos el partido todos juntos. La emoción se sentía en el aire. Cada gol era celebrado por toda la comunidad.'},
            {'t': 'h3', 'v': 'Los festejos'},
            {'t': 'p', 'v': 'Después de cada victoria, salimos a festejar a las calles. Compartimos mates, abrazos y lágrimas de alegría.'},
            {'t': 'p', 'v': 'El Mundial 2026 nos enseñó que el deporte une a las personas y crea lazos que duran toda la vida.'},
        ],
    },
}

# ========================================
# APLICAR MEJORAS
# ========================================

for art in data['articulos']:
    if art['id'] in MEJORAS:
        mejora = MEJORAS[art['id']]
        art.update(mejora)
        print(f'Mejorado: {art["id"]} -> {art["titulo"]}')

# Guardar
with open(DATOS, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Regenerar
sys.path.insert(0, BASE)
from construir_revista_v2 import main as generar
generar()
print('Listo!')
