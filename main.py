import threading
import subprocess

def run_flask_app():
    subprocess.run(["python", "flask_app.py"])

def run_telegram_bot():
    subprocess.run(["python", "telegram_bot.py"])

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    telegram_thread = threading.Thread(target=run_telegram_bot)

    flask_thread.start()
    telegram_thread.start()

    flask_thread.join()
    telegram_thread.join()
