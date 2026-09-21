import os
import threading
from flask import Flask
import telebot
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/")
def home():
    return "Hemyar AI bot is running!"

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "سلام! من همیار هوشمند دری هستم.\nهر پرسشی داری بفرست."
    )

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(
        message,
        "پیامت را به زبان دری بفرست تا پاسخ بدهم."
    )

@bot.message_handler(func=lambda message: True)
def answer(message):
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions=(
                "تو یک دستیار مفید و مؤدب هستی. "
                "همیشه به زبان دری ساده و طبیعی پاسخ بده."
            ),
            input=message.text
        )

        bot.reply_to(message, response.output_text)

    except Exception:
        bot.reply_to(
            message,
            "در پاسخ‌دادن مشکل پیش آمد. لطفاً دوباره تلاش کن."
        )

def run_bot():
    bot.delete_webhook()
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
