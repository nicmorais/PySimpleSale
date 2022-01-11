# This Python file uses the following encoding: utf-8
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtSql import QSqlTableModel
from src.entity.customer import Customer
from src.dao.customerdao import CustomerDAO
from src.dao.statedao import StateDAO
from src.dao.citydao import CityDAO


class CustomerWidget(QWidget):
    def __init__(self):
        super(CustomerWidget, self).__init__()
        uic.loadUi('src/customerwidget.ui', self)
        self.mode = "new"
        self.setCountryModel()

    def edit(self, customer):
        self.mode = "edit"
        self.customerId = customer.id
        self.nameLineEdit.setText(customer.name)
        self.addressLine1LineEdit.setText(customer.addressLine1)
        self.addressLine2LineEdit.setText(customer.addressLine2)
        self.zipcodeLineEdit.setText(customer.zipcode)
        self.emailLineEdit.setText(customer.email)
        self.phoneNumberLineEdit.setText(str(customer.phoneNumber))

        stateDao = StateDAO()
        cityDao = CityDAO()

        stateId = cityDao.select(customer.cityId).stateId
        stateDao = StateDAO()
        state = stateDao.select(stateId)
        cityDao = CityDAO()
        city = cityDao.select(customer.cityId)
        countryId = stateDao.select(stateId).countryId
        self.countryComboBox.setCurrentIndex(countryId - 1)
        stateIndex = self.stateComboBox.findData(state.name, QtCore.Qt.DisplayRole)
        self.stateComboBox.setCurrentIndex(stateIndex)
        cityIndex = self.cityComboBox.findData(city.name, QtCore.Qt.DisplayRole)
        self.cityComboBox.setCurrentIndex(cityIndex)

    def save(self):
        dao = CustomerDAO()
        saveFunction = dao.update

        if self.mode == "new":
            saveFunction = dao.insert
        cityCurrentIndex = self.cityComboBox.currentIndex()
        cityId = self.cityModel.index(cityCurrentIndex, 0).data()

        saveFunction(Customer(self.customerId,
                              self.nameLineEdit.text(),
                              self.addressLine1LineEdit.text(),
                              self.addressLine2LineEdit.text(),
                              self.zipcodeLineEdit.text(),
                              self.emailLineEdit.text(),
                              self.phoneNumberLineEdit.text(),
                              cityId))
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
        self.stateModel.select()
        self.stateComboBox.setModel(self.stateModel)
        self.stateComboBox.setModelColumn(1)

    def setCityModel(self):
        self.cityModel = QSqlTableModel()
        self.cityModel.setTable("city")
        self.cityModel.select()
        self.cityComboBox.setModel(self.cityModel)
        self.cityComboBox.setModelColumn(1)
