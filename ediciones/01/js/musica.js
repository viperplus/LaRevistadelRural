/* ============ Musica de fondo (MIDI) ============ */
(function () {
  "use strict";
  if (!document.body) return;
  if (typeof Tone === "undefined" || typeof Midi === "undefined") return;

  var CLAVE = "rev.musica";
  var MUSICA = [
    { titulo: "Inconsciente colectivo", artista: "Charly Garcia", archivo: "sonidos/musica/inconciente1.mid" },
    { titulo: "Cancion para mi muerte", artista: "Sui Generis", archivo: "sonidos/musica/cancionpara.mid" },
    { titulo: "El estudiante", artista: "Los Twist", archivo: "sonidos/musica/elestudia.mid" },
    { titulo: "Gitana", artista: "Los Fabulosos Cadillacs", archivo: "sonidos/musica/gitana.mid" },
    { titulo: "Rezo por vos", artista: "Charly Garcia", archivo: "sonidos/musica/rezo.mid" },
    { titulo: "Solo le pido a Dios", artista: "Leon Gieco", archivo: "sonidos/musica/sololepido.mid" },
    { titulo: "Y dale alegria a mi corazon", artista: "Fito Paez", archivo: "sonidos/musica/ydaleale.mid" },
  ];

  var estado = { idx: 0, vol: 0.5, playing: false };
  try {
    var guardado = JSON.parse(localStorage.getItem(CLAVE) || "null");
    if (guardado) {
      estado.idx = (guardado.idx || 0) % MUSICA.length;
      estado.vol = (typeof guardado.vol === "number") ? guardado.vol : 0.5;
    }
  } catch (e) {}

  function guardar() {
    try { localStorage.setItem(CLAVE, JSON.stringify({ idx: estado.idx, vol: estado.vol })); }
    catch (e) {}
  }

  var iconoNota =
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">' +
    '<path d="M9 18V5l12-2v13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
    '<circle cx="6" cy="18" r="3" fill="currentColor"/><circle cx="18" cy="16" r="3" fill="currentColor"/></svg>';

  var cont = document.createElement("div");
  cont.className = "musica";
  cont.innerHTML =
    '<button type="button" class="musica__btn" aria-expanded="false" aria-label="Musica de fondo">' +
    iconoNota + '<span class="musica__indicador" hidden></span></button>' +
    '<div class="musica__panel" hidden role="dialog" aria-label="Reproductor de musica">' +
    '<div class="musica__cab">' +
    '<div class="musica__info">' +
    '<p class="musica__titulo" id="musica-titulo">-</p>' +
    '<p class="musica__artista" id="musica-artista">-</p>' +
    '</div>' +
    '<button type="button" class="musica__cerrar" aria-label="Cerrar el reproductor">x</button>' +
    '</div>' +
    '<div class="musica__progreso">' +
    '<span class="musica__tiempo" data-tiempo>0:00</span>' +
    '<input type="range" class="musica__barra" min="0" max="1000" value="0" aria-label="Progreso de la canción">' +
    '<span class="musica__tiempo" data-duracion>0:00</span>' +
    '</div>' +
    '<div class="musica__controles">' +
    '<button type="button" class="musica__b" data-act="ant" aria-label="Cancion anterior">&#9664;&#9664;</button>' +
    '<button type="button" class="musica__b musica__b--play" data-act="play" aria-label="Reproducir">&#9654;</button>' +
    '<button type="button" class="musica__b" data-act="sig" aria-label="Cancion siguiente">&#9654;&#9654;</button>' +
    '</div>' +
    '<div class="musica__volumen">' +
    '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true" focusable="false">' +
    '<path d="M3 9h4l5-4v14l-5-4H3zM16 8a4 4 0 0 1 0 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
    '<input type="range" class="musica__vol" min="0" max="100" value="' + Math.round(estado.vol * 100) + '" aria-label="Volumen">' +
    '</div>' +
    '<p class="musica__estado" data-estado>Cargando...</p>' +
    '</div>';
  document.body.appendChild(cont);

  var btn = cont.querySelector(".musica__btn");
  var panel = cont.querySelector(".musica__panel");
  var indicador = cont.querySelector(".musica__indicador");
  var tituloEl = cont.querySelector("#musica-titulo");
  var artistaEl = cont.querySelector("#musica-artista");
  var tiempoEl = cont.querySelector("[data-tiempo]");
  var duracionEl = cont.querySelector("[data-duracion]");
  var barra = cont.querySelector(".musica__barra");
  var volSlider = cont.querySelector(".musica__vol");
  var playBtn = cont.querySelector('[data-act="play"]');
  var estadoEl = cont.querySelector("[data-estado]");

  var synth = new Tone.PolySynth(Tone.Synth, {
    oscillator: { type: "triangle" },
    envelope: { attack: 0.02, decay: 0.15, sustain: 0.25, release: 0.6 }
  });
  var reverb = new Tone.Reverb({ decay: 1.8, wet: 0.18 });
  synth.connect(reverb);
  reverb.toDestination();

  var duracion = 0;
  var notasProgramadas = [];
  var cargando = false;

  function fmt(seg) {
    seg = Math.max(0, Math.floor(seg || 0));
    var m = Math.floor(seg / 60);
    var s = seg % 60;
    return m + ":" + (s < 10 ? "0" : "") + s;
  }

  function actualizarInfo() {
    var t = MUSICA[estado.idx];
    tituloEl.textContent = t.titulo;
    artistaEl.textContent = t.artista;
    barra.value = 0;
    tiempoEl.textContent = "0:00";
    duracionEl.textContent = "0:00";
  }

  function actualizarBotones() {
    playBtn.textContent = estado.playing ? "II" : ">";
    playBtn.setAttribute("aria-label", estado.playing ? "Pausar" : "Reproducir");
    indicador.hidden = !estado.playing;
    btn.classList.toggle("musica__btn--playing", estado.playing);
  }

  function cargar(idx) {
    if (idx < 0) idx = MUSICA.length - 1;
    if (idx >= MUSICA.length) idx = 0;
    estado.idx = idx;
    cargando = true;
    actualizarInfo();
    estadoEl.textContent = "Cargando...";
    Tone.Transport.stop();
    Tone.Transport.cancel();
    notasProgramadas = [];
    duracion = 0;

    fetch(MUSICA[idx].archivo)
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.arrayBuffer();
      })
      .then(function (buf) {
        var midi = new Midi(buf);
        duracion = midi.duration || 0;
        midi.tracks.forEach(function (track) {
          track.notes.forEach(function (note) {
            var ev = Tone.Transport.schedule(function (time) {
              synth.triggerAttackRelease(note.name, note.duration, time, note.velocity);
            }, note.time);
            notasProgramadas.push(ev);
          });
        });
        Tone.Transport.bpm.value = (midi.header.tempos && midi.header.tempos.length)
          ? midi.header.tempos[0].bpm : 120;
        cargando = false;
        duracionEl.textContent = fmt(duracion);
        estadoEl.textContent = "Listo";
      })
      .catch(function (err) {
        cargando = false;
        estadoEl.textContent = "No se pudo cargar";
      });
  }

  function reproducir() {
    Tone.start().then(function () {
      Tone.Transport.start();
      estado.playing = true;
      guardar();
      actualizarBotones();
      estadoEl.textContent = "Reproduciendo...";
    }).catch(function (e) {
      estadoEl.textContent = "Error de audio";
    });
  }

  function pausar() {
    Tone.Transport.pause();
    estado.playing = false;
    guardar();
    actualizarBotones();
    estadoEl.textContent = "Pausado";
  }

  function anterior() { cargar(estado.idx - 1); estado.playing = true; reproducir(); }
  function siguiente() { cargar(estado.idx + 1); estado.playing = true; reproducir(); }

  btn.addEventListener("click", function () {
    var abierto = !panel.hidden;
    panel.hidden = abierto;
    btn.setAttribute("aria-expanded", abierto ? "false" : "true");
    if (!abierto && !cargando) cargar(estado.idx);
  });
  cont.querySelector(".musica__cerrar").addEventListener("click", function () {
    panel.hidden = true;
    btn.setAttribute("aria-expanded", "false");
  });
  playBtn.addEventListener("click", function () {
    if (cargando) return;
    if (estado.playing) pausar(); else reproducir();
  });
  cont.querySelector('[data-act="ant"]').addEventListener("click", function () { anterior(); });
  cont.querySelector('[data-act="sig"]').addEventListener("click", function () { siguiente(); });

  barra.addEventListener("input", function () {
    if (!duracion) return;
    var pct = parseInt(barra.value, 10) / 1000;
    Tone.Transport.seconds = duracion * pct;
  });
  volSlider.addEventListener("input", function () {
    estado.vol = parseInt(volSlider.value, 10) / 100;
    Tone.Destination.volume.value = Tone.gainToDb(estado.vol);
    guardar();
  });

  function tick() {
    if (estado.playing && duracion > 0) {
      var pos = Tone.Transport.seconds;
      if (pos >= duracion - 0.3) { siguiente(); return; }
      barra.value = Math.round((pos / duracion) * 1000);
      tiempoEl.textContent = fmt(pos);
      duracionEl.textContent = fmt(duracion);
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);

  document.addEventListener("click", function (ev) {
    if (panel.hidden) return;
    if (cont.contains(ev.target)) return;
    panel.hidden = true;
    btn.setAttribute("aria-expanded", "false");
  });
  document.addEventListener("keydown", function (ev) {
    if (panel.hidden) return;
    if (ev.key === "Escape") { panel.hidden = true; btn.setAttribute("aria-expanded", "false"); }
  });

  Tone.Destination.volume.value = Tone.gainToDb(estado.vol);
  actualizarInfo();
  setTimeout(function () { cargar(estado.idx); }, 1500);
})();
