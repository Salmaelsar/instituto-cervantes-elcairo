#!/usr/bin/env python3
"""Divide js/examenes-data.js en módulos por tipo/nivel/prueba para carga lazy."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "js" / "examenes-data.js"
OUT = ROOT / "js" / "data"

def main():
    text = SRC.read_text(encoding="utf-8")
    m = re.search(r"const EXAMENES_DATA = (\{[\s\S]*\});\s*\nfunction obtenerExamen", text)
    if not m:
        raise SystemExit("No se encontró EXAMENES_DATA en examenes-data.js")

    # Evaluar de forma segura el objeto (generado por nosotros)
    data = eval(m.group(1))  # noqa: S307 — fuente controlada del propio proyecto

    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}

    for tipo, niveles in data.items():
        manifest[tipo] = {}
        for nivel, pruebas in niveles.items():
            manifest[tipo][nivel] = {}
            for prueba, contenido in pruebas.items():
                clave = f"{tipo}-{nivel}-{prueba}"
                archivo = f"{clave}.js"
                manifest[tipo][nivel][prueba] = archivo
                payload = json.dumps(contenido, ensure_ascii=False, indent=2)
                OUT.joinpath(archivo).write_text(
                    f"window.EXAMEN_CHUNK_{clave.replace('-', '_')} = {payload};\n",
                    encoding="utf-8",
                )

    manifest_path = OUT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Generados {sum(len(p) for n in manifest.values() for p in n.values())} chunks en {OUT}")

if __name__ == "__main__":
    main()
