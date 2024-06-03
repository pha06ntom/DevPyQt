from datetime import datetime


def timestamps_handler(ts):
    """
    Функция для обработки времени
    """
    dt = datetime.fromtimestamp(ts)
    return dt.strftime("%I%p").lstrip('0')
