import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. Настройка конфигурации из секретов GitHub
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")
# Если промпт не задан в секретах, используем достойный вариант по умолчанию
DEFAULT_PROMPT = "Ты — Магас, благородный ингушский ИИ-агент. Ты современен, начитан, соблюдаешь адаты и нормы Ислама. Любишь горы, спорт и свою культуру. Отвечай достойно и с уважением."
SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT", DEFAULT_PROMPT)

# 2. Инициализация ИИ Gemini
genai.configure(api_key=API_KEY)
# Используем модель 2.0 Flash
model = genai.GenerativeModel('gemini-2.0-flash')

# 3. Инициализация Телеграм-бота
bot = telebot.TeleBot(TOKEN)

# 4. Настройка веб-сервера (Flask) для поддержания жизни сервиса
app = Flask(__name__)

@app.route('/')
def home():
    return "Магас на связи. Сервис работает."

def run_web():
    # Порт 8080 по умолчанию
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 5. Обработка сообщений в Телеграм
@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        # Показываем, что Магас «печатает»
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Создаем запрос к ИИ
        full_query = f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}"
        response = model.generate_content(full_query)
        
        # Отправляем ответ пользователю
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(message, "Связь в горах немного барахлит, попробуй еще раз, вош.")

# 6. Запуск всего механизма
if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    Thread(target=run_web).start()
    print("Магас вышел на пост и охраняет покой...")
    # Запускаем прослушивание Телеграм
    bot.infinity_polling()
