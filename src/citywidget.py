# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, uic
from src.dao.citydao import CityDAO
from src.entity.city import City
from PyQt5.QtCore import pyqtSignal


class CityWidget(QtWidgets.QWidget):
    cityUpserted = pyqtSignal()

    def __init__(self):
        super(CityWidget, self).__init__()
        uic.loadUi('src/citywidget.ui', self)
        self.stateId = 0
        self.mode = "new"

    def edit(self, city):
        self.mode = "edit"
        self.nameLineEdit.setText(city.name)

    def save(self):
        dao = CityDAO()

        if self.mode == "new":
            dao.insert(City(None,
                            self.nameLineEdit.text(),
                            self.stateId))
        else:
            dao.update(City(self.cityId,
                            self.nameLineEdit.text(),
                            self.stateId))
        self.cityUpserted.emit()
        self.close()
