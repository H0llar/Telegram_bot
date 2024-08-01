from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder
import requests

TELEGRAM_TOKEN = '7122572247:AAGdpQv0MSx_JAEwkle6bHj6UtGr92wNVqQ'

# Telegram bot command handlers
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Используйте команду /orders для получения списка заказов или /order <номер> для получения информации о заказе.')

async def get_orders(update: Update, context: CallbackContext) -> None:
    #Тут будет код
    if data['status'] == 'success':
        await update.message.reply_text(data['message'])
    else:
        await update.message.reply_text('Ошибка при получении заказов.')

async def get_order(update: Update, context: CallbackContext) -> None:
    #Тут будет код
    if not order_number:
        await update.message.reply_text('Пожалуйста, укажите номер заказа.')
        return
    #Тут будет код
    if data['status'] == 'success':
        await update.message.reply_text(data['message'])
    else:
        await update.message.reply_text('Ошибка при получении информации о заказе.')

def run_telegram_bot():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    orders_handler = CommandHandler('orders', get_orders)
    order_handler = CommandHandler('order', get_order)

    application.add_handler(start_handler)
    application.add_handler(orders_handler)
    application.add_handler(order_handler)

    application.run_polling()

if __name__ == '__main__':
    run_telegram_bot()
