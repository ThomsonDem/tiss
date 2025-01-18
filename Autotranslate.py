from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from googletrans import Translator


translator = Translator()
group_settings = {}


def set_language(update: Update, context: CallbackContext):
   
    chat_id = update.message.chat_id
    user = update.message.from_user

    
    admins = context.bot.get_chat_administrators(chat_id)
    if user.id not in [admin.user.id for admin in admins]:
        update.message.reply_text("Solo gli admin possono impostare la lingua.")
        return

  
    if len(context.args) != 1:
        update.message.reply_text("Usa il comando così: /setlang [codice lingua]. Ad esempio: /setlang it")
        return

   
    lang_code = context.args[0]
    group_settings[chat_id] = lang_code
    update.message.reply_text(f"Lingua impostata su: {lang_code}")


def translate_message(update: Update, context: CallbackContext):
  
    chat_id = update.message.chat_id
    original_text = update.message.text

   
    target_lang = group_settings.get(chat_id, 'it') 

  
    detected_lang = translator.detect(original_text).lang

    
    if detected_lang != target_lang:
        translated_text = translator.translate(original_text, src=detected_lang, dest=target_lang).text
      
        update.message.reply_text(f"Traduzione: {translated_text}")


def main():
    
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    updater = Updater(TOKEN, use_context=True)

   
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("setlang", set_language))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_message))

    # Avvia il bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
