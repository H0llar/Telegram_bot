from flask import Flask, request, jsonify
import requests
from telegram import Bot

app = Flask(__name__)

API_BASE_URL = 'http://127.0.0.1/Trade6/hs/api'
TELEGRAM_TOKEN = '7122572247:AAGdpQv0MSx_JAEwkle6bHj6UtGr92wNVqQ'
bot = Bot(token=TELEGRAM_TOKEN)

def get_orders_by_telegram_id(telegram_id):
    response = requests.get(f'{API_BASE_URL}/telegram_client/{telegram_id}/orders')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_order_by_number(telegram_id, order_number):
    response = requests.get(f'{API_BASE_URL}/telegram_client/{telegram_id}/orders/{order_number}')
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/orders', methods=['GET'])
def orders():
    # Тут будет код
    if orders:
        response_text = 'Ваши заказы:\n'
        for order in orders:
            response_text += f'Номер: {order["number"]}, Партнер: {order["partner"]}, Дата отгрузки: {order["date_shipment"]}, Статус: {order["status"]}\n'
        bot.send_message(chat_id=chat_id, text=response_text)
        return jsonify({'status': 'success', 'message': 'Orders sent to Telegram chat.'})
    else:
        bot.send_message(chat_id=chat_id, text='Нет заказов для данного Telegram ID.')
        return jsonify({'status': 'error', 'message': 'No orders found for the given Telegram ID.'})

@app.route('/order', methods=['GET'])
def order():
    # Тут будет код
    if order:
        response_text = f'Номер: {order["number"]}, Партнер: {order["partner"]}, Дата отгрузки: {order["date_shipment"]}, Статус: {order["status"]}'
        bot.send_message(chat_id=chat_id, text=response_text)
        return jsonify({'status': 'success', 'message': 'Order details sent to Telegram chat.'})
    else:
        bot.send_message(chat_id=chat_id, text='Нет данных по заданному номеру заказа или ID клиента.')
        return jsonify({'status': 'error', 'message': 'No order found for the given number and Telegram ID.'})

def run_flask():
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    run_flask()
