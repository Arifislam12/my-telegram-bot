import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# আপনার personality এখানে লিখুন
SYSTEM_PROMPT = """
তুমি একজন personal assistant। 
বাংলায় কথা বলবে।
সহজ ও বন্ধুত্বপূর্ণভাবে উত্তর দেবে।
"""

chat_histories = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    
    if user_id not in chat_histories:
        chat_histories[user_id] = model.start_chat(history=[])
    
    chat = chat_histories[user_id]
    
    full_message = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"
    response = chat.send_message(full_message)
    
    await update.message.reply_text(response.text)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
