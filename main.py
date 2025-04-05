import requests
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

bot_token = '7286780819:AAHIjI48bJDWt5NDVQZt7OULb2sQWpJCahA'
bot = Bot(token=bot_token)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Salom! Men bilan suhbatlashishingiz mumkin.')

def ask_local_ai(prompt):
    url = "http://localhost:1234/v1/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "mistral-7b-instruct-v0.2",
        "prompt": f"Savol: {prompt}\nJavob:",
        "max_tokens": 200,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)
        result = response.json()
        return result.get("choices", [{}])[0].get("text", "Javob topilmadi.")
    except Exception as e:
        print("Xato:", e)
        return "AI serverda xatolik yuz berdi."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await bot.send_message(chat_id=update.message.chat_id, text="Hmmm...")
    response = ask_local_ai(user_input)
    await bot.send_message(chat_id=update.message.chat_id, text=response)

def main():
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()