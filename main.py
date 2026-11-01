from flask import Flask
import threading
import os
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN", "91943...የእርስዎን ሙሉ Token")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8...የእርስዎን AQ Key")

app = Flask(__name__)
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/')
def home():
    return "Bot is Running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! እኔ ዝግጁ ነኝ!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_text
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
        print(f"Gemini Error: {e}")

def run_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.run_polling()

threading.Thread(target=run_bot).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
