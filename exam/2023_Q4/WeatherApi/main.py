import os
import sys

from utils import timestamps_handler

from weather import Ui_MainWindow
from PySide6.QtCore import (
    QThreadPool,
)
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
)

from handler_weather import WeatherHandler


class MainWindow(QMainWindow, Ui_MainWindow):

    # Пользовательский интерфейс
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.pressed.connect(self.update_weather)  # Инициализация запроса данных о погоде с помощью кнопки

        self.threadpool = QThreadPool()  # Настройка пула потоков (для исключения зависания приложения выполняем
        # запросы в отдельных потоках)

        self.show()

    # Запрос и обновление данных
    def update_weather(self):
        handler = WeatherHandler(self.lineEdit.text())
        handler.signals.result.connect(self.weather_result)
        handler.signals.error.connect(self.alarm)
        self.threadpool.start(handler)

    def alarm(self, message):
        '''
        Функция для отображения окна с сообщением об ошибке
        '''

        QMessageBox.warning(self, "Warning", message)

    # Обработка результата

    def weather_result(self, weather, forecasts):
        self.latitudeLabel.setText('%.2f °' % weather['coord']['lat'])
        self.longitudeLabel.setText('%.2f °' % weather['coord']['lon'])

        self.windLabel.setText('%.2f m/s' % weather['wind']['speed'])

        self.temperatureLabel.setText('%.1f °C' % weather['main']['temp'])
        self.pressureLabel.setText('%d' % weather['main']['pressure'])
        self.humidityLabel.setText('%d' % weather['main']['humidity'])

        self.weatherLabel.setText('%s (%s)' % (
            weather['weather'][0]['main'],
            weather['weather'][0]['description'],
        )
                                  )

        self.sunriseLabel.setText(timestamps_handler(weather['sys']['sunrise']))

        self.set_weather_icon(self.weatherIcon, weather['weather'])

        # Выполняем итерацию по 5-ти предоставленным прогнозам
        for n, forecast in enumerate(forecasts['list'][:5], 1):
            getattr(self, 'forecastTime%d' % n).setText(timestamps_handler(
                forecast['dt']))  # getattr() возвращает значение атрибута указанного объекта object по его имени name.
            self.set_weather_icon(getattr(self, 'forecastIcon%d' % n), forecast['weather'])
            getattr(self, 'forecastTemp%d' % n).setText('%.1f °C' % forecast['main']['temp'])

    def set_weather_icon(self, label, weather):
        label.setPixmap(QPixmap(os.path.join('images', '%s.png' % weather[0]['icon'])))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
