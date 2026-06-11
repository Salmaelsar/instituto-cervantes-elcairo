/**
 * Carga lazy de exámenes DELE por módulos (js/data/*.js)
 */
(function () {
  const BASE = "js/data/";
  const cache = {};
  const scriptsCargados = {};
  let manifest = null;

  function nombreVariable(tipo, nivel, prueba) {
    return "EXAMEN_CHUNK_" + tipo + "_" + nivel + "_" + prueba;
  }

  function aplanarExamen(datos) {
    const lista = [];
    let num = 1;
    datos.tareas.forEach(function (tarea) {
      tarea.preguntas.forEach(function (p) {
        lista.push({
          numero: num++,
          tarea: tarea.nombre,
          instruccion: tarea.instruccion,
          contexto: p.contexto || tarea.contexto || "",
          enunciado: p.enunciado,
          opciones: p.opciones,
          correcta: p.correcta,
          audio: p.audio || null
        });
      });
    });
    return { meta: datos, preguntas: lista };
  }

  function cargarScript(src) {
    if (scriptsCargados[src]) return scriptsCargados[src];
    scriptsCargados[src] = new Promise(function (resolve, reject) {
      const s = document.createElement("script");
      s.src = src;
      s.async = true;
      s.onload = function () { resolve(); };
      s.onerror = function () { reject(new Error("No se pudo cargar " + src)); };
      document.head.appendChild(s);
    });
    return scriptsCargados[src];
  }

  async function cargarManifest() {
    if (manifest) return manifest;
    const res = await fetch(BASE + "manifest.json");
    if (!res.ok) throw new Error("Manifest no disponible");
    manifest = await res.json();
    return manifest;
  }

  async function contarPreguntasAsync(tipo, nivel, prueba) {
    const m = await cargarManifest();
    return m[tipo]?.[nivel]?.[prueba]?.preguntas || 0;
  }

  async function obtenerExamenAsync(tipo, nivel, prueba) {
    const clave = tipo + "|" + nivel + "|" + prueba;
    if (cache[clave]) return cache[clave];

    const m = await cargarManifest();
    const entrada = m[tipo]?.[nivel]?.[prueba];
    if (!entrada) return null;

    await cargarScript(BASE + entrada.file);
    const varName = nombreVariable(tipo, nivel, prueba);
    const datos = window[varName];
    if (!datos || !datos.tareas?.length) return null;

    const resultado = aplanarExamen(datos);
    cache[clave] = resultado;
    return resultado;
  }

  window.ExamenLoader = {
    cargarManifest: cargarManifest,
    contarPreguntasAsync: contarPreguntasAsync,
    obtenerExamenAsync: obtenerExamenAsync
  };
})();
