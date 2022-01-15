# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import pyqtSignal
from src.dao.supplierdao import SupplierDAO
from src.dao.statedao import StateDAO
from src.dao.citydao import CityDAO
from PyQt5.QtSql import QSqlTableModel
from src.entity.supplier import Supplier


class SupplierWidget(QtWidgets.QWidget):
    supplierUpserted = pyqtSignal()

    def __init__(self):
        super(SupplierWidget, self).__init__()
        uic.loadUi('src/supplierwidget.ui', self)
        self.mode = "new"
        self.setCountryModel()
        self.supplierId = 0

    def edit(self, supplier):
        self.mode = "edit"
        self.supplierId = supplier.id
        self.nameLineEdit.setText(supplier.name)
        self.addressLine1LineEdit.setText(supplier.addressLine1)
        self.addressLine2LineEdit.setText(supplier.addressLine2)

        stateDao = StateDAO()
        cityDao = CityDAO()

        stateId = cityDao.select(supplier.cityId).stateId
        stateDao = StateDAO()
        state = stateDao.select(stateId)
        cityDao = CityDAO()
        city = cityDao.select(supplier.cityId)
        countryId = stateDao.select(stateId).countryId
        self.countryComboBox.setCurrentIndex(countryId - 1)
        stateIndex = self.stateComboBox.findData(state.name, QtCore.Qt.DisplayRole)
        self.stateComboBox.setCurrentIndex(stateIndex)
        cityIndex = self.cityComboBox.findData(city.name, QtCore.Qt.DisplayRole)
        self.cityComboBox.setCurrentIndex(cityIndex)

        self.emailLineEdit.setText(supplier.email)
        self.phoneNumberLineEdit.setText(str(supplier.phoneNumber))

    def save(self):
        dao = SupplierDAO()
        saveFunction = dao.update

        if self.mode == "new":
            saveFunction = dao.insert

        cityCurrentIndex = self.cityComboBox.currentIndex()
        cityId = self.cityModel.index(cityCurrentIndex, 0).data(QtCore.Qt.DisplayRole)

        saveFunction(Supplier(self.supplierId,
                              self.nameLineEdit.text(),
                              self.addressLine1LineEdit.text(),
                              self.addressLine2LineEdit.text(),
                              cityId,
                              self.emailLineEdit.text(),
                              self.phoneNumberLineEdit.text()))
        self.supplierUpserted.emit()
        self.close()

    def setCountryModel(self):
        self.countryModel = QSqlTableModel()
        self.countryModel.setTable("country")
        self.countryModel.select()
        self.countryComboBox.setModel(self.countryModel)
        self.countryComboBox.setModelColumn(1)

    def setStateModel(self):
        self.stateModel = QSqlTableModel()
        self.stateModel.setTable("state")
        currentIndex = self.countryComboBox.currentIndex()
        countryId = self.countryModel.index(currentIndex, 0).data()
        self.stateModel.setFilter("country_id = " + str(countryId))
        self.stateModel.select()
        self.stateComboBox.setModel(self.stateModel)
        self.stateComboBox.setModelColumn(1)

    def setCityModel(self):
        self.cityModel = QSqlTableModel()
        self.cityModel.setTable("city")
        currentIndex = self.stateComboBox.currentIndex()
        stateId = self.stateModel.index(currentIndex, 0).data()
        self.cityModel.setFilter("state_id = " + str(stateId))
        self.cityModel.select()
        self.cityComboBox.setModel(self.cityModel)
        self.cityComboBox.setModelColumn(1)
