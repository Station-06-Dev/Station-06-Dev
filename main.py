import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# 1. Данные из секретов
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")

# 2. Инициализация ИИ с ПРЯМЫМ указанием версии
genai.configure(api_key=API_KEY)

# Мы используем ПОЛНОЕ имя модели, которое понимает версия 3.1
# Это исключает ошибку 404
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-002')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): 
    return "Магас на посту. Модель 1.5 Flash 002 активна."

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Системная установка прямо в запросе
        prompt = f"Ты — благородный Магас, ингушский ИИ. Отвечай кратко и достойно. \nВопрос: {message.text}"
        
        response = model.generate_content(prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Магас задумался, но ответа не пришло. Попробуй еще раз.")
            
    except Exception as e:
        # Выводим подробную ошибку, чтобы понять, если путь снова не тот
        bot.reply_to(message, f"Ответ системы: {str(e)}")

if __name__ == "__main__":
    # Очистка и запуск
    try:
        bot.remove_webhook()
        time.sleep(1)
    except:
        pass
        
    Thread(target=run_web).start()
    print("Магас заступил на дежурство...")
    bot.infinity_polling(timeout=20)
