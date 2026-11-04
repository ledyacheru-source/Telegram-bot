from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")


@app.route('/')
def home():
    return "Demeku Bot Live"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        try:
            headers = {"Authorization": "Bearer " + GROQ_KEY}
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": text}]
            }
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=20)
            reply = r.json()['choices'][0]['message']['content']
        except Exception as e:
            reply = "እንደገና ንገረኝ, " + str(e)
        requests.post("https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage", json={"chat_id": chat_id, "text": reply})
    return "ok"

@app.route('/setwebhook')
def sethook():
    url = "https://" + request.host + "/"
    r = requests.get("https://api.telegram.org/bot" + BOT_TOKEN + "/setWebhook", params={"url": url})
    return r.text
