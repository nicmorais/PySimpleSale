# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, uic
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QHeaderView
from src.countrywidget import CountryWidget


class CountriesWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CountriesWidget, self).__init__()
        uic.loadUi('src/countrieswidget.ui', self)
        self.tableModel = QSqlTableModel()
        self.tableModel.setTable("country")
        self.tableModel.select()
        self.tableView.setModel(self.tableModel)
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def newCountry(self):
        self.countryWidget = CountryWidget()
        self.countryWidget.countryUpserted.connect(self.updateTable)
        self.countryWidget.show()

    def editSelected(self):
        pass

    def updateTable(self):
        self.tableModel.select()

