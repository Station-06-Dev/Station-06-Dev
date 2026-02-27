import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# 1. Настройка данных
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")

SYSTEM_PROMPT = (
    "Ты — Магас, благородный ингушский ИИ-агент, кавказец. Ты современен, начитан, "
    "соблюдаешь адаты и нормы Ислама. Твой девиз: 'Выше папахи только небо'."
)

# 2. Инициализация Google Gemini (Используем максимально точное имя модели)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

# 3. Инициализация Телеграм-бота
bot = telebot.TeleBot(TOKEN)

# 4. Flask-сервер
app = Flask(__name__)

@app.route('/')
def home():
    return "Магас на посту."

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 5. Главный обработчик
@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        full_query = f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}"
        response = model.generate_content(full_query)
        
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Магас задумался. Попробуй еще раз.")
            
    except Exception as e:
        error_str = str(e)
        # Если снова 404, бот сам подскажет
        bot.reply_to(message, f"Магас на связи, но Google капризничает:\n{error_str[:100]}")

# 6. Запуск
if __name__ == "__main__":
    try:
        bot.remove_webhook()
        time.sleep(1)
    except:
        pass
    Thread(target=run_web).start()
    print("Магас заступил на дежурство...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
