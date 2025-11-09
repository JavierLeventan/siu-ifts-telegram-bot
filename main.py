import telebot
from telebot import types

# ===== CONSTANTES =====
_MATERIAS = '📚 Materias'
_EXAMENES = '🧾 Examenes'
_CARRERAS = '🎓 Carreras'
_MIS_DATOS = '🧍 Mis datos'
_VOLVER = '↩️ Volver'
# MENU MATERIAS
_MATERIAS_EN_CURSO = '📚 Materias en curso'
_INASISTENCIAS = '📚 Inasistencias'
_HISTORIA_ACADEMICA = '📚 Historial Academica'
_INSCRIPCION_MATERIAS = '📚 Inscripción a materias'
# MENU EXAMENES
_INSCRIPCION_EXAMENES = '🧾 Inscripción a examenes'
_BAJA_EXAMEN = '🧾 Baja examen'
# MENU CARRERAS
_INSCRIPCION_CARRERAS = '🎓 Inscripción a carreras'
_BAJA_CARRERA = '🎓 Baja carrera'

# ===== CONFIGURACIÓN =====
TOKEN = open("token.txt").read()
bot = telebot.TeleBot(TOKEN)

# Diccionario simple para manejar sesiones de login
usuarios_logueados = {}

# Datos de ejemplo para login (usuario: contraseña)
USUARIOS_VALIDOS = {
    "juan": "1234",
    "maria": "abcd"
}

# ===== LOGIN =====
@bot.message_handler(commands=['login'])
def enviar_login(message):
    chat_id = message.chat.id
    if chat_id in usuarios_logueados:
        bot.send_message(chat_id, "Ya estás logueado ✅")
        responder_menu()
    else:
        bot.send_message(chat_id, "🔐 Por favor, envíame tu usuario:")
        bot.register_next_step_handler(message, pedir_usuario)

def pedir_usuario(message):
    chat_id = message.chat.id
    usuario = message.text.strip()
    if usuario not in USUARIOS_VALIDOS:
        bot.send_message(chat_id, "❌ Usuario no encontrado. Intenta nuevamente con /login.")
        return
    bot.send_message(chat_id, "Ahora envíame tu contraseña (no se guardará en el chat):")
    bot.register_next_step_handler(message, pedir_contrasena, usuario)

def pedir_contrasena(message, usuario):
    chat_id = message.chat.id

    # Intentar borrar el mensaje que contiene la contraseña
    try:
        bot.delete_message(chat_id, message.message_id)
    except Exception as e:
        print(f"No se pudo borrar el mensaje de contraseña: {e}")

    contrasena = message.text.strip()

    if USUARIOS_VALIDOS[usuario] == contrasena:
        usuarios_logueados[chat_id] = usuario
        bot.send_message(chat_id, f"✅ Bienvenido, {usuario}!")
        menu_principal(message)
    else:
        bot.send_message(chat_id, "❌ Contraseña incorrecta. Intenta con /login nuevamente.")

# CHEQUEAR SI ESTA LOGUEADO
@bot.message_handler(func=lambda message: True)
def check_logged(message):
    chat_id = message.chat.id
    
    if not chat_id in usuarios_logueados:
        ayuda(message)

# ==== CREADOR MENUES ======
def crear_menu_materias():
    btn_materias = types.KeyboardButton(_MATERIAS_EN_CURSO)
    btn_inasistencias = types.KeyboardButton(_INASISTENCIAS)
    btn_historia = types.KeyboardButton(_HISTORIA_ACADEMICA)
    btn_inscripcion = types.KeyboardButton(_INSCRIPCION_MATERIAS)
    btn_volver = types.KeyboardButton(_VOLVER)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn_materias, btn_inasistencias)
    markup.add(btn_historia, btn_inscripcion)
    markup.add(btn_volver)
    return markup

def crear_menu_examenes():
    btn_inscripcion = types.KeyboardButton(_INSCRIPCION_EXAMENES)
    btn_baja = types.KeyboardButton(_BAJA_EXAMEN)
    btn_volver = types.KeyboardButton(_VOLVER)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn_inscripcion,btn_baja)
    markup.add(btn_volver)
    return markup

def crear_menu_carerras():
    btn_inscripcion = types.KeyboardButton(_INSCRIPCION_CARRERAS)
    btn_baja = types.KeyboardButton(_BAJA_CARRERA)
    btn_volver = types.KeyboardButton(_VOLVER)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn_inscripcion,btn_baja)
    markup.add(btn_volver)
    return markup

