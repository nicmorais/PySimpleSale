# This Python file uses the following encoding: utf-8
from PyQt5.QtSql import QSqlQuery
from src.entity.sale import Sale
from src.entity.saleproduct import SaleProduct


class SaleDAO:
    def __init__(self):
        pass

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
            products += SaleProduct(query.value("sale_product_id"),
                                    query.value("price"),
                                    query.value("quantity"),
                                    query.value("product_id"))
        return products
