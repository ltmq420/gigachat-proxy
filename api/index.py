import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()

app = Flask(__name__)

GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")
if not GIGACHAT_CREDENTIALS:
    raise ValueError("Не задана переменная окружения GIGACHAT_CREDENTIALS")

# Инициализация клиента с нужным scope
giga = GigaChat(
    credentials=GIGACHAT_CREDENTIALS,
    scope='GIGACHAT_API_PERS',   # для физических лиц
    verify_ssl_certs=False
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_message = data["message"]

    try:
        # Пробуем первый способ: передаём строку
        response = giga.chat(user_message)
        ai_message = response.choices[0].message.content
        return jsonify({"reply": ai_message})
    except Exception as e:
        # Если не вышло, пробуем передать список сообщений
        try:
            response = giga.chat([{"role": "user", "content": user_message}])
            ai_message = response.choices[0].message.content
            return jsonify({"reply": ai_message})
        except Exception as e2:
            return jsonify({"error": str(e2)}), 500

if __name__ == "__main__":
    app.run(debug=False)