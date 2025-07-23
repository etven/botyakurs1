
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, ConversationHandler, filters
)
import os
import csv

ASK_NAME, ASK_EMAIL = range(2)
user_data = {}
CSV_FILE = "subscribers.csv"
TOKEN = os.environ.get("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Да, хочу", callback_data="yes")],
        [InlineKeyboardButton("⏳ Пока не сейчас", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "Привет! 👋 Спасибо за покупку в StylePro!\n\n"
        "✨ Мы рассылаем стильные советы, подборки образов, тренды и вдохновение от стилистов.\n"
        "Хочешь получать всё это прямо на почту?"
    )
    await update.message.reply_text(text, reply_markup=reply_markup)

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "yes":
        await query.edit_message_text("Отлично! 😊 Как тебя зовут?")
        return ASK_NAME
    else:
        await query.edit_message_text("Окей, если передумаешь — просто напиши /start 😉")
        return ConversationHandler.END

async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = {"name": update.message.text}
    await update.message.reply_text("А теперь, пожалуйста, введи e-mail, куда присылать стильные советы 💌")
    return ASK_EMAIL

async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id]["email"] = update.message.text
    name = user_data[user_id]["name"]
    email = user_data[user_id]["email"]

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, email])

    await update.message.reply_text(
        f"Спасибо, {name}! ✨ Ты подписан. Скоро получишь стильные советы на {email} 💌"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Окей, если передумаешь — просто напиши /start 😉")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(handle_choice, pattern="^(yes|no)$")
        ],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Бот запущен")
    app.run_polling()
