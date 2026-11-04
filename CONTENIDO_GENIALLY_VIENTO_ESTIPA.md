# CONTENIDO PARA GENIALLY - "Viento de la Estepa"
## Documento de implementación: texto listo para copiar y pegar

---

## CONFIGURACIÓN GENERAL DE LA PRESENTACIÓN

### Paleta de colores
| Elemento | Código Hex | Uso |
|----------|-----------|-----|
| Fondo principal | #D9E8F5 | Celeste invernal - todas las slides |
| Estructuras/menús | #C2A671 | Ocre arcilloso - bordes, botones, marcos |
| Tecnología activa | #0F4C81 | Azul baja entropía - cables, alternadores, elementos técnicos |
| Alerta/freno | #D9534F | Rojo teja - límites, peligro, mecanismos de corte |

### Tipografía recomendada
- Títulos: Montserrat Bold o similar sans-serif
- Cuerpo: Open Sans Regular
- Ecuaciones: Ecuation Editor o imagen PNG de las fórmulas

---

## SLIDE 1: PORTADA INTERACTIVA

### Elementos visuales a crear
- Fondo: #D9E8F5
- En la base: siluetas de coirones (SVG o imagen PNG con transparencia)
- Título central grande en #0F4C81

### Textos para copiar

**TÍTULO PRINCIPAL:**
```
Viento de la Estepa
```

**SUBTÍTULO:**
```
Física, tecnología y justicia social en la estepa rionegrina
```

### Implementación de interactividad en Genially

**BOTÓN 1 - "COMENZAR LA AVENTURA":**
- Tipo: Botón con texto
- Texto del botón: ▶️ COMENZAR LA AVENTURA
- Color de fondo del botón: #C2A671
- Color del texto: #FFFFFF
- Acción: "Ir a página" → Seleccionar Slide 2 (Mapa de Ruta)

**BOTÓN 2 - "PREGUNTA ORIENTADORA":**
- Tipo: Icono con Etiqueta (Label)
- Icono: ❓ (colocar en esquina superior derecha)
- Configurar: Seleccionar icono → Acción → "Etiqueta"
- Texto de la etiqueta (aparece al pasar el mouse):
```
Si la Patagonia tiene los vientos más potentes del país, ¿por qué un temporal a veces deja sin luz a las escuelas de la estepa? ¡Descubrámoslo explorando estas diapositivas!
```

---

## SLIDE 2: MAPA DE RUTA (MENÚ PRINCIPAL)

### Elementos visuales a crear
- Fondo: #D9E8F5
- Mapa esquemático horizontal de la Línea Sur de Río Negro
- Ilustraciones: meseta, puestos rurales, escuela hogar, aerogenerador
- 6 marcadores interactivos con animación de "pulso"

### Textos para copiar

**TÍTULO DE LA SLIDE:**
```
Tu Ruta de Exploración
```

**SUBTÍTULO:**
```
Elegí tu propio itinerario. Cada marcador es una puerta a un nuevo conocimiento.
```

### Implementación de marcadores interactivos

Para cada marcador, crear un elemento (icono o forma) y asignarle:

| Marcador | Icono | Texto visible | Acción Genially | Destino |
|----------|-------|---------------|-----------------|---------|
| 1 | 🌀 | La Física del Viento | Ir a página | Slide 3 |
| 2 | ⚙️ | La Tradición del Campo | Ir a página | Slide 4 |
| 3 | 🛑 | El Límite Físico | Ir a página | Slide 5 |
| 4 | ⚠️ | La Paradoja de la Tormenta | Ir a página | Slide 6 |
| 5 | 🔋 | Acumular en el Paraje | Ir a página | Slide 7 |
| 6 | 🏫 | Viento de Justicia Social | Ir a página | Slide 8 |

**BOTÓN ESPECIAL - Desafío Técnico:**
- Texto: 📝 Desafío Técnico
- Acción: Ir a página → Slide 9

**BOTÓN ESPECIAL - Trivia:**
- Texto: 🎮 Pone a Prueba tu Mente
- Acción: Ir a página → Slide 10

**BOTÓN GLOBAL EN TODAS LAS SLIDES:**
- Texto: 🏠 Volver al Menú
- Acción: Ir a página → Slide 2
- Posición: Esquina inferior izquierda (consistente en todas las slides)

---

## SLIDE 3: LA FÍSICA DEL VIENTO (LA ECUACIÓN CINÉTICA)

