"""
Файл для повторения темы сигналов

Напомнить про работу с сигналами и изменением Ui.

Предлагается создать приложение, которое принимает в lineEditInput строку от пользователя,
и при нажатии на pushButtonMirror отображает в lineEditMirror введённую строку в обратном
порядке (задом наперед).
"""

from PySide6 import QtWidgets
from form_a import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButtonMirror.clicked.connect(self.mirror)
        self.ui.lineEditInput.textChanged.connect(self.mirror)
        self.ui.lineEditMirror.textEdited.connect(lambda x: self.ui.lineEdit_3.setText(x[::-1]))
        self.ui.radioButton.toggled.connect(self.button)

    def mirror(self):
        input_text = self.ui.lineEditInput.text()[::-1]
        self.ui.lineEditMirror.setText(input_text)

    def button(self, param):
        if param is True:
            self.ui.lineEdit_3.setText("Кнопка нажата")
        else:
            self.ui.lineEdit_3.setText("Кнопка отжата")



if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
