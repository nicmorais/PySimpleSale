# This Python file uses the following encoding: utf-8
from src.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import sys

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.setWindowIcon(QIcon("data/icons/logo.svg"))
    sys.exit(app.exec())
