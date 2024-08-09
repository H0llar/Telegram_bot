from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)


def get_auth_header():
    auth_str = "Admin:"
    auth_bytes = auth_str.encode('ascii')
    auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
    return {"Authorization": f"Basic {auth_base64}"}


@app.route('/get_orders', methods=['GET'])
def get_orders():
    print("Запрос на получение заказов получен")
    telegram_id = request.args.get('telegram_id')
    url = f'http://localhost/Trade6/hs/api/telegram_client/@{telegram_id}/orders'
    headers = get_auth_header()
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return response.text, response.status_code


@app.route('/get_order', methods=['GET'])
def get_order():
    telegram_id = request.args.get('telegram_id')
    order_number = request.args.get('order_number')
    url = f'http://localhost/Trade6/hs/api/telegram_client/@{telegram_id}/orders/{order_number}'
    headers = get_auth_header()
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return response.text, response.status_code


def run_flask_app():
    app.run(port=5000, debug=True)


if __name__ == '__main__':
    run_flask_app()
