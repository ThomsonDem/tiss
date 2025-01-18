# Tiss - Telegram Bot Package

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Languages](https://img.shields.io/badge/Languages-ITA%2FENG%2FRUS-green)

## Descrizione

**Tiss** è un pacchetto per bot Telegram che consente una gestione avanzata di canali e gruppi. Il progetto fornisce strumenti per l'invio di messaggi multipli, traduzione automatica, gestione di firewall, e supporto alle donazioni.

---

## Funzionalità principali

1. **Gestione di canali e gruppi**  
   - Aggiungi canali con il comando `/add_channel`.
   - Visualizza e gestisci i canali con `/list_channels` e `/remove_channel`.
   - Invia messaggi broadcast con `/broadcast <messaggio>`.

2. **Firewall integrato**  
   - Aggiungi amministratori con `/add_admin <user_id>`.
   - Definisci parole vietate con `/add_word <parola>`.
   - Autorizza utenti specifici con `/allow_user <user_id>`.

3. **Traduzione automatica**  
   - Imposta la lingua di destinazione con `/setlang [codice lingua]`.
   - Supporto per: Italiano, Inglese, Francese, Tedesco, Spagnolo, Portoghese, Russo.

4. **Donazioni**  
   - Invia un messaggio con un pulsante per le donazioni tramite `/start`.

---

## Configurazione del progetto

### Pre-requisiti
- **Python**: Versione 3.8 o superiore.
- **Token del bot Telegram**:
  - Vai su [BotFather](https://t.me/BotFather) su Telegram.
  - Crea un nuovo bot con il comando `/newbot` e salva il token fornito.

---

### Installazione

1. **Configura il file Python**
   - Sostituisci `YOUR_BOT_TOKEN` con il token del tuo bot.
   - Sostituisci `AUTHORIZED_USERS` con l'ID Telegram autorizzato.

2. **Esegui in locale**  
   - Installa le librerie necessarie:  
     ```bash
     pip install python-telegram-bot
     ```
   - Avvia il bot:  
     ```bash
     python telegram_bot.py
     ```

3. **Distribuzione su Heroku**  
   - Configura i file `requirements.txt` e `Procfile`.
   - Inizializza un repository Git e carica il progetto su Heroku:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     heroku create
     git push heroku master
     ```
   - Riavvia il bot:
     ```bash
     heroku ps:restart
     ```

---

## Esempi di utilizzo

- **Comandi principali**:
  - `/start`: Avvia il bot.
  - `/help`: Mostra l'elenco dei comandi disponibili.
  - `/broadcast`: Invia messaggi a gruppi e canali configurati.

---

## Contribuire

Contributi sono i benvenuti! Sentiti libero di aprire un'issue o creare una pull request.

---

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

---

## Contatti

Per qualsiasi domanda o supporto, contatta il creatore del progetto su Telegram.
