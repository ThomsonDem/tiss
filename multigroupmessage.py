from telegram.ext import Application, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes

# Token del bot
BOT_TOKEN = "BOT TOKEN"

# Lista degli admin autorizzati (sostituisci con i tuoi ID Telegram)
AUTHORIZED_USERS = [ID]  # Inserisci il tuo ID o quello degli admin autorizzati

# Lista dei canali o gruppi dove inviare i messaggi
GROUPS = ["@test", "@test"]  # Modifica con i tuoi gruppi/canali


# Verifica se l'utente è autorizzato
def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS


# Comando per inviare il messaggio
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("Non sei autorizzato a usare questo comando.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("Usa il comando così: /broadcast <messaggio>")
        return

    # Messaggio da inviare
    message = " ".join(context.args)

    # Invia il messaggio a tutti i gruppi/canali
    for group in GROUPS:
        try:
            await context.bot.send_message(chat_id=group, text=message)
        except Exception as e:
            print(f"Errore nell'invio al gruppo {group}: {e}")

    await update.message.reply_text("Messaggio inviato a tutti i gruppi!")


# Aggiungi un gruppo alla lista
async def add_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("Non sei autorizzato a usare questo comando.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usa il comando così: /add_group <@nome_gruppo>")
        return

    group = context.args[0]
    if group not in GROUPS:
        GROUPS.append(group)
        await update.message.reply_text(f"Gruppo {group} aggiunto alla lista!")
    else:
        await update.message.reply_text(f"Il gruppo {group} è già nella lista.")



async def remove_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("Non sei autorizzato a usare questo comando.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usa il comando così: /remove_group <@nome_gruppo>")
        return

    group = context.args[0]
    if group in GROUPS:
        GROUPS.remove(group)
        await update.message.reply_text(f"Gruppo {group} rimosso dalla lista!")
    else:
        await update.message.reply_text(f"Il gruppo {group} non è nella lista.")



async def list_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("Non sei autorizzato a usare questo comando.")
        return

    if GROUPS:
        groups = "\n".join(GROUPS)
        await update.message.reply_text(f"Ecco i gruppi nella lista:\n{groups}")
    else:
        await update.message.reply_text("Non ci sono gruppi nella lista.")



def main():
   
    application = Application.builder().token(BOT_TOKEN).build()

    
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("add_group", add_group))
    application.add_handler(CommandHandler("remove_group", remove_group))
    application.add_handler(CommandHandler("list_groups", list_groups))

   
    print("Bot in esecuzione... Premi Ctrl+C per fermarlo.")
    application.run_polling()


if __name__ == "__main__":
    main()
