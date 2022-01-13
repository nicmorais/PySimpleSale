# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QCompleter, QHeaderView, QStyledItemDelegate
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from src.dao.saledao import SaleDAO
from src.dao.saleproductdao import SaleProductDAO
from src.dao.productdao import ProductDAO
from src.dao.customerdao import CustomerDAO
from src.entity.saleproduct import SaleProduct
from src.entity.sale import Sale


class SaleWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SaleWidget, self).__init__()
        uic.loadUi('src/salewidget.ui', self)
        self.mode = "new"
        self.customerCompleter = QCompleter()
        self.customerModel = QSqlTableModel()
        self.customerModel.setTable("customer")
        self.customerModel.select()
        self.customerCompleter.setModel(self.customerModel)
        self.customerCompleter.setCompletionColumn(1)
        self.customerLineEdit.setCompleter(self.customerCompleter)
        self.customerCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.productCompleter = QCompleter()
        self.productModel = QSqlTableModel()
        self.productModel.setTable("product")
        self.productModel.select()
        self.productCompleter.setModel(self.productModel)
        self.productCompleter.setCompletionColumn(1)
        self.productLineEdit.setCompleter(self.productCompleter)
        self.productCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.customerLineEdit.setFocus()
        self.tableView.addAction(self.actionDeleteItem)

        self.tableModel = QStandardItemModel()
        self.tableView.setModel(self.tableModel)

        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        self.delegate = QStyledItemDelegate()
        self.tableView.setItemDelegateForColumn(2, self.delegate)
        self.tableView.itemDelegateForColumn(2).closeEditor.connect(self.updateProductsTotals)

        headerLabels = ["Product ID",
                        "Name",
                        "Qty",
                        "Price",
                        "Total"]
        self.tableModel.setHorizontalHeaderLabels(headerLabels)

    def edit(self, sale):
        self.mode = "edit"
        self.saleId = sale.id
        saleDao = SaleDAO()
        productDao = ProductDAO()

        saleProducts = saleDao.selectProducts(sale.id)

        for saleProduct in saleProducts:
            productIdItem = QStandardItem()
            nameItem = QStandardItem()
            qtyItem = QStandardItem()
            priceItem = QStandardItem()
            totalItem = QStandardItem()
            operationItem = QStandardItem()
            saleProductIdItem = QStandardItem()

            productIdItem.setData(saleProduct.productId, QtCore.Qt.DisplayRole)
            name = productDao.select(saleProduct.productId).name
            nameItem.setData(name, QtCore.Qt.DisplayRole)

            qtyItem.setData(saleProduct.quantity, QtCore.Qt.DisplayRole)
            priceItem.setData(saleProduct.price, QtCore.Qt.DisplayRole)

            total = float(saleProduct.quantity) * float(saleProduct.price)
            totalItem.setData(total, QtCore.Qt.DisplayRole)
            operationItem.setData("UPDATE", QtCore.Qt.DisplayRole)
            saleProductIdItem.setData(saleProduct.id, QtCore.Qt.DisplayRole)

            fields = [productIdItem,
                      QStandardItem(productDao.select(saleProduct.productId).name),
                      qtyItem,
                      priceItem,
                      totalItem,
                      operationItem,
                      saleProductIdItem]
            self.tableModel.appendRow(fields)

        self.updateTotalAmount()

        self.dateTimeEdit.setDateTime(QDateTime.fromString(sale.datetime, 'yyyy-MM-dd HH:mm:ss'))
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableView.hideColumn(5)
        self.tableView.hideColumn(6)

        customerDao = CustomerDAO()
        customerId = sale.customerId

        self.customerLineEdit.setText(customerDao.select(customerId).name)
        startIndex = self.customerModel.index(0, 0)
        customerIndex = self.customerModel.match(startIndex, 0, customerId)[0]
        self.customerCompleter.setCurrentRow(customerIndex.row())

    def save(self):
        saleDao = SaleDAO()
        customerId = self.customerCompleter.popup().currentIndex().siblingAtColumn(0).data()
        amount = self.getTotalAmount()
        discount = self.discountSpinBox.value()
        shipping = self.shippingSpinBox.value()
        datetime = self.dateTimeEdit.dateTime().toString('yyyy-MM-dd HH:mm:ss')

        if self.mode == "new":
            self.saleId = saleDao.insert(Sale(None,
                                              customerId,
                                              amount,
                                              discount,
                                              shipping,
                                              datetime))
        else:
            saleDao.update(Sale(self.saleId,
                                customerId,
                                amount,
                                discount,
                                shipping,
                                datetime))

        for row in range(self.tableModel.rowCount()):
            rowData = self.tableModel.index(row, 5).data(QtCore.Qt.DisplayRole)

            if rowData == "INSERT":
                self.insertRow(row)
            elif rowData == "UPDATE":
                self.updateRow(row)
            else:
                self.deleteRow(row)

    def insertRow(self, row):
        dao = SaleProductDAO()
        price = self.tableModel.index(row, 3).data(QtCore.Qt.DisplayRole)
        quantity = self.tableModel.index(row, 2).data(QtCore.Qt.DisplayRole)
        productId = self.tableModel.index(row, 0).data(QtCore.Qt.DisplayRole)
        dao.insert(SaleProduct(None,
                               price,
                               quantity,
                               productId,
                               self.saleId))

    def updateRow(self, row):
        dao = SaleProductDAO()
        id = self.tableModel.index(row, 6).data(QtCore.Qt.DisplayRole)
        price = self.tableModel.index(row, 3).data(QtCore.Qt.DisplayRole)
        quantity = self.tableModel.index(row, 2).data(QtCore.Qt.DisplayRole)
        productId = self.tableModel.index(row, 0).data(QtCore.Qt.DisplayRole)
        dao.update(SaleProduct(id,
                               price,
                               quantity,
                               productId,
                               self.saleId))

    def deleteRow(self, row):
        dao = SaleProductDAO()
        id = self.tableModel.index(row, 6).data(QtCore.Qt.DisplayRole)

        dao.delete(id)

    def addItem(self):
        idItem = QStandardItem()
        nameItem = QStandardItem()
        qtyItem = QStandardItem()
        priceItem = QStandardItem()
        totalItem = QStandardItem()
        operationItem = QStandardItem()

        productCurrentIndex = self.productCompleter.popup().currentIndex()

        id = productCurrentIndex.siblingAtColumn(0).data()
        name = productCurrentIndex.siblingAtColumn(1).data()
        qty = float(self.quantityLineEdit.text())
        price = self.priceSpinBox.value()

        idItem.setData(id, QtCore.Qt.DisplayRole)
        nameItem.setData(name, QtCore.Qt.DisplayRole)
        qtyItem.setData(qty, QtCore.Qt.DisplayRole)
        priceItem.setData(price, QtCore.Qt.DisplayRole)
        totalItem.setData(qty * price, QtCore.Qt.DisplayRole)
        operationItem.setData("INSERT", QtCore.Qt.DisplayRole)

        fields = [idItem,
                  nameItem,
                  qtyItem,
                  priceItem,
                  totalItem,
                  operationItem]

        self.tableModel.appendRow(fields)
        self.quantityLineEdit.setText("1")
        self.productLineEdit.clear()
        self.productLineEdit.setFocus()
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableView.hideColumn(5)
        self.tableView.hideColumn(6)
        self.updateTotalAmount()

    def deleteItem(self):
        selectedIndex = self.tableView.selectionModel().selectedRows()[0]

        if self.mode == "new":
            self.tableView.removeRow(selectedIndex.row())
        else:
            deleteItem = QStandardItem()
            deleteItem.setData("DELETE", QtCore.Qt.DisplayRole)
            self.tableModel.setItem(selectedIndex.row(), 5, deleteItem)
            self.tableView.hideRow(selectedIndex.row())
        self.updateTotalAmount()

    def getTotalAmount(self):
        sum = 0

        for row in range(0, self.tableModel.rowCount()):
            if not self.tableView.isRowHidden(row):
                sum += self.tableModel.item(row, 4).data(QtCore.Qt.DisplayRole)
        return sum

    def selectProduct(self):
        productCurrentIndex = self.productCompleter.popup().currentIndex()
        price = productCurrentIndex.siblingAtColumn(3).data()
        if price is not None:
            self.priceSpinBox.setValue(price)

    def updateTotalAmount(self):
        discount = self.discountSpinBox.value()
        shipping = self.shippingSpinBox.value()
        self.totalAmountLabel.setText("$ " + "{:.2f}".format(self.getTotalAmount() - discount + shipping))

    def updateProductsTotals(self):
        for row in range(0, self.tableModel.rowCount()):
            totalItem = QStandardItem()
            quantity = self.tableModel.index(row, 2).data(QtCore.Qt.DisplayRole)
            price = self.tableModel.index(row, 3).data(QtCore.Qt.DisplayRole)
            totalItem.setData(quantity * price, QtCore.Qt.DisplayRole)
            self.tableModel.setItem(row, 4, totalItem)
