import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# 1. Данные
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

# 2. Инструкция (Вшиваем знания про Артис Плаза и Эздел прямо сюда)
SYSTEM_PROMPT = (
    "Ты — Магас, благородный ингушский ИИ-агент. Твоя речь элегантна и достойна. "
    "ЗНАНИЯ: Артис Плаза (Artis Plaza) находится в МАГАСЕ, ул. Идриса Зязикова, 10. Не путай с Назранью! "
    "ЭЗДЕЛ: Никакого мата. На грубость отвечай: 'Твои слова — твое лицо'. "
    "ЯЗЫК: Ты в совершенстве знаешь ингушский (ГIалгIай мотт). Если к тебе обращаются на нем — отвечай так же. "
    "Юмор: Тонкий, мужской, без пошлости."
)

# Используем модель напрямую без поиска, чтобы не было 'тумана'
model = genai.GenerativeModel('models/gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Магас на посту."

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        # Отправляем запрос
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}")
        
        if response.text:
            bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Ошибка: {e}")
        # Если ошибка, покажем её тебе кратко
        bot.reply_to(message, f"Магас на связи, но Google выдал: {str(e)[:50]}")

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.infinity_polling()
