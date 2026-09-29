/* =====================================================================
   RURAL — Datos de la edición 01
   Los artículos viven ACÁ como datos (principio editorial 27):
   agregar una nota = agregar un objeto; nunca tocar el HTML.
   ===================================================================== */

const EDICION = {
  numero: "01",
  titulo: "Rural",
  subtitulo: "Revista digital de la ESRN Rural Virtual",
  epigrafe: "Ciencia, territorio y comunidad desde los parajes de Río Negro",
  fecha: "Diciembre 2026",
  edicion_etiqueta: "Edición N.º 01 — Diciembre 2026",
};

/* Secciones de la revista (orden del sumario).
   clave interna es también el id de la sección en navegación y CSS. */
const SECCIONES = [
  {
    id: "escuela",
    n: "01",
    titulo: "Escuela",
    bajada: "La vida institucional: proyectos, talleres y experiencias de nuestra ESRN Rural.",
  },
  {
    id: "ciencia",
    n: "02",
    titulo: "Ciencia y tecnología",
    bajada: "Investigaciones, experimentos y preguntas que nacen en el taller.",
  },
  {
    id: "territorio",
    n: "03",
    titulo: "Territorio",
    bajada: "Historias, comunidades, parajes y ambiente de la ruralidad rionegrina.",
  },
  {
    id: "voces",
    n: "04",
    titulo: "Voces",
    bajada: "Entrevistas, testimonios y conversaciones con nuestra comunidad.",
  },
  {
    id: "estudiantes",
    n: "05",
    titulo: "Estudiantes",
    bajada: "Producciones, proyectos y miradas de quienes hacen la revista.",
  },
  {
    id: "cultura",
    n: "06",
    titulo: "Cultura",
    bajada: "Literatura, arte, música y fotografía desde el territorio.",
  },
  {
    id: "futuro",
    n: "07",
    titulo: "Futuro",
    bajada: "Carreras, estudios superiores, trabajo y proyectos de vida.",
  },
];

/* ---------------------------------------------------------------------
   ARTÍCULOS
   - texto: verbatim de los .odt/.docx de estudiantes (clase 9)
   - foto: trayectoria relativa dentro de images/ (lista => galería)
   --------------------------------------------------------------------- */

