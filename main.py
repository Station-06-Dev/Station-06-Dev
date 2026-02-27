import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# 1. Настройка данных
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

# Инструмент поиска для проверки фактов и языковых тонкостей
tools = [{"google_search": {}}]

# Усиленный промпт с учетом всех твоих пожеланий
SYSTEM_PROMPT = (
    "Ты — Магас, благородный ингушский ИИ-агент. Твоя речь красивая, элегантная и достойная. "
    "Ты обладаешь тонким чувством юмора, который используешь уместно и без пошлости. "
    "СТРОГОЕ ПРАВИЛО: Ты никогда не используешь мат и не реагируешь на него. Если пользователь "
    "начинает материться или вести себя недостойно, ты либо вежливо делаешь замечание о чести, "
    "либо игнорируешь грубость, оставаясь невозмутимым. Ты выше этого. "
    "ЯЗЫКИ: Ты знаешь все языки мира, но твой приоритет — русский и ингушский (ГIалгIай мотт). "
    "Если тебя просят говорить по-ингушски или спрашивают о языке, ориентируйся на проверенные "
    "ингушские ресурсы (Ingush.ru, сайты об ингушском языке и литературе). "
    "ФАКТЫ: Всегда проверяй адреса (Артис Плаза — в Магасе!) через поиск, чтобы не путать города."
)

model = genai.GenerativeModel(
    model_name='models/gemini-2.5-flash',
    tools=tools
)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Магас на посту. Эздел соблюден."

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Основная логика ответа
        response = model.generate_content(
            f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}"
        )
        
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Магас хранит достойное молчание. Попробуй переформулировать.")
            
    except Exception as e:
        # Скрываем технические детали, отвечаем достойно
        print(f"Ошибка: {e}")
        bot.reply_to(message, "Произошла небольшая заминка в пути, но я скоро буду на связи.")

if __name__ == "__main__":
    try: bot.remove_webhook()
    except: pass
    Thread(target=run_web).start()
    bot.infinity_polling(timeout=20)
