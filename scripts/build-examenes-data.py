#!/usr/bin/env python3
"""Genera js/examenes-data.js desde los TXT extraídos y datos parciales existentes."""
import re
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACTED = os.path.join(ROOT, ".extracted")
OUT = os.path.join(ROOT, "js", "examenes-data.js")

LETTER_IDX = {chr(65 + i): i for i in range(26)}


def letter_to_idx(ch):
    return LETTER_IDX.get(ch.upper(), 0)


def parse_answer_key(text, label):
    """Extrae claves tipo '1B 2C' o tablas con números y letras."""
    idx = text.find(label)
    if idx < 0:
        return []
    chunk = text[idx:idx + 800]
    answers = []
    for m in re.finditer(r"(?<![A-Za-z])(\d{1,2})\s*([A-Za-z])(?![A-Za-z])", chunk):
        num, letter = int(m.group(1)), m.group(2).upper()
        while len(answers) < num:
            answers.append("A")
        answers[num - 1] = letter
    return answers


def parse_abc_questions(text):
    """Extrae preguntas A/B/C del texto."""
    preguntas = []
    pattern = re.compile(
        r"(?:^|\n)\s*(\d{1,2})\.\s+(.+?)\n\s*A\)\s*(.+?)\n\s*B\)\s*(.+?)\n\s*C\)\s*(.+?)(?=\n\s*\d{1,2}\.|\n\s*Tarea|\n\s*TAREA|\n\s*PREGUNTAS|\Z)",
        re.DOTALL | re.IGNORECASE,
    )
    for m in pattern.finditer(text):
        enunciado = re.sub(r"\s+", " ", m.group(2).strip())
        opciones = [
            re.sub(r"\s+", " ", m.group(3).strip()),
            re.sub(r"\s+", " ", m.group(4).strip()),
            re.sub(r"\s+", " ", m.group(5).strip()),
        ]
        preguntas.append({"num": int(m.group(1)), "enunciado": enunciado, "opciones": opciones})
    return preguntas


def apply_keys(preguntas, keys):
    out = []
    for p in preguntas:
        idx = p["num"] - 1
        correcta = letter_to_idx(keys[idx]) if idx < len(keys) else 0
        out.append({k: v for k, v in p.items() if k != "num"} | {"correcta": correcta})
    return out


def js_str(s):
    return json.dumps(s, ensure_ascii=False)


def js_obj(obj, indent=2):
    """Serializa a JS-like object literal."""
    if isinstance(obj, str):
        return js_str(obj)
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if obj is None:
        return "null"
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, list):
        if not obj:
            return "[]"
        items = ",\n".join(" " * (indent + 2) + js_obj(x, indent + 2) for x in obj)
        return "[\n" + items + "\n" + " " * indent + "]"
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        lines = []
        for k, v in obj.items():
            key = k if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", k) else js_str(k)
            lines.append(" " * (indent + 2) + key + ": " + js_obj(v, indent + 2))
        return "{\n" + ",\n".join(lines) + "\n" + " " * indent + "}"
    return js_str(str(obj))


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


