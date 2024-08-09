from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from strings import (
    START_MESSAGE,
    REQUEST_ORDER_NUMBER_MESSAGE,
    NO_ORDERS_FOUND_MESSAGE,
    NO_ORDER_NUMBER_PROVIDED_MESSAGE,
    ORDER_INFO_TEMPLATE,
)
import requests
import base64
import config


def get_auth_header():
    auth_str = f"{config.AUTH_USERNAME}:{config.AUTH_PASSWORD}"
    auth_bytes = auth_str.encode('ascii')
    auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
    return {"Authorization": f"Basic {auth_base64}"}


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(START_MESSAGE)


async def get_orders(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.username
    url = f'{config.API_BASE_URL}/@{telegram_id}//orders?telegram_id=@{telegram_id}'
    headers = get_auth_header()
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        orders = response.json()
        for order in orders:
            await update.message.reply_text(
                ORDER_INFO_TEMPLATE.format(
                    number=order['number'],
                    product=order['product'],
                    status=order['status'],
                    date=order['date'],
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

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        order = response.json()
        await update.message.reply_text(
            ORDER_INFO_TEMPLATE.format(
                number=order['number'],
                product=order['product'],
                status=order['status'],
                date=order['date'],
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
