#!/usr/bin/env python3
"""Mejorar TODOS los artículos del 2do año."""
import json, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista'
DATOS = os.path.join(BASE, 'datos', 'ediciones.json')
EDIT = os.path.join(BASE, 'ediciones', '01')
SRC = r'C:\Users\black\Desktop\opencode archivos\clase n°4\ARTICULOS 2DO AÑO'

with open(DATOS, encoding='utf-8') as f:
    data = json.load(f)

# ========================================
# ARTÍCULOS A MEJORAR - CONTENIDO CORREGIDO
# ========================================

MEJORAS = {
    'latido_del_equilibrio_ambiental_en_naupa_huen': {
        'titulo': 'Latido del equilibrio ambiental en Naupa Huén',
        'bajada': 'El ambiente es el espacio donde vivimos. Cuidarlo es responsabilidad de todos.',
        'seccion': 'ciencia',
        'cuerpo': [
            {'t': 'p', 'v': 'El ambiente es el espacio donde vivimos, donde se encuentran los seres vivos, el agua, el suelo, el aire y las plantas. Por eso es muy importante cuidarlo y protegerlo de la contaminación.'},
            {'t': 'h3', 'v': '¿Por qué es importante cuidar el ambiente?'},
            {'t': 'p', 'v': 'Para comprender mejor la importancia del cuidado ambiental, a continuación veremos algunas acciones que podemos realizar todos los días.'},
            {'t': 'h3', 'v': '¿Qué podemos hacer?'},
            {'t': 'p', 'v': 'Una de las formas más importantes de cuidar el ambiente es reciclar. Separamos los residuos orgánicos de los inorgánicos y colocamos los plásticos, papeles y vidrios en los contenedores correspondientes.'},
            {'t': 'p', 'v': 'Además, debemos ahorrar energía apagando las luces y los aparatos electrodomésticos cuando no los usamos. También es importante ahorrar agua cerrando bien las canillas.'},
            {'t': 'p', 'v': 'Plantar árboles es otra forma de cuidar el ambiente. Los árboles nos dan oxígeno y ayudan a reducir la contaminación del aire.'},
            {'t': 'p', 'v': 'En conclusión, cuidar el ambiente es responsabilidad de todos. Con pequeñas acciones podemos hacer una gran diferencia para nuestro planeta.'},
        ],
    },
    'acciones_peque_as_para_un_mundo_grande': {
        'titulo': 'Acciones pequeñas para un mundo grande',
        'bajada': '¿Alguna vez te has preguntado en qué afectan los microbasurales?',
        'seccion': 'ciencia',
        'cuerpo': [
            {'t': 'p', 'v': '¿Alguna vez te has preguntado en qué afectan los microbasurales? Los microbasurales se han vuelto muy comunes últimamente en nuestra región.'},
            {'t': 'h3', 'v': '¿Qué son los microbasurales?'},
            {'t': 'p', 'v': 'Conocer cómo se forman los microbasurales es el primer paso para cuidar nuestro ambiente. Los microbasurales son acumulaciones de basura en lugares no autorizados.'},
            {'t': 'h3', 'v': '¿Qué daños causan?'},
            {'t': 'p', 'v': 'Los daños que generan son ambiental: contaminan el suelo y el agua subterránea. También representan riesgo para la salud: atraen ratas, insectos y otros animales que transmiten enfermedades.'},
            {'t': 'h3', 'v': '¿Qué podemos hacer?'},
            {'t': 'p', 'v': 'Podemos ayudar separando la basura, reciclando y tirando los residuos en los lugares correspondientes. También es importante concientizar a nuestra comunidad sobre los problemas que causan los microbasurales.'},
            {'t': 'p', 'v': 'Con acciones pequeñas podemos lograr un mundo más grande y limpio. Cada persona puede aportar desde su lugar para mejorar nuestro entorno.'},
        ],
    },
    'nueva_carpeta_10': {
        'titulo': 'Un problema que nos afecta a todos',
        'bajada': 'El problema del basurero a cielo abierto en Cerro Policia y sus consecuencias para la salud y el ambiente.',
        'seccion': 'ciencia',
        'cuerpo': [
            {'t': 'p', 'v': 'En Cerro Policia existe un gran problema ambiental: un basurero a cielo abierto que afecta a toda la comunidad.'},
            {'t': 'h3', 'v': '¿Qué es un basurero a cielo abierto?'},
            {'t': 'p', 'v': 'Un basurero a cielo abierto es un lugar donde se acumula basura sin ningún tipo de tratamiento. Esta basura contamina el suelo, el agua y el aire.'},
            {'t': 'h3', 'v': 'Consecuencias para la salud'},
            {'t': 'p', 'v': 'Las consecuencias para la salud son graves: problemas respiratorios, irritación de piel y ojos, y enfermedades transmitidas por los animales que se acercan a la basura.'},
            {'t': 'h3', 'v': 'Consecuencias para el ambiente'},
            {'t': 'p', 'v': 'El basurero contamina el suelo y el agua subterránea. Los animales se acercan a buscar comida y pueden enfermarse. El humo de la quema de basura contamina el aire.'},
            {'t': 'h3', 'v': '¿Qué podemos hacer?'},
            {'t': 'p', 'v': 'Podemos ayudar separando la basura, reciclando y tirando los residuos en los lugares correspondientes. También es importante concientizar a la comunidad sobre los problemas del basurero.'},
        ],
    },
    'nueva_carpeta_12': {
        'titulo': 'Prevención y concientización comunitaria',
        'bajada': 'El monóxido de carbono: un enemigo invisible que podemos prevenir.',
        'seccion': 'ciencia',
        'cuerpo': [
            {'t': 'p', 'v': 'El monóxido de carbono es un gas tóxico, incoloro e inodoro que se produce por la combustión incompleta de combustibles como gas, leña o carbón.'},
            {'t': 'h3', 'v': '¿Qué es el monóxido de carbono?'},
            {'t': 'p', 'v': 'Es un gas que no tiene olor ni color, por eso se dice que es el asesino invisible. Se forma cuando la combustión no tiene suficiente oxígeno.'},
            {'t': 'h3', 'v': '¿Cómo afecta al cuerpo?'},
            {'t': 'p', 'v': 'El monóxido de carbono daña la hemoglobina, la proteína que transporta oxígeno en la sangre. Los síntomas incluyen dolor de cabeza, mareos, náuseas y somnolencia.'},
            {'t': 'h3', 'v': '¿Cómo prevenirlo?'},
            {'t': 'p', 'v': 'Es importante revisar los aparatos de gas una vez al año. Mantener siempre buena ventilación. No usar el horno ni las hornallas para calefaccionarse. Y si la llama es amarilla, apagar todo y ventilar.'},
            {'t': 'p', 'v': 'La prevención y la concientización comunitaria son fundamentales para evitar tragedias por monóxido de carbono.'},
        ],
    },
    'nueva_carpeta_2': {
        'titulo': 'Un pequeño descanso, una gran importancia',
        'bajada': 'La pausa de hidratación en el fútbol: por qué es importante y qué pasa si no existe.',
        'seccion': 'ciencia',
        'cuerpo': [
            {'t': 'p', 'v': '¿Alguna vez te preguntaste por qué hay una pausa en el medio del partido de fútbol? Esta pausa se llama "drinking break" o pausa de hidratación.'},
            {'t': 'h3', 'v': '¿Qué es la pausa de hidratación?'},
            {'t': 'p', 'v': 'Es un descanso de 3 minutos que se toma en el segundo tiempo del partido. Su objetivo es que los jugadores se hidraten y recuperen la temperatura corporal.'},
            {'t': 'h3', 'v': 'Beneficios para la salud'},
            {'t': 'p', 'v': 'Esta pausa ayuda a bajar la temperatura del cuerpo, reponer los electrolitos perdidos con el sudor y prevenir golpes de calor. Es fundamental para la salud de los jugadores.'},
            {'t': 'h3', 'v': '¿Qué pasa si no hay pausa?'},
            {'t': 'p', 'v': 'Si no hay pausa, los jugadores pueden sufrir fatiga, calambres y una disminución importante en su rendimiento. En casos extremos, puede haber desmayos y problemas graves de salud.'},
            {'t': 'p', 'v': 'La pausa de hidratación es un pequeño descanso que tiene una gran importancia para la salud y el rendimiento de los jugadores.'},
        ],
    },
    'nueva_carpeta_3': {
        'titulo': 'Las células',
        'bajada': 'Qué son las células, sus partes y funciones.',
        'seccion': 'ciencia',
        'cuerpo': [
            {'t': 'p', 'v': 'Las células son las unidades básicas de la vida. Todo ser vivo está formado por células, desde las bacterias más simples hasta los seres humanos.'},
            {'t': 'h3', 'v': '¿Qué son las células?'},
            {'t': 'p', 'v': 'Una célula es una unidad pequeña que tiene vida propia. Puede ser de dos tipos: procariotas (sin núcleo definido) y eucariotas (con núcleo definido).'},
            {'t': 'h3', 'v': 'Partes de la célula'},
            {'t': 'p', 'v': 'Las partes principales de una célula son: la membrana celular (que la protege), el citoplasma (donde ocurren las reacciones químicas) y el núcleo (que contiene la información genética).'},
            {'t': 'h3', 'v': 'Funciones de la célula'},
            {'t': 'p', 'v': 'Las células tienen varias funciones: obtener energía, crecer, reproducirse y comunicarse con otras células. Cada tipo de célula tiene funciones específicas.'},
            {'t': 'h3', 'v': 'Células animales y vegetales'},
            {'t': 'p', 'v': 'Las células animales y vegetales tienen diferencias importantes. Las células vegetales tienen pared celular y cloroplastos, que las células animales no tienen.'},
        ],
    },
    'nueva_carpeta_8': {
        'titulo': 'Los paisajes de Cerro Policia',
        'bajada': 'Análisis fotográfico de los paisajes de Cerro Policia.',
        'seccion': 'cultura',
        'cuerpo': [
            {'t': 'p', 'v': 'Cerro Policia es un lugar con paisajes muy hermosos. En este artículo, analizaremos algunas fotos que muestran la belleza de nuestra región.'},
            {'t': 'h3', 'v': 'El cerro icónico'},
            {'t': 'p', 'v': 'El Cerro Policia tiene una forma característica que lo hace fácil de reconocer. Su silhouette se parece a un gorra de policía, de ahí viene su nombre.'},
            {'t': 'h3', 'v': 'El camino hacia Santa Lucía'},
            {'t': 'p', 'v': 'El camino que conecta Cerro Policia con Santa Lucía ofrece paisajes impresionantes. Las bardas y la vegetación hacen de este recorrido una experiencia única.'},
            {'t': 'h3', 'v': 'La identidad del pueblo'},
            {'t': 'p', 'v': 'Los paisajes de Cerro Policia son parte de la identidad de nuestro pueblo. A través de la fotografía, podemos capturar y compartir la belleza de nuestro entorno.'},
        ],
    },
    'nueva_carpeta_10': {
        'titulo': 'Un problema que nos afecta a todos',
        'bajada': 'El problema del basurero a cielo abierto en Cerro Policia.',
        'seccion': 'ciencia',
        'cuerpo': [
            {'t': 'p', 'v': 'En Cerro Policia existe un gran problema: un basurero a cielo abierto que contamina el medio ambiente y afecta la salud de los vecinos.'},
            {'t': 'h3', 'v': 'El problema'},
            {'t': 'p', 'v': 'El basurero acumula grandes cantidades de residuos sin ningún tipo de tratamiento. Esto contamina el suelo, el agua y el aire.'},
            {'t': 'h3', 'v': 'Consecuencias'},
            {'t': 'p', 'v': 'Las consecuencias son graves: problemas respiratorios, enfermedades de piel, y contaminación del agua subterránea que utilizamos para consumo.'},
            {'t': 'h3', 'v': '¿Qué podemos hacer?'},
            {'t': 'p', 'v': 'Es importante separar la basura, reciclar y tirar los residuos en los lugares correspondientes. También debemos concientizar a la comunidad sobre este problema.'},
        ],
    },
}

