# Revista Rural — ESRN Rural Virtual

Revista digital de la **ESRN Rural Virtual**: escrita, ilustrada y fotografiada por estudiantes de las sedes de toda la provincia de Río Negro. Ciencia, territorio, cultura y comunidad desde cada paraje.

## Ver la revista

Abrí [`ediciones/01/index.html`](ediciones/01/index.html) en cualquier navegador. Todo es estático: HTML + CSS + imágenes, sin dependencias ni servidor.

La página que sirve de entrada al número es `ediciones/01/index.html`; también hay una página con **todos los artículos** (`articulos.html`), la **presentación** (`presentacion.html`) y el apartado de **egresados** (`egresados.html`).

## Reconstruir la revista

El sitio se genera desde los datos de `datos/ediciones.json`:

```sh
python construir_revista_v2.py
```

El generador vuelca todo en `ediciones/01/` (HTML de portada, secciones, artículos, presentación y egresados).

El mapa de sedes se genera por separado:

```sh
python generar_mapa.py
```

## Estructura

| Carpeta | Contenido |
| --- | --- |
| `ediciones/01/` | La revista generada (una carpeta por artículo, secciones, portada, CSS e imágenes) |
| `css/` | Hojas de estilo fuente del diseño editorial |
| `datos/` | `ediciones.json`: textos y metadatos de los artículos |
| `extras/` | Utilidades de mantenimiento de los datos |
| `images/` | Imágenes de sección |

## Datos personales

Las coordinadoras y coordinadores de la revista resguardan la privacidad de las y los estudiantes. Los trabajos originales (carpeta `odt/`) no se suben a este repositorio.

---

*Revista creada por estudiantes de la ESRN Rural Virtual.*