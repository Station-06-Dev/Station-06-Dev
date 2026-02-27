import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Разведка запущена."

@bot.message_handler(func=lambda message: True)
def get_models(message):
    try:
        # Получаем список всех доступных моделей для твоего ключа
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        response_text = "Твоему ключу доступны эти модели:\n\n" + "\n".join(available_models)
        bot.reply_to(message, response_text)
    except Exception as e:
        bot.reply_to(message, f"Даже разведка не удалась: {str(e)}")

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.infinity_polling()
