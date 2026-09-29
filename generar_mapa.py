# -*- coding: utf-8 -*-
"""generar_mapa.py — Mapa SVG de Río Negro con las sedes de la ESRN Rural.

Contorno provincial simplificado a partir de RIONEGRO.json (alvarezgarcia/
provincias-argentinas-geojson, datos IGN). Proyección equirectangular simple
con estiramiento N/S, para que las coordenadas de las sedes caigan sobre el
territorio real.
"""

import math
import sys


# Polígono simplificado de la Provincia de Río Negro (epsg:4326).
# Fuente: https://github.com/alvarezgarcia/provincias-argentinas-geojson
POLIGONO_RN = [
(-68.25805664062, -37.55328764596), (-67.78564453125, -37.64033489806), (-67.68676757812, -37.83148014503),
    (-67.74169921875, -37.90953361677), (-67.86254882812, -37.90086509257), (-67.87353515625, -37.96152331397),
    (-67.80761718750, -38.08268954484), (-67.69775390625, -38.03943889182), (-67.63183593750, -38.19502155796),
    (-67.35717773438, -38.28131307923), (-67.18139648438, -38.19502155796), (-67.04956054688, -38.37611542404),
    (-66.86279296875, -38.47079371120), (-66.57714843750, -38.52238409020), (-66.65405273438, -38.67693344464),
    (-66.42333984375, -38.76265033833), (-66.24755859375, -38.77121637244), (-66.15966796875, -38.72837591824),
    (-66.07177734375, -38.69408504757), (-65.96191406250, -38.71123253895), (-65.87402343750, -38.77978137805),
    (-65.79711914062, -38.82259097618), (-65.69824218750, -38.84826438870), (-65.62133789062, -38.82259097618),
    (-65.54443359375, -38.76265033833), (-65.36865234375, -38.83114980935), (-65.26977539062, -38.86537485161),
    (-65.18188476562, -38.82259097618), (-65.15991210938, -38.74551518488), (-64.89624023438, -38.84826438870),
    (-64.70947265625, -38.82259097618), (-64.54467773438, -38.83114980935), (-64.35791015625, -38.87392853924),
    (-64.21508789062, -38.94232097948), (-63.96240234375, -39.04478604850), (-63.85253906250, -39.09596293631),
    (-63.74267578125, -39.10448880944), (-63.73168945313, -39.18117526159), (-63.64379882812, -39.19820534889),
    (-63.54492187500, -39.24076251001), (-63.45703125000, -39.30029918615), (-63.39111328125, -39.31730037327),
    (-63.36914062500, -40.72228267283), (-63.23730468750, -40.70562793821), (-63.07250976562, -40.73893324114),
    (-62.89672851562, -40.87198775670), (-62.77587890625, -40.98819156349), (-62.94616699219, -41.08763212468),
    (-63.05053710937, -41.13729606112), (-63.18237304688, -41.16211393940), (-63.36364746094, -41.15384235711),
    (-63.56689453125, -41.14970617454), (-63.74267578125, -41.15384235711), (-63.84704589844, -41.14143302654),
    (-63.90747070312, -41.12488359929), (-63.96240234375, -41.06278606873), (-64.06127929688, -41.03378713522),
    (-64.07775878906, -40.98819156349), (-64.11071777344, -40.97160353280), (-64.14367675781, -41.01721057823),
    (-64.27551269531, -40.97575093158), (-64.42382812500, -40.91351257613), (-64.54467773438, -40.85952522899),
    (-64.67651367188, -40.82212357517), (-64.75891113281, -40.80965166749), (-64.85778808594, -40.83043687765),
    (-64.89074707031, -40.80133575979), (-64.76989746094, -40.77638178483), (-64.80285644531, -40.73477098967),
    (-64.87426757812, -40.71811937975), (-64.92370605469, -40.72644570551), (-64.90173339844, -40.76806170937),
    (-64.97863769531, -40.75557964276), (-65.07751464844, -40.78470081842), (-65.12695312500, -40.85952522899),
    (-65.14892578125, -40.93426521178), (-65.15441894531, -40.99648401438), (-65.15991210938, -41.12902134750),
    (-65.14343261719, -41.19932314128), (-65.10498046875, -41.26954950284), (-65.06652832031, -41.37268648186),
    (-65.03906250000, -41.44272637767), (-65.00610351562, -41.48800607185), (-64.97863769531, -41.56614196477),
    (-65.02258300781, -41.61133539944), (-65.02807617188, -41.67701482203), (-65.02807617188, -41.72213058513),
    (-65.01708984375, -41.76721469421), (-65.00610351562, -41.81226714360), (-65.05004882812, -41.81226714360),
    (-65.03356933594, -41.85319643777), (-65.05554199219, -41.92271616674), (-65.05554199219, -41.98807738309),
    (-71.77917480469, -41.97991089691), (-71.78466796875, -41.89001042402), (-71.79565429688, -41.84501267271),
    (-71.75170898438, -41.81636125072), (-71.75170898438, -41.75901993816), (-71.80114746094, -41.73033005047),
    (-71.80664062500, -41.68522004222), (-71.83410644531, -41.66470503009), (-71.87255859375, -41.61544232468),
    (-71.82861328125, -41.55792157780), (-71.83959960937, -41.49212083969), (-71.83959960937, -41.43860847396),
    (-71.88903808594, -41.36444153054), (-71.88354492188, -41.29431726315), (-71.91101074219, -41.25716209783),
    (-71.85607910156, -41.21172151055), (-71.90002441406, -41.16211393940), (-71.83959960937, -41.12074559017),
    (-71.83410644531, -41.07106913081), (-71.85607910156, -41.03378713522), (-71.87255859375, -41.00477542223),
    (-71.72149658203, -41.02135510867), (-71.60339355469, -41.03585891144), (-71.55395507812, -41.02135510867),
    (-71.49078369141, -41.03378713522), (-71.42761230469, -41.04414536431), (-71.35620117187, -41.09384217130),
    (-71.25732421875, -41.10005163093), (-71.15570068359, -41.06278606873), (-71.14471435547, -41.03171529379),
    (-71.08703613281, -41.00684811121), (-71.08978271484, -40.98611828780), (-71.05407714844, -40.97367726478),
    (-71.02661132812, -40.95293701190), (-71.04858398438, -40.88652440806), (-71.06231689453, -40.84498264925),
    (-71.09527587891, -40.83667117059), (-71.08703613281, -40.81380923057), (-71.11175537109, -40.78678041402),
    (-71.11999511719, -40.76390128095), (-71.09527587891, -40.72644570551), (-71.02661132812, -40.72852712421),
    (-70.99365234375, -40.67647212850), (-70.97442626953, -40.64938745452), (-70.92498779297, -40.62854560637),
    (-70.88653564453, -40.62020704521), (-70.86181640625, -40.59518511582), (-70.80413818359, -40.58684239088),
    (-70.75469970703, -40.57432635193), (-70.67504882812, -40.59101388346), (-70.63934326172, -40.58475654701),
    (-70.61187744141, -40.55137419872), (-70.54595947266, -40.50962284960), (-70.51025390625, -40.49709237270),
    (-70.41961669922, -40.52841417576), (-70.28778076172, -40.49709237270), (-70.22186279297, -40.51171103483),
    (-70.16693115234, -40.48038142908), (-70.18341064453, -40.43022363451), (-70.09277343750, -40.37165889151),
    (-70.08178710938, -40.22921818870), (-69.94995117188, -40.15368685779), (-69.99389648438, -40.05284760182),
    (-70.00488281250, -39.98553841481), (-69.86206054688, -39.90130858575), (-69.65332031250, -39.85072092502),
    (-69.44458007812, -39.79165483525), (-69.34570312500, -39.72408857733), (-69.20288085938, -39.58875727697),
    (-69.00512695312, -39.49556336059), (-68.82934570312, -39.37677199662), (-68.73046875000, -39.26628442213),
    (-68.60961914062, -39.18969082110), (-68.47778320312, -39.06184913429), (-68.30200195312, -39.00211029923),
    (-68.20312500000, -38.98503278696), (-68.07128906250, -38.98503278696), (-67.99987792969, -38.97649248554),
    (-68.17016601562, -38.72837591824), (-68.26904296875, -38.66835610152), (-68.25805664062, -37.55328764596)]

