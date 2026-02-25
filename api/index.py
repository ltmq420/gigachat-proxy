import sys
import traceback

# Попытка импорта с логированием ошибок
try:
    import os
    from flask import Flask, request, jsonify
    from dotenv import load_dotenv
    from gigachat import GigaChat
except Exception as e:
    print("IMPORT ERROR:", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)  # остановить загрузку

load_dotenv()

app = Flask(__name__)

GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")
if not GIGACHAT_CREDENTIALS:
    print("No GIGACHAT_CREDENTIALS set", file=sys.stderr)
    raise ValueError("No GIGACHAT_CREDENTIALS set")

# Инициализация клиента GigaChat с отловом ошибок
try:
    giga = GigaChat(
        credentials=GIGACHAT_CREDENTIALS,
        scope='GIGACHAT_API_PERS',
        verify_ssl_certs=False
    )
    init_error = None
    print("GigaChat initialized successfully", file=sys.stderr)
except Exception as e:
    giga = None
    init_error = str(e)
    print("GigaChat init error:", init_error, file=sys.stderr)
    traceback.print_exc(file=sys.stderr)

@app.route("/chat", methods=["POST"])
def chat():
    if giga is None:
        return jsonify({"error": f"GigaChat initialization failed: {init_error}"}), 500

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_message = data["message"]

    try:
        response = giga.chat({"messages": [{"role": "user", "content": user_message}]})
        ai_message = response.choices[0].message.content
        return jsonify({"reply": ai_message})
    except Exception as e:
        print("Chat error:", str(e), file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()