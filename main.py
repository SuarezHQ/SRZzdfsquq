import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Dictionnaire des soldes utilisateurs
user_balances = {}

# Liste des admins (remplace TON_ID_ADMIN par ton ID Telegram)
ADMIN_IDS = [@suareZ3]  # ← ton ID Telegram ici

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Utilisateur"

    if user_id not in user_balances:
        user_balances[user_id] = 0.00

    balance = user_balances[user_id]

    message = (
        f"👋 Hey, @{username} !\n"
        f"🇫🇷 Bienvenue sur le meilleur AUTOSHOP 🇫🇷\n\n"
        f"💰 Solde: {balance:.2f}€\n"
        f"👇 Choisissez une option :"
    )

    keyboard = [
        [InlineKeyboardButton("💰 Dépôt Crypto 30m~", callback_data='deposit_menu')],
        [InlineKeyboardButton("📄 Canal", url="https://t.me/TON_CANAL_TELEGRAM")],
        [InlineKeyboardButton("🛍️ Shop", callback_data='shop_menu')]
    ]
    await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))


# Gère les boutons callback
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'deposit_menu':
        keyboard = [
            [InlineKeyboardButton("🟣 ETH", callback_data='show_eth')],
            [InlineKeyboardButton("🟠 BTC", url="https://t.me/contact_btc")],
            [InlineKeyboardButton("🔵 SOL", url="https://t.me/contact_sol")],
            [InlineKeyboardButton("🔙 Retour", callback_data='back_to_main')]
        ]
        await query.edit_message_text("💸 Choisissez votre crypto :", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'show_eth':
        eth_address = "0x01c6ACe1932d7cEc7b1441Bd858B2209B75B3E1F"
        await query.edit_message_text(
            f"🟣 *Dépot ETH*\n\nVoici ton adresse :\n`{eth_address}`\n\n⚠️ Envoie uniquement de l'ETH à cette adresse.",
            parse_mode="Markdown"
        )

    elif query.data == 'shop_menu':
        shop_text = (
            "🛍️ *DATA SHOP DISPONIBLE :*\n"
            "- 🇫🇷 CPF Validé : 10€\n"
            "- 🇫🇷 Carte Navigo : 5€\n"
            "- 🇧🇪 Carte Identité Belgique : 12€\n"
            "- + d'autres sur demande"
        )
        keyboard = [[InlineKeyboardButton("🔙 Retour", callback_data='back_to_main')]]
        await query.edit_message_text(shop_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == 'back_to_main':
        await start(update, context)


# Commande /addsolde pour les admins
async def addsolde(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Tu n'as pas les droits pour utiliser cette commande.")
        return

    try:
        amount = float(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Utilisation : /addsolde <montant> (en répondant à un utilisateur)")
        return

    # Soit on répond à un message, soit on crédite soi-même
    target_id = update.message.reply_to_message.from_user.id if update.message.reply_to_message else user_id

    if target_id not in user_balances:
        user_balances[target_id] = 0.00

    user_balances[target_id] += amount
    await update.message.reply_text(f"✅ {amount:.2f}€ ajouté au solde de l'utilisateur.")


# Lancement du bot
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addsolde", addsolde))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("Bot en ligne en mode polling ✅")
    app.run_polling()
