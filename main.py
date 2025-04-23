import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Simule une base de données des soldes utilisateurs
user_balances = {}

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Utilisateur"

    # Si l'utilisateur n'a pas encore de solde, on initialise à 0
    if user_id not in user_balances:
        user_balances[user_id] = 0.00

    balance = user_balances[user_id]

    message = (
        f"👋 Hey, @{username} !\n"
        f"🇫🇷 Vous êtes actuellement sur le meilleur AUTOSHOP de data fr 🇫🇷.\n\n"
        f"🇫🇷 Dépôt doublé tout les lundi 🇫🇷\n"
        f"🔄 Split BOT : https://t.me/RAVVFR\n"
        f"⚡ Dépot Crypto instant BTC/ETH/SOL ... go dm\n"
        f"💰 Solde: {balance:.2f}€"
    )

    keyboard = [
        [InlineKeyboardButton("💰 Depot Crypto 30m~", url="https://t.me/toncontactcrypto")],
        [InlineKeyboardButton("📄 Canal", url="https://t.me/toncanal")],
        [InlineKeyboardButton("👤 Profile", callback_data='profile'),
         InlineKeyboardButton("🛍️ Shop", callback_data='shop')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message, reply_markup=reply_markup)

# Lancement du bot
if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)

    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot en ligne ✅")
    app.run_polling()
