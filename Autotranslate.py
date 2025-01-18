from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from googletrans import Translator

# Inizializza il traduttore e il database delle lingue per i gruppi
translator = Translator()
group_settings = {}

# Funzione per impostare la lingua di traduzione
def set_language(update: Update, context: CallbackContext):
    # Controlla se l'utente è un admin
    chat_id = update.message.chat_id
    user = update.message.from_user

    # Verifica se l'utente è admin
    admins = context.bot.get_chat_administrators(chat_id)
    if user.id not in [admin.user.id for admin in admins]:
        update.message.reply_text("Solo gli admin possono impostare la lingua.")
        return

    # Controlla se è stato fornito un codice lingua
    if len(context.args) != 1:
        update.message.reply_text("Usa il comando così: /setlang [codice lingua]. Ad esempio: /setlang it")
        return

    # Imposta la lingua
    lang_code = context.args[0]
    group_settings[chat_id] = lang_code
    update.message.reply_text(f"Lingua impostata su: {lang_code}")

# Funzione per tradurre i messaggi
def translate_message(update: Update, context: CallbackContext):
    # Ottieni il messaggio originale
    chat_id = update.message.chat_id
    original_text = update.message.text

    # Ottieni la lingua impostata per il gruppo
    target_lang = group_settings.get(chat_id, 'it')  # Predefinito: italiano

    # Rileva la lingua del messaggio
    detected_lang = translator.detect(original_text).lang

    # Se la lingua è diversa da quella impostata, traduci
    if detected_lang != target_lang:
        translated_text = translator.translate(original_text, src=detected_lang, dest=target_lang).text
        # Rispondi con la traduzione
        update.message.reply_text(f"Traduzione: {translated_text}")

# Configurazione del bot
def main():
    # Inserisci il tuo token API qui
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    updater = Updater(TOKEN, use_context=True)

    # Aggiungi i gestori di comandi e messaggi
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("setlang", set_language))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_message))

    # Avvia il bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
