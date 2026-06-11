# Instituto Cervantes de El Cairo — Web y simulador DELE

Sitio web institucional del centro de El Cairo con simulador de examen DELE (lectura y auditiva).

## Contenido

- Página de bienvenida en **español** y **árabe** (RTL)
- Secciones: actividades, cursos, formación, DELE, biblioteca
- Simulador DELE con **510 preguntas** (adultos A1–C2 y escolares)

## Probar en local

```bash
cd "Instituto Cervantes Elcairo"
python3 -m http.server 8765
```

Abrir [http://localhost:8765](http://localhost:8765)

## Publicar en GitHub Pages

### 1. Crear repositorio

```bash
cd "Instituto Cervantes Elcairo"
git init
git add .
git commit -m "Web Instituto Cervantes El Cairo con simulador DELE"
git branch -M main
git remote add origin https://github.com/Salmaelsar/instituto-cervantes-elcairo.git
git push -u origin main
```

> Crea antes el repositorio vacío en [github.com/new](https://github.com/new) con el nombre `instituto-cervantes-elcairo` (sin README ni `.gitignore`).

### 2. Activar GitHub Pages

1. En el repo: **Settings → Pages**
2. **Build and deployment → Source**: seleccionar **GitHub Actions**
3. El workflow `.github/workflows/pages.yml` publicará el sitio en cada push a `main`

La URL será: **https://salmaelsar.github.io/instituto-cervantes-elcairo/**

### 3. (Opcional) Dominio propio

Añadir un archivo `CNAME` en la raíz con el dominio, y configurar DNS en el proveedor.

## Estructura

```
css/          Estilos (cabecera, hero, secciones, simulador, RTL, móvil)
js/           Simulador, i18n, datos DELE
imagenes/     Logos y favicon
scripts/      Generación de preguntas (desarrollo, no necesario en producción)
```

## Regenerar preguntas DELE (desarrollo)

Los PDFs fuente y scripts Python están en `scripts/`. El archivo servido al navegador es `js/examenes-data.js`.
# instituto-cervantes-elcairo