# Las sedes de la ESRN Rural Virtual. Nombre tal como figura en la
# presentación; coordenadas de esrn-rural-mapa/js/anexos.js.
SEDES = [
    ("Valle Verde", -37.6139, -68.0306),
    ("Peñas Blancas", -37.6931, -67.8700),
    ("Lago Pellegrini", -38.6750, -68.0120),
    ("Chelforó", -39.0873, -66.5221),
    ("Cerro Policía", -39.7333, -68.5167),
    ("Aguada Guzmán", -39.9833, -68.8667),
    ("Naupa Huen", -39.8280, -69.5090),
    ("Blancura Centro", -40.3657, -69.7785),
    ("Mencué", -40.4228, -69.6142),
    ("Corralito", -40.7245, -70.7100),
    ("Villa Llanquín", -40.8956, -71.0367),
    ("Laguna Blanca", -40.7333, -69.8500),
    ("Colan Conhué", -40.6670, -69.1060),
    ("Rincón Treneta", -40.9525, -67.0522),
    ("Aguada Cecilio", -40.8483, -65.8392),
    ("Sierra Pailemán", -41.1500, -65.9500),
    ("El Cóndor", -41.0430, -62.8280),
    ("El Manso", -41.5700, -71.7600),
    ("Río Chico", -41.7167, -70.5000),
    ("Mamuel Choique", -41.7711, -70.1369),
    ("El Caín", -41.6333, -68.3167),
    ("Aguada de Guerra", -41.0664, -68.3831),
    ("Comicó", -41.0708, -67.4778),
    ("Yaminué", -40.9764, -67.1922),
    ("Arroyo los Berros", -41.4363, -66.0976),
    ("Cona Niyeu", -41.8657, -66.9380),
]