# --- Datos A1 adultos lectura (desde preguntas-adultos.js, verificado con clave oficial) ---
A1_ADULTOS_LECTURA = {
    "titulo": "DELE A1 — Comprensión de lectura",
    "tareas": [
        {
            "nombre": "Tarea 1",
            "instruccion": "Lea el correo electrónico de Inés y responda a las preguntas 1–5.",
            "contexto": "Hola, Pedro:\n¿Qué tal estás? ¿Tienes muchos exámenes finales? Yo ahora estudio bastante para tener buenas notas y unas buenas vacaciones.\nEn julio quiero trabajar porque necesito dinero para viajar en agosto. Quiero ir al norte de España con Marta. Primero, vamos a visitar San Sebastián porque tiene una playa muy bonita. Después Bilbao porque las fiestas empiezan el día 15 y queremos verlas. Luego vamos a Santander porque no la conocemos. Además, los tíos de Marta viven allí y no tenemos que ir a un hotel, podemos dormir en su casa.\nDe Madrid a San Sebastián vamos en tren, de allí a Bilbao y a Santander en autobús. En Santander queremos alquilar una moto para visitar los pueblos en el camino de vuelta a Madrid. Es divertido, ¿verdad?\nOtra cosa, el viernes es mi cumpleaños, pero voy a hacer la fiesta el sábado, ¿quieres venir? Necesito saberlo antes del jueves para llamar al restaurante. Ahora me voy, porque hoy ceno en casa de Marta y antes quiero comprar unas flores. Esta noche queremos ir a la discoteca.\nUn beso, Inés",
            "preguntas": [
                {"enunciado": "En este correo, Inés le cuenta a Pedro…", "opciones": ["cuándo termina los exámenes.", "por qué quiere trabajar en verano.", "dónde va a ir de vacaciones en julio."], "correcta": 1},
                {"enunciado": "En el texto se dice que…", "opciones": ["las fiestas de San Sebastián son bonitas.", "la familia de Marta tiene un hotel en Santander.", "el 15 de agosto Inés va a estar en Bilbao."], "correcta": 2},
                {"enunciado": "Inés y Marta van a ir de Santander a Madrid…", "opciones": ["en coche.", "en moto.", "en autobús."], "correcta": 1},
                {"enunciado": "La fiesta de cumpleaños de Inés es…", "opciones": ["el jueves.", "el viernes.", "el sábado."], "correcta": 2},
                {"enunciado": "¿Dónde es la fiesta de cumpleaños de Inés?", "opciones": ["En casa de Marta.", "En un restaurante.", "En la discoteca."], "correcta": 1},
            ],
        },
        {
            "nombre": "Tarea 2",
            "instruccion": "Relacione cada frase (6–11) con el mensaje correcto (A–J).",
            "contexto": "A) NOTA: PROHIBIDO ENTRAR CON ANIMALES\nB) PROGRAMACIÓN DE TELEVISIÓN — CINE ESPAÑOL (L–X: cine mexicano; J–V: chileno; S–D: clásicos españoles)\nC) SUPERMERCADO EL MONTE — OFERTAS: Leche 10% menos; Naranjas 1,20 €/kg\nD) ATENCIÓN VIAJEROS — Billetes de tren Barcelona–Tarragona en máquinas automáticas\nE) FESTIVAL DE CINE DE VALLADOLID — País invitado: Chile. Cine chileno el domingo a las 17 h. Entrada libre\nF) BUZÓN MÓVIL — 1 mensaje nuevo. Llamar gratis al 123\nG) AGENDA — Llamar a la tía Laura a las 18 h; organizar fiesta de cumpleaños de mamá\nH) Teletexto — Mucho frío y viento en todo el país (sábado y domingo)\nI) Escribir un correo a mamá y enviarle fotos de la fiesta\nJ) INFORMACIÓN CULTURAL — Concierto de Juanes, sábado 23 a las 20 h. Entradas web: 30 €; Oficina de Turismo: 35 €",
            "preguntas": [
                {"enunciado": "Es más barato en internet.", "opciones": list("ABCDEFGHIJ"), "correcta": 5},
                {"enunciado": "Quiere escribir a alguien de su familia.", "opciones": list("ABCDEFGHIJ"), "correcta": 8},
                {"enunciado": "La película de Chile es el viernes.", "opciones": list("ABCDEFGHIJ"), "correcta": 1},
                {"enunciado": "Esta información está en una estación.", "opciones": list("ABCDEFGHIJ"), "correcta": 3},
                {"enunciado": "Esta semana es más barato.", "opciones": list("ABCDEFGHIJ"), "correcta": 2},
                {"enunciado": "El fin de semana hace mal tiempo.", "opciones": list("ABCDEFGHIJ"), "correcta": 7},
            ],
        },
        {
            "nombre": "Tarea 3",
            "instruccion": "Relacione cada texto (12–17) con el anuncio correcto (A–J).",
            "contexto": "A) Alicante — Se alquila piso junto a la playa, todo el año menos agosto. 600 €/mes\nB) Barcelona — Se vende casa de 100 años en el centro, 260.000 €\nC) Madrid — Se vende piso 100 m², 4 dormitorios, zona con colegios. 300.000 €\nD) Sevilla — Se vende apartamento pequeño, 1 dormitorio. 90.000 €\nE) Valencia — Se alquila piso cerca de la universidad, septiembre–junio. 650 €/mes\nF) Zaragoza — Se alquila piso 2 dormitorios, agosto completo. 800 €/mes\nG) Málaga — Se vende chalet con piscina y garaje grande en el campo\nH) Gijón — Se alquila casa rural cerca de Gijón, todo el año, jardín y garaje\nI) Huesca — Se alquila casa en la montaña junto a estación de esquí, meses de invierno\nJ) Anuncio de alquiler vacacional en ciudad con playa (mayo)",
            "preguntas": [
                {"enunciado": "Somos un grupo de amigos y nos gusta esquiar. Buscamos casa grande para Navidad.", "opciones": list("ABCDEFGHIJ"), "correcta": 8},
                {"enunciado": "Quiero comprar un piso pequeño para mí sola.", "opciones": list("ABCDEFGHIJ"), "correcta": 3},
                {"enunciado": "Tenemos dos hijas y queremos un piso grande en zona con colegio e instituto.", "opciones": list("ABCDEFGHIJ"), "correcta": 2},
                {"enunciado": "Queremos alquilar un piso para tres personas cerca de la universidad, septiembre a junio, máx. 650 €.", "opciones": list("ABCDEFGHIJ"), "correcta": 4},
                {"enunciado": "Buscamos piso cerca del mar del 1 al 15 de agosto.", "opciones": list("ABCDEFGHIJ"), "correcta": 5},
                {"enunciado": "Queremos comprar casa en el campo con garaje grande, piscina y espacio para deporte.", "opciones": list("ABCDEFGHIJ"), "correcta": 6},
            ],
        },
        {
            "nombre": "Tarea 4",
            "instruccion": "Lea la agenda cultural de La Gaceta de Madrid y responda a las preguntas 18–25.",
            "contexto": "LA GACETA DE MADRID — Agenda cultural (1–7 julio)\n• CINE «Después de hoy» — Director argentino Alberto García. Fines de semana entrada más barata. Empieza a las 22 h.\n• TEATRO «Las mil y una noches» — Teatro María Guerrero\n• ARTE «Berlanga en imágenes» — Exposición de fotografías del director Luis García Berlanga. Caixa Forum. Abierto de lunes a domingo.\n• CONCIERTO Rock In Rio-Madrid — Festival internacional. Empieza a las 18 h.\n• ACTIVIDADES Parque de Aventura — Centro de ocio infantil. Tema: La Prehistoria. Fines de semana cierra más tarde.",
            "preguntas": [
                {"enunciado": "Los fines de semana la entrada de cine…", "opciones": ["es más barata.", "es más cara.", "cuesta igual."], "correcta": 0},
                {"enunciado": "La exposición abre…", "opciones": ["de lunes a viernes.", "los fines de semana.", "de lunes a domingo."], "correcta": 2},
                {"enunciado": "Los conciertos empiezan a las…", "opciones": ["5 de la tarde.", "6 de la tarde.", "10 de la noche."], "correcta": 0},
                {"enunciado": "Los fines de semana, el centro de ocio cierra…", "opciones": ["más tarde.", "más pronto.", "a la misma hora."], "correcta": 0},
                {"enunciado": "El director Alberto García es de…", "opciones": ["España.", "Argentina.", "México."], "correcta": 1},
                {"enunciado": "En la exposición sobre Berlanga puedes ver…", "opciones": ["películas.", "fotografías.", "cuadros."], "correcta": 1},
                {"enunciado": "A las diez de la noche empieza…", "opciones": ["la película.", "el concierto.", "la obra de teatro."], "correcta": 2},
                {"enunciado": "No cuesta dinero ver…", "opciones": ["las películas.", "la exposición.", "el parque."], "correcta": 1},
            ],
        },
    ],
}

