/* Visor de fotos: al clickear una imagen se abre en grande.
   Sin dependencias. Usa <dialog>, que ya trae Escape y foco atrapado. */
(function () {
  "use strict";
  if (typeof HTMLDialogElement === "undefined") return;

  var SEL = "figure.fig img, figure.collage__item img, figure.pres__foto img";
  var SEL_FIG = "figure.fig, figure.collage__item, figure.pres__foto";

  var dlg = document.createElement("dialog");
  dlg.className = "visor";
  dlg.setAttribute("aria-label", "Foto en grande");
  dlg.innerHTML =
    '<img class="visor__img" alt="">' +
    '<p class="visor__pie" hidden></p>' +
    '<button class="visor__btn visor__cerrar" type="button" aria-label="Cerrar">&#10005;</button>' +
    '<button class="visor__btn visor__ant" type="button" aria-label="Foto anterior" hidden>&#8249;</button>' +
    '<button class="visor__btn visor__sig" type="button" aria-label="Foto siguiente" hidden>&#8250;</button>';
  document.body.appendChild(dlg);

  var vImg = dlg.querySelector(".visor__img");
  var vPie = dlg.querySelector(".visor__pie");
  var vAnt = dlg.querySelector(".visor__ant");
  var vSig = dlg.querySelector(".visor__sig");
  var lista = [];
  var i = 0;

  function util(img) {
    return img && !img.closest("a");
  }

  /* En el álbum sólo se mira el pliego que está abierto: las demás
     hojas están ocultas y pasar de foto tendría que saltar de página. */
  function a_la_vista(img) {
    var v = img.closest(".album__vista");
    if (!v) return true;
    if (v.classList.contains("saliendo")) return false;
    return v.classList.contains("es-actual");
  }

  function recuento(cont) {
    return Array.prototype.filter.call(cont.querySelectorAll(SEL), function (i) {
      return util(i) && a_la_vista(i);
    });
  }

  function pie(fig) {
    var fc = fig && fig.querySelector("figcaption");
    if (!fc) return "";
    var st = fc.querySelector("strong");
    var sp = fc.querySelector("span");
    if (st && sp) return st.textContent.trim() + " · " + sp.textContent.trim();
    return fc.textContent.replace(/\s+/g, " ").trim();
  }

  function pintar() {
    var o = lista[i];
    if (!o) return;
    vImg.src = o.currentSrc || o.src;
    vImg.alt = o.alt || "";
    var t = pie(o.closest("figure"));
    vPie.textContent = t;
    vPie.hidden = !t;
    vAnt.hidden = vSig.hidden = lista.length < 2;
  }

  function abrir(n) {
    if (n < 0 || n >= lista.length) return;
    i = n;
    pintar();
    if (!dlg.open) {
      dlg.showModal();
      document.documentElement.classList.add("visor-on");
    }
  }

  function paso(d) {
    if (lista.length) abrir((i + d + lista.length) % lista.length);
  }

  document.addEventListener("click", function (e) {
    if (!e.target.closest) return;
    var o = e.target.closest(SEL);
    if (!o) {
      // El pie de la ficha también abre el visor: el cursor ya avisa que sí.
      var fig = e.target.closest(SEL_FIG);
      if (fig) o = fig.querySelector("img");
    }
    if (!util(o)) return;
    var cont = o.closest(".articulo__cuerpo, .collage") || o.closest("figure").parentNode;
    if (!cont) return;
    lista = recuento(cont);
    var n = lista.indexOf(o);
    if (n < 0) return;
    e.preventDefault();
    abrir(n);
  });

  dlg.querySelector(".visor__cerrar").addEventListener("click", function () {
    dlg.close();
  });
  vAnt.addEventListener("click", function () { paso(-1); });
  vSig.addEventListener("click", function () { paso(1); });

  dlg.addEventListener("click", function (e) {
    if (e.target === dlg) dlg.close();
  });

  dlg.addEventListener("close", function () {
    document.documentElement.classList.remove("visor-on");
    vImg.removeAttribute("src");
  });

  document.addEventListener("keydown", function (e) {
    if (!dlg.open) return;
    if (e.key === "ArrowLeft") { e.preventDefault(); paso(-1); }
    else if (e.key === "ArrowRight") { e.preventDefault(); paso(1); }
  });

  /* ------------------------------------------------------------------
     Álbum de figuritas: páginas que se pasan con los botones, el
     deslizador, las flechas del teclado o un gesto horizontal.
     ------------------------------------------------------------------ */
  /* ------------------------------------------------------------------
     Álbum de figuritas: pliegos de dos hojas que se pasan como en un
     libro. La hoja derecha gira sobre el lomo y en su dorso viaja la
     página que viene; la izquierda gira al revés. En pantallas angostas
     se ve una hoja por vez, con el mismo gesto sin el giro completo.
     ------------------------------------------------------------------ */
  (function album() {
    var alb = document.querySelector(".album");
    if (!alb) return;
    var pant = alb.querySelector(".album__pantalla");
    var pags = Array.prototype.slice.call(alb.querySelectorAll(".album__pagina"));
    if (!pant || !pags.length) return;

    var ant = alb.querySelector('.album__btn[data-paso="-1"]');
    var sig = alb.querySelector('.album__btn[data-paso="1"]');
    var nom = alb.querySelector(".album__estado-t");
    var num = alb.querySelector(".album__estado-n");
    var punto = alb.querySelector(".album__punto");
    var rango = alb.querySelector(".album__rango");
    var ir = alb.querySelector(".album__ir");
    var progN = alb.querySelector(".album__progreso-n");
    var progI = alb.querySelector(".album__progreso-i");

    var GIRO = 820;
    var vistas = [];     // { v, paginas, hojas }
    var vistaDe = [];    // número de página -> número de vista
    var primera = {};    // sede -> número de su primera página
    var fichasPag = [];  // figuritas que trae cada página
    var totalFichas = 0;
    var vistasPag = {};  // páginas que ya se miraron: el álbum se va llenando
    var doble = true;
    var anima = false;
    var i = 0;
    var reloj = null;
    var espera = null;
    var guardaReloj = null;

    try {
      vistasPag = JSON.parse(window.localStorage.getItem("album-vistas") || "{}") || {};
    } catch (e) { vistasPag = {}; }

    function malla(q) {
      return !!(window.matchMedia && window.matchMedia(q).matches);
    }

    pags.forEach(function (p, n) {
      if (p.dataset.sede && !(p.dataset.sede in primera)) primera[p.dataset.sede] = n;
    });

    function hoja(lado) {
      var h = document.createElement("div");
      h.className = "album__hoja album__hoja--" + lado;
      var f = document.createElement("div");
      f.className = "album__cara album__cara--frente";
      var a = document.createElement("div");
      a.className = "album__cara album__cara--atras";
      h.appendChild(f);
      h.appendChild(a);
      return h;
    }

    function guarda() {
      var g = document.createElement("div");
      g.className = "album__guarda";
      g.setAttribute("aria-hidden", "true");
      g.innerHTML = '<span class="album__guarda-s">La Revista<br>del Rural</span>';
      return g;
    }

    /* Junta las páginas en pliegos. Con doble página la portada y el
       índice van solos del lado derecho, sobre una guarda, y el resto
       se agrupa de a dos: así el dorso de cada hoja es justamente la
       página siguiente, igual que en un libro encuadernado. A partir de
       46rem de ancho; debajo se ve una hoja por vez, pero la hoja gira
       igual que en un libro. */
    function armar() {
      finalizar(false);
      doble = !window.matchMedia || malla("(min-width: 46rem)");

      pags.forEach(function (p) { pant.appendChild(p); });
      Array.prototype.slice.call(pant.querySelectorAll(".album__vista"))
        .forEach(function (v) { pant.removeChild(v); });

      var plan = [], lados, n;
      if (doble) {
        plan.push([null, pags[0]]);
        if (pags[1]) plan.push([null, pags[1]]);
        for (n = pags[1] ? 2 : 1; n < pags.length; n += 2) {
          plan.push([pags[n], pags[n + 1] || null]);
        }
        lados = ["izq", "der"];
      } else {
        for (n = 0; n < pags.length; n++) plan.push([pags[n]]);
        lados = ["der"];
      }

      var frag = document.createDocumentFragment();
      vistas = [];
      vistaDe = [];
      plan.forEach(function (par, v) {
        var vista = document.createElement("div");
        vista.className = "album__vista";
        vista.setAttribute("data-v", v);
        if (!doble) vista.setAttribute("data-simple", "");
        var hs = [];
        lados.forEach(function (lado, li) {
          var h = hoja(lado);
          h.firstChild.appendChild(par[li] || guarda());
          vista.appendChild(h);
          hs.push(h);
        });
        par.forEach(function (p) {
          if (p) vistaDe[pags.indexOf(p)] = v;
        });
        frag.appendChild(vista);
        vistas.push({ v: vista, paginas: par, hojas: hs });
      });
      pant.appendChild(frag);

      fichasPag = pags.map(function (p) {
        return p.querySelectorAll(".album__ficha").length;
      });
      totalFichas = fichasPag.reduce(function (a, b) { return a + b; }, 0);
    }

    /* El álbum se va completando a medida que se miran las páginas.
       Las que ya se vieron quedan guardadas, así que al volver se
       sigue de donde estaba. */
    function pintarProgreso() {
      if (!progN || !progI) return;
      var vistas_ = 0;
      pags.forEach(function (p, n) {
        if (vistasPag[p.dataset.pag || n]) vistas_ += fichasPag[n] || 0;
      });
      progN.textContent = vistas_ + " / " + totalFichas;
      var pct = totalFichas ? Math.round(vistas_ / totalFichas * 100) : 0;
      progI.style.width = pct + "%";
      if (pct > 0) progI.setAttribute("data-lleno", "1");
      else progI.removeAttribute("data-lleno");
    }

    function marcarVista(v) {
      if (!v) return;
      var cambia = false;
      v.paginas.forEach(function (p) {
        if (!p) return;
        var clave = p.dataset.pag;
        var n = parseInt(clave, 10);
        if (!fichasPag[n]) return;
        if (!vistasPag[clave]) { vistasPag[clave] = 1; cambia = true; }
      });
      if (!cambia) return;
      pintarProgreso();
      if (guardaReloj) clearTimeout(guardaReloj);
      guardaReloj = setTimeout(function () {
        guardaReloj = null;
        try {
          window.localStorage.setItem("album-vistas", JSON.stringify(vistasPag));
        } catch (e) {}
      }, 400);
    }

    function titulo(v) {
      var ts = [];
      v.paginas.forEach(function (p) {
        if (!p) return;
        var t;
        if (p.classList.contains("album__pagina--portada")) t = "Portada";
        else if (p.classList.contains("album__pagina--indice")) t = "Índice";
        else if (p.classList.contains("album__pagina--fin")) t = "Fin del álbum";
        else {
          var h = p.querySelector(".album__cab-t");
          t = h ? h.textContent.replace(/\s+/g, " ").trim() : "";
        }
        if (t && ts.indexOf(t) < 0) ts.push(t);
      });
      return ts.join(" · ");
    }

    /* Las páginas están ocultas hasta que se abren, así que el navegador
       no bajaba las fotos y al pasar de hoja aparecían en vacío. Se marcan
       como urgentes las del pliego actual y de los dos vecinos: con eso
       alcanza para que el giro no se vea pelado. */
    function alistar(n) {
      if (n < 0 || n >= vistas.length) return;
      var imgs = vistas[n].v.querySelectorAll('img[loading="lazy"]');
      for (var k = 0; k < imgs.length; k++) imgs[k].setAttribute("loading", "eager");
    }

    /* Las figuritas miden todas igual, pero el alto que hay para dos
       filas depende de la pantalla y del encabezado de la sede. En vez
       de dejar un hueco abajo, se mide lo que hay y se calcula el ancho
       de la ficha que llena justamente esas dos filas; si por ancho no
       se puede llenar entero, se acorta el pliego hasta que sobre
       exactamente lo mismo de un lado que del otro. El alto de la foto
       sale de su proporción, así que ninguna se deforma. */
    var figLista = false;
    function ajustarFig(forzar) {
      if (!alb || (figLista && !forzar)) return;
      var v = vistas[mostrada];
      if (!v) return;
      var pag = null;
      for (var j = 0; j < v.paginas.length && !pag; j++) {
        if (v.paginas[j] && v.paginas[j].querySelector(".album__grilla")) pag = v.paginas[j];
      }
      if (!pag) return;
      var grilla = pag.querySelector(".album__grilla");
      var card = grilla && grilla.querySelector(".album__ficha");
      var img = card && card.querySelector("img");
      if (!img || !img.offsetWidth || !img.offsetHeight) return;

      /* Se mide contra el alto que manda el CSS, no contra el que ya se
         ajustó: si no, cada medición achicaría el pliego un poco más. */
      alb.style.removeProperty("--alto");
      void pant.offsetHeight;

      var cs = getComputedStyle(pag);
      var cromo = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom);
      var cab = pag.querySelector(".album__cab");
      if (cab && cab.offsetHeight) {
        cromo += cab.offsetHeight + (parseFloat(getComputedStyle(cab).marginBottom) || 0);
      }
      var pie = pag.querySelector(".album__pie");
      if (pie && pie.offsetHeight) {
        cromo += pie.offsetHeight + (parseFloat(getComputedStyle(pie).marginTop) || 0);
      }
      var alto = pag.clientHeight - cromo;

      var gs = getComputedStyle(grilla);
      var col = (gs.gridTemplateColumns || "").trim().split(/\s+/).length;
      if (col < 1) return;
      var filas = Math.ceil(grilla.children.length / col) || 1;
      var ritmoF = parseFloat(gs.rowGap) || 0;
      var altFicha = (alto - ritmoF * (filas - 1)) / filas;

      /* De la ficha ya dibujada se saca todo lo que no es la foto
         (borde, relleno y pie) y la proporción real de la imagen. */
      var ratio = img.offsetHeight / img.offsetWidth;
      var resto = card.offsetHeight - img.offsetHeight;
      var lado = card.offsetWidth - img.offsetWidth;
      var fig = (altFicha - resto) / ratio + lado;

      var ancho = pag.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      var tope = (ancho - (parseFloat(gs.columnGap) || 0) * (col - 1)) / col;
      if (tope > 0) fig = Math.min(fig, tope);
      if (!isFinite(fig) || fig < 24) return;

      var altReal = (fig - lado) * ratio + resto;
      var altoNecesario = altReal * filas + ritmoF * (filas - 1) + cromo;
      alb.style.setProperty("--fig", fig.toFixed(1) + "px");
      alb.style.setProperty("--alto", Math.max(altoNecesario, 352).toFixed(1) + "px");
      figLista = true;
    }

    function pintarBarra() {
      var v = vistas[i];
      if (!v) return;
      if (nom) nom.textContent = titulo(v);
      if (num) num.textContent = (i + 1) + " / " + vistas.length;
      if (ant) ant.disabled = i === 0;
      if (sig) sig.disabled = i >= vistas.length - 1;
      if (rango && String(i + 1) !== rango.value) rango.value = i + 1;
      if (punto) {
        var c = "";
        v.paginas.forEach(function (p) {
          if (c || !p || !p.style || !p.style.getPropertyValue) return;
          c = p.style.getPropertyValue("--sede");
        });
        // Si el pliego no tiene color (portada, índice, cierre) se saca la
        // propiedad: dejarla vacía anularía el color de relleno del CSS.
        if (c) punto.style.setProperty("--sede", c);
        else punto.style.removeProperty("--sede");
      }
      if (ir) {
        var propio = "";
        Object.keys(primera).forEach(function (s) {
          if (propio) return;
          if (v.paginas.indexOf(pags[primera[s]]) >= 0) propio = s;
        });
        ir.value = propio ? String(primera[propio]) : "";
      }
    }

    /* Marca la vista que se está mirando. La que viene puede estar
       asomando debajo mientras la hoja gira, pero eso lo maneja
       abrirGiro: acá sólo se limpia. */
    function pintar() {
      if (!vistas.length) return;
      if (!vistas[mostrada]) mostrada = 0;
      alistar(mostrada - 1);
      alistar(mostrada);
      alistar(mostrada + 1);
      vistas.forEach(function (x, n) {
        var ves = n === mostrada;
        x.v.classList.toggle("es-actual", ves);
        x.v.classList.remove("es-debajo");
        x.v.setAttribute("aria-hidden", ves ? "false" : "true");
      });
      pintarBarra();
      marcarVista(vistas[mostrada]);
      ajustarFig();
    }

    /* ---- pasaje de hojas ------------------------------------------------
       La hoja gira alrededor del lomo, con el mouse o el dedo si se la
       agarra y se la arrastra. El dorso de la hoja que gira lleva la
       página que viene y, debajo, ya asoma el resto del pliego que viene:
       al levantar la página se descubre lo que hay atrás, como en un
       libro de verdad. La vista no cambia hasta que la hoja terminó. */
    var giros = { dir: null, n: -1, hoja: null, origen: null, hijo: null,
                  bajo: -1, ang: 0, p: 0, anim: null };
    var mostrada = 0;      // vista que se está mirando
    var trago = false;     // hubo un arrastre: el clic que sigue no cuenta

    function abrirGiro(n, dir) {
      if (n < 0 || n >= vistas.length) return false;
      var v = vistas[mostrada], w = vistas[n];
      var ladoGira = doble ? (dir === "adelante" ? 1 : 0) : 0;
      var ladoViaje = doble ? (dir === "adelante" ? 0 : 1) : 0;
      var hoja = v.hojas[ladoGira];
      var dorso = hoja.querySelector(".album__cara--atras");
      var frente = w.hojas[ladoViaje].querySelector(".album__cara--frente");
      if (!hoja || !dorso || !frente || !frente.firstElementChild) return false;
      /* En doble página lo que se descubre es el pliego que viene, con
         la hoja que viaja ya vacía. En hoja sola viaja la página entera,
         así que debajo queda la que sigue a la del dorso. */
      var bajo = doble ? n : n + (dir === "adelante" ? 1 : -1);
      if (bajo < 0 || bajo >= vistas.length) bajo = -1;
      giros = {
        dir: dir, n: n, hoja: hoja, origen: dorso, hijo: frente,
        bajo: bajo, ang: 0, p: 0, anim: null
      };
      dorso.appendChild(frente.firstElementChild);
      hoja.style.transformOrigin = dir === "adelante" ? "left center" : "right center";
      hoja.classList.add("girando");
      if (bajo >= 0) {
        alistar(bajo);
        vistas[bajo].v.classList.add("es-debajo");
      }
      return true;
    }

    /* La hoja no gira rígida: se dobla un toque al medio del recorrido,
       como una hoja de papel que alguien levanta de la esquina. El
       doblez va y viene solo, así que en los extremos queda plana. */
    function transformar(grados) {
      var doblez = Math.sin(grados * Math.PI / 180);
      var lado = grados < 0 ? -1 : 1;
      return "rotateY(" + grados + "deg)"
        + " skewY(" + (lado * doblez * 2.4).toFixed(2) + "deg)"
        + " rotateX(" + (doblez * 2.1).toFixed(2) + "deg)";
    }

    function ponerAngulo(grados, ms) {
      var g = giros;
      if (!g.hoja) return;
      var de = g.ang;
      g.ang = grados;
      // La luz y la sombra de la hoja siguen el doblez (0 en los extremos,
      // 1 justo al medio): el CSS lee --giro.
      g.hoja.style.setProperty(
        "--giro", Math.abs(Math.sin(grados * Math.PI / 180)).toFixed(3));
      if (g.anim) { try { g.anim.cancel(); } catch (e) {} g.anim = null; }
      if (!ms || !g.hoja.animate) {
        g.hoja.style.transform = transformar(grados);
        return null;
      }
      // Tres tiempos para que el doblez aparezca y se aplane adentro
      // del movimiento: si fuera de a dos la hoja se iría torcida.
      var anim = g.hoja.animate(
        [{ transform: transformar(de) },
         { transform: transformar((de + grados) / 2), offset: 0.5 },
         { transform: transformar(grados) }],
        { duration: ms, easing: "cubic-bezier(.32,.72,.3,1)", fill: "forwards" });
      g.anim = anim;
      return anim;
    }

    /* Devuelve la página que prestó, saca las marcas de giro y, si
       cerró, recién ahí se pasa a la vista que viene. Se llama también
       si se salta de página a mitad de un giro: ahí no se avanza. */
    function finalizar(cerrar) {
      if (reloj) { clearTimeout(reloj); reloj = null; }
      var g = giros;
      giros = { dir: null, n: -1, hoja: null, origen: null, hijo: null,
                bajo: -1, ang: 0, p: 0, anim: null };
      if (g.anim) { try { g.anim.cancel(); } catch (e) {} }
      if (g.hoja) {
        g.hoja.style.transform = "";
        g.hoja.style.transformOrigin = "";
        g.hoja.style.removeProperty("--giro");
        g.hoja.classList.remove("girando");
      }
      if (g.origen && g.origen.firstElementChild) {
        g.hijo.appendChild(g.origen.firstElementChild);
      }
      if (g.bajo >= 0 && vistas[g.bajo]) vistas[g.bajo].v.classList.remove("es-debajo");
      if (cerrar && g.n >= 0) { mostrada = g.n; i = g.n; }
      if (vistas.length) pintar();
    }

    function irA(n, dir) {
      n = Math.max(0, Math.min(vistas.length - 1, n));
      finalizar(false);
      if (n === i) return;
      dir = dir || (n > i ? "adelante" : "atras");
      alb.dataset.dir = dir;
      i = n;
      pintarBarra();
      if (!anima || !abrirGiro(n, dir)) { mostrada = i; pintar(); return; }
      ponerAngulo(dir === "adelante" ? -180 : 180, GIRO);
      var fin = function () { finalizar(true); };
      if (giros.anim) giros.anim.onfinish = fin;
      reloj = setTimeout(fin, GIRO + 160);
    }

    /* Arrastre: se agarra la hoja y se la lleva con el mouse o el dedo.
       Si llega más de la mitad del camino, la hoja termina de pasar;
       si no, vuelve para atrás. */
    var arr = null;
    function anchoPliego() {
      return (pant.getBoundingClientRect().width || 640);
    }
    pant.addEventListener("pointerdown", function (e) {
      if (e.button !== undefined && e.button !== 0) return;
      if (e.target.closest && e.target.closest("button, a, select, input, .fig")) return;
      if (giros.hoja) return;
      arr = { id: e.pointerId, x0: e.clientX, y0: e.clientY, activo: false, dir: null };
    });
    pant.addEventListener("pointermove", function (e) {
      if (!arr || e.pointerId !== arr.id) return;
      var dx = e.clientX - arr.x0, dy = e.clientY - arr.y0;
      if (!arr.activo) {
        if (Math.abs(dx) < 14 || Math.abs(dx) < Math.abs(dy)) return;
        var dir = dx < 0 ? "adelante" : "atras";
        var hacia = mostrada + (dir === "adelante" ? 1 : -1);
        if (!abrirGiro(hacia, dir)) { arr = null; return; }
        arr.activo = true;
        arr.dir = dir;
        if (pant.setPointerCapture) {
          try { pant.setPointerCapture(e.pointerId); } catch (err) {}
        }
      }
      var p = Math.min(1, Math.abs(dx) / (anchoPliego() * (doble ? .42 : .55)));
      giros.p = p;
      ponerAngulo((arr.dir === "adelante" ? -180 : 180) * p, 0);
      if (e.cancelable) e.preventDefault();
    });
    function soltar(e) {
      if (!arr || (e && e.pointerId !== arr.id)) return;
      var a = arr; arr = null;
      if (!a.activo) return;
      /* El clic que cierra el arrastre no debe abrir el visor: se lo
         traga un instante, nada más. */
      trago = true;
      setTimeout(function () { trago = false; }, 260);
      var p = giros.p || 0;
      var pasar = p > .45;
      var ms = Math.max(200, Math.round(GIRO * (pasar ? 1 - p : .35 + p)));
      ponerAngulo(pasar ? (a.dir === "adelante" ? -180 : 180) : 0, ms);
      var fin = function () { finalizar(pasar); };
      if (giros.anim) giros.anim.onfinish = fin;
      reloj = setTimeout(fin, ms + 160);
    }
    pant.addEventListener("pointerup", soltar);
    pant.addEventListener("pointercancel", soltar);
    /* El clic que cierra un arrastre no debe abrir el visor de fotos. */
    pant.addEventListener("click", function (e) {
      if (!trago) return;
      trago = false;
      e.stopPropagation();
      e.preventDefault();
    }, true);

    Array.prototype.forEach.call(alb.querySelectorAll("[data-paso]"), function (b) {
      b.addEventListener("click", function () {
        irA(i + parseInt(b.dataset.paso, 10));
      });
    });
    alb.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest("[data-ir]") : null;
      if (!b || !alb.contains(b)) return;
      e.preventDefault();
      var pag = parseInt(b.getAttribute("data-ir"), 10) || 0;
      irA(vistaDe[pag] != null ? vistaDe[pag] : 0);
    });
    if (rango) rango.addEventListener("input", function () {
      irA(parseInt(rango.value, 10) - 1);
    });
    if (ir) ir.addEventListener("change", function () {
      if (!ir.value) return;
      var pag = parseInt(ir.value, 10);
      if (vistaDe[pag] != null) irA(vistaDe[pag]);
    });

    document.addEventListener("keydown", function (e) {
      if (dlg.open) return;
      var t = e.target;
      if (t && /^(INPUT|SELECT|TEXTAREA|BUTTON)$/.test(t.tagName)) return;
      if (e.key === "ArrowRight") { e.preventDefault(); irA(i + 1, "adelante"); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); irA(i - 1, "atras"); }
      else if (e.key === "Home") { e.preventDefault(); irA(0, "atras"); }
      else if (e.key === "End") { e.preventDefault(); irA(vistas.length - 1, "adelante"); }
    });

    /* Al cambiar de ancho se vuelve a armar: el mismo álbum, pero con
       una o dos hojas por pliego. Se conserva la página que se miraba. */
    window.addEventListener("resize", function () {
      if (espera) clearTimeout(espera);
      espera = setTimeout(function () {
        espera = null;
        var quiere = !window.matchMedia || malla("(min-width: 46rem)");
        if (quiere !== doble) {
          var abierta = vistas[mostrada].paginas.filter(Boolean)[0] || pags[0];
          var cual = pags.indexOf(abierta);
          armar();
          i = vistaDe[cual] != null ? vistaDe[cual] : 0;
          mostrada = i;
          pintar();
        }
        ajustarFig(true);
      }, 240);
    });

    anima = malla("(prefers-reduced-motion: no-preference)");
    armar();
    if (rango) rango.max = vistas.length;
    pintar();
    pintarProgreso();
  })();
})();

