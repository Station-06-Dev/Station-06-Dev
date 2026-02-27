import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# 1. Данные из секретов
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")

# Настройки Магаса
SYSTEM_PROMPT = (
    "Ты — Магас, благородный ингушский ИИ-агент, кавказец. Ты современен, начитан, "
    "соблюдаешь адаты и нормы Ислама. Твой девиз: 'Выше папахи только небо'. "
    "Отвечай кратко, мудро и с уважением."
)

# 2. Инициализация ИИ (Используем модель 2.5 Flash из твоего списка)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): 
    return "Магас на посту. Модель 2.5 Flash активна."

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 3. Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Запрос к самой новой модели
        full_query = f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}"
        response = model.generate_content(full_query)
        
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Магас задумался. Попробуй еще раз.")
            
    except Exception as e:
        bot.reply_to(message, f"Ошибка связи: {str(e)[:100]}")

# 4. Запуск системы
if __name__ == "__main__":
    try:
        bot.remove_webhook()
        time.sleep(1)
    except:
        pass
        
    Thread(target=run_web).start()
    print("Магас заступил на дежурство (v2.5 Flash)...")
    bot.infinity_polling(timeout=20)
