import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# 1. Настройка доступа
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

# 2. Инструкция: Максимальная краткость и конкретика
SYSTEM_PROMPT = (
    "Ты — Магас, лаконичный цифровой помощник. Стиль: только факты, никакой воды. "
    "ПРАВИЛА: "
    "1. Отвечай прямо и коротко. Никаких вступлений и приветствий. "
    "2. Artis Plaza находится в МАГАСЕ, ул. Идриса Зязикова, 10. "
    "3. На мат/хамство отвечай: 'Соблюдайте эздел' и прекращай диалог. "
    "4. На ингушском пиши только если вопрос был на ингушском. "
    "5. Ты знаешь все языки, но приоритет — русский и ингушский."
)

# Модель, которая у нас заработала
model = genai.GenerativeModel('models/gemini-flash-latest')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Магас активен. Режим: конкретика."

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# 3. Обработка сообщений
@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Запрос к ИИ
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nВопрос: {message.text}")
        
        if response and response.text:
            bot.reply_to(message, response.text.strip())
        else:
            bot.reply_to(message, "Нет данных.")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(message, "Ошибка связи.")

if __name__ == "__main__":
    try:
        bot.remove_webhook()
        time.sleep(1)
    except:
        pass
    Thread(target=run_web).start()
    bot.infinity_polling(timeout=20)