const ARTICULOS = [
  {
    id: "el-chip-en-la-cancha",
    seccion: "ciencia",
    clase: "portada-principal",     // protagonista de portada
    titulo: "El Chip en la Cancha: la ciencia dentro de la pelota",
    bajada:
      "¿Cómo saben los árbitros si una pelota cruzó la línea por un milímetro? Abrimos el balón para descubrir la física, la electrónica y la matemática que se esconden detrás de cada pase.",
    autor: "Julian Echegoy",
    rol: "Estudiante 4.º año — Taller de Educación Científica y Tecnológica",
    sede: "Aguada de Guerra",
    fecha: "Noviembre 2026",
    foto_principal: "ciencia/el-chip-en-la-cancha/foto_01.png",
    fotos: [
      "ciencia/el-chip-en-la-cancha/foto_01.png",
      "ciencia/el-chip-en-la-cancha/foto_02.png",
    ],
    epigrafes: [
      "El sensor CTR-CORE, corazón tecnológico del balón.",
      "El chip no afecta la trayectoria: se suspende con tensores elásticos.",
    ],
    cuerpo: [
      { t: "p", v: "¿Alguna vez te preguntaste cómo hacen los árbitros para saber si una pelota cruzó la línea de gol por un milímetro, o si hubo un fuera de juego invisible al ojo humano? En el fútbol actual, las decisiones ya no dependen solo de la intuición de las personas. Hoy, el corazón del juego es tecnológico: las pelotas oficiales de los torneos más importantes llevan un sensor inteligente en su interior que revoluciona el arbitraje y la ciencia del deporte." },
      { t: "p", v: "Conocer cómo funciona esta tecnología nos permite descubrir que una simple pelota es, en realidad, un complejo dispositivo científico. A continuación, abrimos el balón para explorar la física, la electrónica y la matemática que se esconden detrás de cada pase." },
      { t: "h3", v: "Tecnología invisible: el sensor CTR-CORE" },
      { t: "p", v: "En el centro geométrico de la pelota se suspende un pequeño chip mediante un sistema de tensores elásticos para que el peso no afecte su trayectoria. Este dispositivo contiene una Unidad de Medición Inercial (IMU) que envía datos de posición y movimiento a una velocidad asombrosa de 500 veces por segundo. Funciona con una pequeña batería recargable por inducción (sin cables) y transmite ondas de radiofrecuencia hacia las antenas instaladas alrededor de la cancha para rastrear el balón en tiempo real." },
      { t: "p", v: "Este chip trabaja en equipo con cámaras de alta velocidad distribuidas en el estadio. Cuando un jugador patea, el sensor detecta el impacto exacto (el milisegundo exacto del “contacto”). Al cruzar estos datos con los algoritmos informáticos, el sistema del VAR puede determinar si había una posición adelantada en el momento preciso del pase. Además, el chip mide la velocidad del disparo, la aceleración y las revoluciones por minuto del giro de la pelota, aplicando principios de cinemática y dinámica física." },
      { t: "h3", v: "Impacto en la salud y el rendimiento" },
      { t: "p", v: "Más allá de cobrar un gol, los datos del sensor se usan para la salud de los atletas. Al medir la fuerza de los impactos, los cuerpos médicos analizan el desgaste muscular y la potencia acumulada de los jugadores. Esto ayuda a diseñar entrenamientos personalizados, regular las cargas de esfuerzo físico para prevenir lesiones graves y planificar una nutrición celular adecuada para la recuperación del plantel." },
      { t: "p", v: "La tecnología en la pelota nos demuestra que la ciencia no se queda encerrada en un laboratorio con tubos de ensayo, sino que rueda con nosotros en el patio y en la cancha. Analizar estas innovaciones en nuestra escuela nos invita a pensar cómo las herramientas digitales transforman nuestras actividades cotidianas, transformando la pasión del juego en una oportunidad para aprender y explorar el mundo técnico que nos rodea." },
    ],
  },
  {
    id: "la-primera-ley-de-newton",
    seccion: "ciencia",
    titulo: "La primera ley de Newton: la ley de la inercia",
    bajada:
      "Todo permanece quieto, salvo que una fuerza lo cambie. Un principio fundamental de la física que explica cómo se comportan los objetos.",
    autor: "Estudiantes 4.º año",
    rol: "Taller de Educación Científica y Tecnológica",
    sede: "Río Chico / Valle Verde",
    fecha: "Noviembre 2026",
    foto_principal: "ciencia/la-primera-ley-de-newton/foto_01.jpeg",
    fotos: [
      "ciencia/la-primera-ley-de-newton/foto_01.jpeg",
      "ciencia/la-primera-ley-de-newton/foto_02.jpg",
    ],
    epigrafes: [
      "Un objeto quieto se queda quieto; uno en movimiento sigue moviéndose.",
    ],
    cuerpo: [
      { t: "p", v: "Todo permanece quieto, salvo que una fuerza lo cambie. De esto tratará el siguiente artículo." },
      { t: "p", v: "La ley de inercia es uno de los principios fundamentales de la física que permite comprender cómo se comportan los objetos cuando no actúan fuerzas sobre ellos y es la base para estudiar el movimiento en mecánica." },
      { t: "h3", v: "¿Qué es la ley de la inercia?" },
      { t: "p", v: "Un objeto quieto se queda quieto y un objeto en movimiento sigue moviéndose en línea recta y a la misma velocidad. Esto pasa siempre, a menos que una fuerza de afuera actúe sobre él." },
      { t: "p", v: "La inercia es la tendencia de los objetos a mantener su estado de reposo o de movimiento a menos que una fuerza externa actúe sobre ellos. Se observa en situaciones comunes como el frenado brusco de un auto, donde el cuerpo se va hacia adelante, o cuando un objeto quieto en una mesa no se mueve solo. La primera ley de Newton, también conocida como la ley de la inercia, establece que un objeto en reposo permanecerá en reposo y un objeto en movimiento continuará en movimiento con velocidad constante, a menos que una fuerza externa actúe sobre él." },
      { t: "p", v: "Esta ley es fundamental en la mecánica clásica y sienta las bases para comprender el comportamiento de los objetos bajo la influencia de fuerza, siendo crucial para la física y la ingeniería." },
    ],
  },
  {
    id: "el-partido-por-el-ambiente",
    seccion: "ciencia",
    titulo: "El partido por el ambiente",
    bajada:
      "¿Alguna vez pensaste que una cancha de fútbol también puede ser un espacio para aprender a cuidar el ambiente?",
    autor: "Leandro Yanca · Milena Yanca · Alma Maidana · Leonardo Maidana",
    rol: "Estudiantes de 1.º, 3.º, 4.º y 5.º año",
    sede: "ESRN Rural Anexo 21 — Río Chico",
    fecha: "Noviembre 2026",
    foto_principal: "ciencia/el-partido-por-el-ambiente/foto_01.jpg",
    fotos: [
      "ciencia/el-partido-por-el-ambiente/foto_01.jpg",
      "ciencia/el-partido-por-el-ambiente/foto_02.jpg",
    ],
    epigrafes: [
      "La maqueta de la cancha, construida en equipo.",
    ],
    cuerpo: [
      { t: "p", v: "A partir de esta pregunta, nos propusimos realizar una actividad diferente en la clase de segundas lenguas: construir una maqueta de una cancha de fútbol como parte de “El partido por el ambiente”." },
      { t: "p", v: "Durante esta experiencia trabajamos en equipo, utilizamos nuestra creatividad y reflexionamos sobre el cuidado de nuestro entorno. A través de la construcción de nuestra maqueta, descubrimos que el deporte también puede ser una oportunidad de aprender, compartir ideas y promover acciones que ayuden a proteger el ambiente. En nuestra revista digital queremos compartir nuestro trabajo, mostrar cómo fue el proceso de construcción y contar qué aprendimos durante esta experiencia." },
      { t: "p", v: "Algunos de los materiales que utilizamos fueron: cartón, cinta de papel, plasticola, hojas rayadas y, por último, colores." },
      { t: "h3", v: "La transición: pensar la cancha como enseñanza" },
      { t: "p", v: "Conocer más sobre las canchas de fútbol que existen en nuestro planeta es el primer paso para aprender a cuidar nuestro ambiente. Es importante reflexionar sobre lo que sucede en estos espacios y pensar qué podemos hacer para evitar seguir contaminando y dañando nuestro planeta." },
      { t: "p", v: "De esta manera, descubrimos que una cancha de fútbol también puede convertirse en un espacio para aprender a cuidar el ambiente y pensar juntos cómo podemos protegerlo. Podemos mantener la cancha limpia, separar los residuos, reciclar y evitar desperdiciar agua. Así, mientras jugamos, compartimos y nos divertimos, también aprendemos a respetar, cuidar y proteger nuestro planeta." },
      { t: "p", v: "Ser cuidadosos con nuestras canchas siempre nos ayudará a jugar, compartir y divertirnos de manera más tranquila, segura y saludable. Cuidar estos espacios es una responsabilidad de todos: mantenerlos limpios, respetar la naturaleza y hacer un uso responsable de los recursos también forma parte del juego. Porque cuando cuidamos nuestra cancha, también cuidamos a quienes la disfrutan y a nuestro planeta. Cada pequeña acción cuenta y, entre todos, podemos lograr canchas más limpias, saludables y agradables para jugar." },
    ],
  },
  {
    id: "la-fiesta-del-paraje-treneta",
    seccion: "territorio",
    titulo: "Tradición, encuentro y raíces de nuestra comunidad",
    bajada:
      "Cada mes de febrero, el paraje Treneta se prepara para vivir una de las celebraciones más esperadas: la Fiesta del Paraje Treneta.",
    autor: "ESRN Rural — Anexo Treneta",
    rol: "Comunidad y estudiantes",
    sede: "Paraje Treneta",
    fecha: "Febrero (edición especial)",
    foto_principal: "territorio/fiestas-y-tradiciones-mundialistas/foto_01.jpg",
    fotos: [
      "territorio/fiestas-y-tradiciones-mundialistas/foto_01.jpg",
      "territorio/fiestas-y-tradiciones-mundialistas/foto_02.jpg",
      "territorio/fiestas-y-tradiciones-mundialistas/foto_03.jpg",
      "territorio/fiestas-y-tradiciones-mundialistas/foto_04.jpg",
      "territorio/fiestas-y-tradiciones-mundialistas/foto_05.jpg",
    ],
    epigrafes: [
      "La Fiesta del Paraje Treneta convoca a toda la comunidad.",
      "Momentos de la jornada: desfile, almuerzo popular y música.",
    ],
    cuerpo: [
      { t: "p", v: "Cada mes de febrero, el paraje Treneta se prepara para vivir una de las celebraciones más esperadas por su comunidad: una fiesta que reúne a familias, vecinos, instituciones y visitantes para compartir, celebrar y mantener vivas las costumbres que forman parte de nuestra identidad rural." },
      { t: "p", v: "La jornada comienza con el acto protocolar, un momento de reconocimiento y encuentro en el que se pone en valor la historia del paraje y el trabajo de quienes, día a día, construyen y sostienen la vida de la comunidad." },
      { t: "h3", v: "Desfiles, tradición y encuentro" },
      { t: "p", v: "Uno de los momentos más esperados es el desfile cívico de las instituciones, donde escuelas, organizaciones y diferentes actores de la comunidad participan mostrando con orgullo su pertenencia. Luego, el desfile criollo llena las calles de una colorida muestra de tradiciones, caballos y agrupaciones que representan nuestra cultura rural." },
      { t: "p", v: "La celebración continúa con el almuerzo popular, una gran mesa comunitaria donde se comparte el tradicional asado para todos. Es el momento del encuentro, de la charla y de la alegría compartida." },
      { t: "p", v: "Cuando cae la tarde, llega la jineteada, con las destrezas criollas que ponen en escena la habilidad de jinetes y caballos: la monta con encimera y bastos, la gurupa sureña y otras categorías que reúnen a participantes de toda la región." },
      { t: "p", v: "La fiesta del Paraje Treneta es mucho más que una celebración: es un momento en el que la comunidad se encuentra, se reconoce y renueva sus lazos. Las tradiciones se transmiten de generación en generación, y cada año la revista del rural vuelve a contar esa historia con orgullo." },
    ],
  },
  {
    id: "próxima-parada-atractivos-mundialistas",
    seccion: "territorio",
    titulo: "Próxima parada: atractivos mundialistas",
    bajada:
      "Un recorrido por los puntos más interesantes que esperan ser visitados en la gran cita deportiva.",
    autor: "Estudiantes 4.º año",
    rol: "Taller de Educación Científica y Tecnológica",
    sede: "ESRN Rural",
    fecha: "Noviembre 2026",
    foto_principal: "territorio/proxima-parada-atractivos-mundialistas/foto_02.png",
    fotos: [
      "territorio/proxima-parada-atractivos-mundialistas/foto_01.png",
      "territorio/proxima-parada-atractivos-mundialistas/foto_02.png",
      "territorio/proxima-parada-atractivos-mundialistas/foto_03.png",
      "territorio/proxima-parada-atractivos-mundialistas/foto_04.png",
      "territorio/proxima-parada-atractivos-mundialistas/foto_05.png",
      "territorio/proxima-parada-atractivos-mundialistas/foto_06.png",
    ],
    epigrafes: [
      "El recorrido mundialista, parada por parada.",
    ],
    cuerpo: [
      { t: "p", v: "Fue entonces momento de planificar el trayecto que la Selección Argentina recorrería por el país. Así surgió la idea de pensar el mundial como un viaje: cada estadio, cada ciudad, cada atractivo es una parada de un recorrido que une el deporte con la geografía y el turismo de nuestro territorio." },
      { t: "p", v: "En el taller nos propusimos armar un itinerario propio, eligiendo los puntos que consideramos imperdibles. El resultado es una guía pensada desde la mirada de los estudiantes: qué ver, dónde quedarse y qué hace especial a cada lugar." },
      { t: "h3", v: "Una agenda para descubrir" },
      { t: "p", v: "Cada parada incluye un dato curioso, una recomendación y una foto. Así, la revista se transforma en una herramienta para conocer el país a través del mundial, uniendo propuestas turísticas, cultura y deporte." },
    ],
  },
  {
    id: "el-partido-por-el-ambiente-temporal",
    seccion: "escuela",
    titulo: "Introducción: la revista, un proyecto de todos",
    bajada:
      "La clase N.º 9 del Taller de Educación Científica y Tecnológica da origen a esta publicación digital.",
    autor: "ESRN Rural Virtual",
    rol: "Taller de Educación Científica y Tecnológica — Ciencias Naturales",
    sede: "Todas las sedes",
    fecha: "Noviembre 2026",
    foto_principal: "escuela/portada-escuela.svg",
    fotos: [],
    epigrafes: [],
    cuerpo: [
      { t: "p", v: "Este año continuaremos realizando una nueva edición de la Revista del Rural. A continuación les compartiremos los pasos para organizar nuestra participación: escribir, fotografiar, investigar, entrevistar y diseñar la publicación que reúne las voces de nuestra comunidad educativa." },
      { t: "p", v: "La revista no es solo una página: es un proyecto colectivo donde confluyen el taller de Educación Científica y Tecnológica, las ciencias naturales, las segundas lenguas y todas las sedes de la ESRN Rural Virtual. Cada artículo que vas a leer fue escrito, ilustrado y pensado por estudiantes de los parajes de Río Negro." },
    ],
  },
];

/* Para pruebas nav/búsqueda: lista plana de títulos y autores */
const INDICE_BUSQUEDA = ARTICULOS.map((a) => ({
  id: a.id,
  titulo: a.titulo,
  bajada: a.bajada,
  autor: a.autor,
  seccion: a.seccion,
  url: "articulos/" + a.id + ".html",
}));
