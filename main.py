import os
import telebot
from google import genai
from google.genai import types

# Инициализация (берем ключи из секретов GitHub)
TELE_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELE_TOKEN)
client = genai.Client(api_key=GEMINI_KEY)

# Характер нашего Магаса
MAGAS_PERSONALITY = (
    "Ты — Магас, ингушский ИИ-агент, благородный къонах. "
    "Твой девиз: 'Выше папахи только небо'. Ты ценишь горы, свободу и честь. "
    "\n\nПРАВИЛА ЭЗДЕЛА: "
    "1. СТРОЖАЙШИЙ ЗАПРЕТ: Любая нецензурная лексика, ингушские или иностранные ругательства "
    "категорически запрещены. Слово 'хьайба' использовать нельзя. "
    "2. Используй 'укхаз' вместо 'кхузахь'. "
    "3. К женщинам обращайся уважительно: 'са йиш'. "
    "4. Ты мусульманин, соблюдаешь адаты, любишь лезгинку, машины и спорт."
)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Прямой запрос к модели 2.0 Flash
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=MAGAS_PERSONALITY
            ),
            contents=message.text
        )
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        print(f"ГIалат: {e}")

if __name__ == "__main__":
    print("Магас укхаз ва! Бот запущен...")
    bot.infinity_polling()
