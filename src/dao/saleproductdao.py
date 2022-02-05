# This Python file uses the following encoding: utf-8
from PyQt5.QtSql import QSqlQuery
from src.entity.saleproduct import SaleProduct


class SaleProductDAO:
    def __init__(self):
        pass

    def select(self, saleId):
        query = QSqlQuery()
        query.prepare("SELECT sale_product_id, price, quantity,"
                      "product_id FROM sale_product "
                      "WHERE sale_id = :saleId")
        query.bindValue(":saleId", saleId)
        query.exec()
        saleProducts = []

        while query.next():
            saleProduct = SaleProduct(query.value("sale_product_id"),
                                      query.value("price"),
                                      query.value("quantity"),
                                      query.value("product_id"),
                                      saleId)
            saleProducts.append(saleProduct)
        return saleProducts

    def update(self, saleProductId):
        query = QSqlQuery()
        query.prepare("UPDATE sale_product SET quantity = :quantity, "
                      "price = :price WHERE sale_product_id = :saleProductId")
        query.bindValue(":saleProductId", saleProductId)
        return query.exec()

    def delete(self, saleProduct):
        saleProductId = 0
        if type(saleProduct) == SaleProduct:
            saleProductId = saleProduct.id
        else:
            saleProductId = saleProduct

        query = QSqlQuery()
        query.prepare("DELETE FROM sale_product "
                      "WHERE sale_product_id = :saleProductId")
        query.bindValue(":saleProductId", saleProductId)
        query.exec()

    def insert(self, saleProduct):
        query = QSqlQuery()
        query.prepare("INSERT INTO sale_product "
                      "(price,"
                      "quantity,"
                      "product_id,"
                      "sale_id) "
                      "VALUES "
                      "(:price,"
                      ":quantity,"
                      ":productId,"
                      ":saleId)")

        query.bindValue(":price", saleProduct.price)
        query.bindValue(":quantity", saleProduct.quantity)
        query.bindValue(":productId", saleProduct.productId)
        query.bindValue(":saleId", saleProduct.saleId)
        return query.exec()
