from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

user_balances = {}

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
        [InlineKeyboardButton("📄 Canal", url="https://t.me/ton_canal_telegram")],
        [InlineKeyboardButton("🛍️ Shop", callback_data='shop_menu')]
    ]
    await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))

# Dépôt menu crypto
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'deposit_menu':
        keyboard = [
            [InlineKeyboardButton("🟣 ETH", url="https://t.me/contact_eth")],
            [InlineKeyboardButton("🔙 Retour", callback_data='back_to_main')]
        ]
        await query.edit_message_text("💸 Choisissez votre crypto :", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'shop_menu':
        shop_text = (
            "🛍️ *DATA SHOP :*\n"
            "- 🇫🇷 DATA : 10€\n"
            "- + d'autres sur demande"
        )
        keyboard = [[InlineKeyboardButton("🔙 Retour", callback_data='back_to_main')]]
        await query.edit_message_text(shop_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == 'back_to_main':
        await start(update, context)

