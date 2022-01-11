# This Python file uses the following encoding: utf-8
from PyQt5.QtSql import QSqlQuery
from src.entity.product import Product


class ProductDAO:
    def __init__(self):
        pass

    def select(self, productId):
        query = QSqlQuery()
        query.prepare("SELECT name,"
                      "description,"
                      "price,"
                      "cost,"
                      "quantity,"
                      "barcode,"
                      "unit_id "
                      "FROM product "
                      "WHERE product_id = :productId")

        query.bindValue(":productId", productId)
        query.exec()
        if query.next():
            return Product(productId,
                           query.value("name"),
                           query.value("description"),
                           query.value("price"),
                           query.value("cost"),
                           query.value("quantity"),
                           query.value("barcode"),
                           query.value("unit_id"))

    def insert(self, product):
        query = QSqlQuery()
        query.prepare("INSERT INTO product (name, description, price,"
                      "cost, quantity, barcode, unit_id) VALUES (:name,"
                      ":description, :price, :cost, :quantity, :barcode,"
                      ":unitId)")
        query.bindValue(":name", product.name)
        query.bindValue(":description", product.description)
        query.bindValue(":price", product.price)
        query.bindValue(":cost", product.cost)
        query.bindValue(":quantity", product.quantity)
        query.bindValue(":barcode", product.barcode)
        query.bindValue(":unitId", product.unitId)
        return query.exec()

    def update(self, product):
        query = QSqlQuery()
        query.prepare("UPDATE product SET name = :name,"
                      "description = :description,"
                      "price = :price,"
                      "cost = :cost,"
                      "quantity = :quantity,"
                      "barcode = :barcode,"
                      "unit_id = :unitId "
                      "WHERE product_id = :productId")
        query.bindValue(":name", product.name)
        query.bindValue(":description", product.description)
        query.bindValue(":price", product.price)
        query.bindValue(":cost", product.cost)
        query.bindValue(":quantity", product.quantity)
        query.bindValue(":barcode", product.barcode)
        query.bindValue(":unitId", product.unitId)
        query.bindValue(":productId", product.id)
        return query.exec()
