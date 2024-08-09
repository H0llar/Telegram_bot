START_MESSAGE = "Здравствуйте! Используйте команду /orders для получения заказов и /order для получения информации о конкретном заказе."
REQUEST_ORDER_NUMBER_MESSAGE = "Пожалуйста, введите номер заказа после команды /order"
NO_ORDERS_FOUND_MESSAGE = "Не удалось получить заказы."
NO_ORDER_NUMBER_PROVIDED_MESSAGE = "Пожалуйста, введите номер заказа после команды /order."
ORDER_INFO_TEMPLATE = (
    "Номер: {number}\n"
    "Сделка: {product}\n"
    "Статус: {status}\n"
    "Дата: {date}\n"
    "Партнер: {partner}\n"
    "Сумма: {sum} руб.\n"
    "Телеграм: {telegram_id}\n"
)