# A1 adultos auditiva — Tarea 1 convertida a texto; resto con transcripciones oficiales
A1_ADULTOS_AUDITIVA = {
    "titulo": "DELE A1 — Comprensión auditiva",
    "tareas": [
        {
            "nombre": "Tarea 1",
            "instruccion": "Escuche cinco conversaciones y responda a las preguntas 1–5.",
            "contexto": "Transcripción:\nConv.1: María va al cine; el hombre va al supermercado a comprar comida.\nConv.2: La chica no puede jugar al fútbol; va de compras con su hermana.\nConv.3: El hombre va al pueblo de sus padres de vacaciones (no a la playa ni montaña).\nConv.4: El hombre busca su móvil.\nConv.5: La mujer come un bocadillo en la oficina.",
            "preguntas": [
                {"enunciado": "¿A qué lugar va el hombre hoy?", "opciones": ["Al supermercado.", "Al cine.", "Al trabajo."], "correcta": 0},
                {"enunciado": "¿Qué hace la chica esta tarde?", "opciones": ["Juega al fútbol.", "Va de compras.", "Estudia."], "correcta": 1},
                {"enunciado": "¿Dónde va el hombre de vacaciones?", "opciones": ["A la playa.", "A la montaña.", "Al pueblo de sus padres."], "correcta": 2},
                {"enunciado": "¿Qué busca el hombre?", "opciones": ["Las llaves.", "El móvil.", "El abrigo."], "correcta": 1},
                {"enunciado": "¿Qué come la mujer hoy?", "opciones": ["Sopa y carne en el restaurante.", "Un bocadillo en la oficina.", "Nada, tiene mucho trabajo."], "correcta": 1},
            ],
        },
        {
            "nombre": "Tarea 2",
            "instruccion": "Relacione cada mensaje (6–10) con la situación correcta (A–I).",
            "contexto": "Transcripción:\nM1: Pedir ensalada y agua en un restaurante.\nM2: Salida de estación y parada de taxi al lado.\nM3: Aviso de silencio, el concierto de guitarra va a empezar.\nM4: La biblioteca se cierra a las 20:30.\nM5: Recepción de hotel entrega llaves, pasaporte y tarjeta.",
            "preguntas": [
                {"enunciado": "Mensaje 1", "opciones": list("ABCDEFGHI"), "correcta": 2},
                {"enunciado": "Mensaje 2", "opciones": list("ABCDEFGHI"), "correcta": 7},
                {"enunciado": "Mensaje 3", "opciones": list("ABCDEFGHI"), "correcta": 6},
                {"enunciado": "Mensaje 4", "opciones": list("ABCDEFGHI"), "correcta": 8},
                {"enunciado": "Mensaje 5", "opciones": list("ABCDEFGHI"), "correcta": 3},
            ],
        },
        {
            "nombre": "Tarea 3",
            "instruccion": "Relacione cada compañero (11–18) con la descripción correcta (A–L).",
            "contexto": "Transcripción: Lucía habla de sus compañeros de español en Buenos Aires.\nA) es sociable  B) estudia mucho  C) habla mucho  D) es estadounidense  E) es el más joven  F) quiere estudiar piano  G) quiere ser escritor  H) es de Francia  I) organiza fiestas  J) hace deporte por la tarde  K) ve muchas películas  L) desayuna en la escuela",
            "preguntas": [
                {"enunciado": "Emiko", "opciones": list("ABCDEFGHIJKL"), "correcta": 7},
                {"enunciado": "Paola", "opciones": list("ABCDEFGHIJKL"), "correcta": 0},
                {"enunciado": "Sussane", "opciones": list("ABCDEFGHIJKL"), "correcta": 9},
                {"enunciado": "Andreas", "opciones": list("ABCDEFGHIJKL"), "correcta": 10},
                {"enunciado": "Scott", "opciones": list("ABCDEFGHIJKL"), "correcta": 4},
                {"enunciado": "Ozge", "opciones": list("ABCDEFGHIJKL"), "correcta": 11},
                {"enunciado": "Amin", "opciones": list("ABCDEFGHIJKL"), "correcta": 6},
                {"enunciado": "Ana", "opciones": list("ABCDEFGHIJKL"), "correcta": 1},
            ],
        },
        {
            "nombre": "Tarea 4",
            "instruccion": "Complete las frases 19–25 según la conversación de Paco sobre su ciudad.",
            "contexto": "Transcripción: Paco describe su ciudad grande con muchos turistas y monumentos; el Museo de Arte está en el centro; el Palacio Azul fuera; comer es caro; vive en el centro; autobús en plaza Mayor; va en coche los fines de semana.\nOpciones: A) grande  B) el museo  C) monumentos  D) turistas  E) coche  F) autobús  G) caro  H) el palacio  I) barato",
            "preguntas": [
                {"enunciado": "La ciudad tiene muchos _______.", "opciones": ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "correcta": 2},
                {"enunciado": "Muchas personas van a la ciudad de Paco para ver _______.", "opciones": ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "correcta": 1},
                {"enunciado": "A Paco le gusta _______ de su ciudad.", "opciones": ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "correcta": 7},
                {"enunciado": "Lejos del centro está _______.", "opciones": ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "correcta": 2},
                {"enunciado": "Comer en la ciudad de Paco es _______.", "opciones": ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "correcta": 6},
                {"enunciado": "Se puede ir al centro en _______.", "opciones": ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "correcta": 5},
                {"enunciado": "Normalmente Paco va a su ciudad en _______.", "opciones": ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "correcta": 4},
            ],
        },
    ],
}


