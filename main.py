import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    balance = 14.0276  # Tu peux le rendre dynamique si besoin

    message = (
        f"👋 Hey, @{username} !\n"
        f"🇫🇷 Vous êtes actuellement sur le meilleur AUTOSHOP de data fr 🇫🇷.\n\n"
        f"🇫🇷 Dépôt doublé tout les lundi 🇫🇷\n"
        f"🔄 Split BOT : https://t.me/RAVVFR\n"
        f"⚡ Dépot Crypto instant BTC/ETH/SOL\n"
        f"📩 @suareZ3\n\n"
        f"💰 Solde: {balance:.2f}€"
    )

    await update.message.reply_text(message)

# Lancement du bot
if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)

    # Récupère le token depuis les variables d’environnement
    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot en ligne ✅")
    app.run_polling()
