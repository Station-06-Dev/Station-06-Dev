import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# 1. Настройка данных из секретов
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")

SYSTEM_PROMPT = (
    "Ты — Магас, благородный ингушский ИИ-агент, кавказец. Ты современен, начитан, "
    "соблюдаешь адаты и нормы Ислама. Любишь горы, спорт, машины и лезгинку. "
    "Твой девиз: 'Выше папахи только небо'. Защищай честь женщин и слабых. "
    "Отвечай достойно, с уважением и легким кавказским колоритом."
)

# 2. Инициализация Google Gemini (Модель gemini-pro самая стабильная)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# 3. Инициализация Телеграм-бота
bot = telebot.TeleBot(TOKEN)

# 4. Flask-сервер для "вечной" жизни бота
app = Flask(__name__)

@app.route('/')
def home():
    return "Магас на связи. Сервер работает."

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 5. Главный обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        # Статус "печатает..."
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Формируем запрос к ИИ
        full_query = f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}"
        response = model.generate_content(full_query)
        
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Магас задумался. Попробуй еще раз, йиш.")
            
    except Exception as e:
        error_str = str(e)
        print(f"Ошибка: {error_str}")
        
        # Диагностика для пользователя
        if "API_KEY_INVALID" in error_str or "403" in error_str:
            diag = "❌ Ошибка в ключе API. Проверь секреты на GitHub."
        elif "429" in error_str:
            diag = "⏳ Лимиты превышены. Подожди 5 минут."
        else:
            diag = f"⚠️ Заминка: {error_str[:50]}"
            
        bot.reply_to(message, f"Магас на связи, но случилась проблема:\n\n{diag}")

# 6. Запуск
if __name__ == "__main__":
    # Сброс старых соединений
    try:
        bot.remove_webhook()
        time.sleep(1)
    except:
        pass
    
    # Запуск Flask сервера в фоне
    Thread(target=run_web).start()
    
    print("Магас заступил на дежурство (модель gemini-pro)...")
    # Запуск бота на прослушивание
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