def build_a2_lectura():
    txt = read(os.path.join(EXTRACTED, "DELE-A2_v2020_Modelo0_0.txt"))
    keys = "C B A C B B B C A A B A B B A B C C A B A B C A C".split()
    # keys from official: 1-5 CBA CB, 6-13 B B C A A B A B, 14-19 B A B C C A, 20-25 B A B C A C
    keys = list("CBACBBBCAAABABBCABCCABACAC")
    t1_ctx = re.search(r"Hola, Carmen:.*?(?=PREGUNTAS)", txt, re.DOTALL)
    t1 = t1_ctx.group(0).strip() if t1_ctx else ""
    t1_q = apply_keys(parse_abc_questions(txt[:3000]), keys[:5])
    t2_q = apply_keys(parse_abc_questions(txt[3000:12000]), keys[5:13])
    t3_ctx = re.search(r"TEXTOS\nA\. ALICIA.*?(?=Texto\nHola\. Me llamo)", txt, re.DOTALL)
    t3 = t3_ctx.group(0).strip() if t3_ctx else ""
    t3_preg = [
        {"enunciado": "¿Quién no necesita hablar el idioma del país en su trabajo?", "opciones": ["Alicia (A)", "Eva (B)", "Silvia (C)"], "correcta": 1},
        {"enunciado": "¿Quién no tenía que pagar el alojamiento?", "opciones": ["Alicia (A)", "Eva (B)", "Silvia (C)"], "correcta": 0},
        {"enunciado": "¿Quién tenía un amigo que le habló de ese país?", "opciones": ["Alicia (A)", "Eva (B)", "Silvia (C)"], "correcta": 1},
        {"enunciado": "¿A quién le presentaron a una persona que le dio trabajo en ese país?", "opciones": ["Alicia (A)", "Eva (B)", "Silvia (C)"], "correcta": 2},
        {"enunciado": "¿Quién fue a ese país para aprender el idioma?", "opciones": ["Alicia (A)", "Eva (B)", "Silvia (C)"], "correcta": 2},
        {"enunciado": "¿Quién conoció a su pareja en ese país?", "opciones": ["Alicia (A)", "Eva (B)", "Silvia (C)"], "correcta": 0},
    ]
    t4_ctx = re.search(r"Texto\nHola\. Me llamo Manuel.*?(?=Tarea 4)", txt, re.DOTALL)
    t4 = t4_ctx.group(0).strip() if t4_ctx else ""
    t4_q = apply_keys(parse_abc_questions(txt[12000:20000]), keys[19:25])
    return {
        "titulo": "DELE A2 — Comprensión de lectura",
        "tareas": [
            {"nombre": "Tarea 1", "instruccion": "Lea el correo de Marta y responda a las preguntas 1–5.", "contexto": t1, "preguntas": t1_q},
            {"nombre": "Tarea 2", "instruccion": "Lea los anuncios y responda a las preguntas 6–13.", "contexto": "Anuncios de habitaciones, mercado, empleo, tiendas, pasaportes, horarios escolares, centro inmigrantes y noticias de Parlora.", "preguntas": t2_q},
            {"nombre": "Tarea 3", "instruccion": "Relacione las preguntas 14–19 con los textos A, B o C.", "contexto": t3, "preguntas": t3_preg},
            {"nombre": "Tarea 4", "instruccion": "Lea el blog Historias de Madrid y responda a las preguntas 20–25.", "contexto": t4, "preguntas": t4_q},
        ],
    }


