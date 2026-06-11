/**
 * Simulador DELE — Instituto Cervantes El Cairo
 * Carga lazy · Modo práctica/examen · Temporizador · Progreso local
 */
(function () {
  const simulador = document.getElementById("simulador-dele");
  if (!simulador) return;

  const CLAVE_PROGRESO = "ic-elcairo-progreso-dele";

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

  const TIEMPOS_SUGERIDOS = {
    lectura: 60,
    auditiva: 45
  };

  let estado = {
    tipo: "adultos",
    nivel: "a1",
    prueba: "lectura",
    modo: "practica",
    indice: 0,
    aciertos: 0,
    preguntas: [],
    meta: null,
    respondida: false,
    respuestas: [],
    tiempoRestante: 0,
    timerId: null
  };

  const panelSelector = simulador.querySelector(".simulador__selector");
  const panelExamen = simulador.querySelector(".simulador__examen");
  const panelResultado = simulador.querySelector(".simulador__resultado");
  const btnIniciar = simulador.querySelector("#btn-iniciar-examen");
  const selectTipo = simulador.querySelector("#select-tipo");
  const selectNivel = simulador.querySelector("#select-nivel");
  const selectPrueba = simulador.querySelector("#select-prueba");
  const selectModo = simulador.querySelector("#select-modo");
  const checkTimer = simulador.querySelector("#check-timer");
  const notaEl = simulador.querySelector(".simulador__nota");
  const timerEl = simulador.querySelector(".simulador__timer");
  const audioAviso = simulador.querySelector(".simulador__audio-aviso");
  const contextoEl = simulador.querySelector(".pregunta__contexto");
  const contextoLabel = simulador.querySelector(".pregunta__contexto-etiqueta");
  const tareaEl = simulador.querySelector(".pregunta__tarea");
  const numeroEl = simulador.querySelector(".pregunta__numero");
  const enunciadoEl = simulador.querySelector(".pregunta__enunciado");
  const opcionesEl = simulador.querySelector(".pregunta__opciones");
  const feedbackEl = simulador.querySelector(".feedback");
  const btnComprobar = simulador.querySelector(".simulador__examen .btn-comprobar");
  const btnSiguiente = simulador.querySelector(".btn-siguiente");
  const btnFinalizar = simulador.querySelector(".btn-finalizar");
  const progresoEl = simulador.querySelector(".simulador__progreso");
  const resultadoTexto = simulador.querySelector(".simulador__resultado-texto");
  const resultadoDetalle = simulador.querySelector(".simulador__resultado-detalle");
  const btnReiniciar = simulador.querySelector(".btn-reiniciar");
  const audioPlayer = simulador.querySelector(".simulador__audio");

  function mostrarPanel(panel) {
    [panelSelector, panelExamen, panelResultado].forEach(function (p) {
      if (p) p.hidden = p !== panel;
    });
    if (panel !== panelExamen) detenerTimer();
  }

  function detenerTimer() {
    if (estado.timerId) {
      clearInterval(estado.timerId);
      estado.timerId = null;
    }
    if (timerEl) timerEl.hidden = true;
  }

  function formatearTiempo(segundos) {
    const m = Math.floor(segundos / 60);
    const s = segundos % 60;
    return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
  }

  function iniciarTimer(segundos) {
    detenerTimer();
    if (!checkTimer || !checkTimer.checked || !timerEl) return;

    estado.tiempoRestante = segundos;
    timerEl.hidden = false;
    timerEl.textContent = tr("sim.tiempo") + " " + formatearTiempo(estado.tiempoRestante);

    estado.timerId = setInterval(function () {
      estado.tiempoRestante--;
      timerEl.textContent = tr("sim.tiempo") + " " + formatearTiempo(estado.tiempoRestante);
      if (estado.tiempoRestante <= 0) {
        detenerTimer();
        alert(tr("sim.tiempoAgotado"));
        if (estado.modo === "examen") {
          finalizarExamen();
        }
      }
    }, 1000);
  }

  async function contarPreguntas(tipo, nivel, prueba) {
    if (window.ExamenLoader) {
      try {
        return await window.ExamenLoader.contarPreguntasAsync(tipo, nivel, prueba);
      } catch (e) {
        return 0;
      }
    }
    return 0;
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

  async function actualizarNota() {
    if (!notaEl) return;
    const tipo = selectTipo.value;
    const nivel = selectNivel.value;
    const prueba = selectPrueba ? selectPrueba.value : "lectura";
    notaEl.textContent = tr("sim.cargando");

    const total = await contarPreguntas(tipo, nivel, prueba);
    const pruebaLabel = prueba === "lectura" ? tr("sim.lectura") : tr("sim.auditiva");

    if (total > 0) {
      notaEl.textContent = tr("sim.notaConTotal", { n: total, prueba: pruebaLabel });
    } else {
      notaEl.textContent = tr("sim.notaSin");
    }
  }

  function claveProgreso() {
    return [selectTipo.value, selectNivel.value, selectPrueba.value, selectModo?.value || "practica"].join("|");
  }

  function guardarProgreso() {
    try {
      const datos = JSON.parse(localStorage.getItem(CLAVE_PROGRESO) || "{}");
      datos[claveProgreso()] = {
        indice: estado.indice,
        aciertos: estado.aciertos,
        respuestas: estado.respuestas,
        fecha: new Date().toISOString()
      };
      localStorage.setItem(CLAVE_PROGRESO, JSON.stringify(datos));
    } catch (e) {}
  }

  function cargarProgresoGuardado() {
    try {
      const datos = JSON.parse(localStorage.getItem(CLAVE_PROGRESO) || "{}");
      return datos[claveProgreso()] || null;
    } catch (e) {
      return null;
    }
  }

  async function iniciarExamen(reanudar) {
    const tipo = selectTipo.value;
    const nivel = selectNivel.value;
    const prueba = selectPrueba ? selectPrueba.value : "lectura";
    const modo = selectModo ? selectModo.value : "practica";

    if (btnIniciar) {
      btnIniciar.disabled = true;
      btnIniciar.textContent = tr("sim.cargando");
    }

    let datos = null;
    try {
      if (window.ExamenLoader) {
        datos = await window.ExamenLoader.obtenerExamenAsync(tipo, nivel, prueba);
      }
    } catch (e) {
      datos = null;
    }

    if (btnIniciar) {
      btnIniciar.disabled = false;
      btnIniciar.textContent = tr("simulador.iniciar");
    }

    if (!datos || !datos.preguntas.length) {
      alert(tr("sim.sinPreguntas"));
      return;
    }

    const guardado = reanudar ? cargarProgresoGuardado() : null;

    estado = {
      tipo: tipo,
      nivel: nivel,
      prueba: prueba,
      modo: modo,
      indice: guardado ? guardado.indice : 0,
      aciertos: guardado ? guardado.aciertos : 0,
      preguntas: datos.preguntas,
      meta: datos.meta,
      respondida: false,
      respuestas: guardado ? guardado.respuestas || [] : [],
      tiempoRestante: 0,
      timerId: null
    };

    if (guardado && guardado.indice > 0) {
      const ok = confirm(tr("sim.reanudar"));
      if (!ok) {
        estado.indice = 0;
        estado.aciertos = 0;
        estado.respuestas = [];
      }
    }

    mostrarPanel(panelExamen);
    iniciarTimer(TIEMPOS_SUGERIDOS[prueba] * 60);
    renderPregunta();
  }

  function esModoExamen() {
    return estado.modo === "examen";
  }

  function renderPregunta() {
    const p = estado.preguntas[estado.indice];
    if (!p) return;

    estado.respondida = false;
    feedbackEl.hidden = true;
    feedbackEl.classList.remove("feedback--correcto", "feedback--incorrecto");

    const examen = esModoExamen();
    btnComprobar.hidden = examen;
    if (examen) {
      btnSiguiente.hidden = estado.indice >= estado.preguntas.length - 1;
      if (btnFinalizar) btnFinalizar.hidden = false;
    } else {
      btnSiguiente.hidden = true;
      if (btnFinalizar) btnFinalizar.hidden = true;
    }

    const esAuditiva = estado.prueba === "auditiva";
    if (contextoLabel) {
      contextoLabel.textContent = tr(esAuditiva ? "sim.contextoAuditiva" : "sim.contextoLectura");
    }

    if (audioAviso) {
      audioAviso.hidden = !esAuditiva;
      if (esAuditiva) audioAviso.textContent = tr("sim.audioAviso");
    }

    if (audioPlayer) {
      if (p.audio) {
        audioPlayer.hidden = false;
        audioPlayer.src = p.audio;
      } else {
        audioPlayer.hidden = true;
        audioPlayer.removeAttribute("src");
      }
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
    const previa = estado.respuestas[estado.indice];

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
      if (previa !== undefined && previa === i) input.checked = true;

      label.appendChild(input);
      label.appendChild(document.createTextNode(opcion));
      opcionesEl.appendChild(label);
    });

    if (progresoEl) progresoEl.textContent = estado.meta.titulo || "";
    actualizarBotonSiguiente();
  }

  function obtenerSeleccion() {
    const grupo = "preg-" + estado.tipo + "-" + estado.nivel + "-" + estado.prueba + "-" + estado.indice;
    const seleccionada = opcionesEl.querySelector('input[name="' + grupo + '"]:checked');
    return seleccionada ? parseInt(seleccionada.value, 10) : null;
  }

  function actualizarBotonSiguiente() {
    if (!btnSiguiente || btnSiguiente.hidden) return;
    btnSiguiente.textContent =
      estado.indice < estado.preguntas.length - 1
        ? tr("sim.siguiente")
        : tr("sim.verResultado");
  }

  function registrarRespuesta(indiceElegido) {
    const p = estado.preguntas[estado.indice];
    estado.respuestas[estado.indice] = indiceElegido;
    if (indiceElegido === p.correcta) estado.aciertos++;
    guardarProgreso();
  }

  function comprobarRespuesta() {
    if (estado.respondida || esModoExamen()) return;

    const p = estado.preguntas[estado.indice];
    const indiceElegido = obtenerSeleccion();

    feedbackEl.hidden = false;
    feedbackEl.classList.remove("feedback--correcto", "feedback--incorrecto");

    if (indiceElegido === null) {
      feedbackEl.textContent = tr("sim.selecciona");
      feedbackEl.classList.add("feedback--incorrecto");
      return;
    }

    estado.respondida = true;
    if (estado.respuestas[estado.indice] === undefined) {
      registrarRespuesta(indiceElegido);
    }

    const acertada = indiceElegido === p.correcta;

    if (acertada) {
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
    const indiceElegido = obtenerSeleccion();
    if (indiceElegido !== null && estado.respuestas[estado.indice] === undefined) {
      if (esModoExamen()) {
        estado.respuestas[estado.indice] = indiceElegido;
        guardarProgreso();
      } else {
        registrarRespuesta(indiceElegido);
      }
    }

    if (estado.indice < estado.preguntas.length - 1) {
      estado.indice++;
      renderPregunta();
    } else {
      finalizarExamen();
    }
  }

  function finalizarExamen() {
    const indiceElegido = obtenerSeleccion();
    if (indiceElegido !== null && estado.respuestas[estado.indice] === undefined) {
      estado.respuestas[estado.indice] = indiceElegido;
    }
    if (esModoExamen()) recalcularAciertos();

    detenerTimer();
    mostrarResultado();
    try {
      const datos = JSON.parse(localStorage.getItem(CLAVE_PROGRESO) || "{}");
      delete datos[claveProgreso()];
      localStorage.setItem(CLAVE_PROGRESO, JSON.stringify(datos));
    } catch (e) {}
  }

  function recalcularAciertos() {
    estado.aciertos = 0;
    estado.preguntas.forEach(function (p, i) {
      if (estado.respuestas[i] === p.correcta) estado.aciertos++;
    });
  }

  function mostrarResultado() {
    mostrarPanel(panelResultado);
    const total = estado.preguntas.length;
    const pct = total ? Math.round((estado.aciertos / total) * 100) : 0;
    resultadoTexto.textContent = tr("sim.resultado", {
      a: estado.aciertos,
      t: total,
      p: pct
    });

    if (resultadoDetalle) {
      if (esModoExamen()) {
        let html = "<ul class=\"simulador__resultado-lista\">";
        estado.preguntas.forEach(function (p, i) {
          const elegida = estado.respuestas[i];
          const ok = elegida === p.correcta;
          const textoElegido = elegida !== undefined ? p.opciones[elegida] : tr("sim.sinResponder");
          html += "<li class=\"" + (ok ? "simulador__resultado-ok" : "simulador__resultado-ko") + "\">";
          html += "<strong>" + p.numero + ".</strong> " + textoElegido;
          if (!ok) html += " → " + p.opciones[p.correcta];
          html += "</li>";
        });
        html += "</ul>";
        resultadoDetalle.innerHTML = html;
        resultadoDetalle.hidden = false;
      } else {
        resultadoDetalle.hidden = true;
        resultadoDetalle.innerHTML = "";
      }
    }
  }

  function reiniciar() {
    detenerTimer();
    mostrarPanel(panelSelector);
    selectTipo.value = "adultos";
    if (selectPrueba) selectPrueba.value = "lectura";
    if (selectModo) selectModo.value = "practica";
    actualizarNiveles();
  }

  if (selectTipo) selectTipo.addEventListener("change", actualizarNiveles);
  if (selectNivel) selectNivel.addEventListener("change", actualizarNota);
  if (selectPrueba) selectPrueba.addEventListener("change", actualizarNota);

  document.addEventListener("idioma:cambiado", function () {
    if (!panelSelector.hidden) {
      actualizarNota();
    } else if (!panelExamen.hidden && estado.preguntas.length) {
      renderPregunta();
    } else if (!panelResultado.hidden && estado.preguntas.length) {
      mostrarResultado();
    }
    if (btnIniciar) btnIniciar.textContent = tr("simulador.iniciar");
  });

  actualizarNiveles();

  if (btnIniciar) btnIniciar.addEventListener("click", function () { iniciarExamen(true); });
  if (btnComprobar) btnComprobar.addEventListener("click", comprobarRespuesta);
  if (btnSiguiente) btnSiguiente.addEventListener("click", siguientePregunta);
  if (btnFinalizar) btnFinalizar.addEventListener("click", finalizarExamen);
  if (btnReiniciar) btnReiniciar.addEventListener("click", reiniciar);
})();
