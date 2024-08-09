from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
import base64


def get_auth_header():
    auth_str = "Admin:"
    auth_bytes = auth_str.encode('ascii')
    auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
    return {"Authorization": f"Basic {auth_base64}"}


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Привет! Используй команду /orders для получения заказов и /order <Номер_заказа> для получения информации о '
        'конкретном заказе.')


async def get_orders(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.username
    url = f'http://localhost/Trade6/hs/api/telegram_client/@{telegram_id}/orders?telegram_id=@{telegram_id}'
    headers = get_auth_header()
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        orders = response.json()
        for order in orders:
            await update.message.reply_text(
                f"Номер: {order['number']}\n"
                f"Сделка: {order['product']}\n"
                f"Статус: {order['status']}\n"
                f"Дата: {order['date']}\n"
                f"Партнер: {order['partner']}\n"
                f"Сумма: {order['sum']} рублей\n"
                f"Телеграм: {order['telegram_id']}\n"
            )
    else:
        await update.message.reply_text('Не удалось получить заказы.')

async def get_order_by_number(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.username
    order_number = context.args[0]

    url = f'http://localhost/Trade6/hs/api/telegram_client/@{telegram_id}/orders/{order_number}?telegram_id=@{telegram_id}'
    headers = get_auth_header()

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        order = response.json()
        await update.message.reply_text(
            f"Номер: {order['number']}\n"
            f"Сделка: {order['product']}\n"
            f"Статус: {order['status']}\n"
            f"Дата: {order['date']}\n"
            f"Партнер: {order['partner']}\n"
            f"Сумма: {order['sum']} руб.\n"
            f"Телеграм: {order['telegram_id']}\n"
        )
    else:
        await update.message.reply_text('Не удалось получить информацию о заказе.')



def run_telegram_bot():
    application = Application.builder().token("7122572247:AAGdpQv0MSx_JAEwkle6bHj6UtGr92wNVqQ").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("orders", get_orders))
    application.add_handler(CommandHandler("order", get_order_by_number))

    application.run_polling()

if __name__ == '__main__':
    run_telegram_bot()
