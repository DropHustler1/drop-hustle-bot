from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from flask import Flask
import threading
import os

# Recupera il token dall'ambiente (Render → Environment Variables)
TOKEN = os.getenv("BOT_TOKEN")

# Inizializzazione di Flask per mantenere viva l'app su Render
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ DropHustler Bot is running!"

# Funzione avvio
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "👋 Hi! Thank you for purchasing *Drop Hustle – Drop or Die*.\n\n"
        "📸 If you’ve left an Amazon review, send me a screenshot here and I’ll send you the full technical guide (PDF) for building your store step-by-step – completely *free*, no upselling.\n\n"
        "💬 Just drop the screenshot below and I’ll take care of the rest!",
        parse_mode='Markdown'
    )

# Ricezione screenshot
def handle_photo(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    file_path = f"{user.id}_screenshot.jpg"
    photo_file.download(file_path)

    with open("received_ids.txt", "a") as file:
        file.write(f"{user.username} | {user.id}\n")

    update.message.reply_text("✅ Screenshot received! We’ll verify it manually and send you the PDF shortly.")

# Comando admin per invio PDF
def send_pdf(update: Update, context: CallbackContext) -> None:
    try:
        user_id = int(context.args[0])
    except (IndexError, ValueError):
        update.message.reply_text("⚠️ Please provide a valid Telegram ID.")
        return

    if not os.path.isfile("technical_Guide.pdf"):
        update.message.reply_text("❌ PDF file not found.")
        return

    context.bot.send_document(chat_id=user_id, document=open("technical_Guide.pdf", "rb"))
    update.message.reply_text("✅ PDF sent successfully!")

# Funzione per avviare il bot
def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(CommandHandler("sendpdf", send_pdf))

    updater.start_polling()
    updater.idle()

# Avvio parallelo Flask + Bot
if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
