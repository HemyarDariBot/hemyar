import os
import threading
from flask import Flask
import telebot

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

@app.route("/")
def home():
    return "Hemyar bot is running!"

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "سلام! به همیار خوش آمدی.\nپیامت را بفرست تا پاسخ بدهم."
    )

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(
        message,
        "دستورهای موجود:\n/start - شروع ربات\n/help - راهنما"
    )

@bot.message_handler(func=lambda message: True)
def reply_to_message(message):
    bot.reply_to(message, "پیامت را دریافت کردم: " + message.text)

def run_bot():
    bot.delete_webhook()
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
