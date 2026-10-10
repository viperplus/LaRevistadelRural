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

  /* En el álbum solo se mira la página que se está viendo: las demás están
     ocultas y pasar de foto tendría que saltar de página también. */
  function a_la_vista(img) {
    var pag = img.closest(".album__pagina");
    return !pag || pag.classList.contains("es-actual");
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
  (function album() {
    var alb = document.querySelector(".album");
    if (!alb) return;
    var pags = Array.prototype.slice.call(alb.querySelectorAll(".album__pagina"));
    if (!pags.length) return;
    var total = pags.length;
    var ant = alb.querySelector('.album__btn[data-paso="-1"]');
    var sig = alb.querySelector('.album__btn[data-paso="1"]');
    var nom = alb.querySelector(".album__estado-t");
    var num = alb.querySelector(".album__estado-n");
    var punto = alb.querySelector(".album__punto");
    var rango = alb.querySelector(".album__rango");
    var ir = alb.querySelector(".album__ir");
    var i = 0;

    // Primera página de cada sede, para que el selector marque la que se ve.
    var inicios = {};
    pags.forEach(function (p, n) {
      if (p.dataset.sede && !(p.dataset.sede in inicios)) inicios[p.dataset.sede] = n;
    });

    function titulo(p) {
      if (p.classList.contains("album__pagina--portada")) return "Portada";
      if (p.classList.contains("album__pagina--fin")) return "Fin del álbum";
      var t = p.querySelector(".album__cab-t");
      return t ? t.textContent.replace(/\s+/g, " ").trim() : "";
    }

    function pintar() {
      var p = pags[i];
      pags.forEach(function (q, n) {
        var ves = n === i;
        q.classList.toggle("es-actual", ves);
        q.setAttribute("aria-hidden", ves ? "false" : "true");
      });
      if (nom) nom.textContent = titulo(p);
      if (num) num.textContent = (i + 1) + " / " + total;
      if (ant) ant.disabled = i === 0;
      if (sig) sig.disabled = i === total - 1;
      if (rango && String(i + 1) !== rango.value) rango.value = i + 1;
      if (punto) {
        var c = p.style && p.style.getPropertyValue ? p.style.getPropertyValue("--sede") : "";
        // Si la página no tiene color (portada, índice, cierre) se saca la
        // propiedad: dejarla vacía anularía el color de relleno del CSS.
        if (c) punto.style.setProperty("--sede", c);
        else punto.style.removeProperty("--sede");
      }
      if (ir) {
        var propio = p.dataset.sede && inicios[p.dataset.sede] === i;
        ir.value = propio ? String(i) : "";
      }
    }

    function irA(n, dir) {
      n = Math.max(0, Math.min(total - 1, n));
      if (n === i) { pintar(); return; }
      alb.dataset.dir = dir || (n > i ? "adelante" : "atras");
      i = n;
      pintar();
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
      irA(parseInt(b.getAttribute("data-ir"), 10) || 0);
    });
    if (rango) rango.addEventListener("input", function () {
      irA(parseInt(rango.value, 10) - 1);
    });
    if (ir) ir.addEventListener("change", function () {
      if (ir.value) irA(parseInt(ir.value, 10));
    });

    document.addEventListener("keydown", function (e) {
      if (dlg.open) return;
      var t = e.target;
      if (t && /^(INPUT|SELECT|TEXTAREA|BUTTON)$/.test(t.tagName)) return;
      if (e.key === "ArrowRight") { e.preventDefault(); irA(i + 1, "adelante"); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); irA(i - 1, "atras"); }
      else if (e.key === "Home") { e.preventDefault(); irA(0, "atras"); }
      else if (e.key === "End") { e.preventDefault(); irA(total - 1, "adelante"); }
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

    if (rango) rango.max = total;
    pintar();
  })();
})();
