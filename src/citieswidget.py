# This Python file uses the following encoding: utf-8
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtSql import QSqlQueryModel, QSqlTableModel
from PyQt5.QtWidgets import QHeaderView
from src.citywidget import CityWidget


class CitiesWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CitiesWidget, self).__init__()
        uic.loadUi('src/citieswidget.ui', self)
        self.countryModel = QSqlQueryModel()
        self.stateModel = QSqlTableModel()
        self.cityModel = QSqlTableModel()

        self.countryModel.setQuery("SELECT country_id,"
                                   "c.name, c.code, count(*) "
                                   "FROM state JOIN country c "
                                   "USING (country_id) "
                                   "GROUP BY 1, 2, 3")
        self.countryComboBox.setModel(self.countryModel)
        self.countryComboBox.setModelColumn(1)

        self.stateModel.setTable("state")
        self.stateComboBox.setModel(self.stateModel)
        self.stateComboBox.setModelColumn(1)
        self.setState()

        headers = ["ID",
                   "Name"]

        self.cityModel.setTable("city")
        self.tableView.setModel(self.cityModel)

        headerNum = 0
        for header in headers:
            self.cityModel.setHeaderData(headerNum,
                                         QtCore.Qt.Horizontal,
                                         header)
            headerNum = headerNum + 1

        self.updateTable()
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableView.hideColumn(2)

    def setState(self):
        countryIndex = self.countryComboBox.currentIndex()
        countryId = self.countryModel.index(countryIndex, 0).data()
        self.stateModel.setFilter("country_id = " + str(countryId))
        self.stateModel.select()

    def updateTable(self):
        stateIndex = self.stateComboBox.currentIndex()
        stateId = self.stateModel.index(stateIndex, 0).data()
        self.cityModel.setFilter("state_id = " + str(stateId))
        self.cityModel.select()

    def newCity(self):
        stateIndex = self.stateComboBox.currentIndex()
        stateId = self.stateModel.index(stateIndex, 0).data()
        self.cityWidget = CityWidget()
        self.cityWidget.stateId = stateId
        self.cityWidget.cityUpserted.connect(self.updateTable)
        self.cityWidget.show()
