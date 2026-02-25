import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()

app = Flask(__name__)

GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")
if not GIGACHAT_CREDENTIALS:
    raise ValueError("No GIGACHAT_CREDENTIALS set")

try:
    giga = GigaChat(
        credentials=GIGACHAT_CREDENTIALS,
        scope='GIGACHAT_API_PERS',
        verify_ssl_certs=False
    )
    init_error = None
except Exception as e:
    giga = None
    init_error = str(e)

@app.route("/chat", methods=["POST"])
def chat():
    if giga is None:
        return jsonify({"error": f"GigaChat initialization failed: {init_error}"}), 500

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_message = data["message"]

    try:
       response = giga.chat(messages=[{"role": "user", "content": user_message}])
        ai_message = response.choices[0].message.content
        return jsonify({"reply": ai_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()