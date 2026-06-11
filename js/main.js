/**
 * Simulador DELE — Instituto Cervantes El Cairo
 * Lectura + auditiva | Adultos y escolares
 */
(function () {
  const simulador = document.getElementById("simulador-dele");
  if (!simulador) return;

  function tr(clave, vars) {
    return window.I18N ? window.I18N.t(clave, vars) : clave;
  }

  const NIVELES_ADULTOS = [
    { id: "a1", label: "A1 — Acceso" },
    { id: "a2", label: "A2 — Plataforma" },
    { id: "b1", label: "B1 — Umbral" },
    { id: "b2", label: "B2 — Avanzado" },
    { id: "c1", label: "C1 — Dominio operativo eficaz" },
    { id: "c2", label: "C2 — Maestría" }
  ];

  const NIVELES_ESCOLARES = [
    { id: "a1", label: "A1 Escolar" },
    { id: "a2b1", label: "A2/B1 Escolar" },
    { id: "b2c1", label: "B2/C1 Escolar" }
  ];

  let estado = {
    tipo: "adultos",
    nivel: "a1",
    prueba: "lectura",
    indice: 0,
    aciertos: 0,
    preguntas: [],
    meta: null,
    respondida: false
  };

  const panelSelector = simulador.querySelector(".simulador__selector");
  const panelExamen = simulador.querySelector(".simulador__examen");
  const panelResultado = simulador.querySelector(".simulador__resultado");
  const btnIniciar = simulador.querySelector("#btn-iniciar-examen");
  const selectTipo = simulador.querySelector("#select-tipo");
  const selectNivel = simulador.querySelector("#select-nivel");
  const selectPrueba = simulador.querySelector("#select-prueba");
  const notaEl = simulador.querySelector(".simulador__nota");
  const contextoEl = simulador.querySelector(".pregunta__contexto");
  const contextoLabel = simulador.querySelector(".pregunta__contexto-etiqueta");
  const tareaEl = simulador.querySelector(".pregunta__tarea");
  const numeroEl = simulador.querySelector(".pregunta__numero");
  const enunciadoEl = simulador.querySelector(".pregunta__enunciado");
  const opcionesEl = simulador.querySelector(".pregunta__opciones");
  const feedbackEl = simulador.querySelector(".feedback");
  const btnComprobar = simulador.querySelector(".simulador__examen .btn-comprobar");
  const btnSiguiente = simulador.querySelector(".btn-siguiente");
  const progresoEl = simulador.querySelector(".simulador__progreso");
  const resultadoTexto = simulador.querySelector(".simulador__resultado-texto");
  const btnReiniciar = simulador.querySelector(".btn-reiniciar");

  function mostrarPanel(panel) {
    [panelSelector, panelExamen, panelResultado].forEach(function (p) {
      if (p) p.hidden = p !== panel;
    });
  }

  function contarPreguntas(tipo, nivel, prueba) {
    if (typeof obtenerExamen !== "function") return 0;
    const datos = obtenerExamen(tipo, nivel, prueba);
    return datos ? datos.preguntas.length : 0;
  }

  function actualizarNiveles() {
    const escolar = selectTipo.value === "escolares";
    const niveles = escolar ? NIVELES_ESCOLARES : NIVELES_ADULTOS;
    const nivelActual = selectNivel.value;

    selectNivel.innerHTML = "";
    niveles.forEach(function (n) {
      const opt = document.createElement("option");
      opt.value = n.id;
      opt.textContent = n.label;
      selectNivel.appendChild(opt);
    });

    if (niveles.some(function (n) { return n.id === nivelActual; })) {
      selectNivel.value = nivelActual;
    }

    actualizarNota();
  }

  function actualizarNota() {
    if (!notaEl) return;
    const tipo = selectTipo.value;
    const nivel = selectNivel.value;
    const prueba = selectPrueba ? selectPrueba.value : "lectura";
    const total = contarPreguntas(tipo, nivel, prueba);
    const pruebaLabel = prueba === "lectura" ? tr("sim.lectura") : tr("sim.auditiva");

    if (total > 0) {
      notaEl.textContent = tr("sim.notaConTotal", { n: total, prueba: pruebaLabel });
    } else {
      notaEl.textContent = tr("sim.notaSin");
    }
  }

  function iniciarExamen() {
    const tipo = selectTipo.value;
    const nivel = selectNivel.value;
    const prueba = selectPrueba ? selectPrueba.value : "lectura";
    const datos =
      typeof obtenerExamen === "function" ? obtenerExamen(tipo, nivel, prueba) : null;

    if (!datos || !datos.preguntas.length) {
      alert(tr("sim.sinPreguntas"));
      return;
    }

    estado = {
      tipo: tipo,
      nivel: nivel,
      prueba: prueba,
      indice: 0,
      aciertos: 0,
      preguntas: datos.preguntas,
      meta: datos.meta,
      respondida: false
    };

    mostrarPanel(panelExamen);
    renderPregunta();
  }

  function renderPregunta() {
    const p = estado.preguntas[estado.indice];
    if (!p) return;

    estado.respondida = false;
    feedbackEl.hidden = true;
    feedbackEl.classList.remove("feedback--correcto", "feedback--incorrecto");
    btnComprobar.hidden = false;
    btnSiguiente.hidden = true;

    const esAuditiva = estado.prueba === "auditiva";
    if (contextoLabel) {
      contextoLabel.textContent = tr(esAuditiva ? "sim.contextoAuditiva" : "sim.contextoLectura");
    }

    if (contextoEl) {
      contextoEl.textContent = p.contexto || "";
      contextoEl.hidden = !p.contexto;
      contextoEl.setAttribute(
        "aria-label",
        tr(esAuditiva ? "sim.contextoAuditiva" : "sim.contextoLectura")
      );
    }
    if (tareaEl) tareaEl.textContent = p.tarea + " — " + p.instruccion;
    numeroEl.textContent = tr("sim.pregunta", {
      n: p.numero,
      total: estado.preguntas.length
    });
    enunciadoEl.textContent = p.enunciado;

    opcionesEl.innerHTML = "";
    const grupo = "preg-" + estado.tipo + "-" + estado.nivel + "-" + estado.prueba + "-" + estado.indice;

    p.opciones.forEach(function (opcion, i) {
      const id = grupo + "-op-" + i;
      const label = document.createElement("label");
      label.className = "pregunta__opcion";
      label.setAttribute("for", id);

      const input = document.createElement("input");
      input.type = "radio";
      input.name = grupo;
      input.id = id;
      input.value = String(i);

      label.appendChild(input);
      label.appendChild(document.createTextNode(opcion));
      opcionesEl.appendChild(label);
    });

    if (progresoEl) progresoEl.textContent = estado.meta.titulo || "";
    actualizarBotonSiguiente();
  }

  function actualizarBotonSiguiente() {
    if (!btnSiguiente || btnSiguiente.hidden) return;
    btnSiguiente.textContent =
      estado.indice < estado.preguntas.length - 1
        ? tr("sim.siguiente")
        : tr("sim.verResultado");
  }

  function comprobarRespuesta() {
    if (estado.respondida) return;

    const p = estado.preguntas[estado.indice];
    const grupo = "preg-" + estado.tipo + "-" + estado.nivel + "-" + estado.prueba + "-" + estado.indice;
    const seleccionada = opcionesEl.querySelector('input[name="' + grupo + '"]:checked');

    feedbackEl.hidden = false;
    feedbackEl.classList.remove("feedback--correcto", "feedback--incorrecto");

    if (!seleccionada) {
      feedbackEl.textContent = tr("sim.selecciona");
      feedbackEl.classList.add("feedback--incorrecto");
      return;
    }

    estado.respondida = true;
    const indiceElegido = parseInt(seleccionada.value, 10);
    const acertada = indiceElegido === p.correcta;

    if (acertada) {
      estado.aciertos++;
      feedbackEl.textContent = tr("sim.correcto");
      feedbackEl.classList.add("feedback--correcto");
    } else {
      feedbackEl.textContent = tr("sim.incorrecto", { r: p.opciones[p.correcta] });
      feedbackEl.classList.add("feedback--incorrecto");
    }

    btnComprobar.hidden = true;
    btnSiguiente.hidden = false;
    actualizarBotonSiguiente();
  }

  function siguientePregunta() {
    if (estado.indice < estado.preguntas.length - 1) {
      estado.indice++;
      renderPregunta();
    } else {
      mostrarResultado();
    }
  }

  function mostrarResultado() {
    mostrarPanel(panelResultado);
    const total = estado.preguntas.length;
    const pct = Math.round((estado.aciertos / total) * 100);
    resultadoTexto.textContent = tr("sim.resultado", {
      a: estado.aciertos,
      t: total,
      p: pct
    });
  }

  function reiniciar() {
    mostrarPanel(panelSelector);
    selectTipo.value = "adultos";
    if (selectPrueba) selectPrueba.value = "lectura";
    actualizarNiveles();
  }

  if (selectTipo) {
    selectTipo.addEventListener("change", actualizarNiveles);
  }
  if (selectNivel) {
    selectNivel.addEventListener("change", actualizarNota);
  }
  if (selectPrueba) {
    selectPrueba.addEventListener("change", actualizarNota);
  }

  document.addEventListener("idioma:cambiado", function () {
    if (!panelSelector.hidden) {
      actualizarNota();
    } else if (!panelExamen.hidden && estado.preguntas.length) {
      renderPregunta();
    } else if (!panelResultado.hidden && estado.preguntas.length) {
      mostrarResultado();
    }
  });

  actualizarNiveles();

  if (btnIniciar) btnIniciar.addEventListener("click", iniciarExamen);
  if (btnComprobar) btnComprobar.addEventListener("click", comprobarRespuesta);
  if (btnSiguiente) btnSiguiente.addEventListener("click", siguientePregunta);
  if (btnReiniciar) btnReiniciar.addEventListener("click", reiniciar);
})();
