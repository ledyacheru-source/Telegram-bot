import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Tokens
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
GEMINI_API_KEY = "YOUR_GEMINI_KEY_HERE"

client = genai.Client(api_key=GEMINI_API_KEY)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም ሊድያ! እኔ AI Botሽ ነኝ 🤖")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_text
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"ይቅርታ ስህተት ተከስቷል: {e}")

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
