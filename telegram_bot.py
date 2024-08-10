from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from strings import (
    START_MESSAGE,
    REQUEST_ORDER_NUMBER_MESSAGE,
    NO_ORDERS_FOUND_MESSAGE,
    NO_ORDER_NUMBER_PROVIDED_MESSAGE,
    ORDER_INFO_TEMPLATE,
)
from datetime import datetime
import aiohttp
import asyncio
import requests
import base64
import config
import re
import locale

locale.setlocale(locale.LC_TIME, 'Russian')

def get_auth_header():
    auth_str = f"{config.AUTH_USERNAME}:{config.AUTH_PASSWORD}"
    auth_bytes = auth_str.encode('ascii')
    auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
    return {"Authorization": f"Basic {auth_base64}"}


async def fetch(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return await response.json()


def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    formatted_date = date_obj.strftime('%d %B %Y, %H:%M')
    return formatted_date


def format_status(status):
    words = re.findall(r'[A-ZА-Я][^A-ZА-Я]*', status)
    formatted_status = ' '.join(word.capitalize() for word in words)
    return formatted_status


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(START_MESSAGE)


async def get_orders(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.username
    url = f'{config.API_BASE_URL}/@{telegram_id}/orders?telegram_id=@{telegram_id}'
    headers = get_auth_header()

    async with aiohttp.ClientSession() as session:
        orders = await fetch(session, url, headers)


    if orders:
        for order in orders:
            formatted_status = format_status(order['status'])
            await update.message.reply_text(
                ORDER_INFO_TEMPLATE.format(
                    number=order['number'],
                    product=order['product'],
                    status=formatted_status,
                    date=format_date(order['date']),
                    partner=order['partner'],
                    sum=order['sum'],
                    telegram_id=order['telegram_id']
                )
            )
    else:
        await update.message.reply_text(NO_ORDERS_FOUND_MESSAGE)


async def get_order_by_number(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.username
    order_number = context.args[0]
    url = f'{config.API_BASE_URL}/@{telegram_id}/orders/{order_number}?telegram_id=@{telegram_id}'
    headers = get_auth_header()

    async with aiohttp.ClientSession() as session:
        orders = await fetch(session, url, headers)


    if order:
        formatted_status = format_status(order['status'])
        await update.message.reply_text(
            ORDER_INFO_TEMPLATE.format(
                number=order['number'],
                product=order['product'],
                status=order['status'],
                date=format_date(order['date']),
                partner=order['partner'],
                sum=order['sum'],
                telegram_id=order['telegram_id']
            )
        )
    else:
        await update.message.reply_text(NO_ORDERS_FOUND_MESSAGE)



def run_telegram_bot():
    application = Application.builder().token(config.BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("orders", get_orders))
    application.add_handler(CommandHandler("order", get_order_by_number))

    application.run_polling()

if __name__ == '__main__':
    run_telegram_bot()
