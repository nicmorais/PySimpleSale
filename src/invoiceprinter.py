# This Python file uses the following encoding: utf-8
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QPoint, QSettings
from src.dao.customerdao import CustomerDAO
from src.dao.citydao import CityDAO
from src.dao.statedao import StateDAO
from src.dao.countrydao import CountryDAO
from src.dao.productdao import ProductDAO
from src.dao.saleproductdao import SaleProductDAO


class InvoicePrinter:
    def __init__(self):
        self.painter = QPainter()
        self.printer = QPrinter()
        self.settings = QSettings()
        self.margin = int(self.settings.value("printing/margin"))
        self.lineHeight = int(self.settings.value("printing/lineHeight"))

    def printInvoice(self, sale):
        self.printDialog = QPrintDialog(self.printer)
        if self.printDialog.exec() == QDialog.Accepted:
            customerDao = CustomerDAO()
            customer = customerDao.select(sale.customerId)

            self.painter.begin(self.printer)
            y = self.paintLogo()
            y += 2 * self.lineHeight
            y = self.paintBusiness(self.margin, y)
            y += 2 * self.lineHeight
            y = self.paintCustomer(customer, self.margin, y)
            y += 2 * self.lineHeight
            y = self.paintSaleProducts(sale, self.margin, y)
            y += 2 * self.lineHeight
            self.paintTotal(sale, self.margin, y)
            self.painter.end()

    def paintLogo(self):
        logoPos = int(self.settings.value("printing/logoPosition"))
        logo = QPixmap(self.settings.value("printing/logoPath"))
        logoWidth = int(self.settings.value("printing/logoWidth"))
        logoHeight = int(self.settings.value("printing/logoHeight"))
        logoPoint = QPoint(self.margin, logoPos)
        self.painter.drawPixmap(logoPoint, logo.scaled(logoWidth, logoHeight))
        return logoHeight + logoPos

    def paintBusiness(self, x, y):
        businessName = self.settings.value("business/name")
        businessPhone = self.settings.value("business/phone")
        businessAddressLine1 = self.settings.value("business/addressLine1")
        businessAddressLine2 = self.settings.value("business/addressLine2")
        businessEmail = self.settings.value("business/email")

        fields = [businessName,
                  businessPhone,
                  businessAddressLine1,
                  businessAddressLine2,
                  businessEmail]

        for field in fields:
            self.painter.drawText(QPoint(x, y), field)
            y += self.lineHeight

        return y

    def paintCustomer(self, customer, x, y):
        countryDao = CountryDAO()
        stateDao = StateDAO()
        cityDao = CityDAO()

        customerCity = cityDao.select(customer.cityId)
        customerState = stateDao.select(customerCity.stateId)
        customerCountry = countryDao.select(customerState.countryId)

        fields = [customer.name,
                  customer.addressLine1,
                  customer.addressLine2,
                  customer.zipcode,
                  customer.email,
                  customer.phoneNumber,
                  customerCity.name,
                  customerState.name,
                  customerCountry.name]

        for field in fields:
            self.painter.drawText(QPoint(x, y), field)
            y += self.lineHeight
        return y

    def paintSaleProducts(self, sale, x, y):
        productDao = ProductDAO()
        saleProductDao = SaleProductDAO()
        saleProducts = saleProductDao.select(sale.id)

        for saleProduct in saleProducts:
            productName = productDao.select(saleProduct.productId)
            productTotal = saleProduct.quantity * saleProduct.price
            self.painter.drawText(QPoint(x, y), productName.name)
            y += self.lineHeight
            self.painter.drawText(QPoint(x, y), str(saleProduct.quantity)
                                  + " x " +
                                  str(saleProduct.price)
                                  + " = " +
                                  str(productTotal))
            y += self.lineHeight
        return y

    def paintTotal(self, sale, x, y):
        self.painter.drawText(QPoint(x, y), "Total: $" + "%.2f" % sale.amount)
        y += self.lineHeight
        self.painter.drawText(QPoint(x, y), "Shipping: $" + "%.2f" % sale.shipping)
        y += self.lineHeight
        self.painter.drawText(QPoint(x, y), "Discount: $" + "%.2f" % sale.discount)
