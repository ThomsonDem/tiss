from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
import telegram


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Token del bot
BOT_TOKEN = "TUO BOT TOKEN"

# ID degli amministratori autorizzati
AUTHORIZED_USERS = [ID]  # Sostituisci con il tuo ID Telegram


REQUIRED_CHANNELS = ["@", "@", "@"]
TARGET_CHANNEL = "@"

def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

   
    message = "Ciao! Per accedere al canale richiesto devi prima unirti a questi canali:\n\n"
    for channel in REQUIRED_CHANNELS:
        message += f"- {channel}\n"

   
    keyboard = [[InlineKeyboardButton("Ho completato l'iscrizione", callback_data="check_subscription")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    chat_id = query.message.chat.id

  
    all_subscribed = True
    missing_channels = [] 
    for channel in REQUIRED_CHANNELS:
        try:
           
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user.id)
            if member.status not in ["member", "administrator", "creator"]:
                all_subscribed = False
                missing_channels.append(channel)
        except telegram.error.BadRequest as e:
          
            all_subscribed = False
            missing_channels.append(channel)
            logging.warning(f"Errore nel controllo del canale {channel}: {e}")

    
    if all_subscribed:
        await query.answer("Iscrizione verificata!")
        await context.bot.send_message(chat_id=chat_id, text=f"Perfetto! Ora puoi accedere a {TARGET_CHANNEL}:\n{TARGET_CHANNEL}")
    else:
        await query.answer("Non sei iscritto a tutti i canali richiesti!")
        missing_message = "Non sei iscritto ai seguenti canali:\n" + "\n".join(missing_channels)
        await context.bot.send_message(chat_id=chat_id, text=missing_message)


async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("Non sei autorizzato a utilizzare questo comando.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Usa il comando così: /add_channel <username_canale>")
        return
    channel = context.args[0]
    if channel not in REQUIRED_CHANNELS:
        REQUIRED_CHANNELS.append(channel)
        await update.message.reply_text(f"Canale {channel} aggiunto all'elenco!")
    else:
        await update.message.reply_text(f"Il canale {channel} è già nell'elenco.")


async def remove_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("Non sei autorizzato a utilizzare questo comando.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Usa il comando così: /remove_channel <username_canale>")
        return
    channel = context.args[0]
    if channel in REQUIRED_CHANNELS:
        REQUIRED_CHANNELS.remove(channel)
        await update.message.reply_text(f"Canale {channel} rimosso dall'elenco!")
    else:
        await update.message.reply_text(f"Il canale {channel} non è nell'elenco.")


async def list_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("Non sei autorizzato a utilizzare questo comando.")
        return
    if REQUIRED_CHANNELS:
        channels = "\n".join([f"- {channel}" for channel in REQUIRED_CHANNELS])
        await update.message.reply_text(f"Ecco i canali obbligatori:\n{channels}")
    else:
        await update.message.reply_text("Non ci sono canali obbligatori al momento.")


def main():
    
    application = Application.builder().token(BOT_TOKEN).build()

   
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_subscription, pattern="check_subscription"))

 
    application.add_handler(CommandHandler("add_channel", add_channel))
    application.add_handler(CommandHandler("remove_channel", remove_channel))
    application.add_handler(CommandHandler("list_channels", list_channels))

   
    print("Bot in esecuzione... Premi Ctrl+C per fermarlo.")
    application.run_polling()

if __name__ == "__main__":
    main()
