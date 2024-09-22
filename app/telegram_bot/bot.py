import logging

from telegram._inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram._update import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import asyncio

from config import settings
from telegram_bot.handlers import get_user_by_username, update_user, get_statistics, create_user

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main_menu():
    """ Telegram bot main menu

    :returns:

        InlineKeyBoard: Main menu keyboard
    """
    keyboard = [
        [InlineKeyboardButton("Статистика", callback_data='statistics')],
        [InlineKeyboardButton("Управление", callback_data='management')],
    ]
    return InlineKeyboardMarkup(keyboard)


def management_menu():
    """ Telegram bot main menu

    :returns:

        InlineKeyBoard: Management menu keyboard
    """
    keyboard = [
        [InlineKeyboardButton("Создать тестового пользователя", callback_data='create_test_user')],
        [InlineKeyboardButton("Получить UID пользователя", callback_data='get_user')],
        [InlineKeyboardButton("Редактировать пользователя", callback_data='edit_user')],
        [InlineKeyboardButton("Назад", callback_data='main_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)


def edit_menu():
    """ Telegram bot main menu

    :returns:

        InlineKeyBoard: User edit menu keyboard
    """
    keyboard = [
        [InlineKeyboardButton("Изменить рейтинг", callback_data='edit_rating')],
        [InlineKeyboardButton("Изменить количество монет", callback_data='edit_coins')],
        [InlineKeyboardButton("Назад", callback_data='management_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Telegram bot start command handler

    :returns:

        InlineKeyBoard: Main menu keyboard
    """
    await update.message.reply_text(
        "Добро пожаловать в админ-бот! Выберите опцию:",
        reply_markup=main_menu()
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Telegram bot button click handler """
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == 'statistics':
        await show_statistics(update, context)
    elif data == 'management':
        await query.edit_message_text("Выберите опцию:", reply_markup=management_menu())
    elif data == 'create_test_user':
        created_username = await create_user()
        await query.edit_message_text(text=f"Создан тестовый пользователь: {created_username}",
                                      reply_markup=management_menu())
    elif data == 'edit_user':
        await query.edit_message_text(text="Введите username пользователя для редактирования:")
        context.user_data['mode'] = 'edit_user'
    elif data == 'edit_rating':
        user = context.user_data.get('edit_user')
        if user:
            await query.edit_message_text(f"Введите новый рейтинг для пользователя {user.username}:")
            context.user_data['mode'] = 'new_rating'
        else:
            await query.edit_message_text("Сначала выберите пользователя для редактирования.",
                                          reply_markup=management_menu())
    elif data == 'edit_coins':
        user = context.user_data.get('edit_user')
        if user:
            await query.edit_message_text(f"Введите новое количество монет для пользователя {user.username}:")
            context.user_data['mode'] = 'new_coins'
        else:
            await query.edit_message_text("Сначала выберите пользователя для редактирования.",
                                          reply_markup=management_menu())
    elif data == 'get_user':
        await query.edit_message_text(text="Введите username пользователя для получения UID:")
        context.user_data['mode'] = 'get_user'
    elif data == 'main_menu':
        await query.edit_message_text("Главное меню:", reply_markup=main_menu())
    elif data == 'management_menu':
        await query.edit_message_text("Выберите опцию:", reply_markup=management_menu())


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Telegram bot messages and commands handler """
    mode = context.user_data.get('mode')
    message_text = update.message.text

    if mode == 'edit_user':
        username = message_text
        user = await get_user_by_username(username)
        if not user:
            await update.message.reply_text("Пользователь не найден.", reply_markup=management_menu())
            context.user_data.clear()
            return
        await update.message.reply_text(f"Выберите опцию для редактирования данных пользователя {username}:",
                                        reply_markup=edit_menu())
        context.user_data['edit_user'] = user
        context.user_data['mode'] = None

    if mode == 'get_user':
        username = message_text
        user = await get_user_by_username(username)
        if not user:
            await update.message.reply_text("Пользователь не найден.", reply_markup=management_menu())
            context.user_data.clear()
            return
        await update.message.reply_text(f'UID пользователя {username}: {user.telegram_uid}',
                                        reply_markup=management_menu())
        context.user_data.clear()

    user = context.user_data.get('edit_user')

    if mode == 'new_rating':
        try:
            new_rating = int(message_text)
            await update_user(uid=user.telegram_uid, new_rating=new_rating)
            await update.message.reply_text(
                f"Рейтинг пользователя {user.username} изменен на {new_rating}.",
                reply_markup=management_menu()
            )
            context.user_data.clear()
        except ValueError:
            await update.message.reply_text("Некорректный ввод. Пожалуйста, введите число для рейтинга.")

    elif mode == 'new_coins':
        try:
            new_coins = int(message_text)
            await update_user(uid=user.telegram_uid, new_coins=new_coins)
            await update.message.reply_text(
                f"Количество монет пользователя {user.username} изменено на {new_coins}.",
                reply_markup=management_menu()
            )
            context.user_data.clear()
        except ValueError:
            await update.message.reply_text("Некорректный ввод. Пожалуйста, введите число для монет.")


async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Telegram bot statistics info

    :returns:
        A message with statistics on the clients
    """
    total_users, online_users, unique_users = await get_statistics()
    stats_message = (
        f"Статистика:\n"
        f"Всего пользователей: {total_users}\n"
        f"Пользователей онлайн: {online_users}\n"
        f"Пользователи с рейтингом > 1800 и монетами > 1 млн: {unique_users}"
    )
    await update.callback_query.edit_message_text(stats_message, reply_markup=main_menu())


def run_bot():
    telegram_bot = Application.builder().token(settings.ADMIN_BOT_TOKEN).build()

    telegram_bot.add_handler(CommandHandler("start", start))
    telegram_bot.add_handler(CallbackQueryHandler(button_click))

    telegram_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return telegram_bot


bot = run_bot()

asyncio.run(bot.run_polling())
