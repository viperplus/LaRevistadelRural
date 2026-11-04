/* Genera _tmp_escena.html: copia de prueba de la feria.
   - expone las variables de la IIFE via window.__dbg
   - carga _harness_escena.js
   El archivo original nunca se modifica. */
const fs = require('fs');
const path = require('path');

const dir = __dirname;
const src = fs.readFileSync(path.join(dir, 'visita_virtual.html'), 'utf8');

const inj = '\n;window.__dbg=function(){return{screenObjs:screenObjs,camera:camera,scene:scene,' +
  'renderer:renderer,updateScreens:updateScreens,start:start,spinners:spinners,started:started,' +
  'MP:MP,peers:function(){return MP.peers;},mpAddPeer:mpAddPeer,mpApply:mpApply,' +
  'makeAvatar:makeAvatar,updatePeers:updatePeers,updateRoster:updateRoster,' +
  'chatAdd:chatAdd,openChat:openChat,closeChat:closeChat,sendChat:sendChat,' +
  'mpStart:mpStart,mpStop:mpStop,mpSend:mpSend,mpSetState:mpSetState,' +
  'getPX:function(){return PX;},getPZ:function(){return PZ;},getYAW:function(){return YAW;},' +
  'setPos:function(x,yaw){PX=x;PZ=5;YAW=yaw;},toast:toast,rosterEl:rosterEl,' +
  'chatBox:chatBox,chatIn:chatIn,chatLog:chatLog,chatHint:chatHint,keys:keys};};\n';

const idx = src.lastIndexOf('})();');
if (idx < 0) throw new Error('no se encontró el cierre de la IIFE en visita_virtual.html');
let out = src.slice(0, idx) + inj + src.slice(idx);

const b = out.lastIndexOf('</body>');
if (b < 0) throw new Error('no se encontró </body>');
out = out.slice(0, b) + '<script src="_harness_escena.js"></script>\n' + out.slice(b);

/* dos copias idénticas: cada una actúa como un visitante distinto */
for (const name of ['_tmp_escena.html', '_tmp_escena2.html']) {
  fs.writeFileSync(path.join(dir, name), out, 'utf8');
  console.log('generado: ' + name + '  (' + out.length + ' chars)');
}
console.log('dbg insertado en el offset ' + idx + ', harness en ' + out.lastIndexOf('<script src="_harness_escena.js">'));
