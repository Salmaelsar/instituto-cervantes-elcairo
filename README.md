# Instituto Cervantes de El Cairo — Web y simulador DELE

Sitio web bilingüe (español / árabe) con simulador DELE oficial para el centro de El Cairo.

**En línea:** https://salmaelsar.github.io/instituto-cervantes-elcairo/

## Características

- Página institucional responsive (cabecera, hero, secciones, footer)
- **Español y árabe** con soporte RTL y fuente Noto Sans Arabic
- **Simulador DELE:** 510 preguntas, lectura + auditiva, adultos y escolares
- Modos **práctica** (corrección inmediata) y **examen** (corrección final)
- Temporizador sugerido y **progreso guardado** en el navegador
- Carga **lazy** de preguntas por nivel (mejor rendimiento)
- Convocatorias DELE 2026 y precios (fuente oficial El Cairo)
- Formulario de solicitud de matrícula
- SEO: Open Graph, sitemap.xml, robots.txt

## Probar en local

```bash
cd "Instituto Cervantes Elcairo"
python3 -m http.server 8765
```

Abrir http://localhost:8765

## Publicación

Ver [docs/PUBLICACION.md](docs/PUBLICACION.md).

```bash
git add .
git commit -m "tu mensaje"
git push origin main
```

## Estructura

```
css/           Estilos (responsive, RTL, simulador)
js/
  data/        Módulos DELE (carga lazy)
  examenes-loader.js
  main.js        Motor del simulador
  i18n.js        Traducciones es/ar
  examenes-data.js  Fuente completa (desarrollo)
imagenes/      Logos, favicon, og-preview
scripts/       Generación de preguntas (Python)
```

## Autora

[Salmaelsar](https://github.com/Salmaelsar) — Proyecto formativo / portafolio.