/* ------------------------------------------------------------------
   Barra de secciones: marca la sección activa con aria-current y, si
   la fila no entra en la pantalla, la deja deslizable en horizontal
   (el CSS dibuja los degradados de los costados con data-desborde).
   En las páginas de artículo se toma la sección desde el pie de firma.
   ------------------------------------------------------------------ */
(function nav() {
  "use strict";
  var lista = document.querySelector(".nav-ed__lista");
  if (!lista) return;
  var enlaces = Array.prototype.slice.call(lista.querySelectorAll("a[data-sec]"));
  if (!enlaces.length) return;

  function ruta(u) {
    try {
      return new URL(u, location.href).pathname
        .replace(/\/index\.html$/, "/").replace(/\/+$/, "");
    } catch (e) { return ""; }
  }

  var aqui = ruta(location.pathname);
  var cual = null;
  enlaces.forEach(function (a) {
    if (ruta(a.getAttribute("href")) === aqui) cual = a;
  });
  if (!cual) {
    var meta = document.querySelector(".articulo__meta a[href*='secciones/']");
    if (meta) {
      var sec = ruta(meta.getAttribute("href"));
      enlaces.forEach(function (a) {
        if (ruta(a.getAttribute("href")) === sec) cual = a;
      });
    }
  }
  if (cual) cual.setAttribute("aria-current", "page");

  function medir() {
    if (lista.scrollWidth - lista.clientWidth > 4) {
      lista.setAttribute("data-desborde", "1");
    } else {
      lista.removeAttribute("data-desborde");
      lista.scrollLeft = 0;
    }
  }
  medir();
  /* la sección activa queda a la vista, sin mover la página */
  if (cual) {
    lista.scrollLeft = cual.offsetLeft - (lista.clientWidth - cual.offsetWidth) / 2;
  }
  var reloj = null;
  window.addEventListener("resize", function () {
    if (reloj) clearTimeout(reloj);
    reloj = setTimeout(function () { reloj = null; medir(); }, 180);
  });
})();

