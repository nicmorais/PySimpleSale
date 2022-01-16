# This Python file uses the following encoding: utf-8
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QHeaderView
from src.statewidget import StateWidget


class StatesWidget(QtWidgets.QWidget):
    def __init__(self):
        super(StatesWidget, self).__init__()
        uic.loadUi('src/stateswidget.ui', self)
        self.tableModel = QSqlTableModel()
        self.tableModel.setTable("state")
        self.tableView.setModel(self.tableModel)
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        headers = ["ID",
                   "Name",
                   "Code"]

        headerNum = 0
        for header in headers:
            self.tableModel.setHeaderData(headerNum,
                                          QtCore.Qt.Horizontal,
                                          header)
            headerNum = headerNum + 1

        self.countryModel = QSqlTableModel()
        self.countryModel.setTable("country")
        self.countryModel.select()
        self.countryComboBox.setModel(self.countryModel)
        self.countryComboBox.setModelColumn(1)

        self.updateTable()

    def updateTable(self):
        countryIndex = self.countryComboBox.currentIndex()
        countryId = self.countryModel.index(countryIndex, 0).data()
        self.tableModel.setFilter("country_id = " + str(countryId))
        self.tableModel.select()
        self.tableView.hideColumn(3)

    def newState(self):
        countryIndex = self.countryComboBox.currentIndex()
        countryId = self.countryModel.index(countryIndex, 0).data()
        self.stateWidget = StateWidget()
        self.stateWidget.setCountry(countryId)
        self.stateWidget.stateUpserted.connect(self.updateTable)
        self.stateWidget.show()
