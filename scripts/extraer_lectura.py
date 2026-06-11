#!/usr/bin/env python3
"""Extrae preguntas de comprensión de lectura DELE desde textos PDF."""
import json
import re
import os

BASE = "/Users/salmaelsar/Desktop/Instituto Cervantes Elcairo/.extracted"
OUT = "/Users/salmaelsar/Desktop/Instituto Cervantes Elcairo/js/preguntas-adultos.json"

FILES = {
    "a1": "DELE-A1_v2020_Modelo0_0.txt",
    "a2": "DELE-A2_v2020_Modelo0_0.txt",
    "b1": "dele_b1_modelo0.txt",
    "b2": "dele_b2_modelo0.txt",
    "c1": "INS_CERV_Modelo-0_C1_2.txt",
    "c2": "INS_CERV_Modelo-0_C2_DEF.txt",
}


def parse_abc_block(text):
    """Extrae preguntas tipo A/B/C de un bloque de texto."""
    preguntas = []
    pattern = re.compile(
        r"(\d+)\.\s*(.+?)\n\s*A\)\s*(.+?)\n\s*B\)\s*(.+?)\n\s*C\)\s*(.+?)(?=\n\s*\d+\.|\n\s*Tarea|\n\s*DELE|\Z)",
        re.DOTALL,
    )
    for m in pattern.finditer(text):
        num, enunciado, a, b, c = m.groups()
        preguntas.append({
            "id": int(num),
            "enunciado": " ".join(enunciado.split()),
            "opciones": [
                " ".join(a.split()),
                " ".join(b.split()),
                " ".join(c.split()),
            ],
            "tipo": "abc",
        })
    return preguntas


def parse_claves_lectura(text, nivel):
    """Extrae claves de comprensión de lectura."""
    claves = {}
    m = re.search(
        r"PRUEBA\s*(?:DE\s*)?1\s*:\s*COMPRENSI[ÓO]N\s*DE\s*LECTURA\s*\n(.+?)(?:PRUEBA\s*2|TRANSCRIPCI|$)",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if not m:
        m = re.search(r"CLAVE(?:S)?\s*DE\s*RESPUESTA(?:S)?\s*\n(.+?)(?:PRUEBA|$)", text, re.DOTALL)
    if not m:
        return claves

    block = m.group(1)
    letters = re.findall(r"\b([A-Ja-j])\b", block)
    nums = re.findall(r"\b(\d+)\b", block.split("PRUEBA")[0] if "PRUEBA" in block else block)

    # Formato tabular: "1 2 3 4 5\nB C B C B"
    rows = [ln.strip() for ln in block.split("\n") if ln.strip() and not ln.strip().startswith("PRUEBA")]
    q = 1
    for row in rows:
        nums_row = re.findall(r"^\d+(?:\s+\d+)*", row)
        lets_row = re.findall(r"[A-Ja-j]", row)
        if nums_row and not lets_row:
            continue
        if lets_row and not re.match(r"^\d", row):
            for letter in lets_row:
                claves[q] = letter.upper()
                q += 1
        elif re.match(r"^\d", row):
            parts = row.split()
            nums_part = []
            lets_part = []
            for p in parts:
                if p.isdigit():
                    nums_part.append(int(p))
                elif re.match(r"^[A-Ja-j]$", p):
                    lets_part.append(p.upper())
            if nums_part and lets_part and len(nums_part) == len(lets_part):
                for n, l in zip(nums_part, lets_part):
                    claves[n] = l
            elif lets_part:
                for l in lets_part:
                    claves[q] = l
                    q += 1
    return claves


def extract_reading_section(text):
    """Recorta sección de comprensión de lectura."""
    start = re.search(r"Prueba\s*1\.?\s*Comprensi[oó]n\s*de\s*lectura", text, re.I)
    end = re.search(r"Prueba\s*2\.?\s*Comprensi[oó]n\s*auditiva", text, re.I)
    if not start:
        start = re.search(r"PRUEBA\s*DE\s*COMPRENSI[ÓO]N\s*DE\s*LECTURA", text, re.I)
    if not start:
        return ""
    s = start.start()
    e = end.start() if end else len(text)
    return text[s:e]


def main():
    resultado = {"adultos": {}}

    for nivel, fname in FILES.items():
        path = os.path.join(BASE, fname)
        with open(path, encoding="utf-8") as f:
            text = f.read()

        lectura = extract_reading_section(text)
        preguntas = parse_abc_block(lectura)
        claves = parse_claves_lectura(text, nivel)

        for p in preguntas:
            key = claves.get(p["id"])
            if key and len(p["opciones"]) == 3:
                idx = ord(key.upper()) - ord("A")
                if 0 <= idx < 3:
                    p["correcta"] = idx

        resultado["adultos"][nivel] = {
            "titulo": f"DELE {nivel.upper()} — Comprensión de lectura",
            "prueba": "lectura",
            "preguntas": preguntas,
            "total_claves": len(claves),
        }
        print(f"{nivel.upper()}: {len(preguntas)} preguntas ABC, {len(claves)} claves")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"Guardado en {OUT}")


if __name__ == "__main__":
    main()
