# Instituto Cervantes de El Cairo — Web y simulador DELE

> Sitio web institucional bilingüe (español / árabe) con simulador interactivo del examen DELE, basado en los modelos oficiales del Instituto Cervantes.

[![Demo en vivo](https://img.shields.io/badge/demo-en%20línea-b30000?style=for-the-badge)](https://salmaelsar.github.io/instituto-cervantes-elcairo/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)]()
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)]()
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)]()
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)]()

**Demo:** [salmaelsar.github.io/instituto-cervantes-elcairo](https://salmaelsar.github.io/instituto-cervantes-elcairo/)

---

## Sobre el proyecto

Proyecto web desarrollado para el **Instituto Cervantes de El Cairo** (Egipto). Combina una página institucional responsive con un **simulador DELE** que permite practicar comprensión lectora y auditiva con preguntas extraídas de los modelos oficiales (Modelo 0).

Pensado para estudiantes de español en Egipto y el mundo árabe, con interfaz en **español y árabe (RTL)**.

### Problema que resuelve

- Centraliza información del centro (cursos, DELE, biblioteca, actividades).
- Ofrece práctica gratuita del DELE sin instalar aplicaciones.
- Facilita el acceso en árabe a contenido educativo en español.

---

## Funcionalidades principales

| Área | Detalle |
|------|---------|
| **Web institucional** | Cabecera responsive, hero, 5 secciones de menú, footer con contacto |
| **Bilingüe** | Español ↔ عربي, RTL, fuente Noto Sans Arabic, preferencia guardada |
| **Simulador DELE** | 510 preguntas · adultos A1–C2 · escolares A1, A2/B1, B2/C1 |
| **Modos de práctica** | Práctica (corrección inmediata) y examen (corrección al final) |
| **Extras** | Temporizador, progreso en localStorage, carga lazy por nivel |
| **Contenido vivo** | Convocatorias DELE 2026 y precios (fuente oficial El Cairo) |
| **SEO** | Open Graph, sitemap.xml, robots.txt |

---

## Stack tecnológico

- **Frontend:** HTML5, CSS3 (Flexbox, Grid, media queries, RTL), JavaScript vanilla
- **Datos:** 18 módulos JSON/JS generados desde modelos PDF oficiales
- **Backend:** Sin servidor — sitio estático en GitHub Pages
- **Tooling:** Python (extracción y generación de preguntas desde PDF)
- **CI/CD:** GitHub Actions → GitHub Pages

---

## Capturas

> Añade aquí 2–3 capturas en `docs/capturas/` (escritorio, móvil, simulador).

---

## Cómo probarlo

### En línea (recomendado)

Abre [https://salmaelsar.github.io/instituto-cervantes-elcairo/](https://salmaelsar.github.io/instituto-cervantes-elcairo/)

### En local

```bash
cd "Instituto Cervantes Elcairo"
python3 -m http.server 8765
```

Abrir `http://localhost:8765`

---

## Estructura del repositorio

```
css/                 Estilos modulares (header, hero, RTL, móvil, simulador)
js/
  data/              18 módulos DELE (carga lazy)
  examenes-loader.js Cargador asíncrono
  main.js            Motor del simulador
  i18n.js            Internacionalización es/ar
  examenes-data.js   Fuente completa (desarrollo)
imagenes/            Logos institucionales, favicon, Open Graph
scripts/             Pipelines Python para generar preguntas
docs/                Guía de publicación
```

---

## Publicación

Despliegue automático en cada push a `main`. Ver [docs/PUBLICACION.md](docs/PUBLICACION.md).

---

## Autora

**Salma Elsar** — Desarrolladora web en formación

- GitHub: [@Salmaelsar](https://github.com/Salmaelsar)
- Web: [salmaelsar.com](https://www.salmaelsar.com/)
- LinkedIn: [Salma E.](https://www.linkedin.com/in/salma-e-28b246260)

Proyecto formativo / portafolio. No es la web oficial del Instituto Cervantes.

---

## Licencia y aviso

Contenido educativo basado en modelos DELE del Instituto Cervantes. Logos y marca pertenecen al [Instituto Cervantes](https://www.cervantes.es). Uso con fines académicos y de práctica.
