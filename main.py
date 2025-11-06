import telebot
from telebot import types
import re

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
def escapar_markdownv2(text: str) -> str:
    """
    Escapa todos los caracteres especiales requeridos por el formato MarkdownV2 
    fuera de los bloques de formato.
    """
    # Lista de caracteres especiales en MarkdownV2:
    # _ * [ ] ( ) ~ ` > # + - = | { } . !
    
    # El patrón de expresión regular busca cualquiera de estos caracteres.
    # El símbolo de barra invertida (\) también debe ser escapado para la regex.
    escape_chars = r'_*[]()~`>#+-.=|{}!'
    
    # Reemplaza cada carácter especial encontrado con una barra invertida delante.
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

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
@bot.message_handler(func=lambda message: not "/ayuda")
def ayuda(message):
    chat_id = message.chat.id
    
    if not chat_id in usuarios_validos:
        ayuda(message)

# ==== MATERIAS ====
def historia_academica(message):
    chat_id = message.chat.id
    usuario = usuarios_logueados[chat_id]

    if usuario == "juan":
        datos = [
            {
                "Actividad": "Modelado y Diseño de Software (TS_ASb_1.2.3.)",
                "Fecha inscripción": "06/08/2025 23:49",
                "Año": "2025",
                "Período lectivo": "2do Cuatrimestre (IFTS)",
                "Propuesta": "IFTS18 - TS en Análisis de Sistemas (2024)",
                "Comisión": "Modelado y Diseño de Software",
                "Estado": "Aceptada"
                # ... puedes omitir campos vacíos como Subcomisión, Turno, Cátedra
            },
            {
                "Actividad": "PP I: Aproximación al Campo Laboral (TS_ASb_1.2.5.)",
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
                "Actividad": "Inglés (TS_ASb_1.2.4.)",
                "Fecha inscripción": "06/08/2025 22:08",
                "Año": "2025",
                "Período lectivo": "2do Cuatrimestre (IFTS)",
                "Propuesta": "IFTS18 - TS en Análisis de Sistemas (2024)",
                "Comisión": "Inglés",
                "Ubicación": "IFTS N° 18",
                "Estado": "Aceptada"
            },
            {
                "Actividad": "Desarrollo de Sistemas Orientado a Objetos (TS_ASb_1.2.1.)",
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

    bot.send_message(chat_id, texto_lista)
    menu_materias(message)

# ==== MENU MATERIAS ======
def crear_menu_materias():
    b_materias = types.KeyboardButton('📅 Materias en curso')
    b_inasistencias = types.KeyboardButton('📚 Inasistencias')
    b_historia = types.KeyboardButton('📚 Historial Academica')
    b_inscripcion = types.KeyboardButton('📚 Inscripción a materias')
    b_volver = types.KeyboardButton('Volver')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(b_materias, b_inasistencias)
    markup.add(b_historia, b_inscripcion)
    return markup



def crear_menu_examenes():
    b_inscripcion = types.KeyboardButton('🧾 Inscripcion a examenes')
    b_baja = types.KeyboardButton('🧾 Baja examen')
    b_volver = types.KeyboardButton('volver')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn_inscripcion,btn_baja)
    markup.add(btn_volver)
    return markup

# ====== MENU PRINCIPAL ======
def crear_menu_principal():
    b_materias = types.KeyboardButton('📚 Materias')
    b_examenes = types.KeyboardButton('🧾 Examenes')
    b_examenes = types.KeyboardButton('🎓 Carreras')
    b_tramites = types.KeyboardButton('🧍 Mis datos')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(b_materias, b_examenes, b_tramites)
    return markup

@bot.message_handler(commands=['menu'])
def menu_principal(message):
    chat_id = message.chat.id

    # Verificar si el usuario está logueado
    if chat_id not in usuarios_logueados:
        bot.send_message(chat_id, "⚠️ Debes iniciar sesión primero con /login.")
        return

    bot.send_message(chat_id, "✅ Selecciona una opción del menu.", reply_markup=crear_menu_principal())
    bot.register_next_step_handler(message, respuesta_menu_principal)

def respuesta_menu_principal(message):
    chat_id = message.chat.id
    texto = message.text
    
    elif texto.startswith('📚') or texto == 'Materias':
        menu_materias(message)
    elif texto.startswith('🧾') or texto == 'Examenes':
        menu_exam
    elif texto.startswith('🧍') or texto == 'Mis datos':
        usuario = usuarios_logueados[chat_id]
        bot.send_message(chat_id, f"Tus datos personales:\n👤 Usuario: {usuario}")
    else:
        bot.send_message(chat_id, f"❌ Opcion no encontrada")
        bot.register_next_step_handler(message, menu_principal)

@bot.message_handler(func=lambda message: True)
def ayuda(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, (
    "🤖 Bot del IFTS 18\n"
    "- Para ingresar tu usuario, escribe /login.\n"
    "- Para ver el menu, escribe /menu"
    ))