# El mapa se dibuja en píxeles de viewBox (≈ píxeles de pantalla): así las
# etiquetas y los puntos mantienen un tamaño legible sea cual sea el ancho.
LON_W, LON_E = -72.06, -62.55
LAT_N, LAT_S = -37.45, -42.10
ESTIRADO = 1.30        # estiramiento N/S (aprox. 1/cos(mid lat)) en píxeles
MAP_W_PX = 900.0       # ancho del territorio en el viewBox
PPL = MAP_W_PX / (LON_E - LON_W)
FS = 13.0             # tamaño de las etiquetas, en px de viewBox
RADIO = 7.5           # radio de los puntos, en px de viewBox

VERDE_PROV = "#e6f2e4"
LINEA_PROV = "#9dc4a8"
VERDE_PUNTO = "#1f9a5c"
TINTA_ETIQUETA = "#2c4635"
MAR = "#7fa8c6"

MARGEN_IZQ = 185.0
MARGEN_DER = 55.0
MARGEN_TOP = 70.0
MARGEN_BOT = 60.0


def _proy(lng, lat):
    x = (lng - LON_W) * PPL + MARGEN_IZQ
    y = (LAT_N - lat) * PPL * ESTIRADO + MARGEN_TOP
    return x, y


def _bbox_label(texto, x, y, ancla):
    """Caja aproximada de una etiqueta para evitar solapamientos."""
    ancho = len(texto) * FS * 0.62
    alto = FS * 1.35
    if ancla == "start":
        return (x, y - alto, ancho, alto)
    if ancla == "end":
        return (x - ancho, y - alto, ancho, alto)
    return (x - ancho / 2, y - alto, ancho, alto)


