from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext


def start(update: Update, context: CallbackContext):
   
    keyboard = [
        [InlineKeyboardButton("Buy Me a Coffee ☕️", url="https://buymeacoffee.com/tuonome")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

 
    update.message.reply_text(
        "Grazie per il tuo supporto! Se vuoi offrirmi un caffè, clicca sul pulsante qui sotto.",
        reply_markup=reply_markup
    )

def main():
  
    updater = Updater("TUO_TOKEN_BOT")


    updater.dispatcher.add_handler(CommandHandler("start", start))

 
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
