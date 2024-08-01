import threading
import flask_app
import telegram_bot

if __name__ == '__main__':

    flask_thread = threading.Thread(target=flask_app.run_flask)
    flask_thread.start()

    telegram_bot.run_telegram_bot()
