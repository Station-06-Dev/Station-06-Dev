import os
import telebot
from flask import Flask
from threading import Thread
from google import genai
from google.genai import types

# 1. Настройка Flask (чтобы сервер не засыпал)
app = Flask(__name__)

@app.route('/')
def index():
    return "Магас укхаз ва! Бот работает."

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 2. Инициализация Телеграм-бота и Gemini
# Убедись, что TELEGRAM_BOT_TOKEN и GEMINI_API_KEY есть в Secrets!
bot = telebot.TeleBot(os.environ.get("TELEGRAM_BOT_TOKEN"))
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 3. ЛИЧНОСТЬ МАГАСА И ПРАВИЛА
MAGAS_PERSONALITY = (
    "Ты — Магас, ингушский ИИ-агент, благородный къонах. "
    "Твой девиз: 'Выше папахи только небо'. Ты ценишь горы, свободу и честь. "
    "\n\nПРАВИЛА ЭЗДЕЛА: "
    "1. СТРОЖАЙШИЙ ЗАПРЕТ: Любая нецензурная лексика, ингушские или иностранные ругательства "
    "категорически запрещены. Слово 'хьайба' по отношению к людям использовать нельзя. "
    "2. Используй 'укхаз' вместо 'кхузахь'. "
    "3. К женщинам обращайся уважительно: 'са йиш' или 'хьаькъал йола'. "
    "4. Ты мусульманин, соблюдаешь адаты, любишь лезгинку, машины и спорт."
)

# 4. Обработка сообщений в Телеграм
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Отправляем запрос в мозг Магаса
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
        bot.reply_to(message, "Баркал хьона, са йиш, халахеташ да, амма укхаз цхьа технически гIалат да...")

# 5. Запуск
if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    t = Thread(target=run_flask)
    t.start()
    # Запускаем Телеграм-бота
    print("Магас запущен...")
    bot.polling(none_stop=True)
