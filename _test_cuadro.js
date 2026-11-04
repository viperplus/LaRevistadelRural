/* Test: el cuadro debe verse como cuadro.
   Verifica capas en Z, que quede embebido en la pared y que
   NINGUNA pieza tape el rectángulo del video. */
const fs = require('fs');
const html = fs.readFileSync(__dirname + '/visita_virtual.html', 'utf8');

// --- valores reales del HTML ---
function grab(re, name) {
  const m = html.match(re);
  if (!m) throw new Error('no se pudo leer ' + name + ' de visita_virtual.html');
  return m;
}
const sc = grab(/cx:([\-\d.]+),\s*cy:([\-\d.]+),\s*cz:([\-\d.]+),\s*ry:([\-\d.]+),\s*w:([\-\d.]+),\s*h:([\-\d.]+)\,?/, 'SCREENS');
const s = { cx: +sc[1], cy: +sc[2], cz: +sc[3], ry: +sc[4], w: +sc[5], h: +sc[6] };
const FD = +grab(/var FD=([\d.]+),\s*FW=([\d.]+),\s*GAP=([\d.]+);/, 'FD')[1];
const FW = +grab(/var FD=([\d.]+),\s*FW=([\d.]+),\s*GAP=([\d.]+);/, 'FW')[2];
const GAP = +grab(/var FD=([\d.]+),\s*FW=([\d.]+),\s*GAP=([\d.]+);/, 'GAP')[3];
const LT = +grab(/var LT=([\d.]+),/, 'LT')[1];
const WALL_H = +grab(/WALL_H\s*=\s*([\d.]+)/, 'WALL_H')[1];
const T = +grab(/T=([\d.]+);/, 'T')[1];
const wm = grab(/wall\(-12,-30,12,-30\)/, 'muro sur'); // exists?

console.log('SCREENS =', JSON.stringify(s));
console.log(`FD=${FD} FW=${FW} GAP=${GAP} LT=${LT}  WALL_H=${WALL_H} T=${T}`);

const OW = s.w + GAP * 2 + FW * 2;   // ancho exterior del marco
const OH = s.h + GAP * 2 + FW * 2;   // alto exterior del marco

// --- muro sur (wall(-12,-30,12,-30)) ---
const wall = { minX: -12, maxX: 12, zC: -30, minZ: -30 - T / 2, maxZ: -30 + T / 2, h: WALL_H };
const wallFace = wall.maxZ;          // cara interna mirando al salón

let fail = 0;
const chk = (ok, desc, got) => {
  if (!ok) fail++;
  console.log(`${ok ? 'OK  ' : 'FALLO'}  ${desc}${got !== undefined ? '   [' + got + ']' : ''}`);
};

// ============ capas en Z (profundidad de mundo) ============
const zFrameBack = s.cz - FD, zFrameFront = s.cz;
const zMat = s.cz - 0.045;
const zVideo = s.cz - 0.035;
const zLipBack = s.cz - 0.045, zLipFront = s.cz - 0.005;
const zIcon = s.cz - 0.015;
const zPlq = s.cz + 0.03;

chk(zFrameBack <= wallFace,
  'respaldo del marco embebido en la pared',
  `marco atrás=${zFrameBack.toFixed(3)} cara muro=${wallFace.toFixed(3)}`);
chk(zFrameFront > wallFace,
  'marco sobresale de la pared (parece cuadro)',
  `marco frente=${zFrameFront.toFixed(3)} = ${(zFrameFront - wallFace).toFixed(2)}m`);
chk(zVideo > wallFace, 'video por delante de la pared', zVideo.toFixed(3));
chk(zMat < zVideo, 'paspartú DETRÁS del video', `mat=${zMat.toFixed(3)} < video=${zVideo.toFixed(3)}`);
chk(zLipFront > zVideo, 'filo dorado por delante del video', `filo=${zLipFront.toFixed(3)} > video=${zVideo.toFixed(3)}`);
chk(zIcon > zVideo, 'icono play por delante del video', zIcon.toFixed(3));
chk(zIcon < zFrameFront, 'icono play por detrás del frente del marco', zIcon.toFixed(3));
chk(zPlq > zFrameFront, 'placa por delante del marco', zPlq.toFixed(3));

// ============ XY: nada tapa el rectángulo del video ============
const vid = { x0: s.cx - s.w / 2, x1: s.cx + s.w / 2, y0: s.cy - s.h / 2, y1: s.cy + s.h / 2 };
const overlap = (a, b) => a.x0 < b.x1 && a.x1 > b.x0 && a.y0 < b.y1 && a.y1 > b.y0;