def crear_menu_principal():
    btn_materias = types.KeyboardButton(_MATERIAS)
    btn_examenes = types.KeyboardButton(_EXAMENES)
    btn_carreras = types.KeyboardButton(_CARRERAS)
    btn_datos = types.KeyboardButton(_MIS_DATOS)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn_materias, btn_examenes)
    markup.add(btn_carreras,btn_datos)
    return markup

# ==== MATERIAS ====
def menu_materias(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "✅ Selecciona una opción del menu.", reply_markup=crear_menu_materias())
    bot.register_next_step_handler(message, respuesta_menu_materias)

def respuesta_menu_materias(message):
    chat_id = message.chat.id
    texto = message.text
    
    if texto == _MATERIAS_EN_CURSO:
        materias_en_curso(message)
    elif texto == _HISTORIA_ACADEMICA:
        historia_academica(message)
    elif texto == _INASISTENCIAS:
        inasistencias(message)
    elif texto == _INSCRIPCION_MATERIAS:
        inscripcion_materias(message)
    elif texto == _VOLVER:
        menu_principal(message)
    else:
        bot.send_message(chat_id, f"❌ Opción no encontrada")
        bot.register_next_step_handler(message, menu_materias)

@bot.message_handler(func=lambda message: message.text == _MATERIAS_EN_CURSO)
def materias_en_curso(message):
    chat_id = message.chat.id
    usuario = usuarios_logueados[chat_id]

    if usuario == "juan":
        materias = [
            "Modelado y Diseño de Software",
            "PP I: Aproximación al Campo Laboral"
        ]
    elif usuario == "maria":
        materias = [
            "Inglés",
            "Desarrollo de Sistemas Orientado a Objetos"
        ]
    else:
        materias = []

    if materias:
        texto_lista = "*📚 Tus Materias en Curso:*\n\n"
        for i, materia in enumerate(materias):
            texto_lista += f"{i + 1}. {materia}\n"
    else:
        texto_lista = "No se encontraron materias en curso."

    bot.send_message(chat_id, texto_lista, parse_mode='Markdown')
    menu_materias(message)

@bot.message_handler(func=lambda message: message.text == _HISTORIA_ACADEMICA)
def historia_academica(message):
    chat_id = message.chat.id
    usuario = usuarios_logueados[chat_id]

    if usuario == "juan":
        datos = [
            {
                "Actividad": "Modelado y Diseño de Software (TS_ASbtn_1.2.3.)",
                "Fecha inscripción": "06/08/2025 23:49",
                "Año": "2025",
                "Período lectivo": "2do Cuatrimestre (IFTS)",
                "Propuesta": "IFTS18 - TS en Análisis de Sistemas (2024)",
                "Comisión": "Modelado y Diseño de Software",
                "Estado": "Aceptada"
            },
            {
                "Actividad": "PP I: Aproximación al Campo Laboral (TS_ASbtn_1.2.5.)",
                "Fecha inscripción": "06/08/2025 22:12",
                "Año": "2025",
                "Período lectivo": "2do Cuatrimestre (IFTS)",
                "Propuesta": "IFTS18 - TS en Análisis de Sistemas (2024)",
                "Comisión": "PPI Aproximacion al campo laboral",
                "Estado": "Aceptada"
            }
        ]
    elif usuario == "maria":
        datos = [
            {
                "Actividad": "Inglés (TS_ASbtn_1.2.4.)",
                "Fecha inscripción": "06/08/2025 22:08",
                "Año": "2025",
                "Período lectivo": "2do Cuatrimestre (IFTS)",
                "Propuesta": "IFTS18 - TS en Análisis de Sistemas (2024)",
                "Comisión": "Inglés",
                "Ubicación": "IFTS N° 18",
                "Estado": "Aceptada"
            },
            {
                "Actividad": "Desarrollo de Sistemas Orientado a Objetos (TS_ASbtn_1.2.1.)",
                "Fecha inscripción": "06/08/2025 22:08",
                "Año": "2025",
                "Período lectivo": "2do Cuatrimestre (IFTS)",
                "Propuesta": "IFTS18 - TS en Análisis de Sistemas (2024)",
                "Comisión": "Desarrollo de Sistemas Orientado a Objetos",
                "Ubicación": "IFTS N° 18",
                "Estado": "Aceptada"
            }
        ]
    else:
        datos = [{ "No se encontraron materias." }]

    texto_lista = "*📅 Tu Historia Academica*\n\n"
    
    for i, materia in enumerate(datos):
        # Título de la materia en Negrita (ej. 1. Modelado y Diseño de Software)
        texto_lista += f"*{i + 1}. {materia['Actividad'].split('(')[0].strip()}*\n"
        # Iterar sobre los campos para crear la lista
        for clave, valor in materia.items():
            if clave != "Actividad": # Evitamos duplicar el título
                texto_lista += f"• _{clave}:_ {valor}\n"
        texto_lista += "\n" # Espacio entre materias

    bot.send_message(chat_id, texto_lista, parse_mode='Markdown')
    menu_materias(message)