### Elementos visuales a crear
- Fondo: #D9E8F5
- Ilustración central: flechas azules (#0F4C81) representando corriente de aire intersectando el área de barrido de una hélice
- Recuadro estilo pizarra escolar con la ecuación

### Textos para copiar

**TÍTULO:**
```
La Física del Viento
```

**SUBTÍTULO:**
```
La ecuación que gobierna toda la energía eólica del planeta
```

**ECUACIÓN (imagen o texto):**
```
P = ½ · ρ · A · v³
```

**TEXTO EXPLICATIVO INFERIOR:**
```
La potencia disponible en el viento depende de tres variables físicas. Hacé clic en cada una para descubrir su significado.
```

### Implementación de puntos calientes (Hotspots)

**HOTSPOT 1 - Densidad del aire (ρ):**
- Posicionar sobre la letra ρ en la ecuación
- Seleccionar el elemento → Acción → "Ventana emergente" (Popup)
- Título del popup: "ρ - Densidad del Aire"
- Contenido del popup:
```
El viento no es aire vacío; es una corriente de moléculas de gases con masa física real. En la estepa fría, la densidad promedio es de aproximadamente 1.2 kg/m³.

A menor temperatura, el aire se vuelve más denso y pesado, transportando mayor fuerza de impacto sobre las palas del aerogenerador.
```

**HOTSPOT 2 - Área de barrido (A):**
- Posicionar sobre la letra A en la ecuación
- Acción → "Ventana emergente"
- Título del popup: "A - El Círculo de Captación"
- Contenido del popup:
```
Representa el área interceptada por el giro de las palas:

A = π · r²

Cuanto más largas sean las palas del aerogenerador, el círculo barrido será más grande y capturará una porción mayor de la masa de viento en movimiento. Por eso las turbinas modernas tienen diámetros de hasta 120 metros.
```

**HOTSPOT 3 - Velocidad al cubo (v³):**
- Posicionar sobre v³ en la ecuación
- Acción → "Ventana emergente"
- Título del popup: "v³ - La Regla del Cubo"
- Contenido del popup:
```
¡Aquí es donde la física rompe las estimaciones lineales! La velocidad del viento está elevada al cubo.

Esto significa que si el viento en Maquinchao pasa de un día calmo de 5 m/s (18 km/h) a un día ventoso de 10 m/s (36 km/h), la velocidad se duplicó, pero la potencia disponible en el aire ¡se multiplicó por 8! (2³ = 2 × 2 × 2 = 8)

Por esta razón, el viento patagónico es un recurso extraordinario para generar electricidad.
```

---

## SLIDE 4: TRADICIÓN VS. MODERNIDAD

### Elementos visuales a crear
- Fondo: #D9E8F5
- Layout dividido en dos mitades simétricas
- Izquierda: molino multipala rural de chapa bombeando agua
- Derecha: aerogenerador moderno de 3 palas en torre de acero

### Textos para copiar

**TÍTULO:**
```
Tradición vs. Modernidad
```

**SUBTÍTULO:**
```
Dos siglos de ingeniería eólica: del bombeo mecánico a la generación eléctrica
```

**ETIQUETA IZQUIERDA (debajo del molino):**
```
Molino Multipala (12-24 palas de chapa)
```

**ETIQUETA DERECHA (debajo del aerogenerador):**
```
Aerogenerador Moderno (3 palas aerodinámicas)
```

### Implementación de ventanas emergentes

**BOTÓN IZQUIERDO - "Fórmula de Arrastre" (⚙️):**
- Colocar icono ⚙️ sobre el molino multipala
- Acción → "Ventana emergente"
- Título: "El Molino Multipala - Arrastre Aerodinámico"
- Contenido:
```
Funciona porque el viento choca directamente contra sus 12 a 24 chapas de hierro y las empuja mecánicamente (arrastre).

FÍSICA DEL SISTEMA:
• Funciona a baja velocidad y ALTO TORQUE (fuerza de giro)
• Requiere ráfagas muy suaves para empezar a girar
• Esta inmensa fuerza mecánica es ideal para tirar de la pesada varilla de hierro vertical que bombea agua desde pozos subterráneos muy profundos de la estepa
• No necesita corriente eléctrica para funcionar
• Es un sistema de RECURSO DE STOCK (depende del agua del pozo)
```

**BOTÓN DERECHO - "Fórmula de Sustentación" (⚡):**
- Colocar icono ⚡️ sobre el aerogenerador
- Acción → "Ventana emergente"
- Título: "El Aerogenerador Moderno - Sustentación Aerodinámica"
- Contenido:
```
Sus 3 palas estilizadas tienen perfiles alares curvados como las alas de un avión. El aire pasa más rápido por una cara de la pala que por la otra, creando una diferencia de presiones que genera una fuerza de "succión" o empuje lateral (sustentación).

FÍSICA DEL SISTEMA:
• Funciona a alta velocidad de rotación y BAJO TORQUE
• No tiene la fuerza bruta para bombear agua directamente
• Su velocidad de giro es ideal para hacer funcionar un alternador
• Produce corriente eléctrica limpia
• Es un sistema de RECURSO DE FLUJO (depende del viento atmosférico)
```

---

## SLIDE 5: EL TECHO DE LA NATURALEZA (LEY DE ALBERT BETZ)

### Elementos visuales a crear
- Fondo: #D9E8F5
- Izquierda: foto o ilustración de Albert Betz (físico alemán, 1919)
- Derecha: esquema de corriente de viento cruzando una hélice, mostrando reducción de velocidad y desvío de flujo

### Textos para copiar

**TÍTULO:**
```
El Techo de la Naturaleza
```

**SUBTÍTULO:**
```
La Ley de Albert Betz: el límite infranqueable de la física
```

**TEXTO DESTACADO:**
```
Ninguna máquina del planeta puede capturar más del 59.3% de la energía del viento.
```

### Implementación de ventanas emergentes

**BOTÓN 1 - "La Paradoja del Muro de Aire" (🛑):**
- Acción → "Ventana emergente"
- Título: "¿Por qué no existe una máquina 100% eficiente?"
- Contenido:
```
Si un aerogenerador perfecto pudiera absorber el 100% de la energía cinética del viento, la velocidad del aire detrás de sus palas tendría que ser de 0 m/s (el aire quedaría inmóvil).

Pero si el aire se detiene por completo, se formaría un tapón o "muro de aire estancado" detrás del molino. El nuevo viento que viene soplando no podría pasar y tendría que esquivar el aerogenerador por los costados, resultando en una generación de 0 W.

Este es el principio físico que limita toda máquina eólica del universo.
```

**BOTÓN 2 - "El Límite del 59.3%" (📊):**
- Acción → "Ventana emergente"
- Título: "El Límite Físico de Betz (1919)"
- Contenido:
```
Albert Betz calculó matemáticamente el equilibrio de fluidos y la termodinámica óptima. Demostró que el máximo teórico absoluto es del 59.3% (fracción de 16/27).

RENDIMIENTO REAL DE LAS TURBINAS:
• Las turbinas industriales más avanzadas operan al 45% - 50% de eficiencia
• Se pierde energía por fricción mecánica y calor residual (entropía)
• Los catálogos comerciales que prometen eficiencias mayores ¡violan las leyes físicas del universo!

Dato clave: Un aerogenerador real en la estepa rionegrina convierte entre el 35% y el 45% del viento disponible en electricidad útil.
```

---

## SLIDE 6: LA PARADOJA DE LAS TORMENTAS (VELOCIDAD DE CORTE)

### Elementos visuales a crear
- Fondo: #D9E8F5
- Gráfico interactivo de la Curva de Potencia de un aerogenerador
- La curva tiene 3 tramos: ascenso gradual → meseta → corte abrupto a cero
- Cada tramo es clickeable

### Textos para copiar

**TÍTULO:**
```
La Paradoja de las Tormentas
```

**SUBTÍTULO:**
```
Cuando el viento se vuelve demasiado fuerte, el generador se apaga
```

**ETIQUETA DEL GRÁFICO:**
```
Hacé clic en cada tramo de la curva para entender qué sucede
```

### Implementación de tramos interactivos

**TRAMO 1 (curva ascendente inicial) - "Velocidad de Arranque":**
- Color sugerido: verde (#5CB85C)
- Acción → "Etiqueta flotante"
- Contenido:
```
🟢 VELOCIDAD DE ARRANQUE (Cut-in)

Es la brisa mínima necesaria para que las palas venzan la inercia interna de los engranajes y arranquen a girar.

• Valor típico: 3 m/s a 4 m/s (11 a 14 km/h)
• Con menos viento, el rotor permanece quieto
• Generación: 0 W

En la estepa patagónica, esta velocidad se alcanza casi todos los días.
```

**TRAMO 2 (meseta de la curva) - "Velocidad Nominal":**
- Color sugerido: azul (#0F4C81)
- Acción → "Etiqueta flotante"
- Contenido:
```
🔵 VELOCIDAD NOMINAL (Rated Speed)

Es el punto óptimo de funcionamiento donde el alternador alcanza la potencia máxima indicada en su folleto técnico.

• Valor típico: 11 m/s a 13 m/s (unos 45 km/h)
• El generador entrega su potencia nominal (ej: 2 kW)
• Rendimiento máximo del sistema

En la Línea Sur, esta velocidad se alcanza regularmente en los meses de otoño e invierno.
```

**TRAMO 3 (corte abrupto a cero) - "Velocidad de Corte":**
- Color sugerido: rojo (#D9534F)
- Acción → "Ventana emergente"
- Título: "🔴 LA VELOCIDAD DE CORTE (Cut-out)"
- Contenido:
```
CUANDO EL VIENTO ES DEMASIADO FUERTE:

Cuando las ráfagas en la estepa patagónica superan los 25 m/s (90 km/h), el viento ejerce fuerzas extremas sobre la torre y el rotor, arriesgando el colapso de la estructura.

MECANISMO DE SEGURIDAD:
El sistema automático frena mecánicamente el equipo y gira las palas sobre su eje para ponerlas "en bandera" (paralelas al viento para no ofrecer resistencia).

LA PARADOJA:
El equipo se detiene por completo. Por lo tanto, en el día de mayor viento de la tormenta, el generador produce exactamente CERO energía.

Esto demuestra por qué el almacenamiento en baterías es indispensable en la estepa.
```

---

## SLIDE 7: EL CORAZÓN ELÉCTRICO RURAL (SISTEMAS OFF-GRID)

### Elementos visuales a crear
- Fondo: #D9E8F5
- Esquema simplificado del circuito eléctrico de una Escuela Hogar
- Líneas animadas que muestran el flujo de energía
- Componentes: Aerogenerador → Alternador → Regulador de carga → Banco de baterías → Inversor → Luces de las aulas

### Textos para copiar

**TÍTULO:**
```
El Corazón Eléctrico Rural
```

**SUBTÍTULO:**
```
Así funciona el sistema Off-Grid que da luz a las escuelas de la estepa
```

**INSTRUCCIÓN AL USUARIO:**
```
Hacé clic en cada componente del circuito para entender su función
```

### Implementación de componentes interactivos

**COMPONENTE 1 - "Alternador de la Góndola":**
- Elemento: recuadro azul (#0F4C81) sobre la zona del alternador
- Acción → "Etiqueta"
- Contenido:
```
GENERADOR TRIFÁSICO

Transforma la energía mecánica de rotación de las palas en corriente alterna (CA) de frecuencia variable.

La frecuencia de la corriente generada varía con la velocidad del viento, por lo que no es directamente utilizable para los artefactos escolares.
```

**COMPONENTE 2 - "Regulador de Carga":**
- Elemento: recuadro sobre el regulador
- Acción → "Ventana emergente"
- Título: "El Cerebro Eléctrico"
- Contenido:
```
RECIBE la corriente alterna del alternador.

LA RECTIFICA a corriente continua (CC).

CONTROLA con precisión el voltaje de carga para proteger la vida útil química del banco de baterías, evitando sobrecargas térmicas.

Sin este componente, las baterías se destruirían en pocas semanas.
```

**COMPONENTE 3 - "Banco de Baterías":**
- Elemento: recuadro sobre las baterías
- Acción → "Ventana emergente"
- Título: "El Amortiguador Químico"
- Contenido:
```
ALMACENA la energía eléctrica en forma de energía química cuando el viento sopla con fuerza.

LIBERA esa energía de forma continua durante la noche o los períodos de calma patagónica.

GARANTIZA el suministro ininterrumpido en la escuela rural, incluso cuando el viento no sopla.

Tipos comunes: baterías de plomo-ácido o litio, diseñadas para ciclos profundos de carga y descarga.
```

**COMPONENTE 4 - "Inversor / Ondulador":**
- Elemento: recuadro sobre el inversor
- Acción → "Ventana emergente"
- Título: "El Conversor de Onda"
- Contenido:
```
Las baterías entregan corriente continua de 24 V.

Pero los artefactos escolares y las computadoras funcionan con corriente alterna de 220 V a 50 Hz.

El inversor realiza esta conversión mediante conmutación electrónica de alta frecuencia, transformando CC en CA utilizable.

Sin este componente, no se podrían encender las luces, las computadoras ni el equipamiento escolar.
```

---

## SLIDE 8: JUSTICIA SOCIAL Y ENERGÍA (EL IMPACTO DEL PERMER)

### Elementos visuales a crear
- Fondo: #D9E8F5
- Foto o dibujo de una Escuela Hogar en la meseta nevada en invierno
- Mapa comparativo dinámico con botón tipo switch "ANTES" vs. "AHORA"

### Textos para copiar

**TÍTULO:**
```
Justicia Social y Energía
```

**SUBTÍTULO:**
```
El Proyecto PERMER: cómo la energía eólica cambia vidas en la ruralidad
```

### Implementación del switch interactivo

**CONFIGURACIÓN DEL SWITCH:**
- Crear dos estados visuales superpuestos
- Botón toggler que alterna entre ambos estados
- Estado 1: "ANTES (Recursos de Stock)"
- Estado 2: "AHORA (Recursos de Flujo)"

**CONTENIDO ESTADO "ANTES" - Motor Diésel:**
```
LA DEPENDENCIA DEL COMBUSTIBLE FÓSIL

La escuela dependía de motores generadores diésel. Esto requería:

• La compra y el costoso transporte de gasoil (recurso de stock no renovable)
• Camiones que debían transitar huellas rurales intransitables por el barro o el hielo invernal
• El suministro era ruidoso, contaminante y limitado a unas pocas horas al día
• El ruido del motor impedía dar clases durante su funcionamiento
• Dependencia total del precio internacional del petróleo

DATO: El costo de transportar gasoil a un paraje remoto de la Línea Sur puede superar los $500 por litro (incluyendo flete).
```

**CONTENIDO ESTADO "AHORA" - Energía Eólica:**
```
LA AUTONOMÍA DEL VIENTO (PERMER)

El Proyecto de Energías Renovables en Mercados Rurales instala sistemas eólicos Off-Grid autónomos. Al aprovechar el recurso de flujo constante de la estepa (viento), se sustituye la quema de combustibles fósiles.

DERECHOS FUNDAMENTALES GARANTIZADOS:

📚 EDUCACIÓN Y CONECTIVIDAD:
Permite mantener encendidas las antenas de internet satelital y las netbooks escolares, rompiendo el aislamiento de los jóvenes rionegrinos.

🏥 SALUD:
Asegura el funcionamiento diario de la heladera de la escuela hogar para almacenar vacunas y comida fresca.

🌱 AMBIENTE:
Elimina las emisiones de CO₂ y la contaminación acústica del motor diésel.

💰 ECONOMÍA:
Reduce drásticamente los costos operativos al eliminar la dependencia del gasoil transportado.
```

---

## SLIDE 9: DESAFÍO DE CAMPO (EFECTO VENTURI EN LA ESCUELA)

### Elementos visuales a crear
- Fondo: #D9E8F5
- Plano ilustrado en perspectiva isométrica de un colegio secundario
- Dos zonas marcadas con banderas interactivas:
  - Bandera 1: Patio abierto en el centro
  - Bandera 2: Pasillo estrecho entre paredes del gimnasio

### Textos para copiar

**TÍTULO:**
```
Desafío de Campo
```

**SUBTÍTULO:**
```
Efecto Venturi en tu propia escuela: el viento que se acelera solo
```

**INSTRUCCIÓN:**
```
Efectúá el experimento en tu predio escolar con un anemómetro casero de tapitas plásticas
```

### Implementación de banderas interactivas

**BANDERA 1 - "Patio Abierto" (🚩):**
- Posicionar sobre el área central del patio
- Acción → "Etiqueta flotante"
- Contenido:
```
PUNTO A - EL PATIO ABIERTO

El viento fluye libremente sin obstáculos.

Registra la velocidad promedio aquí con tu anemómetro de tapitas plásticas casero. Esta velocidad representará la corriente eólica de base en tu localidad.

Ejemplo de medición: 4 m/s (14.4 km/h)
```

**BANDERA 2 - "Pasillo Estrecho" (🚩):**
- Posicionar sobre el pasillo entre paredes
- Acción → "Ventana emergente"
- Título: "PUNTO B - El Estrechamiento (Efecto Venturi)"
- Contenido:
```
CUANDO LA MASA DE AIRE CHOCA CONTRA EL EDIFICIO:

La corriente de viento se ve obligada a pasar por el pasillo estrecho formado entre las paredes. Al reducirse el espacio físico de tránsito:

• El aire disminuye su presión
• El aire aumenta drásticamente su velocidad
• Se conserva el flujo constante (ecuación de continuidad)

DESAFÍO MATEMÁTICO:

Si la velocidad medida en el patio es de 4 m/s y en el pasillo es de 8 m/s (se duplicó por el estrechamiento):

Potencia relativa = (8 / 4)³ = 2³ = 8

¡La energía eólica en el pasillo es 8 VECES MAYOR gracias a la micro-arquitectura escolar!

Esto demuestra por qué los aerogeneradores reales nunca se instalan al azar en la provincia. La ubicación estratégica es clave para maximizar la generación.
```

---

## SLIDE 10: TRIVIA EÓLICA INTERACTIVA (GAMIFICACIÓN)

### Estructura de páginas en Genially

Esta slide requiere crear 4 páginas en total:
1. **Página principal** (Slide 10): La pregunta
2. **Página de Error A**: Respuesta incorrecta A
3. **Página de Acierto B**: Respuesta correcta
4. **Página de Error C**: Respuesta incorrecta C

### PÁGINA PRINCIPAL - La Pregunta

**TÍTULO:**
```
🎮 Trivia Eólica - Pone a Prueba tu Mente
```

**PREGUNTA CENTRAL:**
```
Llega un folleto comercial a la dirección de tu escuela de la Línea Sur de Río Negro. El fabricante asegura que su nuevo aerogenerador de diseño aerodinámico de 2 kW nominales entregará de forma ininterrumpida esa potencia las 24 horas del día gracias a un rendimiento de palas del 75%.

¿Qué decisión técnica debe tomar la escuela?
```

**BOTÓN OPCIÓN A:**
- Texto: "Comprarlo de inmediato, porque al tener un rendimiento del 75% el equipo generará suficiente electricidad para el invierno sin depender de la batería"
- Acción → "Ir a página" → Página de Error A

**BOTÓN OPCIÓN B:**
- Texto: "Rechazar la propuesta del fabricante, ya que la potencia nominal de catálogo es de laboratorio y en la estepa el Factor de Capacidad promedia el 35%, sumado a que el Límite de Betz restringe la eficiencia de las palas a un máximo teórico del 59.3%"
- Acción → "Ir a página" → Página de Acierto B

**BOTÓN OPCIÓN C:**
- Texto: "Aceptar la compra pero retirar el banco de baterías del proyecto, ya que el viento de corte extrema de las tormentas patagónicas mantendrá girando el alternador a velocidad nominal continua"
- Acción → "Ir a página" → Página de Error C

---

### PÁGINA DE ERROR A

**TÍTULO:**
```
¡Inténtalo de nuevo! ❌
```

**CONTENIDO:**
```
Estás cayendo en el pensamiento lineal de catálogo.

ERRORES DETECTADOS:

1. Generación ininterrumpida: El sol no brilla de noche y el viento fluctúa constantemente. Es imposible generar de manera ininterrumpida sin un banco de baterías que almacene la energía.

2. Rendimiento del 75%: Es físicamente imposible. La Ley de Betz establece que ninguna máquina puede capturar más del 59.3% de la energía del viento. Un fabricante que promete un 75% de rendimiento está violando las leyes de la termodinámica.

3. Factor de Capacidad: En la estepa rionegrina, el Factor de Capacidad promedia el 35%, lo que significa que la potencia real promedio es apenas un tercio de la potencia nominal de catálogo.

CONCLUSIÓN: Esta decisión dejaría a la escuela sin luz cuando el viento no sople y con un equipo que nunca entregará lo prometido.
```

**BOTÓN:**
- Texto: 🔄 Volver a intentar
- Acción → "Ir a página" → Página principal (Slide 10)

---

### PÁGINA DE ACIERTO B

**TÍTULO:**
```
¡EXCELENTE TRABAJO TÉCNICO! 🏆
```

**CONTENIDO:**
```
Has aplicado el rigor científico con maestría.

LO QUE COMPRENDISTE:

✅ La potencia de folleto de un generador comercial NO equivale a su generación real continua debido a la variabilidad del viento y el Factor de Capacidad local.

✅ Albert Betz demostró en 1919 que ninguna máquina del universo puede capturar más del 59.3% del viento, haciendo que una promesa de venta del 75% sea un fraude técnico.

✅ En la estepa patagónica, el Factor de Capacidad promedia el 35%, lo que significa que un generador de 2 kW nominales producirá en promedio apenas 0.7 kW de potencia real continua.

ESTADO: ¡Estás listo para graduarte como un ciudadano y técnico crítico en la transición energética de Río Negro!

SIGUIENTE PASO: Volvé al menú para seguir explorando las demás dimensiones de la energía eólica en la Línea Sur.
```

**BOTÓN:**
- Texto: 🏠 Ir al Menú Principal
- Acción → "Ir a página" → Slide 2 (Mapa de Ruta)

---

### PÁGINA DE ERROR C

**TÍTULO:**
```
¡Fallo Estructural! ❌
```

**CONTENIDO:**
```
Recordá la paradoja de las tormentas de la estepa.

EL ERROR CRÍTICO:

Cuando el viento supera la velocidad de corte de 25 m/s (90 km/h), el sistema frena por completo el aerogenerador y pone las palas en bandera para evitar la rotura de la torre por fatiga de materiales.

¿POR QUÉ ES PELIGROSO RETIRAR LAS BATERÍAS?

• Durante un gran temporal, la generación es CERO
• Sin baterías, la escuela queda sin luz durante toda la tormenta
• Las tormentas patagónicas pueden durar varios días
• Las escuelas hogar necesitan energía continua para:
  - Heladera (vacunas y alimentos)
  - Internet satelital (conexión con familias)
  - Iluminación para las aulas
  - Equipamiento médico básico

CONCLUSIÓN: Las baterías no son un accesorio opcional; son el corazón del sistema Off-Grid. Sin ellas, la energía eólica no puede cumplir su función social en la ruralidad.
```

**BOTÓN:**
- Texto: 🔄 Volver a intentar
- Acción → "Ir a página" → Página principal (Slide 10)

---

## INSTRUCCIONES GENERALES PARA GENIALLY

### Creación de la presentación
1. Ir a genially.com → Crear → Presentación → Blanco
2. Definir tamaño: 1920 × 1080 px (16:9)
3. Aplicar fondo #D9E8F5 en todas las slides

### Configuración de navegación
1. En Slide 2 (Mapa de Ruta), configurar cada marcador con acción "Ir a página"
2. En cada slide temática, agregar botón "🏠 Volver al Menú" con acción "Ir a página" → Slide 2
3. Para la trivia, crear 4 páginas (principal + 3 resultados) y configurar branching

### Animaciones recomendadas
| Elemento | Animación Genially |
|----------|-------------------|
| Títulos | Fade In (entrada suave) |
| Iconos interactivos | Pulse (pulso continuo) |
| Marcadores del mapa | Appear (aparición) |
| Componentes del circuito | Slide (deslizamiento) |

### Exportación
- Compartir → Enlace público para alumnos
- O Incorporar → Código iframe para LMS (Moodle, Google Classroom)

---

## RESUMEN DE ELEMENTOS INTERACTIVOS POR SLIDE

| Slide | Etiquetas | Popups | Branching | Otros |
|-------|-----------|--------|-----------|-------|
| 1 | 1 (Pregunta) | 0 | 1 botón | Animación viento |
| 2 | 0 | 0 | 8 botones | Marcadores con pulso |
| 3 | 0 | 3 (ρ, A, v³) | 1 (volver) | Ecuación interactiva |
| 4 | 2 (tradicional/moderno) | 2 (arrastre/sustentación) | 1 (volver) | Layout dividido |
| 5 | 0 | 2 (Betz) | 1 (volver) | Foto + esquema |
| 6 | 2 (tramos 1 y 2) | 1 (tramo 3) | 1 (volver) | Gráfico de curva |
| 7 | 1 (alternador) | 3 (regulador, baterías, inversor) | 1 (volver) | Circuito animado |
| 8 | 0 | 0 | 1 (volver) | Switch Antes/Ahora |
| 9 | 1 (patio) | 1 (pasillo Venturi) | 1 (volver) | Plano isométrico |
| 10 | 0 | 0 | 3 (ac/error) + 4 (volver) | Trivia ramificada |
| **TOTAL** | **7** | **13** | **16** | |
