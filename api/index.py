import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()

app = Flask(__name__)

GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")
if not GIGACHAT_CREDENTIALS:
    raise ValueError("No GIGACHAT_CREDENTIALS")

giga = GigaChat(credentials=GIGACHAT_CREDENTIALS, verify_ssl_certs=False)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing message"}), 400
    user_message = data["message"]
    try:
        # Передаём список сообщений
        response = giga.chat([{"role": "user", "content": user_message}])
        ai_message = response.choices[0].message.content
        return jsonify({"reply": ai_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if name == "__main__":
    app.run()