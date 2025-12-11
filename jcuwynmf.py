import logging
import nest_asyncio
import asyncio
import json
from html import escape
import logging
import os
import random
from psycopg2 import Error
import re
import time
import httpx
import psycopg2
from telegram.ext import Application, ApplicationBuilder, CallbackContext, CommandHandler, ContextTypes, filters, \
    MessageHandler, CallbackQueryHandler
from telegram import Update, User, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, ChatPermissions, Message
from telegram.constants import ChatAction, ParseMode
from datetime import datetime, timezone, timedelta
from collections import defaultdict, OrderedDict
from typing import Optional, Tuple, List, Dict
from telegram.helpers import mention_html
from psycopg2.extras import DictCursor
from telegram.error import BadRequest
from functools import wraps, partial
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Применяем nest_asyncio
nest_asyncio.apply()

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Замените на ваш ID чата администраторов
ADMIN_CHAT_ID = ('-1003272139228')

# Обработка нажатий на кнопки
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'yes':
        message_text = (
            "<b>▎Отправь ниже список голосов:\n\n"
            "пример:</b>\n"
            "<blockquote>пикми чата - @алина, @иван, @марина\nкороль чата - @вадим\nкринж чата - @паша, @кристина</blockquote>"
        )
        await query.edit_message_text(text=message_text, parse_mode=ParseMode.HTML)

    elif query.data == 'no':
        message_text = (
            "<b><i>Хорошо! Твои голоса были учтены!\nРезультаты голосования будут оглашены 31.12.2025 </i></b>✨"
        )
        await query.edit_message_text(text=message_text, parse_mode=ParseMode.HTML)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.message.from_user.username
    message_text = (
            f"<i>{username}, Привет! С наступающим новым годом! 🎄\n\n"
            "▎Тут ты можешь принять участие в голосовании в новогодней номинации чата @Gruppa_mobly\n\n"
            "📋 <b>В этом году следующие номинации:</b></i>\n"  # ИСПОЛЬЗУЕМ <b>
            "<blockquote>«ᴨиᴋʍи чᴀᴛᴀ»\n«ᴋᴩинж чᴀᴛᴀ»\n«королева чᴀᴛᴀ»\n«король чᴀᴛᴀ»\n«харизма чᴀᴛᴀ»\n«быдло чᴀᴛᴀ»</blockquote>\n\n"
            "▎<b>Важно!</b>\n"
            "<i>Если у человека нет юза, пишите его ид ( узнать его можно в чате по команде «.ид» в ответ на сообщение нужного человека)</i>\n\n"
            "<b>📩  Как голосовать?</b> \n"
            "<blockquote>1) Выберите до 3х человек на каждую номинацию \n2) Отправте в бота свои голоса\nпр: пикми чата - @алина, @иван, @марина\nкороль чата - @вадим</blockquote>"
    )
    await update.message.reply_text(
        message_text,
        parse_mode=ParseMode.HTML  # ДОБАВЛЯЕМ parse_mode
        )


# Обработка текстовых сообщений

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text or ""
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Без имени"

    # Экранируем данные пользователя перед отправкой с parse_mode=HTML
    safe_user_message = escape(user_message)
    safe_username = escape(username)

    admin_message = (
        f"Сообщение от @{safe_username} (ID: {user_id}):\n"
        f"{safe_user_message}"
    )
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=admin_message,
        parse_mode=ParseMode.HTML
    )

    # Формируем текст ответа в стиле вашего примера start
    message_text = (
        "▎<b>Хочешь дополнить свои голоса?</b> 📩"
    )

    # Создаём кнопки "Да" и "Нет"
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data='yes'),
            InlineKeyboardButton("Нет", callback_data='no'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )

async def main() -> None:
    # Вставьте токен вашего бота
    application = ApplicationBuilder().token("8219379510:AAG4GvqOCk0ATO7_IqCvgJU2ccWnqsFDvzc").build()

    # Регистрация обработчиков команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