const bars = {
  'barra superior': { x0: s.cx - OW / 2, x1: s.cx + OW / 2, y0: s.cy + OH / 2 - FW, y1: s.cy + OH / 2 },
  'barra inferior': { x0: s.cx - OW / 2, x1: s.cx + OW / 2, y0: s.cy - OH / 2, y1: s.cy - OH / 2 + FW },
  'barra izquierda': { x0: s.cx - OW / 2, x1: s.cx - OW / 2 + FW, y0: s.cy - OH / 2, y1: s.cy + OH / 2 },
  'barra derecha': { x0: s.cx + OW / 2 - FW, x1: s.cx + OW / 2, y0: s.cy - OH / 2, y1: s.cy + OH / 2 }
};
for (const [n, r] of Object.entries(bars))
  chk(!overlap(r, vid), `${n} NO tapa el video`, overlap(r, vid) ? 'SÍ LO TAPA' : 'libre');

const lips = {
  'filo sup': { x0: s.cx - (s.w / 2 + LT), x1: s.cx + (s.w / 2 + LT), y0: s.cy + s.h / 2, y1: s.cy + s.h / 2 + LT },
  'filo inf': { x0: s.cx - (s.w / 2 + LT), x1: s.cx + (s.w / 2 + LT), y0: s.cy - s.h / 2 - LT, y1: s.cy - s.h / 2 },
  'filo izq': { x0: s.cx - s.w / 2 - LT, x1: s.cx - s.w / 2, y0: s.cy - s.h / 2, y1: s.cy + s.h / 2 },
  'filo der': { x0: s.cx + s.w / 2, x1: s.cx + s.w / 2 + LT, y0: s.cy - s.h / 2, y1: s.cy + s.h / 2 }
};
for (const [n, r] of Object.entries(lips))
  chk(!overlap(r, vid), `${n} NO tapa el video`, overlap(r, vid) ? 'SÍ LO TAPA' : 'libre');

// ============ el marco completo dentro del muro ============
const frame = { x0: s.cx - OW / 2, x1: s.cx + OW / 2, y0: s.cy - OH / 2, y1: s.cy + OH / 2 };
chk(frame.x0 >= wall.minX && frame.x1 <= wall.maxX, 'marco dentro del ancho del muro',
  `marco x ${frame.x0.toFixed(2)}..${frame.x1.toFixed(2)} / muro ${wall.minX}..${wall.maxX}`);
chk(frame.y0 >= 0 && frame.y1 <= WALL_H, 'marco dentro de la altura del muro/techo',
  `marco y ${frame.y0.toFixed(2)}..${frame.y1.toFixed(2)} / muro 0..${WALL_H}`);

// ============ placa ============
const plqH = 1.05 / 2.844;
const frameBot = s.cy - (s.h / 2 + GAP + FW);
const plq = { y0: frameBot - 0.05 - plqH, y1: frameBot - 0.05 };
chk(!overlap({ x0: s.cx - 0.525, x1: s.cx + 0.525, ...plq }, frame),
  'placa por debajo del marco, sin choque', `placa y ${plq.y0.toFixed(3)}..${plq.y1.toFixed(3)} vs marco desde ${frame.y0.toFixed(3)}`);
chk(plq.y0 > 0, 'placa no toca el piso', `y=${plq.y0.toFixed(3)}`);

// ============ paspartú ============
const mat = { x0: s.cx - (s.w / 2 + GAP), x1: s.cx + (s.w / 2 + GAP), y0: s.cy - (s.h / 2 + GAP), y1: s.cy + (s.h / 2 + GAP) };
chk(mat.x0 >= frame.x0 + FW - 1e-9 && mat.x1 <= frame.x1 - FW + 1e-9,
  'paspartú cubre exactamente la ventana del marco', `mat ${mat.x0.toFixed(2)}..${mat.x1.toFixed(2)} / ventana ${(frame.x0 + FW).toFixed(2)}..${(frame.x1 - FW).toFixed(2)}`);

// ============ coherencia de SCREENS ============
const aspect = s.w / s.h;
chk(Math.abs(aspect - 480 / 848) < 0.003, 'relación de aspecto = video 480x848',
  `${aspect.toFixed(4)} vs ${(480 / 848).toFixed(4)}`);

console.log(fail === 0 ? '\nTODOS LOS CASOS PASARON' : `\n${fail} CASOS FALLARON`);
process.exit(fail ? 1 : 0);
