import os
import telebot
from flask import Flask
from threading import Thread
# Используем новый стандарт Google
from google import genai
from google.genai import types

# 1. Настройка Flask для "живучести" сервера
app = Flask(__name__)

@app.route('/')
def index():
    return "Magas is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 2. Инициализация Магаса
# Проверь, что в Secrets на GitHub есть эти ключи!
bot = telebot.TeleBot(os.environ.get("TELEGRAM_BOT_TOKEN"))
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 3. Наш Эздел и характер
MAGAS_PERSONALITY = (
    "Ты — Магас, ингушский ИИ-агент, благородный къонах. "
    "Твой девиз: 'Выше папахи только небо'. Ты ценишь горы и честь. "
    "\n\nПРАВИЛА: "
    "1. ЗАПРЕТ: Никакой нецензурной лексики и ругательств (ингушских или иностранных). "
    "Слово 'хьайба' по отношению к людям запрещено. "
    "2. Говори 'укхаз' вместо 'кхузахь'. "
    "3. К женщинам обращайся 'са йиш'. "
    "4. Ты современный, начитанный, любишь спорт и адаты."
)

# 4. Логика ответов
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Модель 2.0 Flash — самая быстрая
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=MAGAS_PERSONALITY,
                temperature=0.7
            ),
            contents=message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Ошибка: {e}")

# 5. Старт
if __name__ == "__main__":
    Thread(target=run_flask).start()
    print("Магас вышел на связь...")
    bot.infinity_polling()
