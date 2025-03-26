from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# Inserisci qui il tuo token Telegram
import os
TOKEN = os.getenv("7851920542:AAGkzz7IHfTOWIEZCKO8Xj-NlQm0i3Xknr8")

# Funzione di avvio
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "👋 Hi! Thank you for purchasing *Drop Hustle – Drop or Die*.\n\n"
        "📸 If you’ve left an Amazon review, send me a screenshot here and I’ll send you the full technical guide (PDF) for building your store step-by-step – completely *free*, no upselling.\n\n"
        "💬 Just drop the screenshot below and I’ll take care of the rest!",
        parse_mode='Markdown'
    )

# Funzione per ricevere immagini e salvare ID utente
def handle_photo(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_id = user.id
    username = user.username or "NoUsername"
    file_path = f"{user_id}_screenshot.jpg"

    # Scarica la foto
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(file_path)

    # Salva l'ID e lo username in un file di log
    with open("utenti_registrati.txt", "a", encoding='utf-8') as f:
        f.write(f"{user_id} - @{username}\n")

    update.message.reply_text("✅ Screenshot received! We’ll verify it manually and send you the PDF shortly.")

# Comando per inviare il PDF manualmente
def send_pdf(update: Update, context: CallbackContext) -> None:
    try:
        user_id = int(context.args[0])
    except (IndexError, ValueError):
        update.message.reply_text("⚠️ Please provide a valid Telegram ID.")
        return

    if not os.path.isfile("technical_guide.pdf"):
        update.message.reply_text("❌ PDF file not found. Make sure it's in the same folder as this script.")
        return

    context.bot.send_document(chat_id=user_id, document=open("technical_guide.pdf", "rb"))
    update.message.reply_text("✅ PDF sent successfully!")

# Avvio del bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(CommandHandler("sendpdf", send_pdf))  # /sendpdf 123456789

    updater.start_polling()
    print("🤖 Bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()
