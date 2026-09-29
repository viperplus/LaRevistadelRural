# -*- coding: utf-8 -*-
"""generador/templates.py — Plantillas canonicas de "Rural".

Contrato de claves  (todo lo que puede poner {clave} en estas plantillas
sera provisto por construir_revista.py; el generador NUNCA pone llaves
libres). El texto visual/editorial vive en datos/ediciones.json + textos
y fotos verbatim en enviar_aqui/imagenes_odt/<slug>/ (punto 3/26/48).

Un solo juego de nombres — sin alias ni sinónimos:
   TEMPLATE_INDEX     portada + sumario
   TEMPLATE_SECCION   página patron de una sección (título + rejilla)
   TEMPLATE_ART       página patron de un artículo (cuerpo editorial)
"""

# ---------------------------------------------------------------------------
# PÁGINA PATRÓN — ARTÍCULO  (puntos 4/5/7/11/16 · foto manda, epígrafe,
# autoría y navegación editorial)
# ---------------------------------------------------------------------------
TEMPLATE_ART = """<!doctype html>
<html lang="es" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITULO} · {REVISTA}</title>
<meta name="description" content="{BAJADA}">
<meta name="generator" content="Rural · {EDICION}">
<link rel="icon" href="../../favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,600;0,700;0,800;1,400&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../css/editorial.css">
<link rel="stylesheet" href="../../css/componentes-2.css">
</head>
<body>
<a class="salto" href="#contenido">Saltar al contenido</a>
<header class="masthead contenedor" role="banner">
  <p class="masthead__marca"><a href="../../index.html">{REVISTA}</a></p>
  <nav aria-label="Secciones" class="nav-ed">
    {NAV}
  </nav>
</header>
<main id="contenido" class="contenedor">
  <article class="articulo grid-12" itemscope itemtype="https://schema.org/Article">
    <header class="cabeza grid-12" style="grid-column:3/span 8">
      <p class="cabeza__superior">{SEC_ETIQUETA}</p>
      <h1 itemprop="headline">{TITULO}</h1>
      <p class="cabeza__bajada">{BAJADA}</p>
      <p class="cabeza__meta">
        <span itemprop="author">{AUTOR}</span> · <time datetime="{FECHA_ISO}">{FECHA}</time>
        · <a href="{SEC_URL}">{SEC_TITULO_NAV}</a>
      </p>
    </header>
    <div class="articulo__cuerpo" itemprop="articleBody">
      {CUERPO}
    </div>
    <footer class="articulo__fin">
      <a class="volver" href="{SEC_URL}">← Volver a {SEC_TITULO_NAV}</a>
    </footer>
  </article>
</main>
<footer class="pie" role="contentinfo">
  <div class="pie__interior contenedor">
    <p class="pie__credito">{REVISTA} · {SUBNOMBRE} · {EDICION}.
      Escrita, ilustrada y fotografiada por estudiantes de la ESRN
      Rural Virtual.</p>
  </div>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# PÁGINA PATRÓN — SECCIÓN  (retícula compartida, acento por sección)
# ---------------------------------------------------------------------------
TEMPLATE_SECCION = """<!doctype html>
<html lang="es" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{SEC_TITULO} · {REVISTA}</title>
<meta name="description" content="{SEC_DESCRIP}">
<meta name="generator" content="Rural · {EDICION}">
<link rel="icon" href="../../favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,600;0,700;0,800;1,400&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../css/editorial.css">
<link rel="stylesheet" href="../../css/componentes-2.css">
</head>
<body>
<a class="salto" href="#contenido">Saltar al contenido</a>
<header class="masthead contenedor" role="banner">
  <p class="masthead__marca"><a href="../../index.html">{REVISTA}</a></p>
  <nav aria-label="Secciones" class="nav-ed">
    {NAV}
  </nav>
</header>
<main id="contenido" class="contenedor">
  <header class="sec-portada">
    <p class="sec-portada__num">{SEC_NUM} / {SEC_TOTAL}</p>
    <h1>{SEC_TITULO}</h1>
    <p class="sec-portada__descrip">{SEC_DESCRIP}</p>
  </header>
  <div class="sec-listado grid-12" aria-label="{SEC_TITULO}">
    {LISTA_ARTICULOS}
  </div>
</main>
<footer class="pie" role="contentinfo">
  <div class="pie__interior contenedor">
    <p class="pie__credito">{REVISTA} · {SUBNOMBRE} · {EDICION}.
      Escrita, ilustrada y fotografiada por estudiantes de la ESRN
      Rural Virtual.</p>
  </div>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# PÁGINA PATRÓN — PORTADA + SUMARIO  (punto 5 · índice editorial)
# ---------------------------------------------------------------------------
TEMPLATE_INDEX = """<!doctype html>
<html lang="es" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{REVISTA} · {EDICION}</title>
<meta name="description" content="{SUBNOMBRE}. {EDICION} — periodismo,
  ciencia y territorios de la ESRN Rural Virtual, escrito por estudiantes.">
<meta name="generator" content="Rural · {EDICION}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,600;0,700;0,800;1,400&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/editorial.css">
<link rel="stylesheet" href="css/componentes-2.css">
</head>
<body>
<a class="salto" href="#contenido">Saltar al contenido</a>
<header class="masthead contenedor" role="banner">
  <p class="masthead__marca">{REVISTA}</p>
  <nav aria-label="Secciones" class="nav-ed">
    {NAV_INDEX}
  </nav>
</header>
<main id="contenido" class="contenedor">
  <section class="portada" aria-labelledby="portada-titulo">
    <p class="portada__sec">{EDICION} · {ED_NUM}</p>
    <h1 id="portada-titulo" class="portada__h1">{REVISTA}</h1>
    <p class="portada__bajada">{SUBNOMBRE}</p>
    {PORTADA_IMAGEN}
  </section>

  <nav class="sumario" aria-label="Sumario">
    <p class="sumario__cabecera">Sumario · {EDICION}</p>
    <ul class="sumario__lista">
      {SUMARIO}
    </ul>
  </nav>

  <section class="secciones" aria-label="Secciones">
    <h2 class="secciones__titulo">Secciones</h2>
    <div class="grid-12">
      {INDEX_SEC}
    </div>
  </section>
</main>
<footer class="pie" role="contentinfo">
  <div class="pie__interior contenedor">
    <p class="pie__credito">{REVISTA} · {SUBNOMBRE} · {EDICION}.
      Escrita, ilustrada y fotografiada por estudiantes de la ESRN
      Rural Virtual.</p>
  </div>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# ITEMS REUTILIZABLES (bloques de un solo uso dentro de una plantilla)
# ---------------------------------------------------------------------------
# Ítem del sumario — NUNCA una página completa.
TEMPLATE_SUMARIO_ITEM = """<li class="sumario__item">
  <span class="sumario__num">{num}</span>
  <span class="sumario__sec">{sec_tag}</span>
  <a class="sumario__art" href="{url}">{titulo}</a>
</li>"""

# Tarjeta de sección en la portada.
TEMPLATE_SEC_ITEM = """<article class="sec_card grid-12">
  <h3 class="sec_card__titulo"><a href="{URL}">{SEC_TITULO}</a></h3>
  <p class="sec_card__bajada">{SEC_BAJADA}</p>
</article>"""
