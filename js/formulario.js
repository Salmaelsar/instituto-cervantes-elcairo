/**
 * Formulario de matrícula — envío por correo
 */
(function () {
  const form = document.getElementById("form-matricula");
  if (!form) return;

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    if (!form.reportValidity()) return;

    const datos = new FormData(form);
    const nombre = datos.get("nombre");
    const email = datos.get("email");
    const telefono = datos.get("telefono") || "";
    const curso = datos.get("curso") || "";
    const mensaje = datos.get("mensaje");

    const asunto = encodeURIComponent("Solicitud de información — Instituto Cervantes El Cairo");
    const cuerpo = encodeURIComponent(
      "Nombre: " + nombre + "\n" +
      "Email: " + email + "\n" +
      "Teléfono: " + telefono + "\n" +
      "Curso/nivel: " + curso + "\n\n" +
      "Mensaje:\n" + mensaje
    );

    window.location.href = "mailto:info.cairo@cervantes.es?subject=" + asunto + "&body=" + cuerpo;
  });
})();
