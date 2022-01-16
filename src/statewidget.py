# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, uic, QtCore
from src.entity.state import State
from src.dao.statedao import StateDAO
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import pyqtSignal


class StateWidget(QtWidgets.QWidget):
    stateUpserted = pyqtSignal()

    def __init__(self):
        super(StateWidget, self).__init__()
        uic.loadUi('src/statewidget.ui', self)
        self.mode = "new"
        self.countryModel = QSqlTableModel()
        self.countryModel.setTable("country")
        self.countryModel.select()
        self.countryComboBox.setModel(self.countryModel)

    def setCountry(self, countryId):
        countryIndex = self.countryComboBox.findData(countryId, QtCore.Qt.DisplayRole)
        self.countryComboBox.setCurrentIndex(countryIndex)
        self.countryComboBox.setModelColumn(1)

    def edit(self, state):
        self.mode = "edit"

    def save(self):
        countryIndex = self.countryComboBox.currentIndex()
        countryId = self.countryModel.index(countryIndex, 0).data()
        dao = StateDAO()
        if self.mode == "new":
            dao.insert(State(None,
                             self.nameLineEdit.text(),
                             self.codeLineEdit.text(),
                             countryId))
        self.stateUpserted.emit()
        self.close()
