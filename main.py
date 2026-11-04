from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

@app.route('/')
def home():
    return "Demeku Bot Live - OK"

@app.route('/setwebhook')
def sethook():
    url = "https://telegram-bot-bu8e.onrender.com/"
    r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={url}")
    return r.text

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data or 'message' not in data:
        return "ok"
    chat_id = data['message']['chat']['id']
    text = data['message'].get('text','')
    try:
        h = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        p = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": text}]}
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=h, json=p, timeout=20)
        reply = r.json()['choices'][0]['message']['content']
    except Exception as e:
        reply = "Try again - error"
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": reply})
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
