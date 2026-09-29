#!/usr/bin/env python3
import json, sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos')

with open(os.path.join(DATOS, 'ediciones.json'), encoding='utf-8') as f:
    data = json.load(f)

def limpiar(txt):
    txt = re.sub(r'PDF\+?\s*\d*', '', txt)
    return txt.strip()

def a_cuerpo_con_subtitulos(titulo_original, txt):
    """Convierte texto limpio en cuerpo con subtítulos automáticos."""
    # Separar por párrafos (3+ espacios o saltos de línea)
    partes = re.split(r'\s{3,}|\n\n', txt)
    paras = []
    for p in partes:
        p = p.strip()
        if not p or p == 'PDF':
            continue
        if re.match(r'^(SEDE:|TUTOR|CURSO:|NOMBRE|PARTICIPANTES:|TEMA:|4TO AÑO|CLASE|CIENTÍFICA)', p):
            continue
        if p == titulo_original:
            continue
        paras.append(p)
    
    # Detectar subtítulos: líneas cortas que terminan en : o ? o que son títulos de sección
    resultado = []
    for p in paras:
        lineas = p.split('\n')
        for l in lineas:
            l = l.strip()
            if not l or l == 'PDF':
                continue
            # Es subtítulo si es corto y termina en : o ?
            if len(l) < 60 and (l.endswith(':') or l.endswith('?')):
                resultado.append({"t": "h3", "v": l})
            # Es subtítulo si parece título (empieza con mayúscula y es corto)
            elif len(l) < 40 and l[0].isupper() and not l.endswith('.'):
                resultado.append({"t": "h3", "v": l})
            else:
                resultado.append({"t": "p", "v": l})
    return resultado

