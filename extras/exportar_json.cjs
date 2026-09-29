// extras/exportar_json.cjs
// Lee datos/edicion-01.js, lo envuelve en una IIFE y le pide devolver
// { EDICION, SECCIONES, ARTICULOS } (sus const quedan en el scope de esa
// funcion, asi el return los ve). Escribe datos/ediciones.json con el JSON
// canonico. Tecnica estandar de "evaluar JS como modulo" con Node.
'use strict';
const fs   = require('fs');
const vm   = require('vm');
const path = require('path');

const BASE = path.resolve(__dirname, '..');
const ORIG = process.argv[2] ? path.resolve(process.argv[2])
                             : path.join(BASE, 'datos', 'edicion-01.js');
const OUT  = process.argv[3] ? path.resolve(process.argv[3])
                             : path.join(BASE, 'datos', 'ediciones.json');

const src = fs.readFileSync(ORIG, 'utf8');

// IIFE: ( function () { <fuente real> ; return { EDICION, SECCIONES, ARTICULOS }; } )()
const wrapper = '(function () {\n' + src + '\n'
  + '  ;return { EDICION, SECCIONES, ARTICULOS };\n})();';

const sandbox = {
  console: { log() {}, warn() {}, error(m) { console.error(m); } },
  setTimeout, clearTimeout,
  URL, URLSearchParams,
  require(id) { throw new Error('require(' + id + ') no disponible'); },
};
sandbox.window = sandbox;

let datos;
try {
  datos = vm.runInNewContext(wrapper, sandbox, { filename: 'edicion-01.js' });
} catch (e) {
  console.error('ERR evaluando edicion-01.js: ' + e.message);
  process.exit(1);
}

if (!datos.EDICION || !Array.isArray(datos.SECCIONES) || !Array.isArray(datos.ARTICULOS)) {
  console.error('Datos incompletos: EDICION=%s SECCIONES=%s ARTICULOS=%s',
    typeof datos.EDICION, Array.isArray(datos.SECCIONES),
    Array.isArray(datos.ARTICULOS));
  process.exit(1);
}

const payload = JSON.stringify(
  { edicion: datos.EDICION, secciones: datos.SECCIONES, articulos: datos.ARTICULOS },
  (k, v) => (typeof v === 'string' ? v.replace(/[\u0000-\u001f]/g, ' ') : v),
  2);

fs.writeFileSync(OUT, payload, 'utf8');
console.log('OK  %s  %dB  secciones=%d articulos=%d',
  path.relative(BASE, OUT), Buffer.byteLength(payload, 'utf8'),
  datos.SECCIONES.length, datos.ARTICULOS.length);

// Envuelvo el fuente real en una IIFE que devuelve las const; detalles:
//   * vm ya no necesita promesas ni Array.map en el fuente — se ejecuta tal cual.
