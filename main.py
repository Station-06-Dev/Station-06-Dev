import os
import telebot
from google import genai
from flask import Flask
from threading import Thread

# Загрузка конфигурации из секретов GitHub
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")
SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT", "Ты — Магас, благородный ингушский ИИ-агент. Помогай людям, соблюдая адаты.")

# Инициализация бота и клиента ИИ
bot = telebot.TeleBot(TOKEN)
client = genai.Client(api_key=API_KEY)

# Настройка Flask (чтобы сервис не засыпал)
app = Flask(__name__)

@app.route('/')
def home():
    return "Magas is online"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        # Запрос к Gemini 2.0
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}"
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(message, "Вош/Йиш, связь в горах барахлит. Попробуй еще раз!")

if __name__ == "__main__":
    # Запуск веб-сервера в отдельном потоке
    Thread(target=run_web).start()
    print("Магас вышел на пост...")
    # Запуск бота
    bot.infinity_polling()
