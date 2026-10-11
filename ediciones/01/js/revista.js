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
    var giro = null;
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
       página siguiente, igual que en un libro encuadernado.
       A partir de 46rem de ancho: ahí empieza el pasaje de hojas. En
       pantallas más angostas no hay doble página y la hoja entra con
       un barrido. */
    function armar() {
      finalizar();
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

    function pintar() {
      alistar(i - 1);
      alistar(i);
      alistar(i + 1);
      var v = vistas[i];
      vistas.forEach(function (x, n) {
        var ves = n === i;
        x.v.classList.toggle("es-actual", ves);
        x.v.setAttribute("aria-hidden", ves ? "false" : "true");
      });
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

    /* Devuelve a la hoja que prestó para el giro y saca las marcas de
       animación. Siempre se llama: también si se salta de página a
       mitad de un giro anterior. */
    function finalizar() {
      if (reloj) { clearTimeout(reloj); reloj = null; }
      if (!giro) return;
      var g = giro;
      giro = null;
      if (g.origen && g.origen.firstElementChild) {
        g.hijo.appendChild(g.origen.firstElementChild);
      }
      g.vieja.classList.remove("saliendo", "gira-adelante", "gira-atras");
      g.nueva.classList.remove("entrando");
    }

    function irA(n, dir) {
      n = Math.max(0, Math.min(vistas.length - 1, n));
      if (n === i) { pintar(); return; }
      finalizar();
      var vieja = vistas[i], nueva = vistas[n];
      dir = dir || (n > i ? "adelante" : "atras");
      alb.dataset.dir = dir;
      i = n;
      pintar();
      if (!anima) return;

      nueva.v.classList.add("entrando");
      var g = { vieja: vieja.v, nueva: nueva.v, origen: null, hijo: null };
      if (doble) {
        // Adelante gira la hoja derecha y en su dorso viaja la página
        // izquierda que viene; atrás gira la izquierda con la derecha.
        var lado = dir === "adelante" ? 1 : 0;
        var otro = dir === "adelante" ? 0 : 1;
        var dorso = vieja.hojas[lado].querySelector(".album__cara--atras");
        var frente = nueva.hojas[otro].querySelector(".album__cara--frente");
        if (dorso && frente && frente.firstElementChild) {
          dorso.appendChild(frente.firstElementChild);
          g.origen = dorso;
          g.hijo = frente;
        }
        vieja.v.classList.add("saliendo");
        vieja.v.classList.add(dir === "adelante" ? "gira-adelante" : "gira-atras");
        reloj = setTimeout(finalizar, GIRO);
      } else {
        reloj = setTimeout(finalizar, 440);
      }
      giro = g;
    }

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

    var x0 = null;
    alb.addEventListener("touchstart", function (e) {
      x0 = e.touches[0].clientX;
    }, { passive: true });
    alb.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      x0 = null;
      if (Math.abs(dx) < 45) return;
      irA(i + (dx < 0 ? 1 : -1), dx < 0 ? "adelante" : "atras");
    }, { passive: true });

    /* Al cambiar de ancho se vuelve a armar: el mismo álbum, pero con
       una o dos hojas por pliego. Se conserva la página que se miraba. */
    window.addEventListener("resize", function () {
      if (espera) clearTimeout(espera);
      espera = setTimeout(function () {
        espera = null;
        var quiere = !window.matchMedia || malla("(min-width: 46rem)");
        if (quiere === doble) return;
        var abierta = vistas[i].paginas.filter(Boolean)[0] || pags[0];
        var cual = pags.indexOf(abierta);
        armar();
        i = vistaDe[cual] != null ? vistaDe[cual] : 0;
        pintar();
      }, 240);
    });

    anima = malla("(prefers-reduced-motion: no-preference)");
    armar();
    if (rango) rango.max = vistas.length;
    pintar();
  })();
})();