def _choca(a, b):
    return (a[0] < b[0] + b[2] and a[0] + a[2] > b[0] and
            a[1] < b[1] + b[3] and a[1] + a[3] > b[1])


def _dentro(x, y, poly):
    c = False
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[(i + 1) % len(poly)]
        if ((yi > y) != (yj > y)) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
    return c


def _nudge(p_poli, pts):
    """Desvía puntos que quedaron fuera del contorno (por el redondeo de las
    coordenadas) hacia el interior, empujándolos a través de la arista más
    cercana. Ajuste cosmético de pocos kilómetros: si quedó lejos del borde se
    deja como está, para no inventar geografía."""
    INS = 6.0    # px ~ 4-6 km de margen interior
    TOPE = 14.0  # si hace falta mover más que esto, no tocar
    mensajes = []
    nuevos = []
    for (x, y) in pts:
        if _dentro(x, y, p_poli):
            nuevos.append((x, y))
            continue
        # arista proyectada más cercana
        dmin, mejor = 1e18, None
        for i in range(len(p_poli)):
            ax, ay = p_poli[i]
            bx, by = p_poli[(i + 1) % len(p_poli)]
            dx, dy = bx - ax, by - ay
            L2 = dx * dx + dy * dy
            t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L2))
            px, py = ax + t * dx, ay + t * dy
            d = math.hypot(x - px, y - py)
            if d < dmin:
                dmin, mejor = d, (px, py)
        if mejor is None or dmin > TOPE:
            nuevos.append((x, y))
            if mejor and dmin > TOPE:
                mensajes.append("sede muy lejos del borde: revisar (%d km)" % round(dmin / PPL * 110))
            continue
        # cruzar la arista desde el punto hacia adentro
        cx, cy = mejor
        pas = math.hypot(x - cx, y - cy)
        if pas < 1e-9:
            nuevos.append((x, y))
            continue
        ux, uy = (x - cx) / pas, (y - cy) / pas
        nxp, nyp = x - ux * (dmin + INS), y - uy * (dmin + INS)
        nuevos.append((nxp, nyp))
    for m in mensajes:
        print("AVISO mapa:", m, file=sys.stderr)
    return nuevos