# ========================================
# ARTÍCULOS CON TEXTO DEL PDF (limpiar)
# ========================================

def limpiar_texto_pdf(texto):
    """Limpia el texto extraído de PDF."""
    # Eliminar líneas que son solo "PDF"
    lineas = [l for l in texto.split('\n') if l.strip() and l.strip() != 'PDF']
    return '\n'.join(lineas)

def limpiar_metadata(texto):
    """Elimina metadata de clase del inicio del texto."""
    patrones = [
        r'CLASE \d+.*?ESTUDIANTE[S]?:.*?\n',
        r'CLASE \d+.*?SEDE:.*?\n',
        r'CLASE \d+.*?TUTOR[A]?:.*?\n',
        r'NOMBRE Y APELLIDO:.*?\n',
        r'SEDE:.*?\n',
        r'TUTOR/A:.*?\n',
    ]
    for patron in patrones:
        texto = re.sub(patron, '', texto, flags=re.IGNORECASE)
    return texto.strip()

# ========================================
# APLICAR MEJORAS
# ========================================

for art in data['articulos']:
    if art['id'] in MEJORAS:
        mejora = MEJORAS[art['id']]
        art.update(mejora)
        print(f'Mejorado: {art["id"]} -> {art["titulo"]}')

# ========================================
# LIMPIAR ARTÍCULOS CON TEXTO DEL PDF
# ========================================

