# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal
from src.dao.productdao import ProductDAO
from src.dao.unitdao import UnitDAO
from src.entity.product import Product
from PyQt5.QtSql import QSqlTableModel
from src.unitwidget import UnitWidget


class ProductWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ProductWidget, self).__init__()
        uic.loadUi('src/productwidget.ui', self)
        self.mode = "new"
        self.unitModel = QSqlTableModel()
        self.unitModel.setTable("unit")
        self.unitModel.select()
        self.unitComboBox.setModel(self.unitModel)
        self.unitComboBox.setModelColumn(2)
        self.productId = None
        self.productUpserted = pyqtSignal()

    def edit(self, product):
        self.productId = product.id
        self.nameLineEdit.setText(product.name)
        self.descriptionLineEdit.setText(product.description)
        self.priceSpinBox.setValue(product.price)
        self.costSpinBox.setValue(product.cost)
        self.quantitySpinBox.setValue(product.quantity)
        self.barcodeLineEdit.setText(product.barcode)
        self.mode = "edit"
        dao = UnitDAO()
        abbr = dao.select(product.unitId).abbreviation
        unitIndex = self.unitComboBox.findData(abbr, QtCore.Qt.DisplayRole)
        self.unitComboBox.setCurrentIndex(unitIndex)

    def setUnitMeasure(self):
        self.quantitySpinBox.setSuffix(" " + self.unitComboBox.currentText())

    def save(self):
        dao = ProductDAO()
        saveFunction = dao.update
        unitCurrentIndex = self.unitComboBox.currentIndex()
        if self.mode == "new":
            saveFunction = dao.insert

        saveFunction(Product(self.productId,
                             self.nameLineEdit.text(),
                             self.descriptionLineEdit.text(),
                             self.priceSpinBox.value(),
                             self.costSpinBox.value(),
                             self.quantitySpinBox.value(),
                             self.barcodeLineEdit.text(),
                             self.unitModel.index(unitCurrentIndex, 0).data()))
        self.close()

    def cancel(self):
        self.cancelMessage = QMessageBox(self)
        self.cancelMessage.setWindowTitle("Cancel")
        self.cancelMessage.setText("Are you sure?")
        self.cancelMessage.addButton("Yes", QMessageBox.AcceptRole)
        self.cancelMessage.addButton("No", QMessageBox.RejectRole)
        if(self.cancelMessage.exec() == QMessageBox.AcceptRole):
            self.close()

    def newUnitMeasure(self):
        self.unitWidget = UnitWidget()
        self.unitWidget.show()
