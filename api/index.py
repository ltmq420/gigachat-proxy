from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing message"}), 400
    return jsonify({"reply": f"Вы сказали: {data['message']}"})

if __name__ == "__main__":
    app.run()