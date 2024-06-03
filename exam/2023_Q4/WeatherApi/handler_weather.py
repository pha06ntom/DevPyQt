import json
from urllib.parse import urlencode

import constants
import requests

from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
    Slot,
)

# OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")


# Определение пользовательских сигналов (событий), которые может посылать рабочий сервер
class HandlerSignals(QObject):
    finished = Signal()  # сигнал завершения рабочего процесса
    error = Signal(str)  # сигнал, выдающий сообщение об ошибке
    result = Signal(dict,
                    dict)  # сигнал, который возвращает данные вызова API в виде двух dict.Один представляет текущую
    # погоду, другой - прогноз погоды


class WeatherHandler(QRunnable):
    '''
    Worker thread for weather updates
    '''

    signals = HandlerSignals()
    is_interrupted = False

    def __init__(self, location):
        super().__init__()
        self.location = location  # местоположение

    @Slot()  # Используем для уменьшения объема требуемой памяти и увеличении скорости передачи сигналов
    def run(self):
        try:
            params = dict(q=self.location, appid=constants.OPENWEATHERMAP_API_KEY)
            url = 'http://api.openweathermap.org/data/2.5/weather?%s&units=metric' % urlencode(params)
            resp = requests.get(url)  # Запрос данных о текущей погоде
            weather = json.loads(resp.text)  # Функция loads() json преобразует строку в формате JSON в объект Python

            # Проверка не произошел ли сбой при запросе
            if weather['cod'] != 200:
                raise Exception(weather['message'])

            url = 'http://api.openweathermap.org/data/2.5/forecast?%s&units=metric' % urlencode(params)
            resp = requests.get(url)  # Запрос данных о прогнозе погоды на ближайшее время
            forecast = json.loads(resp.text)

            self.signals.result.emit(weather,
                                         forecast)  # signals позволяют передавать .emit значения, которые
            # используются в другом части кода
        except Exception as e:
            self.signals.error.emit(str(e))

        self.signals.finished.emit()

