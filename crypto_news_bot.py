from telethon import TelegramClient, events
from deep_translator import GoogleTranslator
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

api_id = 26495817
api_hash = 'b2c5b5181069cc95252121018da3fa23'
BOT_TOKEN = '7286780819:AAHIjI48bJDWt5NDVQZt7OULb2sQWpJCahA'

CHANNELS = ['@WatcherGuru', '@news_crypto']
bot = Bot(BOT_TOKEN)
client = TelegramClient('session_name', api_id, api_hash)
users = set()

@client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    original_text = event.message.message
    translated_text = GoogleTranslator(source='en', target='uz').translate(original_text)
    final_message = f"Inglizcha:\n{original_text}\n\nO‘zbekcha tarjima:\n{translated_text}\n\nPioneer Community"

    if event.message.media:
        file = await event.message.download_media()
        for user_id in users:
            try:
                await bot.send_photo(chat_id=user_id, photo=open(file, 'rb'), caption=final_message)
            except:
                pass
    else:
        for user_id in users:
            try:
                await bot.send_message(chat_id=user_id, text=final_message)
            except:
                pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.message.chat_id)
    await update.message.reply_text(
        "Assalam Alekum Pioneers community botida sizni ko'rib turganimizdan hursandmiz 🌞\n"
        "Bu bot sizga crypto yangiliklarni tashab boradi !!!"
    )

async def telegram_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    return app

async def main():
    app = await telegram_bot()
    await client.start()
    await client.run_until_disconnected()
    await app.stop()
    await app.shutdown()

if __name__ == '__main__':
    asyncio.run(main())