# Artículos que necesitan subtítulos (según análisis)
articulos_subtitulos = {
    'los-festejos-de-una-localidad': {
        'cuerpo': [
            {"t": "p", "v": "¿Alguna vez pensaste como un deporte puede unir tanto a una comunidad? A lo largo del tiempo podemos ver como los festejos Argentinos han sido eufóricos y cargados de una pasión inexplicable, que podemos decir que al día de hoy ya es propio de nosotros como nación."},
            {"t": "p", "v": "Esto ha sido trasladado a distintas zonas del país, algunas más eufóricas que otras, y otras un tanto calmadas. A continuación les daremos detalladamente los festejos de nuestra localidad."},
            {"t": "h3", "v": "La Scaloneta nos unió"},
            {"t": "p", "v": "Durante el mundial de fútbol Fifa World Cup 2026, en Río Chico se vivió el fútbol con mucha emoción y entusiasmo. Cada partido de la selección Argentina se esperaba con muchas ganas y todos queríamos que la Scaloneta ganara. Habían nervios cuando el partido estaba parejo y mucha alegría cuando Argentina lograba ganar."},
            {"t": "p", "v": "A medida que la Scaloneta avanzaba de ronda, aumentaba la emoción y las ganas de verla llegar a la final. Hasta que llegó el momento de jugar contra los ingleses, ese partido se vivió de una manera diferente, había nervios, ansiedad y preocupación, pero después de los 90 minutos logró ganar la Scaloneta."},
            {"t": "p", "v": "Esa tarde salimos a festejar todo el pueblo, llorábamos, pero no de tristeza, sino de alegría, ese festejo se vivió como si Argentina hubiera ganado la final."},
            {"t": "h3", "v": "La final contra España"},
            {"t": "p", "v": "Era todo perfecto hasta que llegó la final contra España. Se vivió con muchos nervios, ilusión y orgullo por todo el camino recorrido. Aunque la Argentina haya perdido la final, quedó la tristeza por no conseguir el campeonato, pero también mucho orgullo."},
            {"t": "h3", "v": "Recuerdos inolvidables"},
            {"t": "p", "v": "El mundial 2026 en Río Chico conseguimos muchos recuerdos, emociones y momentos compartidos con la familia y la comunidad. En conclusión, el mundial 2026 se vivió con mucha fe y emoción en Río Chico. Fue una oportunidad para compartir con la familia y los amigos, sentir orgullo por nuestra selección y disfrutar juntos de cada partido."},
        ],
        "fotos": [],
        "epigrafes": []
    },
    'la-llegada-de-la-primavera': {
        'cuerpo': [
            {"t": "p", "v": "Con esta obra intentamos representar que la primavera ya se acerca y que todo a nuestro alrededor empieza a cambiar."},
            {"t": "h3", "v": "El árbol y las mariposas"},
            {"t": "p", "v": "Elegimos un árbol porque representa la vida y el crecimiento. En sus ramas colocamos mariposas de muchos colores para mostrar que la naturaleza comienza a llenarse de vida. Queremos transmitir que, con la llegada de la primavera, todo se vuelve más colorido, alegre y luminoso. Las mariposas representan los cambios y las cosas nuevas que están por llegar. También representan la libertad y la posibilidad de comenzar una nueva etapa."},
            {"t": "h3", "v": "Nuevas oportunidades"},
            {"t": "p", "v": "Para nosotros, la primavera no solo significa el cambio de estación, sino también nuevas oportunidades para todos. Así como el árbol vuelve a llenarse de vida, nosotros también podemos dejar atrás los momentos difíciles y empezar de nuevo."},
            {"t": "p", "v": "Con esta obra queremos transmitir esperanza, alegría y que podemos aprovechar cada nueva oportunidad. Creemos que la llegada de la primavera nos recuerda que siempre podemos crecer, cambiar y volver a empezar. Por eso, las mariposas llenan el árbol de color y representan todas las cosas buenas que pueden llegar."},
        ],
        "fotos": [],
        "epigrafes": []
    },
    'gol-de-ciencia': {
        'cuerpo': [
            {"t": "p", "v": "El mundial de fútbol es uno de los eventos deportivos más importantes del mundo. Pero detrás de cada gol, cada carrera y cada esfuerzo de los jugadores también se encuentra la ciencia. La química está presente en el cuerpo de los jugadores, en los materiales que utilizan y hasta en la copa del mundo."},
            {"t": "p", "v": "Aunque el fútbol parece ser solamente un deporte, muchos procesos químicos están presentes durante un partido y ayudan a que los jugadores puedan dar lo mejor de sí."},
            {"t": "h3", "v": "Energía para correr"},
            {"t": "p", "v": "Los jugadores necesitan energía para correr, saltar y patear. Esta energía se obtiene de la glucosa, una molécula proveniente de los alimentos que el cuerpo transforma en energía a través de reacciones químicas."},
            {"t": "h3", "v": "El sudor regula la temperatura"},
            {"t": "p", "v": "El sudor está formado principalmente por agua y sales minerales. Al evaporarse, ayuda a regular la temperatura del cuerpo y evita el sobrecalentamiento durante la actividad física."},
            {"t": "h3", "v": "Materiales de alto rendimiento"},
            {"t": "p", "v": "La pelota, las camisetas y los botines están fabricados con materiales como los polímeros, que les brindan resistencia, comodidad y mejor rendimiento durante el juego."},
            {"t": "h3", "v": "El oro de la copa"},
            {"t": "p", "v": "La copa del mundo contiene oro, un metal valioso, brillante y resistente a la corrosión. Por estas características, es un símbolo perfecto para representar el máximo premio del deporte mundial."},
            {"t": "p", "v": "En conclusión, la química está presente en muchos aspectos del mundial. Esto demuestra que detrás de la emoción y la pasión del fútbol también existe la ciencia."},
        ],
        "fotos": [],
        "epigrafes": []
    },
    'cuidemos-el-ambiente': {
        'cuerpo': [
            {"t": "p", "v": "Cuidar el ambiente es responsabilidad de todos. La sostenibilidad busca proteger los recursos naturales y satisfacer nuestras necesidades sin perjudicar a las futuras generaciones."},
            {"t": "h3", "v": "Acciones simples, grandes cambios"},
            {"t": "p", "v": "Con acciones simples, como reciclar, ahorrar agua y energía y reducir los residuos, podemos ayudar a construir un planeta más saludable. Cuidar el ambiente es fundamental para lograr una vida más saludable y un futuro mejor."},
            {"t": "h3", "v": "¿Qué podemos hacer?"},
            {"t": "p", "v": "El cuidado del ambiente implica adoptar acciones que ayuden a reducir el daño que provocamos en la naturaleza. Algunas de las más importantes son separar y reciclar los residuos, reducir el uso de plástico, ahorrar agua y energía, y mantener limpios los espacios públicos."},
            {"t": "h3", "v": "Sostenibilidad"},
            {"t": "p", "v": "La sostenibilidad es fundamental, porque busca utilizar los recursos naturales de manera responsable. Esto significa aprovechar lo que necesitamos sin desperdiciar ni agotar los recursos del planeta."},
            {"t": "p", "v": "Cada persona puede contribuir realizando pequeños cambios en su vida cotidiana. Si todos asumimos responsabilidad y trabajamos juntos, podemos disminuir la contaminación y construir un ambiente más saludable y sostenible."},
        ],
        "fotos": [],
        "epigrafes": []
    },
    'tecnologia-mundialista': {
        'cuerpo': [
            {"t": "p", "v": "En el Mundial 2026, los árbitros utilizaron un sistema avanzado de tecnología que incluye cámaras corporales, sensores y conexión permanente con inteligencia artificial."},
            {"t": "h3", "v": "Cámaras corporales"},
            {"t": "p", "v": "Una cámara corporal compacta integrada con el uniforme del juez principal, estabilizada por inteligencia artificial. También usaban auriculares y micrófonos incorporados y relojes inteligentes para mantener contacto directo con el VAR."},
            {"t": "h3", "v": "GPS y dispositivos corporales"},
            {"t": "p", "v": "Dispositivo de posicionamiento global para registrar el movimiento del juez en tiempo real. Esta tecnología permite que las decisiones arbitrales sean más precisas y rápidas."},
            {"t": "h3", "v": "Inteligencia artificial"},
            {"t": "p", "v": "El sistema de IA analiza las imágenes de las cámaras y los datos del GPS para detectar jugadas polémicas como el fuera de juego, las manos y las faltas. Esto ayuda a los árbitros a tomar mejores decisiones."},
            {"t": "p", "v": "La tecnología en el Mundial demuestra que el fútbol moderno combina pasión deportiva con innovación científica, haciendo que el juego sea más justo y emocionante para todos."},
        ],
        "fotos": [],
        "epigrafes": []
    },
    'la-contaminacion': {
        'cuerpo': [
            {"t": "p", "v": "La contaminación es un problema que nos afecta a todos. ¿Alguna vez pensaste cómo afecta la contaminación al lugar donde vivimos? La contaminación está presente en nuestro ambiente y puede afectar el agua, el aire y el suelo."},
            {"t": "h3", "v": "Causas de la contaminación"},
            {"t": "p", "v": "Una de las principales causas es la acumulación de residuos. Cuando la basura se arroja en lugares incorrectos, puede contaminar el suelo y el agua. También la contaminación del aire puede producirse por el humo de los vehículos, las industrias y la quema de residuos."},
            {"t": "h3", "v": "¿Qué podemos hacer?"},
            {"t": "p", "v": "Para cuidar nuestro ambiente podemos separar los residuos, evitar tirar basura en la calle, reutilizar materiales y reducir el uso innecesario de productos descartables. También es importante cuidar el agua y los espacios naturales de nuestra comunidad."},
            {"t": "h3", "v": "La educación es clave"},
            {"t": "p", "v": "La educación y la participación de todas las personas son fundamentales para generar hábitos más responsables. Si cada uno aporta desde su lugar, podemos lograr cambios positivos en nuestro entorno."},
            {"t": "p", "v": "La contaminación es un problema que nos involucra a todos. Cuidar el ambiente no significa hacer grandes cosas, sino comenzar con pequeñas acciones todos los días. ¡Cuidar el planeta es cuidar nuestro futuro!"},
        ],
        "fotos": [],
        "epigrafes": []
    },
    'no-a-la-basura': {
        'cuerpo': [
            {"t": "p", "v": "¿No te molesta la basura a tu alrededor? Cada vez que vas por la ruta o caminas por las bardas siempre te encontrás con basura. En este artículo vamos a investigar sus causas, sus consecuencias y qué podemos hacer con este problema."},
            {"t": "h3", "v": "¿De dónde viene la basura?"},
            {"t": "p", "v": "La basura corresponde a los camiones que llevan cargas volátiles que viajan descubiertos, lo que ocasiona que con el viento que genera la velocidad dejan residuos en las banquinas o en los arbustos que hay en la ruta."},
            {"t": "p", "v": "A veces las personas que circulan por la ruta van tirando residuos por las ventanillas y eso causa que con el viento se acumulen en los arbustos o en las jarillas."},
            {"t": "p", "v": "Por la ruta se encuentra un basural donde la gente va a dejar sus residuos en camiones o en camionetas, mientras viajan algunos de estos se van perdiendo en el camino."},
            {"t": "h3", "v": "La quema de basura"},
            {"t": "p", "v": "Otro factor contaminante es la quema y el humo de la basura; la quema de la basura puede extenderse por la zona y eso lleva a un gran problema del campo, el humo también, este puede ser más o menos contaminante según la basura que se quema."},
            {"t": "h3", "v": "Tips para mejorar"},
            {"t": "p", "v": "Clasificar la basura en casa: orgánicos (podemos hacer compost), plásticos (juntar todos los nylon en una botella), vidrios y papeles para reciclar."},
            {"t": "p", "v": "Cuando se transporta la basura, asegurarse de que no se vuele nada. Tirar la basura donde corresponde. Campañas de concientización social."},
        ],
        "fotos": [],
        "epigrafes": []
    },
}

# Aplicar cambios
for art in data['articulos']:
    if art['id'] in articulos_subtitulos:
        cambios = articulos_subtitulos[art['id']]
        art['cuerpo'] = cambios['cuerpo']
        art['fotos'] = cambios.get('fotos', [])
        art['epigrafes'] = cambios.get('epigrafes', [])
        print(f'Arreglado: {art["id"]}')

# Guardar
with open(os.path.join(DATOS, 'ediciones.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Regenerar
sys.path.insert(0, BASE)
from construir_revista import main as generar
generar()
print('Listo!')
