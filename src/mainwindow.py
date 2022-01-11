# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QMainWindow, QMenu, QHeaderView
from PyQt5 import uic, QtCore
from PyQt5.QtSql import QSqlTableModel
from src.productwidget import ProductWidget
from src.sqlconnection import SqlConnection
from src.dao.customerdao import CustomerDAO
from src.dao.productdao import ProductDAO
from src.customerwidget import CustomerWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('src/mainwindow.ui', self)
        self.show()
        self.conn = SqlConnection()
        self.setUpTableView()

    def newProduct(self):
        self.productWidget = ProductWidget()
        self.productWidget.show()

    def newCustomer(self):
        self.customerWidget = CustomerWidget()
        self.customerWidget.show()

    def editItem(self, row):
        currentIndex = self.tabWidget.currentIndex()
        recordId = self.tableModel.index(row, 0).data()

        if(currentIndex == 0):
            dao = CustomerDAO()
            self.customerWidget = CustomerWidget()
            self.customerWidget.edit(dao.select(recordId))
            self.customerWidget.show()

        elif(currentIndex == 1):
            pass

        elif(currentIndex == 2):
            dao = ProductDAO()
            product = dao.select(recordId)

            self.productWidget = ProductWidget()
            self.productWidget.edit(product)
            self.productWidget.show()

    def deleteItem(self):
        print("delete row")

    def customContextMenuRequestedTableView(self, pos):
        contextMenu = QMenu()
        contextMenu.addAction(self.actionEditItem)
        contextMenu.addAction(self.actionDeleteItem)
        contextMenu.exec(self.tableView.mapToGlobal(pos))

    def doubleClickedTableView(self, modelIndex):
        self.editItem(modelIndex.row())

    @QtCore.pyqtSlot()
    def setUpTableView(self):
        self.tableModel = QSqlTableModel()
        currentIndex = self.tabWidget.currentIndex()

        columnsToHide = []
        columnsToShow = []
        headers = []

        if(currentIndex == 0):
            self.tableModel.setTable("customer")
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
            self.tableModel.setFilter(" UPPER(name) LIKE UPPER('" + self.searchProductLineEdit.text() + "'||'%')")
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
            columnsToShow += [0, 1, 2, 3]
            headers += ["ID",
                        "Customer",
                        "Amount",
                        "Date"]

        elif(currentIndex == 4):
            self.tableModel.setTable("purchase_view")
            columnsToShow += [0, 1, 2, 3]
            headers += ["ID",
                        "Supplier",
                        "Amount",
                        "Date"]

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
