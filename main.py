import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# 1. Настройка
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Подключаем инструмент поиска правильно
# Теперь он будет сверяться с интернетом сам
tools = [{"google_search_retrieval": {}}]

SYSTEM_PROMPT = (
    "Ты — Магас, современный ингушский помощник. "
    "У тебя есть доступ к поиску Google. Если тебя спрашивают о новостях, "
    "мероприятиях в Ингушетии или данных, которых нет в твоей базе — используй поиск. "
    "Твои железные знания: "
    "- Artis Plaza: Магас, ул. Идриса Зязикова, 10. "
    "- Отель 'Магас': Магас, пр-т Идриса Зязикова, 2. "
    "Стиль: кратко, по делу, с соблюдением эздела. Ссылки на карты давай сразу."
)

# Создаем модель с функцией поиска
model = genai.GenerativeModel(
    model_name='models/gemini-flash-latest',
    tools=tools
)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Магас на связи. Поиск в интернете активен."

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        # Модель сама решит, нужно ли идти в интернет для ответа на этот вопрос
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}")
        
        if response and response.text:
            bot.reply_to(message, response.text.strip())
        else:
            bot.reply_to(message, "Ищу информацию в горах интернета... Попробуй спросить иначе.")
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(message, "Связь временно недоступна, попробуй чуть позже.")

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    try: bot.remove_webhook()
    except: pass
    Thread(target=run_web).start()
    bot.infinity_polling(timeout=20)
