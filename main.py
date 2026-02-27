import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# 1. Конфигурация
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")
SYSTEM_PROMPT = "Ты — Магас, благородный ингушский ИИ-агент. Ты современен, начитан, соблюдаешь адаты и нормы Ислама. Отвечай достойно."

# 2. Инициализация ИИ
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Инициализация Бота
bot = telebot.TeleBot(TOKEN)

# 4. Flask для жизни сервиса
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
        
        # Запрос к ИИ
        full_query = f"{SYSTEM_PROMPT}\n\nUser: {message.text}"
        response = model.generate_content(full_query)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Магас задумался, попробуй еще раз.")
            
    except Exception as e:
        err = str(e)
        print(f"Ошибка: {err}")
        if "429" in err:
            bot.reply_to(message, "Йиш, лимиты превышены. Подожди пару минут.")
        else:
            bot.reply_to(message, f"Связь барахлит. (Код: {err[:20]})")

# 6. Запуск
if __name__ == "__main__":
    # Сброс старых сессий
    try:
        bot.remove_webhook()
    except:
        pass
        
    time.sleep(1)
    
    # Запуск сервера
    Thread(target=run_web).start()
    
    print("Магас заступил на дежурство...")
    # Запуск бота
    bot.infinity_polling()
