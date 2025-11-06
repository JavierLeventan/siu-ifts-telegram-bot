import telebot
from telebot import types

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
        mostrar_menu_principal(message)
    else:
        bot.send_message(chat_id, "❌ Contraseña incorrecta. Intenta con /login nuevamente.")

# CHEQUEAR SI ESTA LOGUEADO
@bot.message_handler(func=lambda message: not "/ayuda")
def ayuda(message):
    chat_id = message.chat.id
    
    if not chat_id in usuarios_validos:
        ayuda(message)


#--- 1. Definición del Menú Principal ---
def crear_menu_principal():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    b_materias = types.KeyboardButton('📚 MATERIAS')
    b_examenes = types.KeyboardButton('🧾 EXAMENES')
    b_carreras = types.KeyboardButton('🎓 CARRERAS')
    b_mis_datos = types.KeyboardButton('👤 MIS DATOS')
    
    markup.row(b_materias, b_examenes)
    markup.row(b_carreras, b_mis_datos)
    return markup

# --- 2. Definición del Submenú: MATERIAS ---
def crear_menu_materias():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Subopciones
    b1 = types.KeyboardButton('C. Materias en curso')
    b2 = types.KeyboardButton('C. Historia Académica')
    b3 = types.KeyboardButton('C. Inasistencias')
    b4 = types.KeyboardButton('C. Inscripción a materias')
    
    # Botón para volver al menú anterior
    b_volver = types.KeyboardButton('↩️ Volver al Principal') 
    
    markup.row(b1, b2)
    markup.row(b3, b4)
    markup.add(b_volver)
    return markup

# --- 3. Definición del Submenú: EXAMENES ---
def crear_menu_examenes():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton('E. Inscripción a exámenes')
    b2 = types.KeyboardButton('E. Baja examen')
    b_volver = types.KeyboardButton('↩️ Volver al Principal')
    
    markup.add(b1, b2)
    markup.add(b_volver)
    return markup

# --- 4. Definición del Submenú: CARRERAS ---
def crear_menu_carreras():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton('R. Inscripción a carreras')
    b2 = types.KeyboardButton('R. Baja inscripción')
    b_volver = types.KeyboardButton('↩️ Volver al Principal')
    
    markup.add(b1, b2)
    markup.add(b_volver)
    return markup

# --- 5. Manejador del Menú Principal (Inicio) ---
@bot.message_handler(commands=['menu'])
def mostrar_menu_principal(message):
    chat_id = message.chat.id
    if chat_id not in usuarios_logueados:
        bot.send_message(chat_id, "⚠️ Debes iniciar sesión primero con /login.")
        return
        
    bot.send_message(
        chat_id, 
        "🏠 *Menú Principal:* Elige una categoría:", 
        reply_markup=crear_menu_principal(),
        parse_mode="Markdown"
    )

# --- 6. Manejadores de Nivel 1 (Categorías) ---
@bot.message_handler(func=lambda message: message.text == '📚 MATERIAS')
def submenu_materias(message):
    bot.send_message(
        message.chat.id, 
        "📚 *Submenú de Materias:* ¿Qué deseas hacer?",
        reply_markup=crear_menu_materias(),
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.text == '🧾 EXAMENES')
def submenu_examenes(message):
    bot.send_message(
        message.chat.id, 
        "🧾 *Submenú de Exámenes:* Elige una opción:",
        reply_markup=crear_menu_examenes(),
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.text == '🎓 CARRERAS')
def submenu_carreras(message):
    bot.send_message(
        message.chat.id, 
        "🎓 *Submenú de Carreras:* Acciones disponibles:",
        reply_markup=crear_menu_carreras(),
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.text == '👤 MIS DATOS')
def accion_mis_datos(message):
    bot.send_message(message.chat.id, "Mostrando tus datos personales... ")
    # IMPORTANTE: Después de la acción, volvemos a mostrar el menú principal
    mostrar_menu_principal(message)

# --- 7. Manejador para Volver (Común) ---

@bot.message_handler(func=lambda message: message.text == '↩️ Volver al Principal')
def volver_al_principal(message):
    mostrar_menu_principal(message)

# --- 8. Manejadores de Nivel 2 (Acciones Específicas) ---
# Usa los prefijos para diferenciar las opciones con un solo manejador si quieres.

@bot.message_handler(func=lambda message: message.text.startswith(('C.', 'E.', 'R.')))
def accion_submenus(message):
    texto = message.text
    chat_id = message.chat.id

    if texto == 'C. Materias en curso':
        bot.send_message(chat_id, "Accediendo a tus materias actuales...")
    elif texto == 'C. Historia Académica':
        bot.send_message(chat_id, "Cargando tu historial de notas...")
    # ... (y así sucesivamente con todas las 8 subopciones)
    elif texto == 'R. Baja inscripción':
        bot.send_message(chat_id, "Iniciando proceso de baja de inscripción a carrera...")
    
    # Después de cada acción, regresamos al menú que corresponde al grupo (ej. C. vuelve a Materias)
    if texto.startswith('C.'):
        submenu_materias(message)
    elif texto.startswith('E.'):
        submenu_examenes(message)
    elif texto.startswith('R.'):
        submenu_carreras(message)

# El truco para evitar el desorden es:
# 1. Definir un menú (ReplyKeyboardMarkup) para cada nivel.
# 2. Usar un @message_handler con una función lambda (func=...) para detectar el texto exacto del botón.
# 3. Después de cada acción, llamar a la función del menú (ej. submenu_materias(message)) 
#    para volver a mostrar los botones.

# Ayuda que captura si no es ningun mensaje anterior
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