@bot.message_handler(func=lambda message: message.text == _INASISTENCIAS)
def inasistencias(message):
    chat_id = message.chat.id
    usuario = usuarios_logueados[chat_id]

    if usuario == "juan":
        inasistencias = {
            "Modelado y Diseño de Software": 2,
            "PP I: Aproximación al Campo Laboral": 0
        }
    elif usuario == "maria":
        inasistencias = {
            "Inglés": 1,
            "Desarrollo de Sistemas Orientado a Objetos": 3
        }
    else:
        inasistencias = {}

    texto_lista = "*📚 Tus Inasistencias:*\n\n"
    for materia, faltas in inasistencias.items():
        texto_lista += f"• {materia}: {faltas}\n"

    bot.send_message(chat_id, texto_lista, parse_mode='Markdown')
    menu_materias(message)

@bot.message_handler(func=lambda message: message.text == _INSCRIPCION_MATERIAS)
def inscripcion_materias(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🔔 La inscripción a materias aún no está disponible.")
    menu_materias(message)

# ====== MENU EXAMENES ======
def menu_examenes(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "✅ Selecciona una opción del menu.", reply_markup=crear_menu_examenes())
    bot.register_next_step_handler(message, respuesta_menu_examenes)

def respuesta_menu_examenes(message):
    chat_id = message.chat.id
    texto = message.text
    
    if texto == _INSCRIPCION_EXAMENES:
        inscripcion_examenes(message)
    elif texto == _BAJA_EXAMEN:
        baja_examen(message)
    elif texto == _VOLVER:
        menu_principal(message)
    else:
        bot.send_message(chat_id, f"❌ Opción no encontrada")
        bot.register_next_step_handler(message, menu_examenes)

@bot.message_handler(func=lambda message: message.text == _INSCRIPCION_EXAMENES)
def inscripcion_examenes(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🔔 La inscripción a examenes aún no está disponible.")
    menu_examenes(message)

@bot.message_handler(func=lambda message: message.text == _BAJA_EXAMEN)
def baja_examen(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🔔 La baja de examenes aún no está disponible.")
    menu_examenes(message)

# ====== INSCRIPCION CARRERAS ======
@bot.message_handler(func=lambda message: message.text == _CARRERAS)
def menu_carreras(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "✅ Selecciona una opción del menu.", reply_markup=crear_menu_carerras())
    bot.register_next_step_handler(message, respuesta_menu_carreras)

def respuesta_menu_carreras(message):
    chat_id = message.chat.id
    texto = message.text
    
    if texto == _INSCRIPCION_CARRERAS:
        inscripcion_carreras(message)
    elif texto == _BAJA_CARRERA:
        baja_carrera(message)
    elif texto == _VOLVER:
        menu_principal(message)
    else:
        bot.send_message(chat_id, f"❌ Opción no encontrada")
        bot.register_next_step_handler(message, menu_carreras)

@bot.message_handler(func=lambda message: message.text == _INSCRIPCION_CARRERAS)
def inscripcion_carreras(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🔔 La inscripción a carreras aún no está disponible.")
    menu_carreras(message)

@bot.message_handler(func=lambda message: message.text == _BAJA_CARRERA)
def baja_carrera(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🔔 La baja de carreras aún no está disponible.")
    menu_carreras(message)

# ====== MENU PRINCIPAL ======
@bot.message_handler(commands=['menu'])
def menu_principal(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "✅ Selecciona una opción del menu.", reply_markup=crear_menu_principal())
    bot.register_next_step_handler(message, respuesta_menu_principal)

def respuesta_menu_principal(message):
    chat_id = message.chat.id
    texto = message.text
    
    if texto == _MATERIAS:
        menu_materias(message)
    elif texto == _EXAMENES:
        menu_examenes(message)
    elif texto == _CARRERAS:
        menu_carreras(message)
    elif texto == _MIS_DATOS:
        usuario = usuarios_logueados[chat_id]
        bot.send_message(chat_id, f"Tus datos personales:\n👤 Usuario: {usuario}")
    else:
        bot.send_message(chat_id, f"❌ Opción no encontrada")
        ayuda(message)

@bot.message_handler(func=lambda message: True)
def ayuda(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, (
    "🤖 Bot del IFTS 18\n"
    "- Para ingresar tu usuario, escribe /login.\n"
    "- Para ver el menu, escribe /menu"
    ))

if __name__ == "__main__":
    print("🤖 Bot en ejecución...")
    bot.infinity_polling()