/* ============ Herramientas de accesibilidad ============
   Un botón fijo abre un panel con ajustes que el lector prende o
   apaga: tamaño de letra, contraste alto, modo nocturno, enlaces
   subrayados, movimiento calmo y letras más claras para dislexia.
   Cada ajuste se guarda en localStorage y un script chico del
   <head> lo reaplica antes del primer pintado, así no hay
   destello del tema anterior al entrar en la página. */
(function () {
  "use strict";
  if (!document.body) return;

  var CLAVE = "rev.acc";
  var ESCALAS = [
    { v: "90",  txt: "A\u2212" },
    { v: "",    txt: "Normal" },
    { v: "112", txt: "A+" },
    { v: "125", txt: "A++" },
    { v: "140", txt: "A+++" }
  ];
  var AJUSTES = [
    { k: "escala",     etq: "Tamaño de letra",     tipo: "escala" },
    { k: "contraste",  etq: "Contraste alto",      v: "1" },
    { k: "tema",       etq: "Modo nocturno",       v: "oscuro" },
    { k: "subrayar",   etq: "Enlaces subrayados",  v: "1" },
    { k: "calma",      etq: "Movimiento calmo",    v: "1" },
    { k: "dislexia",   etq: "Letras más claras",   v: "1" },
    { k: "mayusculas", etq: "Textos en mayúsculas", v: "1" },
    { k: "voz",        etq: "Leer en voz alta",    v: "1" }
  ];

  function leer() {
    try { return JSON.parse(localStorage.getItem(CLAVE) || "{}"); }
    catch (e) { return {}; }
  }
  var estado = leer();

  function guardar() {
    try { localStorage.setItem(CLAVE, JSON.stringify(estado)); }
    catch (e) {}
  }

  function aplicar() {
    var h = document.documentElement, i, v;
    for (i = 0; i < AJUSTES.length; i++) {
      v = estado[AJUSTES[i].k] || "";
      if (v) h.setAttribute("data-" + AJUSTES[i].k, v);
      else h.removeAttribute("data-" + AJUSTES[i].k);
    }
  }

  function boton(k, v, txt, escala) {
    return '<button type="button" class="acc__t' +
      (escala ? " acc__t--escala" : " acc__t--fila") + '" data-k="' + k +
      '" data-v="' + v + '" aria-pressed="false">' + txt + "</button>";
  }

  function grupo(a) {
    var i, h;
    if (a.tipo === "escala") {
      h = '<span class="acc__etq" id="acc-etq-' + a.k + '">' + a.etq +
        '</span><div class="acc__fila" role="group" aria-labelledby="acc-etq-' +
        a.k + '">';
      for (i = 0; i < ESCALAS.length; i++) {
        h += boton(a.k, ESCALAS[i].v, ESCALAS[i].txt, true);
      }
      return h + "</div>";
    }
    /* Los demás son una fila entera: nombre a la izquierda y el
       estado a la derecha, para que se lea prendido/apagado */
    return boton(a.k, a.v, a.etq + '<span class="acc__estado">Apagado</span>', false);
  }

  var html = '<button type="button" class="acc__btn" aria-expanded="false"' +
    ' aria-controls="acc-panelo" aria-label="Herramientas de accesibilidad">' +
    '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"' +
    ' focusable="false"><circle cx="12" cy="4.3" r="2.1"/>' +
    '<path d="M3.6 8.3h16.8M12 8.3v6.5M12 14.8l-3.5 6.5M12 14.8l3.5 6.5"' +
    ' fill="none" stroke="currentColor" stroke-width="2"' +
    ' stroke-linecap="round" stroke-linejoin="round"/></svg></button>' +
    '<div class="acc__panelo" id="acc-panelo" role="group"' +
    ' aria-label="Herramientas de accesibilidad" hidden>' +
    '<p class="acc__titulo">Accesibilidad</p>';
  var i;
  for (i = 0; i < AJUSTES.length; i++) html += grupo(AJUSTES[i]);
  html += '<div class="acc__fila"><button type="button"' +
    ' class="acc__t acc__t--reset" data-reset="1">Restablecer todo' +
    "</button></div></div>";

  var cont = document.createElement("div");
  cont.className = "acc";
  cont.innerHTML = html;
  document.body.appendChild(cont);

  var btn = cont.querySelector(".acc__btn");
  var panelo = cont.querySelector(".acc__panelo");

  /* "Normal" es el único con data-v vacío: prendido cuando no hay
     escala guardada, y al apagarlo se borra el atributo. */
  function sincronizar() {
    var bs = cont.querySelectorAll("[data-k]"), n, b, k, v, on, est;
    for (n = 0; n < bs.length; n++) {
      b = bs[n];
      k = b.getAttribute("data-k");
      v = b.getAttribute("data-v");
      on = v === "" ? !estado[k] : estado[k] === v;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      est = b.querySelector(".acc__estado");
      if (est) est.textContent = on ? "Prendido" : "Apagado";
    }
  }

  function abrir(si) {
    panelo.hidden = !si;
    btn.setAttribute("aria-expanded", si ? "true" : "false");
    if (si) {
      var on = panelo.querySelector('[aria-pressed="true"]') ||
        panelo.querySelector("[data-k]");
      if (on) on.focus();
    } else {
      btn.focus();
    }
  }

  cont.addEventListener("click", function (ev) {
    var b = ev.target.closest ? ev.target.closest("[data-k],[data-reset]") : null;
    if (!b || !cont.contains(b)) return;
    if (b.hasAttribute("data-reset")) {
      estado = {};
    } else {
      var k = b.getAttribute("data-k");
      var v = b.getAttribute("data-v");
      if (estado[k] === v) delete estado[k];
      else estado[k] = v;
    }
    aplicar();
    sincronizar();
    guardar();
    /* los demás módulos (lectura en voz alta) escuchan este aviso */
    if (document.dispatchEvent) {
      document.dispatchEvent(new CustomEvent("rev:acc", { detail: estado }));
    }
  });

  btn.addEventListener("click", function () { abrir(panelo.hidden); });

  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape" && !panelo.hidden) abrir(false);
  });

  document.addEventListener("click", function (ev) {
    if (!panelo.hidden && !cont.contains(ev.target)) abrir(false);
  });

  aplicar();
  sincronizar();
})();

