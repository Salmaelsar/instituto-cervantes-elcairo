/**
 * Menú de navegación responsive — Instituto Cervantes El Cairo
 * Día 1: apertura/cierre del menú hamburguesa en móvil
 */
(function () {
  const menuBtn = document.getElementById("menu-btn");
  const navLista = document.getElementById("nav-principal");

  if (!menuBtn || !navLista) return;

  function etiquetaMenu(abierto) {
    if (window.I18N) {
      menuBtn.setAttribute(
        "aria-label",
        window.I18N.t(abierto ? "a11y.menu.cerrar" : "a11y.menu.abrir")
      );
    }
  }

  menuBtn.addEventListener("click", function () {
    const abierto = navLista.classList.toggle("abierto");
    menuBtn.setAttribute("aria-expanded", String(abierto));
    etiquetaMenu(abierto);
  });

  /* Cerrar menú al pulsar un enlace (móvil) */
  document.querySelectorAll(".cabecera__nav-lista a, .cabecera__utilidades-lista a").forEach(function (enlace) {
    enlace.addEventListener("click", function () {
      if (window.innerWidth <= 768 && navLista.classList.contains("abierto")) {
        navLista.classList.remove("abierto");
        menuBtn.setAttribute("aria-expanded", "false");
      }
    });
  });

  /* Cerrar menú al redimensionar a escritorio */
  window.addEventListener("resize", function () {
    if (window.innerWidth > 768) {
      navLista.classList.remove("abierto");
      menuBtn.setAttribute("aria-expanded", "false");
    }
  });
})();