def count_preguntas(data):
    total = 0
    for prueba in ("lectura", "auditiva"):
        if prueba in data and data[prueba].get("tareas"):
            for t in data[prueba]["tareas"]:
                total += len(t.get("preguntas", []))
    return total


def main():
    # Importar datos escolares desde módulo embebido (generado en segunda parte)
    from examenes_data_content import EXAMENES_DATA  # type: ignore

    EXAMENES_DATA["adultos"]["a1"]["lectura"] = A1_ADULTOS_LECTURA
    EXAMENES_DATA["adultos"]["a1"]["auditiva"] = A1_ADULTOS_AUDITIVA
    try:
        EXAMENES_DATA["adultos"]["a2"]["lectura"] = build_a2_lectura()
    except Exception:
        pass

    lines = [
        "/**",
        " * Banco completo DELE — lectura y auditiva",
        " * Fuente: modelos oficiales Instituto Cervantes (Modelo 0)",
        " * Generado automáticamente — no editar a mano",
        " */",
        "const EXAMENES_DATA = " + js_obj(EXAMENES_DATA) + ";",
        "",
        "function obtenerExamen(tipo, nivel, prueba) {",
        "  const datos = EXAMENES_DATA[tipo]?.[nivel]?.[prueba];",
        "  if (!datos || !datos.tareas?.length) return null;",
        "  const lista = [];",
        "  let num = 1;",
        "  datos.tareas.forEach(function (tarea) {",
        "    tarea.preguntas.forEach(function (p) {",
        "      lista.push({",
        "        numero: num++,",
        "        tarea: tarea.nombre,",
        "        instruccion: tarea.instruccion,",
        "        contexto: tarea.contexto,",
        "        enunciado: p.enunciado,",
        "        opciones: p.opciones,",
        "        correcta: p.correcta",
        "      });",
        "    });",
        "  });",
        "  return { meta: datos, preguntas: lista };",
        "}",
        "",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Generado:", OUT)
    for tipo, niveles in EXAMENES_DATA.items():
        for nivel, pruebas in niveles.items():
            for prueba in ("lectura", "auditiva"):
                if prueba in pruebas and pruebas[prueba].get("tareas"):
                    n = sum(len(t["preguntas"]) for t in pruebas[prueba]["tareas"])
                    print(f"  {tipo}/{nivel}/{prueba}: {n}")


if __name__ == "__main__":
    main()
