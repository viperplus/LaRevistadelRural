/* Arnes: se inyecta en la copia instrumentalizada (_tmp_escena.html).
   Observa y ejercita la feria sin modificar el archivo original.
   Con ?harness=0 se queda callado (lo usa el test de red). */
(function(){
if(location.search.indexOf('harness=0')>=0)return;
var results=[], done=false, tries=0, diag='';
var pre=document.createElement('pre');
pre.id='salida_test';
pre.style.cssText='position:fixed;left:0;top:0;right:0;z-index:99999;margin:0;padding:8px;'+
  'background:#0b1520;color:#d7e6f5;font:12px/1.35 Consolas,monospace;max-height:90vh;overflow:auto;white-space:pre-wrap';
document.body.appendChild(pre);

function chk(ok,label,got){
  results.push((ok?'OK   ':'FALLO ')+label+(got!==undefined?'   ['+got+']':''));
}
function finish(){
  if(done)return; done=true;
  var nOK=0,nF=0;
  for(var i=0;i<results.length;i++){
    if(results[i].indexOf('OK')===0)nOK++;
    else if(results[i].indexOf('FALLO')===0)nF++;
  }
  pre.textContent='RESULTADOS ('+nOK+' OK, '+nF+' FALLO)\n'+
    '--------------------------------------------------\n'+results.join('\n')+
    '\n--------------------------------------------------\n'+
    (nF===0?'TODOS LOS CASOS PASARON':'HAY FALLOS');
  document.title='TEST_DONE';
}
function fail(msg){ results.push('FALLO '+msg); finish(); }

function near(scene,x,z,tol){
  var hit=null;
  scene.traverse(function(n){
    if(hit||!n.position||n.position.y>0.6)return;
    if(Math.abs(n.position.x-x)<tol&&Math.abs(n.position.z-z)<tol)hit=n;
  });
  return hit;
}

var iv=setInterval(function(){
  tries++;
  var D=null;
  try{ D=window.__dbg?window.__dbg():null; }catch(e){ diag='__dbg: '+e.message; }
  if(D&&D.screenObjs&&D.camera&&D.scene&&D.updateScreens&&D.screenObjs.length){
    clearInterval(iv);
    setTimeout(function(){ run(D); },600);
    return;
  }
  if(tries>400){ clearInterval(iv); fail('TIMEOUT esperando la escena. '+diag+
    ' tries='+tries+' started='+(D?D.started:'?')); }
},50);

setTimeout(function(){ if(!done){ results.push('FALLO TIMEOUT global'); results.push('DIAG '+diag); finish(); } },70000);

function run(D){
  try{
    /* --- 1. arranque --- */
    try{ D.start(); results.push('OK   start() sin error'); }
    catch(e){ results.push('FALLO start() '+e.message); }

    var o=D.screenObjs[0], s=o.s;

    /* --- 2. el cuadro --- */
    chk(o.mesh&&o.mesh.type==='Group','el video es un GRUPO (cuadro), no un plano suelto',o.mesh?o.mesh.type:'nulo');
    var kids=o.mesh?o.mesh.children.length:0;
    chk(kids>=11,'piezas del cuadro (4 barras + paspartú + respaldo + video + 4 filos)',kids);
    chk(!!o.plane&&Math.abs(o.plane.geometry.parameters.width-s.w)<1e-9,'plano del video con el ancho correcto',o.plane?o.plane.geometry.parameters.width:'nulo');
    chk(!!o.plaque,'placa con el nombre bajo el marco',!!o.plaque);
    chk(!!o.icon,'icono de play',!!o.icon);

    var matOK=false,backOK=false,videoOK=false,lips=0,bars=0;
    if(o.mesh)o.mesh.children.forEach(function(c){
      if(c===o.plane)videoOK=true;
      else if(c.geometry&&c.geometry.type==='BoxGeometry'){
        var d=c.geometry.parameters.depth;
        if(Math.abs(d-0.11)<1e-6)bars++;
        else if(Math.abs(d-0.04)<1e-6)lips++;
        else if(Math.abs(d-0.03)<1e-6)backOK=true;
      } else if(c.geometry&&c.geometry.type==='PlaneGeometry')matOK=true;
    });
    chk(bars===4,'4 barras del marco',bars);
    chk(lips===4,'4 filos dorados',lips);
    chk(backOK,'respaldo oscuro detrás del paspartú',backOK);
    chk(matOK,'paspartú (plano) presente',matOK);
    chk(videoOK,'video es hijo del grupo del cuadro',videoOK);

    /* --- 3. embebido contra la pared --- */
    var wallFace=-30+0.22/2;
    var grpZ=o.mesh.position.z;
    chk(grpZ-0.11<=wallFace,'respaldo del marco dentro de la pared',(grpZ-0.11).toFixed(3)+' <= '+wallFace.toFixed(3));
    chk(grpZ>wallFace,'frente del marco sobresale de la pared',(grpZ-wallFace).toFixed(3)+'m');
    var expPlq=s.cy-(s.h/2+0.05+0.15)-0.05-(1.05/2.844)/2;
    chk(Math.abs(o.plaque.position.y-expPlq)<1e-4,'placa colgada bajo el marco',o.plaque.position.y.toFixed(3)+' (esperado '+expPlq.toFixed(3)+')');
    chk(o.plaque.position.y>0,'placa no cae al piso',o.plaque.position.y.toFixed(3));
    chk(!!(o.plane.material&&o.plane.material.map),'textura de video asignada',!!(o.plane.material&&o.plane.material.map));

    /* --- 4. ambientación de turismo --- */
    chk(D.spinners.length===1,'globo terráqueo creado (rota en el bucle)',D.spinners.length);
    chk(!!near(D.scene,6.9,4.1,0.4),'letrero de destinos');
    chk(!!near(D.scene,-6.9,4.1,0.4),'globo en su pedestal');
    chk(!!near(D.scene,3.6,4.7,0.5),'valijas (derecha)');
    chk(!!near(D.scene,-3.6,4.7,0.5),'valijas (izquierda)');
    chk(!!near(D.scene,0,3.6,0.5),'folletos sobre el escritorio');
    chk(!!near(D.scene,-15.4,2.2,0.5),'tablas de surf (oeste)');
    chk(!!near(D.scene,15.4,2.2,0.5),'tablas de surf (este)');

    /* --- 5. oclusión real moviendo la cámara --- */
    var cam=D.camera, old=cam.position.clone();
    function probe(px,pz,expect,label){
      cam.position.set(px,1.65,pz);
      cam.updateMatrixWorld(true);
      cam.matrixWorldInverse.copy(cam.matrixWorld).invert();
      D.updateScreens();
      var got=!!(o.visible&&o.mesh.visible&&o.plaque.visible);
      chk(got===expect,label,(got?'visible':'oculto')+' (esperado '+(expect?'visible':'oculto')+')');
      cam.position.copy(old);
      cam.updateMatrixWorld(true);
      cam.matrixWorldInverse.copy(cam.matrixWorld).invert();
    }
    probe(0,-25,  true,  'en el salón, frente al video -> se ve');
    probe(0,-12,  true,  'en el pasillo -> se ve por el vano');
    probe(0,0,    true,  'en el vestíbulo -> se ve por el vano');
    probe(8,0,    false, 'vestíbulo derecho -> NO se ve a través del muro');
    probe(-8,0,   false, 'vestíbulo izquierdo -> NO se ve a través del muro');
    probe(-14,0,  false, 'sala oeste -> NO se ve a través del muro');
    probe(14,0,   false, 'sala este -> NO se ve a través del muro');
    probe(0,10,   false, 'fuera del edificio -> NO se ve a través del muro');
    probe(0,-34,  false, 'detrás del muro -> NO se ve a través del muro');
    probe(10,-28, true,  'esquina sureste del salón -> se ve');

    cam.position.copy(old);
    cam.updateMatrixWorld(true);
    cam.matrixWorldInverse.copy(cam.matrixWorld).invert();
    D.updateScreens();
    results.push('OK   cámara restaurada en ('+old.x.toFixed(1)+','+old.z.toFixed(1)+')');

    /* ============ 6. multijugador: avatares ============ */
    var before=D.scene.children.length;
    var av=D.makeAvatar('Ana',0xe76f51);
    chk(av.g.type==='Group','makeAvatar devuelve un grupo en la escena',av.g.type);
    chk(av.tag&&av.tag.type==='Sprite','el avatar lleva un cartel con su nombre',av.tag?av.tag.type:'nulo');
    chk(D.scene.children.length===before+1,'el avatar se agregó a la escena',before+' -> '+D.scene.children.length);
    chk(!!(av.g.children.length>=8),'piezas del avatar (cuerpo, cabeza, pelo, brazos, piernas, cartel)',av.g.children.length);
    D.scene.remove(av.g);

    /* ============ 7. multijugador: registro y roster ============ */
    D.MP.on=true;D.MP.name='Profe';D.MP.color=0x2a9d8f;D.MP.isHost=true;
    var n0=Object.keys(D.peers()).length;
    D.mpAddPeer('p-ana','Ana',0xe76f51);
    D.mpAddPeer('p-beto','Beto',0x9b5de5);
    chk(Object.keys(D.peers()).length===n0+2,'se registraron dos compañeros',Object.keys(D.peers()).length);
    D.updateRoster();
    chk(D.rosterEl.classList.contains('show'),'el roster se muestra en el HUD');
    chk(D.rosterEl.innerHTML.indexOf('Profe')>=0,'el roster lista al jugador actual');
    chk(D.rosterEl.innerHTML.indexOf('Beto')>=0,'el roster lista a los compañeros');
    chk(D.rosterEl.innerHTML.indexOf('p-beto')<0,'el roster no expone ids internos',D.rosterEl.innerHTML.indexOf('p-beto')<0?'oculto':'filtrado');

    /* ============ 8. multijugador: interpolación de posición ============ */
    var A=D.peers()['p-ana'];
    var x0=A.g.position.x, z0=A.g.position.z;
    A.tx=x0+2.5;A.tz=z0-3.0;A.tyaw=1.1;A.moving=true;
    D.updatePeers(0.25,1.0);
    var moved=Math.abs(A.g.position.x-x0)+Math.abs(A.g.position.z-z0);
    chk(moved>0.2,'el avatar se desplaza hacia el destino en el bucle','Δ='+moved.toFixed(3));
    chk(Math.abs(A.g.rotation.y-1.1)>0.05,'el avatar gira hacia el destino','yaw='+A.g.rotation.y.toFixed(3));

    /* ============ 9. multijugador: mensajes ============ */
    D.mpApply({t:'st',from:'p-ana',x:1,z:-4,r:0.5,mv:true});
    chk(A.tx===1&&A.tz===-4&&A.tyaw===0.5,'estado recibido aplicado al avatar','tx='+A.tx+' tz='+A.tz+' r='+A.tyaw);
    var logN=D.chatLog.children.length;
    D.mpApply({t:'chat',name:'Ana',color:0xe76f51,text:'hola a todos'});
    chk(D.chatLog.children.length===logN+1,'el chat recibe mensajes remotos','msgs='+D.chatLog.children.length);
    chk(D.chatLog.innerHTML.indexOf('hola a todos')>=0,'el texto del chat se muestra');
    var logN2=D.chatLog.children.length;
    D.mpApply({t:'chat',name:'Eva',color:0x9b5de5,text:'<img src=x onerror=alert(1)>'});
    chk(D.chatLog.children.length===logN2+1,'llega el mensaje malicioso');
    chk(D.chatLog.innerHTML.indexOf('<img')<0,'el chat escapa HTML (sin inyección)','escapado');

    /* ============ 10. multijugador: baja de compañeros ============ */
    var beforeDrop=Object.keys(D.peers()).length;
    var sceneN=D.scene.children.length;
    D.mpApply({t:'bye',id:'p-ana'});
    chk(Object.keys(D.peers()).length===beforeDrop-1,'el avatar se da de baja','quedan '+Object.keys(D.peers()).length);
    chk(D.scene.children.length===sceneN-1,'su mesh se quitó de la escena',sceneN+' -> '+D.scene.children.length);

    /* ============ 11. chat: teclado y apertura ============ */
    D.MP.on=false;D.updateRoster();
    chk(!D.rosterEl.classList.contains('show'),'el roster se oculta sin sala');
    D.openChat();
    chk(D.chatBox.classList.contains('show'),'Enter/T abre el chat');
    window.dispatchEvent(new KeyboardEvent('keydown',{code:'KeyW',bubbles:true}));
    chk(!D.keys.KeyW,'con el chat abierto el jugador NO camina');
    window.dispatchEvent(new KeyboardEvent('keyup',{code:'KeyW',bubbles:true}));
    var logN3=D.chatLog.children.length;
    D.chatIn.value='  me gusta el puesto 3  ';
    D.sendChat();
    chk(D.chatLog.children.length===logN3+1,'el mensaje propio entra en el chat');
    chk(D.chatLog.innerHTML.indexOf('me gusta el puesto 3')>=0,'con el texto correcto');
    chk(!D.chatBox.classList.contains('show'),'enviar cierra el chat');
    chk(D.chatIn.value==='','el campo queda limpio',JSON.stringify(D.chatIn.value));
    window.dispatchEvent(new KeyboardEvent('keydown',{code:'KeyW',bubbles:true}));
    chk(!!D.keys.KeyW,'con el chat cerrado el jugador camina normalmente');
    window.dispatchEvent(new KeyboardEvent('keyup',{code:'KeyW',bubbles:true}));
    D.openChat();
    chk(D.chatBox.classList.contains('show'),'se puede volver a abrir el chat');
    window.dispatchEvent(new KeyboardEvent('keydown',{code:'KeyW',bubbles:true}));
    chk(!D.keys.KeyW,'y de nuevo el chat bloquea el movimiento');
    window.dispatchEvent(new KeyboardEvent('keydown',{code:'Escape',bubbles:true}));
    chk(!D.chatBox.classList.contains('show'),'con el chat abierto, Esc lo cierra');
    window.dispatchEvent(new KeyboardEvent('keydown',{code:'KeyW',bubbles:true}));
    chk(!!D.keys.KeyW,'al cerrar con Esc se recupera el control');
    window.dispatchEvent(new KeyboardEvent('keyup',{code:'KeyW',bubbles:true}));
    D.closeChat(false);

    /* ============ 12. salida limpia ============ */
    var nPeers=Object.keys(D.peers()).length;
    D.mpAddPeer('p-final','Zoe',0x06d6a0);
    chk(Object.keys(D.peers()).length===nPeers+1,'se puede seguir sumando compañeros',
        nPeers+' -> '+Object.keys(D.peers()).length);
    D.closeChat(false);D.MP.on=false;D.MP.peers={};
    results.push('OK   pruebas de multijugador terminadas');
  }catch(e){
    results.push('FALLO excepción: '+e.message+' @ '+((e.stack||'').split('\n')[1]||''));
  }
  finish();
}
})();