for art in data['articulos']:
    cuerpo = art.get('cuerpo', [])
    nuevo_cuerpo = []
    
    for p in cuerpo:
        # Eliminar párrafos que son solo "PDF"
        if p.get('v', '').strip() == 'PDF':
            continue
        
        # Limpiar metadata
        titulo = p.get('v', '').strip()
        titulo = limpiar_metadata(titulo)
        
        # Eliminar consignas de clase
        if titulo in ['Introducción:', 'Transición:', 'Cuerpo del artículo:', 'Introducción', 'Transición', 'Cuerpo del artículo']:
            continue
        
        # Eliminar líneas que empiezan con "Introducción:", etc.
        if titulo.startswith('Introducción:') or titulo.startswith('Transición:') or titulo.startswith('Cuerpo del artículo:'):
            continue
        
        if titulo:
            nuevo_cuerpo.append(p)
    
    if len(nuevo_cuerpo) != len(cuerpo):
        art['cuerpo'] = nuevo_cuerpo
        print(f'Limpiado: {art["id"]} ({len(cuerpo)} -> {len(nuevo_cuerpo)} párrafos)')

# Guardar
with open(DATOS, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Regenerar
sys.path.insert(0, BASE)
from construir_revista_v2 import main as generar
generar()
print('Listo!')
