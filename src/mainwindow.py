# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QMainWindow, QMenu, QHeaderView, QMessageBox
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlTableModel
from src.productwidget import ProductWidget
from src.sqlconnection import SqlConnection
from src.dao.customerdao import CustomerDAO
from src.dao.productdao import ProductDAO
from src.dao.countrydao import CountryDAO
from src.dao.statedao import StateDAO
from src.customerwidget import CustomerWidget
from src.salewidget import SaleWidget
from src.dao.saledao import SaleDAO
from src.supplierwidget import SupplierWidget
from src.dao.supplierdao import SupplierDAO
from src.reportswidget import ReportsWidget
from src.countrieswidget import CountriesWidget
from src.stateswidget import StatesWidget
from src.citieswidget import CitiesWidget
from src.unitswidget import UnitsWidget
from src.settingswidget import SettingsWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('src/mainwindow.ui', self)
        self.show()
        self.conn = SqlConnection()
        self.setUpTableView()
        self.searchSaleDateEdit.setDate(QDate.currentDate())

    def newCustomer(self):
        self.customerWidget = CustomerWidget()
        self.customerWidget.customerUpserted.connect(self.setUpTableView)
        self.customerWidget.show()

    def newProduct(self):
        self.productWidget = ProductWidget()
        self.productWidget.productUpserted.connect(self.setUpTableView)
        self.productWidget.show()

    def newSale(self):
        self.saleWidget = SaleWidget()
        self.saleWidget.saleUpserted.connect(self.setUpTableView)
        self.saleWidget.show()

    def newSupplier(self):
        self.suplierWidget = SupplierWidget()
        self.suplierWidget.show()

    def editItem(self, row):
        currentIndex = self.tabWidget.currentIndex()
        recordId = self.tableModel.index(row, 0).data()

        if currentIndex == 0:
            dao = CustomerDAO()
            self.customerWidget = CustomerWidget()
            self.customerWidget.edit(dao.select(recordId))
            self.customerWidget.customerUpserted.connect(self.setUpTableView)
            self.customerWidget.show()

        elif currentIndex == 1:
            dao = SupplierDAO()
            self.supplierWidget = SupplierWidget()
            self.supplierWidget.edit(dao.select(recordId))
            self.supplierWidget.supplierUpserted.connect(self.setUpTableView)
            self.supplierWidget.show()

        elif currentIndex == 2:
            dao = ProductDAO()
            product = dao.select(recordId)

            self.productWidget = ProductWidget()
            self.productWidget.edit(product)
            self.productWidget.productUpserted.connect(self.setUpTableView)
            self.productWidget.show()

        elif currentIndex == 3:
            dao = SaleDAO()
            self.saleWidget = SaleWidget()
            self.saleWidget.edit(dao.select(recordId))
            self.saleWidget.saleUpserted.connect(self.setUpTableView)
            self.saleWidget.show()

    def deleteItem(self):
        currentIndex = self.tabWidget.currentIndex()
        row = self.tableView.selectionModel().selectedRows()[0].row()
        recordId = self.tableModel.index(row, 0).data()

        message = QMessageBox()
        message.setWindowTitle("Delete item")
        message.setText("Are you sure?")
        message.addButton("Yes", QMessageBox.AcceptRole)
        message.addButton("No", QMessageBox.RejectRole)

        if(message.exec() == QMessageBox.RejectRole):
            return

        dao = None
        success = True

        if currentIndex == 0:
            dao = CustomerDAO()
            success = dao.delete(recordId)

        elif currentIndex == 1:
            dao = SupplierDAO()
            success = dao.delete(recordId)

        elif currentIndex == 2:
            dao = ProductDAO()
            success = dao.delete(recordId)

        elif currentIndex == 3:
            dao = SaleDAO()
            success = dao.delete(recordId)

        self.setUpTableView()
        if not success:
            error = dao.lastError.driverText
            errorMessage = QMessageBox()
            errorMessage.setWindowTitle("Error")
            errorMessage.setText("Could not delete item: " + error)
            errorMessage.exec()

    def customContextMenuRequestedTableView(self, pos):
        contextMenu = QMenu()
        contextMenu.addAction(self.actionEditItem)
        contextMenu.addAction(self.actionDeleteItem)
        contextMenu.exec(self.tableView.mapToGlobal(pos))

    def doubleClickedTableView(self, modelIndex):
        self.editItem(modelIndex.row())

    def setUpTableView(self):
        scrollValue = self.tableView.verticalScrollBar().value()
        self.tableModel = QSqlTableModel()
        currentIndex = self.tabWidget.currentIndex()

        columnsToHide = []
        columnsToShow = []
        headers = []
        filter = ""
        if(currentIndex == 0):
            self.tableModel.setTable("customer")
            filter = "UPPER(name) LIKE UPPER ('{0}'||'%')"
            filter = filter.format(self.searchCustomerLineEdit.text())
            columnsToHide += [2, 3, 4, 7]
            columnsToShow += [0, 1, 8]
            headers += ["ID",
                        "Name",
                        "Address Line 1",
                        "Address Line 2",
                        "Zipcode",
                        "E-mail",
                        "Phone"]

        elif(currentIndex == 1):
            self.tableModel.setTable("supplier")
            filter = "UPPER(name) LIKE UPPER('{0}'||'%')"
            filter = filter.format(self.searchSupplierLineEdit.text())
            columnsToHide += [2, 3, 4]
            columnsToShow += [0, 1, 5, 6]
            headers += ["ID",
                        "Name",
                        "Address Line 1",
                        "Address Line 2",
                        "City ID",
                        "E-mail",
                        "Phone"]

        elif(currentIndex == 2):
            self.tableModel.setTable("product")
            filter = "UPPER(name) LIKE UPPER('{0}'||'%')"
            filter = filter.format(self.searchProductLineEdit.text())
            columnsToHide += [2, 6, 7]
            columnsToShow += [0, 1, 3, 4, 5]
            headers += ["ID",
                        "Name",
                        "Description",
                        "Price",
                        "Cost",
                        "Quantity"]

        elif(currentIndex == 3):
            self.tableModel.setTable("sale_view")

            if self.searchSaleCheckBox.isChecked():
                filter = "UPPER(name) LIKE UPPER('{0}'||'%')"
                filter = filter.format(self.searchSaleLineEdit.text())
            else:
                dt = self.searchSaleDateEdit.dateTime().toString('yyyy-MM-dd')
                filter = ("UPPER(name) LIKE UPPER('{0}'||'%') "
                          "AND datetime LIKE ('{1}'||'%')")
                filter = filter.format(self.searchSaleLineEdit.text(), dt)
            columnsToShow += [0, 1, 2, 3]
            headers += ["ID",
                        "Customer",
                        "Amount",
                        "Date"]

        elif(currentIndex == 4):
            self.tableModel.setTable("purchase_view")
            filter = "UPPER(name) LIKE UPPER('{0}'||'%')"
            filter.format(self.searchPurchaseLineEdit.text())

            columnsToShow += [0, 1, 2, 3]
            headers += ["ID",
                        "Supplier",
                        "Amount",
                        "Date"]

        self.tableModel.setFilter(filter)
        self.tableView.setModel(self.tableModel)
        self.tableModel.select()

        headerNum = 0
        for header in headers:
            self.tableModel.setHeaderData(headerNum,
                                          QtCore.Qt.Horizontal,
                                          header)
            headerNum = headerNum + 1

        for column in columnsToHide:
            self.tableView.hideColumn(column)

        for column in columnsToShow:
            self.tableView.showColumn(column)

        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableView.verticalScrollBar().setValue(scrollValue)

    def openReports(self):
        self.reportsWidget = ReportsWidget()
        self.reportsWidget.show()

    def openCountries(self):
        self.countriesWidget = CountriesWidget()
        self.countriesWidget.show()

    def openStates(self):
        dao = CountryDAO()
        countryCount = dao.count()

        if(countryCount == 0):
            errorMessage = QMessageBox()
            errorMessage.setWindowTitle("Error")
            errorMessage.setText("Error: no countries were found in the database.")
            errorMessage.exec()
        else:
            self.statesWidget = StatesWidget()
            self.statesWidget.show()

    def openCities(self):
        dao = StateDAO()
        stateCount = dao.count()

        if(stateCount == 0):
            errorMessage = QMessageBox()
            errorMessage.setWindowTitle("Error")
            errorMessage.setText("Error: no states were found in the database.")
            errorMessage.exec()
        else:
            self.citiesWidget = CitiesWidget()
            self.citiesWidget.show()

    def openUnits(self):
        self.unitsWidget = UnitsWidget()
        self.unitsWidget.show()

    def openSettings(self):
        self.settingsWidget = SettingsWidget()
        self.settingsWidget.show()
