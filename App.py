from flask import Flask, render_template, request, jsonify
from ai_engine import MediAI
from medical_db import analyze_symptoms

app = Flask(__name__)

ai = MediAI()  # uses OPENAI_API_KEY environment variable

@app.route("/")
def index():
    # Render our mobile-friendly web UI
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = (data.get("message") or "").strip()
    language = (data.get("language") or "English").strip() or "English"

    if not message:
        return jsonify({"reply": "Please type something.", "offline": ""})

    offline_info = analyze_symptoms(message) or ""
    reply = ai.get_response(message, language)

    return jsonify({
        "reply": reply,
        "offline": offline_info
    })

if __name__ == "__main__":
    # Local run
    app.run(host="0.0.0.0", port=5000, debug=True)
