import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# 1. Настройка конфигурации
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")
# Наш благородный системный промпт
SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT", "Ты — Магас, благородный ингушский ИИ-агент. Ты современен, начитан, соблюдаешь адаты и нормы Ислама. Отвечай достойно, кратко и по делу.")

# 2. Инициализация ИИ (Переходим на более стабильную 1.5 Flash)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Инициализация Телеграм-бота
bot = telebot.TeleBot(TOKEN)

# 4. Настройка Flask
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
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Запрос к ИИ
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}")
        
        # Небольшая пауза, чтобы не злить лимиты Google
        time.sleep(1)
        
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Ошибка: {e}")
        # Если всё же лимит превышен, вежливо просим подождать
        if "429" in str(e):
            bot.reply_to(message, "Йиш, слишком много запросов. Подожди минуту, Магасу нужно совершить дуа.")
        else:
            bot.reply_to(message, "Связь в горах барахлит, попробуй чуть позже.")

if __name__ == "__main__":
    Thread(target=run_web).start()
    print("Магас перешел на 1.5 Flash и готов к службе...")
    bot.infinity_polling()
