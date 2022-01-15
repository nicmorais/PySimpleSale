# This Python file uses the following encoding: utf-8
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtSql import QSqlQueryModel


class ReportsWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ReportsWidget, self).__init__()
        uic.loadUi('src/reportswidget.ui', self)
        self.setUpTable()

    def setUpTable(self):
        self.tableModel = QSqlQueryModel()
        currentIndex = self.revenueComboBox.currentIndex()
        if currentIndex == 0:
            self.tableModel.setQuery("SELECT SUBSTR(datetime, 1, 7) AS Month, "
            "SUM(amount) AS Total FROM sale GROUP BY 1")
        else:
            self.tableModel.setQuery("SELECT SUBSTR(datetime, 1, 4) AS Year, "
            "SUM(amount) AS Total FROM sale GROUP BY 1")
        self.tableView.setModel(self.tableModel)
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