/* ============ Lectura en voz alta ============
   Se prende desde la barra de accesibilidad ("Leer en voz alta").
   Toma los bloques legibles de la página, los lee uno por uno con
   la voz del navegador y pinta el bloque que está sonando: así
   quien no puede seguir con los ojos igual sabe dónde va el texto.
   El panel flota abajo a la izquierda, del lado opuesto a la
   barra de accesibilidad, para no pisarse. */
(function () {
  "use strict";
  var CLAVE = "rev.acc";
  var CLAVE_VOZ = "rev.voz";

  /* Navegador sin Web Speech: el interruptor no tiene sentido,
     se borra del panel y no se ofrece nada que no funcione. */
  if (!("speechSynthesis" in window) || typeof SpeechSynthesisUtterance === "undefined") {
    var mord = document.querySelector('.acc [data-k="voz"]');
    if (mord && mord.parentNode) mord.parentNode.removeChild(mord);
    return;
  }

  function leerJSON(clave, porDefecto) {
    try { return JSON.parse(localStorage.getItem(clave) || "null") || porDefecto; }
    catch (e) { return porDefecto; }
  }

  var bloques = [];
  var actual = -1;
  var corriendo = false;
  var pausado = false;
  var activo = false;
  var gen = 0;              /* invalida los onend de un ciclo viejo */
  var voces = [];
  var vozElegida = leerJSON(CLAVE_VOZ, null);
  var relojCromo = null;
  var fallos = 0;

  function texto(el) {
    return (el.textContent || "").replace(/\s+/g, " ").trim();
  }

  /* Ruido que no aporta al oído: firma, fecha, "volver", rótulos */
  function sirve(el) {
    return !el.closest(".articulo__meta, .articulo__fin, .articulo__sec, .salto, .masthead, .pie, .volver, .todos__enlace, .sumario__item");
  }

  function reunir() {
    var cuerpo = document.querySelector(".articulo__cuerpo");
    var sel = cuerpo
      ? ".articulo__cuerpo > p, .articulo__cuerpo > h2, .articulo__cuerpo > h3," +
        " .articulo__cuerpo > h4, .articulo__cuerpo > blockquote," +
        " .articulo__cuerpo > ul, .articulo__cuerpo > ol," +
        " .articulo__cuerpo > figure figcaption"
      : "main h1, main h2, main h3, main h4, main p, main figcaption, main li";
    var lista = document.querySelectorAll(sel), i, out = [];
    for (i = 0; i < lista.length; i++) {
      if (texto(lista[i]) && sirve(lista[i])) out.push(lista[i]);
    }
    return out;
  }

  /* ---------- panel flotante ---------- */
  var voz = document.createElement("div");
  voz.className = "voz";
  voz.hidden = true;
  voz.innerHTML =
    '<p class="voz__cab"><span>Leer en voz alta</span>' +
    '<span class="voz__n" data-n>0 / 0</span></p>' +
    '<div class="voz__fila">' +
    '<button type="button" class="acc__t voz__b" data-act="ant" aria-label="Parte anterior">&lsaquo;</button>' +
    '<button type="button" class="acc__t voz__b voz__prin" data-act="play" aria-label="Empezar a leer">&#9654;</button>' +
    '<button type="button" class="acc__t voz__b" data-act="sig" aria-label="Parte siguiente">&rsaquo;</button>' +
    '<button type="button" class="acc__t voz__b" data-act="stop" aria-label="Detener la lectura">&#9632;</button>' +
    '<select class="voz__voz" data-voz aria-label="Voz para leer"></select>' +
    '</div>';
  document.body.appendChild(voz);

  var bPlay = voz.querySelector('[data-act="play"]');
  var bAnt = voz.querySelector('[data-act="ant"]');
  var bSig = voz.querySelector('[data-act="sig"]');
  var bStop = voz.querySelector('[data-act="stop"]');
  var caja = voz.querySelector("[data-n]");
  var selVoz = voz.querySelector("[data-voz]");

  function cuenta() {
    caja.textContent = (actual >= 0 ? actual + 1 : 0) + " / " + bloques.length;
  }

  function marcar() {
    var i, previo = voz.querySelectorAll(".voz-leyendo");
    for (i = 0; i < previo.length; i++) previo[i].classList.remove("voz-leyendo");
    if (actual < 0 || !bloques[actual]) { cuenta(); return; }
    var el = bloques[actual];
    el.classList.add("voz-leyendo");
    var r = el.getBoundingClientRect();
    var lejos = r.top < 8 || r.bottom > window.innerHeight - 8;
    if (lejos) {
      var calmo = document.documentElement.hasAttribute("data-calma");
      try {
        el.scrollIntoView({ block: "center", behavior: calmo ? "auto" : "smooth" });
      } catch (e) { el.scrollIntoView(); }
    }
    cuenta();
  }

  function icono_play(si) {
    bPlay.innerHTML = si ? "&#10074;&#10074;" : "&#9654;";
    bPlay.setAttribute("aria-label", si ? "Pausar la lectura" : "Empezar a leer");
    bPlay.setAttribute("aria-pressed", si ? "true" : "false");
  }

  /* Chrome pausa la síntesis después de un rato: un refresco
     periódico mientras se está leyendo lo mantiene despierto */
  function despertar() {
    if (relojCromo) clearInterval(relojCromo);
    relojCromo = setInterval(function () {
      if (!corriendo) { clearInterval(relojCromo); relojCromo = null; return; }
      if (!speechSynthesis.paused) speechSynthesis.resume();
    }, 9000);
  }

  function decir(i) {
    if (!corriendo) return;
    if (i < 0 || i >= bloques.length) { detener(); return; }
    actual = i;
    marcar();
    var miGen = gen;
    var u = new SpeechSynthesisUtterance(texto(bloques[i]));
    u.lang = (vozElegida && vozElegida.lang) || "es-AR";
    if (vozElegida) u.voice = vozElegida;
    u.rate = 1;
    u.pitch = 1;
    /* una frase que arranca bien reinicia el conteo de fallos */
    u.onstart = function () { fallos = 0; };
    u.onend = function () {
      if (miGen !== gen || !corriendo) return;
      decir(i + 1);
    };
    u.onerror = function (ev) {
      if (miGen !== gen || !corriendo) return;
      var r = ev && ev.error;
      /* "interrupted"/"canceled" son nuestras propias órdenes de
         parar: no cuentan como fallo de la voz */
      if (r === "interrupted" || r === "canceled" || r === "aborted") return;
      fallos++;
      if (fallos >= 2) { detener("No se pudo leer en voz alta"); return; }
      if (i + 1 < bloques.length) decir(i + 1); else detener();
    };
    speechSynthesis.speak(u);
  }

  function arrancar(desde) {
    if (!bloques.length) bloques = reunir();
    if (!bloques.length) return;
    corriendo = true;
    pausado = false;
    gen++;
    fallos = 0;
    speechSynthesis.cancel();
    icono_play(true);
    despertar();
    decir(typeof desde === "number" ? desde : (actual >= 0 ? actual : 0));
  }

  function pausar() {
    if (corriendo) {
      speechSynthesis.pause();
      pausado = true;
      corriendo = false;
      icono_play(false);
    } else if (pausado) {
      speechSynthesis.resume();
      pausado = false;
      corriendo = true;
      icono_play(true);
      /* si el navegador se comió la frase mientras estaba en pausa,
         seguimos por la siguiente */
      if (!speechSynthesis.speaking) decir(actual + 1);
      else despertar();
    }
  }

  function detener(msg) {
    gen++;
    corriendo = false;
    pausado = false;
    fallos = 0;
    speechSynthesis.cancel();
    if (relojCromo) { clearInterval(relojCromo); relojCromo = null; }
    icono_play(false);
    actual = -1;
    marcar();
    if (msg) caja.textContent = msg;
  }

  function irA(i) {
    if (i < 0 || i >= bloques.length) return;
    if (corriendo || pausado) {
      arrancar(i);
    } else {
      actual = i;
      marcar();
    }
  }

  /* ---------- voces ---------- */
  function rellenar() {
    var i, op, actualSel = vozElegida ? vozElegida.name : null;
    selVoz.innerHTML = "";
    if (!voces.length) {
      selVoz.hidden = true;
      return;
    }
    selVoz.hidden = false;
    for (i = 0; i < voces.length; i++) {
      op = document.createElement("option");
      op.value = String(i);
      op.textContent = (voces[i].name || "Voz " + (i + 1)).replace(/\s*\(.*?\)\s*$/, "");
      if (actualSel && voces[i].name === actualSel) op.selected = true;
      selVoz.appendChild(op);
    }
    if (!actualSel) {
      vozElegida = voces[0];
      selVoz.value = "0";
    }
  }

  function cargarVoces() {
    var todas = speechSynthesis.getVoices() || [], i, es = [];
    for (i = 0; i < todas.length; i++) {
      if (/^es/i.test(todas[i].lang)) es.push(todas[i]);
    }
    /* si el sistema no trae castellano, mostramos lo que haya:
       el navegador igual puede sintetizar con lang es-AR */
    voces = es.length ? es : todas;
    if (vozElegida) {
      var esta = false;
      for (i = 0; i < voces.length; i++) if (voces[i].name === vozElegida.name) esta = true;
      if (!esta) vozElegida = voces[0] || null;
    } else {
      vozElegida = voces[0] || null;
    }
    rellenar();
  }

  if (typeof speechSynthesis.addEventListener === "function") {
    speechSynthesis.addEventListener("voiceschanged", cargarVoces);
  }
  cargarVoces();

  selVoz.addEventListener("change", function () {
    var n = parseInt(selVoz.value, 10);
    vozElegida = voces[n] || null;
    try { localStorage.setItem(CLAVE_VOZ, JSON.stringify(vozElegida ? vozElegida.name : null)); }
    catch (e) {}
    if (corriendo || pausado) arrancar(actual >= 0 ? actual : 0);
  });

  /* ---------- controles ---------- */
  voz.addEventListener("click", function (ev) {
    var b = ev.target.closest ? ev.target.closest("[data-act]") : null;
    if (!b) return;
    var a = b.getAttribute("data-act");
    if (a === "play") {
      if (corriendo || pausado) pausar();
      else arrancar(actual >= 0 ? actual : 0);
    }
    else if (a === "stop") detener();
    else if (a === "ant") irA(Math.max(0, (actual >= 0 ? actual : 0) - 1));
    else if (a === "sig") irA(Math.min(bloques.length - 1, (actual >= 0 ? actual : 0) + 1));
  });

  /* Saltar a un párrafo con el mouse mientras se escucha. Los enlaces
     y botones del texto siguen siendo enlaces y botones. */
  document.addEventListener("click", function (ev) {
    if (!activo || !corriendo) return;
    var t = ev.target;
    if (!t.closest) return;
    if (t.closest("a, button, select, input, textarea, label")) return;
    var el = t.closest("p, h1, h2, h3, h4, li, blockquote, figcaption");
    if (!el) return;
    var i = bloques.indexOf(el);
    if (i >= 0) { ev.preventDefault(); irA(i); }
  });

  /* ---------- encendido desde la barra de accesibilidad ---------- */
  function encender() {
    activo = true;
    voz.hidden = false;
    bloques = reunir();
    actual = -1;
    cuenta();
    if (bPlay) bPlay.focus();
  }

  function apagar() {
    activo = false;
    detener();
    voz.hidden = true;
  }

  document.addEventListener("rev:acc", function (ev) {
    var on = !!(ev.detail && ev.detail.voz === "1");
    if (on === activo) return;
    if (on) encender(); else apagar();
  });

  /* Al entrar con la preferencia guardada se muestra el panel, pero
     no se habla solo: los navegadores cortan la voz sin un gesto. */
  if (leerJSON(CLAVE, {}).voz === "1") {
    activo = true;
    voz.hidden = false;
    bloques = reunir();
    cuenta();
  }
})();

