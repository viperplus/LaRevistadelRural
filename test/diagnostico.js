const fs = require('fs');
const path = require('path');
const dir = process.argv[2];
const d = JSON.parse(Buffer.from(fs.readFileSync(path.join(dir, 'test/datos.b64.txt'), 'utf8').trim(), 'base64').toString('utf8'));

console.log('--- REPASO (3 preguntas) ---');
d.QUIZ.forEach((q, i) => {
  console.log((i + 1) + ') ' + q.q);
  console.log('   opciones: ' + q.opts.join('  /  '));
  console.log('   correcta: indice ' + q.ok + ' -> ' + q.opts[q.ok]);
});

console.log('');
console.log('--- LISTA PARA LA CASA ---');
d.TRANSFER.forEach(t => console.log('  ' + t.t + '   ||   ' + t.n));

const todas = [];
Object.values(d.CONSIGNAS).forEach(x => todas.push(x));
Object.values(d.INTROS).forEach(x => todas.push(x.text));
Object.values(d.DEFS).forEach(x => { todas.push(x.narra); todas.push(x.titulo); });
Object.values(d.GROW_MSG).forEach(x => todas.push(x));
d.QUIZ.forEach(q => { todas.push(q.q); q.opts.forEach(o => todas.push(o)); todas.push(q.fb); });
d.TRANSFER.forEach(t => { todas.push(t.t); todas.push(t.n); });

console.log('');
console.log('--- CONTEO DE VOSEO ---');
console.log('frases totales: ' + todas.length);
const marcas = ['tocá', 'tenés', 'buscá', 'hacés', 'pedí', 'elegí', 'mirá', 'entotá', 'comé', 'contá', 'revisá', 'sembrás', 'podés', 'necesitás', 'querés', 'tocás'];
let conVoseo = 0;
for (const m of marcas) {
  const n = todas.filter(t => t.toLowerCase().includes(m)).length;
  if (n) { conVoseo += n; console.log('  ' + m + ': ' + n); }
}
console.log('frases con al menos una forma de voseo: ' + conVoseo);
console.log('');
console.log('prueba regex /\\btocá\\b/i sobre "Tocá las TRES plantas": ' + /\btocá\b/i.test('Tocá las TRES plantas'));
console.log('prueba includes("tocá") sobre la misma: ' + 'Tocá las TRES plantas'.toLowerCase().includes('tocá'));
console.log('');
console.log('--- ETIQUETAS DE ETAPA (para el aviso de punto final) ---');
Object.entries(d.STAGE_INFO).forEach(([k, v]) => console.log('  ' + k + ' -> ' + JSON.stringify(v.t)));
console.log('');
console.log('--- GROW_MSG ---');
Object.entries(d.GROW_MSG).forEach(([k, v]) => console.log('  ' + k + ' -> ' + JSON.stringify(v)));
