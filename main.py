import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# 1. Настройка конфигурации из секретов
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")
# Твой благородный системный промпт
DEFAULT_PROMPT = "Ты — Магас, благородный ингушский ИИ-агент. Ты современен, начитан, соблюдаешь адаты и нормы Ислама. Отвечай достойно и с уважением."
SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT", DEFAULT_PROMPT)

# 2. Инициализация ИИ (Самая легкая и быстрая модель)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-8b')

# 3. Инициализация Телеграм-бота
bot = telebot.TeleBot(TOKEN)

# 4. Настройка Flask для поддержания жизни на сервере
app = Flask(__name__)

@app.route('/')
def home():
    return "Магас на посту. Связь стабильна."

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 5. Обработка сообщений
@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        # Показываем статус "печатает"
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Формируем запрос
        prompt = f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}"
        response = model.generate_content(prompt)
        
        # Если ответ пустой
        if not response.text:
            bot.reply_to(message, "Магас задумался и не смог подобрать слов. Попробуй еще раз.")
            return

        bot.reply_to(message, response.text)
        
    except Exception as e:
        error_msg = str(e)
        print(f"Ошибка: {error_msg}")
        
        if "429" in error_msg:
            bot.reply_to(message, "Йиш, лимиты Google временно исчерпаны. Магасу нужно 5 минут на отдых.")
        elif "API_KEY_INVALID" in error_msg:
            bot.reply_to(message, "Ошибка: Кажется, API ключ указан неверно. Проверь секреты в GitHub.")
        else:
            bot.reply_to(message, f"Связь барахлит (Ошибка: {error_msg[:50]}...)")

# 6. Запуск
if __name__ == "__main__":
    # Очищаем старые соединения перед стартом
    bot.remove_webhook()
    time.sleep(1)
    
    # Запуск веб-сервера
    Thread(target=run_web).start()
    
    print("Магас (версия 8b) вышел на связь...")
    # Бесконечный цикл работы
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
