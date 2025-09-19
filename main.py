from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = open("token.txt").read()

# Definir los manejadores de comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía un mensaje de bienvenida cuando se emite el comando /start."""
    await update.message.reply_text('Omedeto puto-san')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía un mensaje de ayuda cuando se emite el comando /help."""
    await update.message.reply_text('Atiendo boludos. No ves que atiendo boludos?')

# Procesa cualquier mensaje de texto que no sea un comando.
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde al mensaje del usuario con el mismo texto."""
    await update.message.reply_text(f"Has escrito: {update.message.text}")

# Captura y reporta cualquier error que ocurra durante el manejo de actualizaciones.
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Imprime un error en la consola."""
    print(f"Update {update} causó el error: {context.error}")


def main() -> None:
    """Inicia el bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Añade un manejador para mensajes de texto (no comandos)
    # El filtro 'filters.TEXT' asegura que solo procese mensajes de texto.
    # El '~filters.COMMAND' excluye los comandos para evitar duplicación.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Añade el manejador de errores
    application.add_error_handler(error_handler)

    # Inicia el polling del bot para recibir actualizaciones de Telegram
    # El polling es un método que comprueba si hay nuevos mensajes o interacciones.
    application.run_polling()

if __name__ == '__main__':
    main()