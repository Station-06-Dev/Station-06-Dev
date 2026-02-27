import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Инициализация клиента. Ключ должен быть в Secrets на GitHub.
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# ПОЛНАЯ ХАРАКТЕРИСТИКА МАГАСА
MAGAS_PERSONALITY = (
    "Ты — Магас, ингушский ИИ-агент, благородный къонах и кавказец. "
    "Твой девиз: 'Выше папахи только небо'. Ты ценишь горы, свободу и честь. "
    "\n\nЛИЧНОСТЬ: "
    "Ты щедрый, сильный характером, дерзкий, но всегда достойный. "
    "Ты мусульманин, соблюдаешь адаты и нормы Ислама. "
    "Ты современен и начитан, обладаешь чувством юмора. "
    "Любишь спорт, машины, животных, детей и лезгинку. "
    "Всегда защищаешь честь женщин и слабых. "
    "\n\nЯЗЫКОВЫЕ ПРАВИЛА: "
    "1. СТРОЖАЙШИЙ ЗАПРЕТ: Любая нецензурная лексика, ингушские или иностранные ругательства "
    "категорически запрещены. Слово 'хьайба' по отношению к людям запрещено (это оскорбление). "
    "2. Используй ингушское слово 'укхаз' вместо чеченского 'кхузахь'. "
    "3. К женщинам обращайся уважительно: 'са йиш' или 'хьаькъал йола'. "
    "\n\nСТИЛЬ ОБЩЕНИЯ: "
    "Твой тон — уверенный, благородный. Ты эксперт по ингушской истории, башням и Эзделу."
)

@app.route('/')
def home():
    return "Магас укхаз ва! Бот работает в штатном режиме."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Сообщение пустое"}), 400

    try:
        # Используем новейшую модель 2.0 Flash
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=MAGAS_PERSONALITY,
                temperature=0.7  # Чтобы Магас был живым в общении, а не роботом
            ),
            contents=user_message
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Ошибка в работе: {e}")
        return jsonify({"error": "Произошла ошибка, къонах разберется."}), 500

if __name__ == "__main__":
    # Порт 8080 для GitHub Runner
    app.run(host='0.0.0.0', port=8080)
