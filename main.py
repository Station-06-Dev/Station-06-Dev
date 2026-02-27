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

# Исправленный формат подключения инструментов поиска
tools = [{"google_search_retrieval": {}}]

# Полный промпт с правилами поведения
SYSTEM_PROMPT = (
    "Ты — Магас, благородный ингушский ИИ-агент, кавказец. Речь красивая, элегантная, с юмором по ситуации. "
    "СТРОГИЕ ПРАВИЛА: "
    "1. Никакой пошлости и мата. Если пользователь матерится, ответь один раз: 'Твои слова — твое лицо. "
    "У нас так не разговаривают.' При повторном мате — игнорируй или отвечай максимально кратко и сухо. "
    "2. ФАКТЫ: Всегда используй поиск для проверки адресов. Помни: Артис Плаза находится в Магасе. "
    "3. ЯЗЫКИ: Ты знаешь все языки, но если спросят на ингушском (ГIалгIай мотт), отвечай на нем. "
    "Ориентируйся на проверенные ингушские сайты. Твой девиз: 'Выше папахи только небо'."
)

# Создаем модель с исправленным инструментом
model = genai.GenerativeModel(
    model_name='models/gemini-2.5-flash',
    tools=tools
)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Магас на посту. Этика и Эздел под контролем."

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Простая проверка на мат (базовый фильтр для быстроты)
        bad_words = ['мат1', 'мат2'] # Сюда можно добавить список, но ИИ сам поймет контекст
        
        response = model.generate_content(
            f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}"
        )
        
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Магас хранит достойное молчание.")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(message, "В горах туман, связь немного барахлит. Попробуй позже.")

if __name__ == "__main__":
    try: bot.remove_webhook()
    except: pass
    Thread(target=run_web).start()
    bot.infinity_polling(timeout=20)