/* ------------------------------------------------------------------ */
/* Galería deslizable: <figure class="slides" data-slides>             */
/* ------------------------------------------------------------------ */
(function () {
  var figs = document.querySelectorAll("[data-slides]");
  if (!figs.length) return;

  Array.prototype.forEach.call(figs, function (fig) {
    var img = fig.querySelector("[data-slides-img]");
    var num = fig.querySelector("[data-slides-num]");
    var datos = fig.querySelector("[data-slides-datos]");
    var prev = fig.querySelector(".slides__nav--prev");
    var next = fig.querySelector(".slides__nav--next");
    if (!img || !datos) return;

    var fotos;
    try { fotos = JSON.parse(datos.textContent || "[]"); } catch (e) { return; }
    if (!fotos.length) return;

    var total = fotos.length;
    var actual = 0;
    var cache = {};

    function precargar(n) {
      n = ((n % total) + total) % total;
      var f = fotos[n];
      if (cache[f]) return;
      cache[f] = 1;
      var p = new Image();
      p.src = f;
    }

    function pintar(n) {
      actual = ((n % total) + total) % total;
      var f = fotos[actual];
      if (num) num.textContent = (actual + 1) + " / " + total;
      precargar(actual + 1);
      precargar(actual - 1);
      if (img.getAttribute("src") === f) return;
      img.setAttribute("data-cambiando", "1");
      var prox = new Image();
      prox.onload = function () {
        img.src = f;
        img.removeAttribute("data-cambiando");
      };
      prox.onerror = function () {
        img.src = f;
        img.removeAttribute("data-cambiando");
      };
      prox.src = f;
    }

    function ir(n) { pintar(n); }

    if (prev) prev.addEventListener("click", function () { ir(actual - 1); });
    if (next) next.addEventListener("click", function () { ir(actual + 1); });

    fig.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowLeft") { ir(actual - 1); ev.preventDefault(); }
      else if (ev.key === "ArrowRight") { ir(actual + 1); ev.preventDefault(); }
      else if (ev.key === "Home") { ir(0); ev.preventDefault(); }
      else if (ev.key === "End") { ir(total - 1); ev.preventDefault(); }
    });

    /* Deslizar con el dedo o el mouse */
    var x0 = null, y0 = null, activo = false;
    fig.addEventListener("pointerdown", function (ev) {
      if (ev.target.closest("button")) return;
      x0 = ev.clientX; y0 = ev.clientY; activo = true;
    });
    fig.addEventListener("pointerup", function (ev) {
      if (!activo) return;
      activo = false;
      if (x0 === null) return;
      var dx = ev.clientX - x0, dy = ev.clientY - y0;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) {
        ir(actual + (dx < 0 ? 1 : -1));
      }
      x0 = null;
    });
    fig.addEventListener("pointercancel", function () { activo = false; x0 = null; });

    precargar(1);
    if (num) num.textContent = "1 / " + total;
  });
})();

