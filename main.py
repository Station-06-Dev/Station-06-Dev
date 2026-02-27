import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# 1. Данные из секретов
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

# 2. Инструкция Магаса
SYSTEM_PROMPT = (
    "Ты — Магас, благородный ингушский ИИ-агент. Твоя речь элегантна и достойна. "
    "ЗНАНИЯ: Артис Плаза (Artis Plaza) находится в МАГАСЕ, ул. Идриса Зязикова, 10. "
    "ЭЗДЕЛ: Никакого мата. На грубость отвечай: 'Твои слова — твое лицо'. "
    "ЯЗЫК: Ты знаешь ингушский (ГIалгIай мотт). Если обращаются на нем — отвечай так же. "
    "Будь мудрым, кратким и современным. Используй юмор только к месту."
)

# 3. Инициализация (Используем универсальный адрес модели из твоего списка)
model = genai.GenerativeModel('models/gemini-flash-latest')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Магас на посту. Система стабилизирована."

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Отправляем запрос напрямую
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}")
        
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Магас задумался. Попробуй еще раз.")
            
    except Exception as e:
        # Показываем чуть больше текста ошибки для диагностики
        bot.reply_to(message, f"Заминка: {str(e)[:100]}")

if __name__ == "__main__":
    try:
        bot.remove_webhook()
        time.sleep(1)
    except:
        pass
        
    Thread(target=run_web).start()
    bot.infinity_polling(timeout=20)
