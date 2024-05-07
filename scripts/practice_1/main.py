# import sys
# from PySide6.QtWidgets import QApplication, QWidget
#
# app = QApplication(sys.argv)
#
# window = QWidget()
# window.setWindowTitle('Простейшее окно')
# window.show()
#
# sys.exit(app.exec())

from PySide6 import QtWidgets

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Основное окно')
        self.resize(300, 200)

app = QtWidgets.QApplication()

window = MainWindow()
window.show()

app.exec()