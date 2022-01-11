# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore, uic
from PyQt5 import QtWidgets
from src.dao.saledao import SaleDAO

class SaleWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SaleWidget, self).__init__()
        uic.loadUi('src/salewidget.ui', self)
        self.mode = "new"

    def edit(self, sale):
        self.mode = "edit"
        self.saleId = sale.id
        saledao = SaleDAO()
        products = saledao.selectProducts(sale.id)

    def save(self):
        pass

    def addItem(self):
        pass
