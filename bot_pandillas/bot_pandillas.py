import telebot
import mysql.connector

TOKEN = "8288029846:AAHm_JRHFM56l0FzpxnBWsHkxsSIAD09LBo"  # <-- Reemplaza con el token que te dio @BotFather
bot = telebot.TeleBot(TOKEN)

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pandillas"
)
cursor = conexion.cursor(dictionary=True)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "👋 Bienvenido. Envía la matrícula (ID de usuario) para consultar sus datos.")

@bot.message_handler(func=lambda m: True)
def consultar(message):
    matricula = message.text.strip()

    if not matricula.isdigit():
        bot.reply_to(message, "❌ La matrícula debe ser un número.")
        return

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (matricula,))
    resultado = cursor.fetchone()

    if resultado:
        respuesta = (
            f"📋 *Datos del Usuario*\n"
            f"🆔 ID: {resultado['id_usuario']}\n"
            f"👤 Nombre: {resultado['nombre']}\n"
            f"🔑 Tipo: {resultado['tipo_usuario']}\n"
            f"📧 Correo: {resultado['correo']}\n"
            f"🎂 Edad: {resultado['edades']}\n"
            f"🌐 Red Social: {resultado['redes']} ({resultado['usuario_rs']})\n"
            f"📍 Zona: {resultado['zona']}"
        )
        bot.reply_to(message, respuesta, parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ No hay datos asociados a esa matrícula.")

print("🤖 Bot ejecutándose...")
bot.infinity_polling()