def mapa_sedes_svg():
    """Devuelve el SVG del mapa con las sedes (puntos verdes + etiquetas)."""
    p_poli = [_proy(lng, lat) for lng, lat in POLIGONO_RN]
    path = "M" + "L".join("%.1f,%.1f" % p for p in p_poli) + "Z"

    proy_pts = _nudge(p_poli, [_proy(lng, lat) for _, lat, lng in SEDES])
    mar_x = (LON_E - 0.30 - LON_W) * PPL + MARGEN_IZQ
    W = max(max(x for x, _ in proy_pts), mar_x + 90.0) + MARGEN_DER
    H = max(max(y for _, y in proy_pts), max(y for _, y in p_poli)) + MARGEN_BOT

    # Ubicación de etiquetas: para cada una se prueban posiciones en anillos
    # alrededor del punto y se elige la que menos choca; luego se refina por
    # pasadas hasta no dejar etiquetas pisadas. Una línea guía une cada punto
    # con su etiqueta.
    radios = [13.0, 27.0, 42.0, 58.0]
    candidatos = []
    for r in radios:
        for a in range(24):
            ang = math.radians(a / 24 * 360)
            dx = r * math.cos(ang)
            dy = r * math.sin(ang)
            ancla = "middle" if abs(dx) < 5 else ("start" if dx > 0 else "end")
            candidatos.append((dx, dy, ancla))

    def caja_para(i, dx, dy, ancla):
        tx = proy_pts[i][0] + dx
        ty = proy_pts[i][1] + dy
        return _bbox_label(SEDES[i][0], tx, ty, ancla), tx, ty

    def fuera(c, tx):
        return (tx < MARGEN_IZQ - 4 or tx + c[2] > W - 8 or
                c[1] < MARGEN_TOP - 4 or c[1] + c[3] > H - 6)

    def n_colisiones(c, boxes):
        return sum(1 for b in boxes if b and _choca(c, b))

    boxes = [None] * len(SEDES)
    posis = [None] * len(SEDES)
    orden = sorted(range(len(SEDES)), key=lambda i: -len(SEDES[i][0]))
    for i in orden:
        opciones = []
        for dx, dy, ancla in candidatos:
            c, tx, ty = caja_para(i, dx, dy, ancla)
            if fuera(c, tx):
                continue
            opciones.append((n_colisiones(c, boxes), abs(dx) + abs(dy), c, tx, ty, ancla))
        opciones.sort(key=lambda o: (o[0], o[1]))
        _, _, c, tx, ty, ancla = opciones[0]
        boxes[i] = c
        posis[i] = (tx, ty, ancla)

    for _rnd in range(20):
        peores = set()
        for i in range(len(SEDES)):
            for j in range(i + 1, len(SEDES)):
                if boxes[i] and boxes[j] and _choca(boxes[i], boxes[j]):
                    peores.add(i)
                    peores.add(j)
        if not peores:
            break
        for i in sorted(peores, key=lambda p: -len(SEDES[p][0])):
            opciones = []
            for dx, dy, ancla in candidatos:
                c, tx, ty = caja_para(i, dx, dy, ancla)
                if fuera(c, tx):
                    continue
                opciones.append((n_colisiones(c, boxes), abs(dx) + abs(dy), c, tx, ty, ancla))
            opciones.sort(key=lambda o: (o[0], o[1]))
            nc, _, c, tx, ty, ancla = opciones[0]
            if nc < n_colisiones(boxes[i], boxes):
                boxes[i] = c
                posis[i] = (tx, ty, ancla)

    dot_svg = []
    led = []
    for i, (nombre, lat, lng) in enumerate(SEDES):
        px, py = proy_pts[i]
        tx, ty, ancla = posis[i]
        led.append('<line class="mapa__leader" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                   % (px, py, tx, ty))
        dot_svg.append('<circle class="mapa__punto" cx="%.1f" cy="%.1f" r="%s">'
                       '<title>%s</title></circle>' % (px, py, RADIO, nombre))
        dot_svg.append('<text class="mapa__etiqueta" x="%.1f" y="%.1f" '
                       'text-anchor="%s">%s</text>' % (tx, ty, ancla, nombre))

    mar_svg = ('<text class="mapa__mar" x="%.1f" y="%.1f" '
               'text-anchor="middle" transform="rotate(-90 %.1f %.1f)">'
               'Mar Argentino</text>' % (mar_x, H * 0.5, mar_x, H * 0.5))

    return ('<svg class="mapa" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="Mapa de la Provincia de Río Negro con las %d sedes de '
            'la ESRN Rural Virtual" viewBox="0 0 %.1f %.1f">\n'
            '<path class="mapa__provincia" d="%s"/>\n'
            '%s\n%s\n%s\n'
            '<g class="mapa__rosa" transform="translate(%.1f %.1f)">'
            '<circle r="10" class="mapa__rosa_c"/><path class="mapa__rosa_n" '
            'd="M0 -9 L3.4 6 L0 3 L-3.4 6 Z"/><text class="mapa__rosa_t" '
            'x="13" y="5">N</text></g>\n'
            '</svg>'
            % (len(SEDES), W, H, path, "\n".join(led), "\n".join(dot_svg),
               mar_svg, W - 55, MARGEN_TOP + 18))


if __name__ == "__main__":
    import sys, io
    sys.stdout.reconfigure(encoding="utf-8")
    out = mapa_sedes_svg()
    ruta = sys.argv[1] if len(sys.argv) > 1 else "ediciones/01/mapa_sedes.svg"
    io.open(ruta, "w", encoding="utf-8").write(out)
    print("mapa escrito:", ruta, "(", len(out), "bytes )")