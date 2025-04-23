import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

user_balances = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Utilisateur"

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

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    TOKEN = os.environ["BOT_TOKEN"]
    WEBHOOK_URL = os.environ["WEBHOOK_URL"]
    PORT = int(os.environ.get("PORT", 8443))

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot en ligne avec Webhook ✅")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )
