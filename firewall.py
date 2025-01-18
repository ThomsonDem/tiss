from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Token del bot (inserisci il tuo token qui)
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Database semplice (usiamo dizionari per semplicità)
admins = [123456789]  # ID Telegram degli admin iniziali
forbidden_words = ["parola1", "parola2"]  # Lista parole vietate
allowed_users = []  # Lista di utenti autorizzati a inviare file
pending_users = {}  # Per la gestione CAPTCHA dei nuovi utenti


def is_admin(user_id):
    return user_id in admins


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Ciao! Sono il bot di gestione del gruppo.")


def check_message(update: Update, context: CallbackContext):
    for word in forbidden_words:
        if word in update.message.text.lower():
            update.message.delete()
            context.bot.restrict_chat_member(
                chat_id=update.message.chat.id,
                user_id=update.message.from_user.id,
                permissions={"can_send_messages": False},
            )
            update.message.reply_text(f"Messaggio vietato! {update.message.from_user.first_name} è stato mutato.")
            return


def handle_files(update: Update, context: CallbackContext):
    if update.message.from_user.id not in allowed_users and not is_admin(update.message.from_user.id):
        update.message.delete()
        update.message.reply_text("Non sei autorizzato a inviare file!")


def new_member(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        keyboard = [
            [InlineKeyboardButton("Verifica", callback_data=f"verify_{member.id}")]
        ]
        pending_users[member.id] = member
        context.bot.restrict_chat_member(
            chat_id=update.message.chat.id,
            user_id=member.id,
            permissions={"can_send_messages": False},
        )
        update.message.reply_text(
            f"Benvenuto {member.first_name}! Completa la verifica per accedere al gruppo.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

def verify_user(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = int(query.data.split("_")[1])
    if user_id in pending_users:
        context.bot.restrict_chat_member(
            chat_id=query.message.chat.id,
            user_id=user_id,
            permissions={
                "can_send_messages": True,
                "can_send_media_messages": True,
                "can_add_web_page_previews": True,
            },
        )
        del pending_users[user_id]
        query.edit_message_text("Verifica completata! Benvenuto nel gruppo.")
    else:
        query.edit_message_text("Errore: utente non trovato.")

# Comando /add_admin per aggiungere admin
def add_admin(update: Update, context: CallbackContext):
    if is_admin(update.message.from_user.id):
        try:
            new_admin = int(context.args[0])
            if new_admin not in admins:
                admins.append(new_admin)
                update.message.reply_text(f"Utente {new_admin} aggiunto come admin.")
            else:
                update.message.reply_text("Questo utente è già un admin.")
        except (IndexError, ValueError):
            update.message.reply_text("Errore: specifica un ID utente valido.")
    else:
        update.message.reply_text("Non hai i permessi per eseguire questo comando.")


def add_word(update: Update, context: CallbackContext):
    if is_admin(update.message.from_user.id):
        try:
            new_word = context.args[0].lower()
            if new_word not in forbidden_words:
                forbidden_words.append(new_word)
                update.message.reply_text(f"Parola vietata aggiunta: {new_word}")
            else:
                update.message.reply_text("Questa parola è già vietata.")
        except IndexError:
            update.message.reply_text("Errore: specifica una parola da vietare.")
    else:
        update.message.reply_text("Non hai i permessi per eseguire questo comando.")


def allow_user(update: Update, context: CallbackContext):
    if is_admin(update.message.from_user.id):
        try:
            user_id = int(context.args[0])
            if user_id not in allowed_users:
                allowed_users.append(user_id)
                update.message.reply_text(f"Utente autorizzato a inviare file: {user_id}")
            else:
                update.message.reply_text("Questo utente è già autorizzato.")
        except (IndexError, ValueError):
            update.message.reply_text("Errore: specifica un ID utente valido.")
    else:
        update.message.reply_text("Non hai i permessi per eseguire questo comando.")


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

  
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add_admin", add_admin, pass_args=True))
    dp.add_handler(CommandHandler("add_word", add_word, pass_args=True))
    dp.add_handler(CommandHandler("allow_user", allow_user, pass_args=True))

   
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_message))
    dp.add_handler(MessageHandler(Filters.document, handle_files))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
    dp.add_handler(CallbackQueryHandler(verify_user))

  
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
