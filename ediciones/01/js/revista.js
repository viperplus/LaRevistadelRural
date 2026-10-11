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

    var GIRO = 820;
    var vistas = [];     // { v, paginas, hojas }
    var vistaDe = [];    // número de página -> número de vista
    var primera = {};    // sede -> número de su primera página
    var doble = true;
    var anima = false;
    var i = 0;
    var reloj = null;
    var espera = null;

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

    function ponerAngulo(grados, ms) {
      var g = giros;
      if (!g.hoja) return;
      var de = g.ang;
      g.ang = grados;
      if (g.anim) { try { g.anim.cancel(); } catch (e) {} g.anim = null; }
      if (!ms || !g.hoja.animate) {
        g.hoja.style.transform = "rotateY(" + grados + "deg)";
        return null;
      }
      var anim = g.hoja.animate(
        [{ transform: "rotateY(" + de + "deg)" },
         { transform: "rotateY(" + grados + "deg)" }],
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
  })();
})();
