# Guía de publicación e institucionalización

## GitHub Pages (actual)

- **URL:** https://salmaelsar.github.io/instituto-cervantes-elcairo/
- **Repositorio:** https://github.com/Salmaelsar/instituto-cervantes-elcairo
- **Despliegue:** automático con `.github/workflows/pages.yml` en cada push a `main`

### Comprobar despliegue

1. [Actions del repositorio](https://github.com/Salmaelsar/instituto-cervantes-elcairo/actions)
2. El último workflow debe estar en verde
3. **Settings → Pages → Build and deployment → Source:** GitHub Actions

## Dominio propio (pendiente institucional)

1. Registrar dominio o subdominio (ej. `dele.elcairo.cervantes.es`)
2. En GitHub: **Settings → Pages → Custom domain**
3. Añadir registro DNS `CNAME` apuntando a `salmaelsar.github.io`
4. Crear archivo `CNAME` en la raíz del proyecto con el dominio

## Validación del Instituto Cervantes

Este proyecto es educativo/portafolio. Para uso oficial:

- Contactar con la dirección del [centro de El Cairo](https://elcairo.cervantes.es/es/default.shtm)
- Email: cencai@cervantes.es
- Solicitar revisión de contenidos, logos y enlace desde la web oficial

## Regenerar datos del simulador

```bash
# Tras modificar js/examenes-data.js:
node -e "
const fs=require('fs');const path=require('path');
const fn=new Function(fs.readFileSync('js/examenes-data.js','utf8')+'; return EXAMENES_DATA;');
const data=fn(); const out='js/data'; fs.mkdirSync(out,{recursive:true});
const manifest={};
for (const [tipo,niveles] of Object.entries(data)) {
  manifest[tipo]={};
  for (const [nivel,pruebas] of Object.entries(niveles)) {
    manifest[tipo][nivel]={};
    for (const [prueba,contenido] of Object.entries(pruebas)) {
      let n=0; contenido.tareas.forEach(t=>n+=t.preguntas.length);
      const clave=tipo+'-'+nivel+'-'+prueba;
      manifest[tipo][nivel][prueba]={file:clave+'.js',preguntas:n};
      const v='EXAMEN_CHUNK_'+clave.replace(/-/g,'_');
      fs.writeFileSync(path.join(out,clave+'.js'),'window.'+v+' = '+JSON.stringify(contenido,null,2)+';\\n');
    }
  }
}
fs.writeFileSync('js/data/manifest.json',JSON.stringify(manifest,null,2));
console.log('OK');
"
```
