import asyncio
from telegram._update import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import settings

PRODUCTION_TOKEN = settings.PRODUCTION_BOT_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать! Откройте [HTML Страницу](https://vadmitrii.github.io/crypto_game/production)",
        parse_mode='Markdown'
    )


def run_html_bot():
    app = Application.builder().token(PRODUCTION_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    return app


production_bot = run_html_bot()
asyncio.run(production_bot.run_polling())
