from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Comando /start
def start(update: Update, context: CallbackContext):
    # Crea il pulsante "Buy Me a Coffee"
    keyboard = [
        [InlineKeyboardButton("Buy Me a Coffee ☕️", url="https://buymeacoffee.com/tuonome")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Invia il messaggio con il pulsante
    update.message.reply_text(
        "Grazie per il tuo supporto! Se vuoi offrirmi un caffè, clicca sul pulsante qui sotto.",
        reply_markup=reply_markup
    )

def main():
    # Inserisci il tuo token del bot
    updater = Updater("TUO_TOKEN_BOT")

    # Aggiungi il comando /start
    updater.dispatcher.add_handler(CommandHandler("start", start))

    # Avvia il bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
