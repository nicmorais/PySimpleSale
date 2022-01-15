# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, uic
from src.entity.country import Country
from src.dao.countrydao import CountryDAO
from PyQt5.QtCore import pyqtSignal


class CountryWidget(QtWidgets.QWidget):
    countryUpserted = pyqtSignal()

    def __init__(self):
        super(CountryWidget, self).__init__()
        uic.loadUi('src/countrywidget.ui', self)
        self.mode = "new"

    def edit(self, country):
        self.mode = "edit"
        self.countryId = country.id
        self.nameLineEdit.setText(country.name)
        self.codeLineEdit.setText(country.code)

    def save(self):
        dao = CountryDAO()
        if self.mode == "new":
            dao.insert(Country(self.nameLineEdit.text(),
                               self.codeLineEdit.text()))
        else:
            dao.update(Country(self.nameLineEdit.text()),
                       self.codeLineEdit.text())

        self.countryUpserted.emit()
