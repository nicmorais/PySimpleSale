# This Python file uses the following encoding: utf-8
from PyQt5.QtSql import QSqlQuery, QSqlError
from src.entity.sale import Sale
from src.entity.saleproduct import SaleProduct


class SaleDAO:
    def __init__(self):
        self.lastError = QSqlError()

    def select(self, saleId):
        query = QSqlQuery()
        query.prepare("SELECT customer_id, amount, discount, "
                      "shipping, datetime FROM sale WHERE sale_id = :saleId")
        query.bindValue(":saleId", saleId)
        query.exec()
        if query.next():
            return Sale(saleId,
                        query.value("customer_id"),
                        query.value("amount"),
                        query.value("discount"),
                        query.value("shipping"),
                        query.value("datetime"))

    def selectProducts(self, saleId):
        query = QSqlQuery()
        query.prepare("SELECT sale_product_id,"
                      "price, quantity, product_id "
                      "FROM sale_product WHERE sale_id = :saleId")
        query.bindValue(":saleId", saleId)
        query.exec()
        products = []
        while query.next():
            products.append(SaleProduct(query.value("sale_product_id"),
                            query.value("price"),
                            query.value("quantity"),
                            query.value("product_id"),
                            saleId))
        return products

    def insert(self, sale):
        query = QSqlQuery()
        query.prepare("INSERT INTO sale (customer_id,"
                      "amount, discount, shipping, datetime) "
                      "VALUES (:customerId, :amount, :discount,"
                      ":shipping, :datetime) RETURNING sale_id")
        query.bindValue(":customerId", sale.customerId)
        query.bindValue(":amount", sale.amount)
        query.bindValue(":discount", sale.discount)
        query.bindValue(":shipping", sale.shipping)
        query.bindValue(":datetime", sale.datetime)
        query.exec()
        self.lastError = query.lastError()
        if query.next():
            return query.value("sale_id")

    def update(self, sale):
        query = QSqlQuery()
        query.prepare("UPDATE sale SET customer_id = :customerId,"
                      "amount = :amount,"
                      "discount = :discount,"
                      "shipping = :shipping,"
                      "datetime = :datetime "
                      "WHERE sale_id = :saleId")
        query.bindValue(":customerId", sale.customerId)
        query.bindValue(":amount", sale.amount)
        query.bindValue(":discount", sale.discount)
        query.bindValue(":shipping", sale.shipping)
        query.bindValue(":datetime", sale.datetime)
        query.bindValue(":saleId", sale.id)
        success = query.exec()
        self.lastError = query.lastError()
        return success

    def delete(self, sale):
        saleId = 0
        if type(sale) == Sale:
            saleId = sale.id
        else:
            saleId = sale

        query = QSqlQuery()
        query.prepare("DELETE FROM sale WHERE sale_id = :saleId")
        query.bindValue(":saleId", saleId)
        success = query.exec()
        self.lastError = query.lastError()
        return success
