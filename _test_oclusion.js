/* Test: el cuadro de video NO debe verse a través de las paredes.
   Reconstruye las colisiones de los muros desde visita_virtual.html
   y ejercita screenOccluded() con la misma lógica del código. */
const fs = require('fs');
const html = fs.readFileSync(__dirname + '/visita_virtual.html', 'utf8');

const WALL_H = 4, T = 0.22;
const colliders = [];

function addCollider(cx, cz, w, d, h) {
  colliders.push({
    minX: cx - w / 2, maxX: cx + w / 2,
    minZ: cz - d / 2, maxZ: cz + d / 2,
    h: (h === undefined ? WALL_H : h)
  });
}
function wall(x1, z1, x2, z2, mat) {
  const horiz = Math.abs(x2 - x1) > Math.abs(z2 - z1);
  const len = horiz ? Math.abs(x2 - x1) : Math.abs(z2 - z1);
  const w = horiz ? len : T, d = horiz ? T : len;
  addCollider((x1 + x2) / 2, (z1 + z2) / 2, w, d);
}
function lintel(x1, z1, x2, z2, y0) {
  /* el dintel queda por encima de la mirada: no debe ocluir */
}

// --- extrae TODOS los wall()/lintel() del HTML (plano de la feria) ---
const re = /\b(wall|lintel)\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*(?:,[^)]*)?\)/g;
let m, count = 0;
while ((m = re.exec(html)) !== null) {
  const args = [2, 3, 4, 5].map(i => parseFloat(m[i]));
  if (args.some(isNaN)) continue;
  if (m[1] === 'wall') wall(...args); else lintel(...args);
  count++;
}
console.log(`muros cargados: ${count}  colisiones: ${colliders.length}`);

// --- segBlocked: idéntico al del HTML ---
function segBlocked(x1, z1, x2, z2, eye) {
  const dx = x2 - x1, dz = z2 - z1;
  for (let i = 0; i < colliders.length; i++) {
    const c = colliders[i];
    if (c.h < eye) continue;
    let t0 = 0, t1 = 1, ok = true, ta, tb, q;
    if (Math.abs(dx) < 1e-9) { if (x1 < c.minX || x1 > c.maxX) ok = false; }
    else {
      ta = (c.minX - x1) / dx; tb = (c.maxX - x1) / dx;
      if (ta > tb) { q = ta; ta = tb; tb = q; }
      if (ta > t0) t0 = ta; if (tb < t1) t1 = tb; if (t0 > t1) ok = false;
    }
    if (!ok) continue;
    if (Math.abs(dz) < 1e-9) { if (z1 < c.minZ || z1 > c.maxZ) continue; }
    else {
      ta = (c.minZ - z1) / dz; tb = (c.maxZ - z1) / dz;
      if (ta > tb) { q = ta; ta = tb; tb = q; }
      if (ta > t0) t0 = ta; if (tb < t1) t1 = tb; if (t0 > t1) continue;
    }
    if (t0 <= 1) return true;
  }
  return false;
}

// --- la pantalla (debe coincidir con SCREENS del HTML) ---
const s = { cx: 0, cy: 2.4, cz: -29.79, ry: 0, w: 1.5, h: 2.65 };
function cornersOf(s) {
  const rx = Math.cos(s.ry), rz = -Math.sin(s.ry), hw = s.w / 2, hh = s.h / 2;
  return [
    { x: s.cx - rx * hw, z: s.cz - rz * hw },
    { x: s.cx + rx * hw, z: s.cz + rz * hw },
    { x: s.cx + rx * hw, z: s.cz + rz * hw },
    { x: s.cx - rx * hw, z: s.cz - rz * hw }
  ];
}
function screenOccluded(cam, s) {
  let free = 0;
  const cs = cornersOf(s);
  if (!segBlocked(cam.x, cam.z, s.cx, s.cz, cam.eye)) free += 2;
  for (const c of cs) if (!segBlocked(cam.x, cam.z, c.x, c.z, cam.eye)) free++;
  return free < 2;
}

const EYE = 1.65;
const cases = [
  ['Salón, frente al video',            { x: 0, z: -25 },   false, 'debe verse'],
  ['Salón, costado izq.',               { x: -9, z: -24 },  false, 'debe verse'],
  ['Pasillo (centro)',                  { x: 0, z: -12 },   false, 'se ve por el vano'],
  ['Pasillo, costado',                  { x: 2.6, z: -10 }, false, 'se ve por el vano'],
  ['Vestíbulo (centro)',                { x: 0, z: 0 },     false, 'se ve por el vano'],
  ['Vestíbulo, a la derecha',           { x: 8, z: 0 },     true,  'NUNCA a través del muro'],
  ['Vestíbulo, a la izquierda',         { x: -8, z: 0 },    true,  'NUNCA a través del muro'],
  ['Sala oeste (Gastronomía)',          { x: -14, z: 0 },   true,  'NUNCA a través del muro'],
  ['Sala este (Artesanías)',            { x: 14, z: 0 },    true,  'NUNCA a través del muro'],
  ['Fuera del edificio (al norte)',     { x: 0, z: 10 },    true,  'NUNCA a través del muro'],
  ['Detrás del muro del video',         { x: 0, z: -34 },   true,  'NUNCA a través del muro'],
  ['Salón, esquina sureste',            { x: 10, z: -28 },  false, 'debe verse'],
  ['Pasillo, pegado al muro oeste',     { x: -2.6, z: -14 },false, 'se ve por el vano']
];

let fail = 0;
for (const [name, p, expectOccluded, why] of cases) {
  const cam = { x: p.x, z: p.z, eye: EYE };
  const occ = screenOccluded(cam, s);
  const ok = occ === expectOccluded;
  if (!ok) fail++;
  console.log(`${ok ? 'OK  ' : 'FALLO'}  ${name.padEnd(30)} ocluido=${occ ? 'si' : 'no'}  (esperado ${expectOccluded ? 'si' : 'no'})  -> ${why}`);
}
console.log(fail === 0 ? '\nTODOS LOS CASOS PASARON' : `\n${fail} CASOS FALLARON`);
process.exit(fail ? 1 : 0);
