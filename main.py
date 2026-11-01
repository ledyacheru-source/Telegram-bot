import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Tokens from Render
9194333229:AAGuugJ5e8G_4c3AVGpaiwkR1rXH3IkPUMAQ.Ab8RN6KMeNKteWYf5Ukm3g-CP7N7l9_JzdXNH82M6O0d21YJCg
AQ.Ab8RN6KMeNKteWYf5Ukm3g-CP7N7l9_JzdXNH82M6O0d21YJCg
client = genai.Client(api_key=GEMINI_API_KEY)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! እኔ ሎይዴ ነኝ! 🙏")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_text
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"ችግር: {e}")

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
