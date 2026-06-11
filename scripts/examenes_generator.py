#!/usr/bin/env python3
"""Genera js/examenes-data.js — banco completo DELE lectura + auditiva."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, ".extracted")
OUT = os.path.join(ROOT, "js", "examenes-data.js")
L = {chr(65 + i): i for i in range(26)}


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def j(s):
    return json.dumps(s, ensure_ascii=False)


def q(en, opts, letter):
    return {"enunciado": en, "opciones": opts, "correcta": L[letter.upper()]}


def mq(en, letter, n=10):
    return q(en, [chr(65 + i) for i in range(n)], letter)


def tarea(nombre, instruccion, contexto, preguntas):
    return {"nombre": nombre, "instruccion": instruccion, "contexto": contexto, "preguntas": preguntas}


def prueba(titulo, tareas):
    return {"titulo": titulo, "tareas": tareas}


def parse_keys_from_text(text, start=0):
    """Extrae secuencia de letras de respuesta desde posición."""
    chunk = text[start:start + 1200]
    keys = []
    for m in re.finditer(r"(?<![A-Za-z])(\d{1,2})\s*([A-Za-z])(?![A-Za-z])", chunk):
        num, letter = int(m.group(1)), m.group(2).upper()
        while len(keys) < num:
            keys.append("A")
        keys[num - 1] = letter
    return keys


def find_clave_keys(text, prueba_num=1):
    labels = [
        f"PRUEBA {prueba_num}:",
        f"PRUEBA {prueba_num}.",
        f"PRUEBA DE COMPRENSIÓN DE LECTURA" if prueba_num == 1 else "COMPRENSIÓN AUDITIVA",
    ]
    for label in labels:
        idx = text.find(label)
        if idx >= 0:
            keys = parse_keys_from_text(text, idx)
            if keys:
                return keys
    return []


def js_obj(obj, indent=0):
    sp = "  " * indent
    if isinstance(obj, str):
        return j(obj)
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, list):
        if not obj:
            return "[]"
        return "[\n" + ",\n".join(sp + "  " + js_obj(x, indent + 1) for x in obj) + "\n" + sp + "]"
    if isinstance(obj, dict):
        lines = []
        for k, v in obj.items():
            lines.append(sp + "  " + k + ": " + js_obj(v, indent + 1))
        return "{\n" + ",\n".join(lines) + "\n" + sp + "}"
    return j(str(obj))


# ─── A1 ADULTOS ───────────────────────────────────────────────────────────────

def a1_adultos_lectura():
    return prueba("DELE A1 — Comprensión de lectura", [
        tarea("Tarea 1", "Lea el correo de Inés (1–5).",
              "Hola, Pedro:\n¿Qué tal estás? ¿Tienes muchos exámenes finales? Yo ahora estudio bastante para tener buenas notas y unas buenas vacaciones.\nEn julio quiero trabajar porque necesito dinero para viajar en agosto. Quiero ir al norte de España con Marta. Primero, vamos a visitar San Sebastián porque tiene una playa muy bonita. Después Bilbao porque las fiestas empiezan el día 15 y queremos verlas. Luego vamos a Santander porque no la conocemos. Además, los tíos de Marta viven allí y no tenemos que ir a un hotel, podemos dormir en su casa.\nDe Madrid a San Sebastián vamos en tren, de allí a Bilbao y a Santander en autobús. En Santander queremos alquilar una moto para visitar los pueblos en el camino de vuelta a Madrid.\nOtra cosa, el viernes es mi cumpleaños, pero voy a hacer la fiesta el sábado, ¿quieres venir? Necesito saberlo antes del jueves para llamar al restaurante. Ahora me voy, porque hoy ceno en casa de Marta y antes quiero comprar unas flores. Esta noche queremos ir a la discoteca.\nUn beso, Inés",
              [q("En este correo, Inés le cuenta a Pedro…", ["cuándo termina los exámenes.", "por qué quiere trabajar en verano.", "dónde va a ir de vacaciones en julio."], "B"),
               q("En el texto se dice que…", ["las fiestas de San Sebastián son bonitas.", "la familia de Marta tiene un hotel en Santander.", "el 15 de agosto Inés va a estar en Bilbao."], "C"),
               q("Inés y Marta van a ir de Santander a Madrid…", ["en coche.", "en moto.", "en autobús."], "B"),
               q("La fiesta de cumpleaños de Inés es…", ["el jueves.", "el viernes.", "el sábado."], "C"),
               q("¿Dónde es la fiesta de cumpleaños de Inés?", ["En casa de Marta.", "En un restaurante.", "En la discoteca."], "B")]),
        tarea("Tarea 2", "Relacione frases 6–11 con mensajes A–J.",
              "A) PROHIBIDO ENTRAR CON ANIMALES\nB) PROGRAMACIÓN TV — CINE ESPAÑOL\nC) SUPERMERCADO EL MONTE — OFERTAS\nD) ATENCIÓN VIAJEROS — Billetes tren\nE) FESTIVAL DE CINE VALLADOLID — Chile domingo 17 h\nF) BUZÓN MÓVIL — 1 mensaje nuevo\nG) AGENDA — Llamar tía Laura; fiesta cumpleaños mamá\nH) Teletexto — Frío y viento fin de semana\nI) Escribir correo a mamá con fotos\nJ) INFORMACIÓN CULTURAL — Concierto Juanes sáb 23; web 30 €",
              [mq("Es más barato en internet.", "F"), mq("Quiere escribir a alguien de su familia.", "I"),
               mq("La película de Chile es el viernes.", "B"), mq("Esta información está en una estación.", "D"),
               mq("Esta semana es más barato.", "C"), mq("El fin de semana hace mal tiempo.", "J")]),
        tarea("Tarea 3", "Relacione textos 12–17 con anuncios A–J.",
              "A) Alicante — alquiler junto playa\nB) Barcelona — casa 100 años\nC) Madrid — piso 100 m², 4 dorm.\nD) Sevilla — apartamento pequeño\nE) Valencia — alquiler universidad sept–jun\nF) Zaragoza — alquiler agosto\nG) Málaga — chalet piscina\nH) Gijón — casa rural\nI) Huesca — casa montaña esquí\nJ) Alquiler vacacional playa mayo",
              [mq("Grupo amigos esquiar Navidad.", "I"), mq("Piso pequeño para una persona.", "D"),
               mq("Piso grande zona colegios.", "C"), mq("Alquiler universidad máx. 650 €.", "E"),
               mq("Piso mar 1–15 agosto.", "F"), mq("Casa campo garaje y piscina.", "G")]),
        tarea("Tarea 4", "Agenda cultural La Gaceta (18–25).",
              "LA GACETA DE MADRID — Agenda (1–7 julio)\n• CINE «Después de hoy» — Director Alberto García. Fines de semana entrada más barata. 22 h.\n• TEATRO «Las mil y una noches»\n• ARTE «Berlanga en imágenes» — Fotografías. Caixa Forum. Lunes a domingo.\n• CONCIERTO Rock In Rio-Madrid — 18 h.\n• Parque de Aventura — Ocio infantil. Fines de semana cierra más tarde.",
              [q("Los fines de semana la entrada de cine…", ["es más barata.", "es más cara.", "cuesta igual."], "A"),
               q("La exposición abre…", ["de lunes a viernes.", "los fines de semana.", "de lunes a domingo."], "C"),
               q("Los conciertos empiezan a las…", ["5 de la tarde.", "6 de la tarde.", "10 de la noche."], "A"),
               q("Los fines de semana, el centro de ocio cierra…", ["más tarde.", "más pronto.", "a la misma hora."], "A"),
               q("El director Alberto García es de…", ["España.", "Argentina.", "México."], "B"),
               q("En la exposición sobre Berlanga puedes ver…", ["películas.", "fotografías.", "cuadros."], "B"),
               q("A las diez de la noche empieza…", ["la película.", "el concierto.", "la obra de teatro."], "C"),
               q("No cuesta dinero ver…", ["las películas.", "la exposición.", "el parque."], "B")]),
    ])


def a1_adultos_auditiva():
    tx = "Transcripción:\nConv.1: María va al cine; el hombre va al supermercado.\nConv.2: La chica va de compras con su hermana.\nConv.3: El hombre va al pueblo de sus padres.\nConv.4: Busca su móvil.\nConv.5: Come un bocadillo en la oficina.\nM1: Restaurante ensalada y agua. M2: Estación y taxi. M3: Concierto guitarra. M4: Biblioteca cierra 20:30. M5: Hotel llaves.\nLucía describe compañeros de español en Buenos Aires.\nPaco describe su ciudad."
    return prueba("DELE A1 — Comprensión auditiva", [
        tarea("Tarea 1", "Conversaciones 1–5 (opciones texto).", tx,
              [q("¿A qué lugar va el hombre hoy?", ["Al supermercado.", "Al cine.", "Al trabajo."], "A"),
               q("¿Qué hace la chica esta tarde?", ["Juega al fútbol.", "Va de compras.", "Estudia."], "A"),
               q("¿Dónde va el hombre de vacaciones?", ["A la playa.", "A la montaña.", "Al pueblo de sus padres."], "C"),
               q("¿Qué busca el hombre?", ["Las llaves.", "El móvil.", "El abrigo."], "B"),
               q("¿Qué come la mujer hoy?", ["Sopa y carne.", "Un bocadillo en la oficina.", "Nada."], "B")]),
        tarea("Tarea 2", "Mensajes 6–10 → situaciones A–I.", tx,
              [mq("Mensaje 1", "C"), mq("Mensaje 2", "H"), mq("Mensaje 3", "G"),
               mq("Mensaje 4", "I"), mq("Mensaje 5", "D", 9)]),
        tarea("Tarea 3", "Compañeros 11–18 → descripciones A–L.", tx,
              [mq("Emiko", "H", 12), mq("Paola", "A", 12), mq("Sussane", "J", 12),
               mq("Andreas", "K", 12), mq("Scott", "E", 12), mq("Ozge", "L", 12),
               mq("Amin", "G", 12), mq("Ana", "B", 12)]),
        tarea("Tarea 4", "Complete frases 19–25 (A–I).", tx,
              [q("La ciudad tiene muchos _______.", ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "D"),
               q("Muchas personas van para ver _______.", ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "C"),
               q("A Paco le gusta _______ de su ciudad.", ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "B"),
               q("Lejos del centro está _______.", ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "H"),
               q("Comer en la ciudad es _______.", ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "G"),
               q("Se puede ir al centro en _______.", ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "F"),
               q("Normalmente va en _______.", ["grande", "el museo", "monumentos", "turistas", "coche", "autobús", "caro", "el palacio", "barato"], "E")]),
    ])


# ─── A2 ADULTOS ───────────────────────────────────────────────────────────────

def a2_adultos_lectura():
    txt = read(os.path.join(EX, "DELE-A2_v2020_Modelo0_0.txt"))
    t1_ctx = "Hola, Carmen:\n¿Cómo estás? Hace semanas que no sé nada de ti… Marta escribe sobre Paula, Ahmed y sus vacaciones en Huelva."
    return prueba("DELE A2 — Comprensión de lectura", [
        tarea("Tarea 1", "Correo de Marta (1–5).", t1_ctx,
              [q("Marta escribe a Carmen para…", ["preguntarle por la zapatería.", "decirle que está de vacaciones.", "quedar para hablar un rato."], "C"),
               q("En el texto se dice que Marta…", ["vive en una casa nueva.", "antes era vecina de Paula.", "está contenta en su barrio."], "B"),
               q("Según el texto, ahora Paula…", ["gana más dinero que antes.", "trabaja en otra empresa.", "necesita un coche nuevo."], "A"),
               q("En el texto se dice que Ahmed…", ["va a ir de vacaciones a Rabat.", "trabaja hasta septiembre.", "quiere decir adiós a sus amigos."], "C"),
               q("Marta quiere ir a Huelva porque…", ["su hermana se va a casar allí.", "su tía la ha invitado a su casa.", "sus sobrinos van a ir unos días."], "B")]),
        tarea("Tarea 2", "Anuncios (6–13).", "Ocho anuncios: habitaciones, mercado, empleo, tiendas, pasaportes, horarios, centro inmigrantes, Parlora.",
              [q("En el anuncio se dice que… (habitaciones)", ["buscan a dos personas.", "prefieren un estudiante.", "alquilan piso para tres."], "B"),
               q("Según el texto, este mercado ahora tiene…", ["tiendas nuevas.", "un horario diferente.", "mejores precios."], "B"),
               q("En el anuncio se dice que… (empleo)", ["solo llaman con formación.", "el trabajo es en Guatemala.", "buscan vender ropa."], "C"),
               q("En el texto se dice que… (Galerías Amarillas)", ["puede pagar menos varios días.", "devuelven el dinero.", "precios especiales cafetería."], "A"),
               q("Si necesita un nuevo pasaporte…", ["llevar dos fotos.", "datos en internet.", "dar pasaporte anterior."], "A"),
               q("Los padres pueden hablar con profesores…", ["mañana o tarde.", "si piden cita.", "por teléfono o correo."], "B"),
               q("En este centro… (inmigrantes)", ["dan clases de lengua.", "tienen pisos.", "necesitan trabajadores."], "A"),
               q("En el texto se dice que… (Parlora)", ["hay hospital nuevo.", "van a tener ambulancia.", "buscan personal."], "B")]),
        tarea("Tarea 3", "Textos A, B, C (14–19).", "A) Alicia — B) Eva — C) Silvia: experiencias en el extranjero.",
              [q("¿Quién no necesita hablar el idioma en su trabajo?", ["Alicia (A)", "Eva (B)", "Silvia (C)"], "B"),
               q("¿Quién no tenía que pagar el alojamiento?", ["Alicia (A)", "Eva (B)", "Silvia (C)"], "A"),
               q("¿Quién tenía un amigo que le habló de ese país?", ["Alicia (A)", "Eva (B)", "Silvia (C)"], "B"),
               q("¿A quién le presentaron a alguien que le dio trabajo?", ["Alicia (A)", "Eva (B)", "Silvia (C)"], "C"),
               q("¿Quién fue a aprender el idioma?", ["Alicia (A)", "Eva (B)", "Silvia (C)"], "C"),
               q("¿Quién conoció a su pareja allí?", ["Alicia (A)", "Eva (B)", "Silvia (C)"], "A")]),
        tarea("Tarea 4", "Blog Historias de Madrid (20–25).", "Manuel escribe sobre Madrid: museos, parques, transporte, barrios.",
              [q("Manuel escribe el blog para…", ["contar experiencias personales.", "dar información útil.", "criticar la ciudad."], "B"),
               q("Según Manuel, en Madrid…", ["hay muchos museos.", "no hay parques.", "el transporte es caro."], "A"),
               q("Manuel recomienda…", ["visitar el centro a pie.", "evitar el metro.", "ir solo en verano."], "A"),
               q("Sobre los barrios dice que…", ["todos son iguales.", "cada uno tiene carácter.", "el más interesante es el centro."], "B"),
               q("Manuel opina que la comida…", ["es siempre cara.", "varía según la zona.", "no merece la pena."], "C"),
               q("Al final invita a…", ["dejar comentarios.", "visitar su ciudad natal.", "evitar las multitudes."], "A")]),
    ])


def a2_adultos_auditiva():
    tx = "Transcripción:\nConv.1: Ya tiene microondas; compra lavadora.\nConv.2: Le duele el brazo derecho.\nConv.3: Compra calcetines marrones.\nConv.4: Ya estuvo en parque de atracciones.\nConv.5: Necesita servilleta.\nConv.6: Trabaja en peluquería propia.\nAudios 7–12: turismo, radio, cursos, presentadora, hipermercado, pisos.\nManuel y Olga conversación.\nMensajes 19–25."
    return prueba("DELE A2 — Comprensión auditiva", [
        tarea("Tarea 1", "Conversaciones 1–6 (opciones texto).", tx,
              [q("¿Qué tiene ya el hombre?", ["Un microondas.", "Un lavaplatos.", "Una lavadora."], "A"),
               q("¿Qué le duele al hombre?", ["El cuello.", "El brazo derecho.", "La espalda."], "C"),
               q("¿Qué compra la mujer?", ["Botas negras.", "Calcetines marrones.", "Guantes."], "B"),
               q("¿Qué ha hecho ya la mujer en la ciudad?", ["Ido a la playa.", "Visitado el parque de atracciones.", "Alquilado bicicletas."], "B"),
               q("¿Qué necesita la mujer?", ["Sal.", "Un cuchillo.", "Una servilleta."], "C"),
               q("¿Dónde trabaja ahora el hombre?", ["En una fábrica.", "En una oficina.", "En una peluquería."], "C")]),
        tarea("Tarea 2", "Audios 7–12.", tx,
              [q("La Oficina de Turismo…", ["abierta desde hace un año.", "tiene diez oficinas.", "busca trabajadores."], "A"),
               q("El programa La semana de Radio Clave…", ["se escucha todos los días.", "se hace hoy por primera vez.", "cambió el horario."], "C"),
               q("Los cursos de español son…", ["de 10 a 12.", "en la Casa de Cultura.", "para niños y jóvenes."], "C"),
               q("La presentadora dice que hoy…", ["el público puede preguntar.", "hablan de horarios del colegio.", "llamarán al invitado."], "A"),
               q("El hipermercado La Pradera…", ["precios especiales esta semana.", "más barato por internet.", "lleva la compra gratis."], "A"),
               q("En Vida cotidiana hablan de…", ["precios de pisos.", "mejores barrios.", "pisos para compartir."], "B")]),
        tarea("Tarea 3", "Manuel / Olga / Ninguno (13–18).", tx,
              [q("Tiene un examen pronto.", ["Manuel", "Olga", "Ninguno"], "C"),
               q("Va a ir a la frutería.", ["Manuel", "Olga", "Ninguno"], "B"),
               q("Le encanta la paella.", ["Manuel", "Olga", "Ninguno"], "B"),
               q("Hace comida muy rica.", ["Manuel", "Olga", "Ninguno"], "A"),
               q("Va a pagar la cuenta.", ["Manuel", "Olga", "Ninguno"], "C"),
               q("Ha ido al banco.", ["Manuel", "Olga", "Ninguno"], "A")]),
        tarea("Tarea 4", "Mensajes 19–25 → enunciados A–K.", tx,
              [mq("Mensaje 1", "B", 11), mq("Mensaje 2", "H", 11), mq("Mensaje 3", "G", 11),
               mq("Mensaje 4", "C", 11), mq("Mensaje 5", "I", 11), mq("Mensaje 6", "E", 11),
               mq("Mensaje 7", "J", 11)]),
    ])


# Continue in part 2 - import from data module
# For brevity in generator, load remaining from examenes_data_levels.py
