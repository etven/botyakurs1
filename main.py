
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, ConversationHandler, filters

import os

ASK_NAME, ASK_EMAIL = range(2)
user_data = {}

TOKEN = 7703194563:AAEc0DU_QdCwFCc2b5h_G37v5YwmZa3XWD0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! 👋 Спасибо за покупку в StylePro! Давай познакомимся 😊\nКак тебя зовут?")
    return ASK_NAME

async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = {"name": update.message.text}
    await update.message.reply_text("А теперь, пожалуйста, введи e-mail, куда присылать стильные советы ✨")
    return ASK_EMAIL

async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]["email"] = update.message.text
    name = user_data[update.effective_user.id]["name"]
    email = user_data[update.effective_user.id]["email"]

    await update.message.reply_text(f"Спасибо, {name}! ✨ Ты подписан. Скоро получишь стильные советы на {email} 💌")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Окей, если передумаешь — просто напиши /start 😉")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Бот запущен")
    app.run_polling()
