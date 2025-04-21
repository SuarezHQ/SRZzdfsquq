import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, MessageHandler, filters

# Stock temporaire des demandes
user_inputs = {}

# Commande /depot
async def depot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📥 Déposer Data", callback_data="deposer_data")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choisissez une action :", reply_markup=reply_markup)

# Quand le bouton est cliqué
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "deposer_data":
        await query.message.reply_text("📄 Combien de fichiers/lignes souhaitez-vous déposer ?")
        context.user_data["awaiting_input"] = True

# Gestion de la réponse utilisateur (le nombre de lignes)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_input"):
        lignes = update.message.text
        user_inputs[update.effective_user.id] = lignes
        context.user_data["awaiting_input"] = False

        # Bouton de paiement
        keyboard = [[InlineKeyboardButton("💳 Payer", callback_data="payer")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"✅ Vous avez indiqué {lignes} lignes.\nCliquez sur 'Payer' pour finaliser.",
            reply_markup=reply_markup
        )

    else:
        await update.message.reply_text("Commande non reconnue. Utilisez /start ou /depot.")

# Quand on clique sur "Payer"
async def payer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    lignes = user_inputs.get(user_id, "0")
    prix = int(lignes) * 0.10  # Par exemple : 0,10€ par ligne

    await query.message.reply_text(
        f"💳 Total à payer pour {lignes} lignes : {prix:.2f}€\n"
        "💰 Paiement crypto → @suareZ3"
    )

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username

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