/* ============ Tutorial de navegación ============
   La primera vez que alguien entra, un cartel breve explica cómo
   moverse por la revista y dónde quedan las herramientas de
   accesibilidad. Se cierra con "Listo, a leer", con Escape o
   tocando afuera, y no vuelve a aparecer: queda anotado en
   localStorage. Para recuperarlo hay un enlace en el pie y un
   botón en el panel de accesibilidad. */
(function () {
  "use strict";
  if (!document.body) return;

  var CLAVE = "rev.tuto";
  var PASOS = [
    {
      t: "El menú de arriba",
      v: "<strong>Índice</strong> te devuelve siempre a esta portada. " +
         "Al lado están las secciones: Escuela, Ciencia y tecnología, " +
         "Territorio, Voces, Estudiantes, Cultura y Proyectos. " +
         "Al final, <strong>Egresados</strong>.",
      p: "En el celular, el menú se desliza de costado."
    },
    {
      t: "De la portada al artículo",
      v: "El <strong>sumario</strong> lista las secciones de la edición. " +
         "Adentro de cada una están los artículos, con fotos, audios y " +
         "videos. Al pie de cada artículo, <strong>Volver</strong> te deja " +
         "en la sección.",
      p: "¿Buscás algo puntual? Al final del sumario está el enlace con todos los artículos de la edición."
    },
    {
      t: "Si te cuesta leer",
      v: "El botón verde de la esquina —el símbolo de la persona— abre las " +
         "<strong>herramientas de accesibilidad</strong>: tamaño de letra, " +
         "contraste alto, modo nocturno, enlaces subrayados, movimiento " +
         "calmo, letras para dislexia, textos en mayúsculas y lectura en " +
         "voz alta.",
      p: "La revista recuerda tus ajustes la próxima vez que entres.",
      demo: true
    }
  ];

  var icono =
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"' +
    ' focusable="false"><circle cx="12" cy="4.3" r="2.1"/>' +
    '<path d="M3.6 8.3h16.8M12 8.3v6.5M12 14.8l-3.5 6.5M12 14.8l3.5 6.5"' +
    ' fill="none" stroke="currentColor" stroke-width="2"' +
    ' stroke-linecap="round" stroke-linejoin="round"/></svg>';

  var pasosHtml = "", puntosHtml = "", i;
  for (i = 0; i < PASOS.length; i++) {
    pasosHtml +=
      '<div class="tuto__paso" data-paso="' + i + '"' + (i ? " hidden" : "") + ">" +
      '<h3 class="tuto__h"><span class="tuto__num" aria-hidden="true">' + (i + 1) +
      "</span>" + PASOS[i].t + "</h3>" +
      '<p class="tuto__p" id="tuto-p-' + i + '">' + PASOS[i].v + "</p>" +
      (PASOS[i].demo
        ? '<p class="tuto__demo"><span class="tuto__demo-btn">' + icono +
          '</span><span>Herramientas de accesibilidad</span></p>'
        : "") +
      '<p class="tuto__pista">' + PASOS[i].p + "</p></div>";
    puntosHtml += '<span class="tuto__punto" data-punto="' + i + '"></span>';
  }

  var capa = document.createElement("div");
  capa.className = "tuto";
  capa.hidden = true;
  capa.innerHTML =
    '<div class="tuto__caja" role="dialog" aria-modal="true"' +
    ' aria-labelledby="tuto-t" tabindex="-1">' +
    '<button type="button" class="tuto__cerrar" aria-label="Cerrar el tutorial">' +
    '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"' +
    ' focusable="false"><path d="M6 6l12 12M18 6L6 18" fill="none"' +
    ' stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></button>' +
    '<p class="tuto__marca">La Revista del Rural</p>' +
    '<h2 class="tuto__t" id="tuto-t">Cómo navegar la revista</h2>' +
    '<div class="tuto__pasos">' + pasosHtml + "</div>" +
    '<div class="tuto__pie">' +
    '<span class="tuto__puntos" aria-hidden="true">' + puntosHtml + "</span>" +
    '<p class="tuto__prog" data-prog aria-live="polite">Paso 1 de ' + PASOS.length + "</p>" +
    '<span class="tuto__acciones">' +
    '<button type="button" class="tuto__b" data-nav="-1">Anterior</button>' +
    '<button type="button" class="tuto__b tuto__b--prin" data-nav="1">Siguiente</button>' +
    "</span></div></div>";
  document.body.appendChild(capa);

  var caja = capa.querySelector(".tuto__caja");
  var pasos = capa.querySelectorAll(".tuto__paso");
  var puntos = capa.querySelectorAll(".tuto__punto");
  var bAnt = capa.querySelector('[data-nav="-1"]');
  var bSig = capa.querySelector('[data-nav="1"]');
  var prog = capa.querySelector("[data-prog]");
  var actual = 0;
  var previo = null;

  function ir(n) {
    if (n < 0) n = 0;
    if (n > PASOS.length - 1) n = PASOS.length - 1;
    actual = n;
    for (var j = 0; j < pasos.length; j++) pasos[j].hidden = j !== n;
    for (j = 0; j < puntos.length; j++) {
      if (j === n) puntos[j].setAttribute("aria-current", "step");
      else puntos[j].removeAttribute("aria-current");
    }
    bAnt.disabled = n === 0;
    bSig.textContent = n === PASOS.length - 1 ? "Listo, a leer" : "Siguiente";
    prog.textContent = "Paso " + (n + 1) + " de " + PASOS.length;
    caja.setAttribute("aria-describedby", "tuto-p-" + n);
  }

  function abrir() {
    if (!capa.hidden) return;
    /* si el panel de accesibilidad estaba abierto, se cierra */
    var accBtn = document.querySelector(".acc__btn");
    if (accBtn && accBtn.getAttribute("aria-expanded") === "true") accBtn.click();
    previo = document.activeElement;
    capa.hidden = false;
    /* el fondo no se mueve mientras dura el tutorial */
    var ancho = window.innerWidth - document.documentElement.clientWidth;
    document.body.style.overflow = "hidden";
    if (ancho > 0) document.body.style.paddingRight = ancho + "px";
    ir(0);
    caja.focus();
  }

  function cerrar() {
    if (capa.hidden) return;
    capa.hidden = true;
    document.body.style.overflow = "";
    document.body.style.paddingRight = "";
    try { localStorage.setItem(CLAVE, "1"); } catch (e) {}
    try { sessionStorage.setItem(CLAVE, "1"); } catch (e) {}
    if (previo && previo.focus && document.contains(previo)) previo.focus();
  }

  function visto() {
    try { if (localStorage.getItem(CLAVE) === "1") return true; } catch (e) {}
    try { if (sessionStorage.getItem(CLAVE) === "1") return true; } catch (e) {}
    return false;
  }

  capa.addEventListener("click", function (ev) {
    var b = ev.target.closest ? ev.target.closest("[data-nav]") : null;
    if (b) {
      var d = parseInt(b.getAttribute("data-nav"), 10);
      if (d > 0 && actual === PASOS.length - 1) { cerrar(); return; }
      ir(actual + d);
      return;
    }
    if (ev.target === capa) cerrar();
  });
  capa.querySelector(".tuto__cerrar").addEventListener("click", cerrar);

  document.addEventListener("keydown", function (ev) {
    if (capa.hidden) return;
    if (ev.key === "Escape") { ev.preventDefault(); cerrar(); return; }
    if (ev.key !== "Tab") return;
    var f = caja.querySelectorAll('button:not([disabled]), [href], input,' +
      ' select, textarea, [tabindex]:not([tabindex="-1"])');
    if (!f.length) return;
    var prim = f[0], ult = f[f.length - 1];
    if (ev.shiftKey && (document.activeElement === prim || document.activeElement === caja)) {
      ev.preventDefault(); ult.focus();
    } else if (!ev.shiftKey && document.activeElement === ult) {
      ev.preventDefault(); prim.focus();
    }
  });

  /* lanzadores: enlace del pie y botón del panel de accesibilidad */
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest ? ev.target.closest("[data-tuto]") : null;
    if (!b) return;
    ev.preventDefault();
    abrir();
  });

  var panelo = document.querySelector(".acc__panelo");
  if (panelo) {
    var lanzador = document.createElement("button");
    lanzador.type = "button";
    lanzador.className = "acc__t acc__t--reset";
    lanzador.setAttribute("data-tuto", "1");
    lanzador.textContent = "Ver el tutorial";
    panelo.appendChild(lanzador);
  }

  /* ?tuto=1 permite volver a verlo sin borrar los datos del navegador */
  var forzar = /[?&]tuto=1(?:&|$)/.test(window.location.search);
  if (!visto() || forzar) {
    window.setTimeout(function () { abrir(); }, 700);
  }
})();
