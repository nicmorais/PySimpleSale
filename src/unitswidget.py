# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QHeaderView
from src.unitwidget import UnitWidget


class UnitsWidget(QtWidgets.QWidget):
    def __init__(self):
        super(UnitsWidget, self).__init__()
        uic.loadUi('src/unitswidget.ui', self)
        self.tableModel = QSqlTableModel()
        self.tableModel.setTable("unit")
        self.tableView.setModel(self.tableModel)
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.updateTable()

        headers = ["ID",
                   "Name",
                   "Abbreviation"]

        headerNum = 0
        for header in headers:
            self.tableModel.setHeaderData(headerNum,
                                          QtCore.Qt.Horizontal,
                                          header)
            headerNum = headerNum + 1

    def newUnit(self):
        self.unitWidget = UnitWidget()
        self.unitWidget.unitUpserted.connect(self.updateTable)
        self.unitWidget.show()

    def updateTable(self):
        self.tableModel.select()
