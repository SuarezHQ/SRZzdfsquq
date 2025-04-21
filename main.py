from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Simuler un solde (à remplacer par une vraie base de données si besoin)
USER_BALANCE = {
    "default": 14.0276  # Valeur d'exemple en euros
}

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    balance = USER_BALANCE.get("default", 0)

    # Texte du message principal
    message = (
        f"👋 Hey, @{username} !\n"
        f"🇫🇷 Vous êtes actuellement sur le meilleur AUTOSHOP de data fr 🇫🇷.\n\n"
        f"🔄 Split BOT : https://t.me/RAVVFR\n"
        f"⚡ Dépot Crypto instant BTC/ETH/SOL ... go dm\n"
        f"📩 @suareZ3\n\n"
        f"💰 Solde: {balance:.2f}€"
    )

    # Boutons interactifs
    keyboard = [
        [InlineKeyboardButton("🧍‍♂️ Profile", callback_data='profile'),
         InlineKeyboardButton("🛍 Data", callback_data='shop')],
        [InlineKeyboardButton("🏦 Depot Crypto 30m~", callback_data='deposit')],
        [InlineKeyboardButton("📢 Canal", url='https://t.me/RAVVFR')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message, reply_markup=reply_markup)

# Lancer le bot
import os
app = ApplicationBuilder().token(os.environ["8179818961:AAEPH9b6ltprKM7L7bjO7EuVAxfEVmGOlQE"]).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
