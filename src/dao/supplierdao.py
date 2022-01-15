# This Python file uses the following encoding: utf-8
from PyQt5.QtSql import QSqlQuery, QSqlError
from src.entity.supplier import Supplier
from src.dao.dao import DAO


class SupplierDAO(DAO):
    def __init__(self):
        self.lastError = QSqlError()

    def select(self, supplierId):
        query = QSqlQuery()
        query.prepare("SELECT name,"
                      "address_line1,"
                      "address_line2,"
                      "city_id,"
                      "email,"
                      "phone_number "
                      "FROM supplier "
                      "WHERE supplier_id = :supplierId")

        query.bindValue(":supplierId", supplierId)
        query.exec()
        query.next()
        return Supplier(supplierId,
                        query.value("name"),
                        query.value("address_line1"),
                        query.value("address_line2"),
                        query.value("city_id"),
                        query.value("email"),
                        query.value("phone_number"))

    def insert(self, supplier):
        query = QSqlQuery()
        query.prepare("INSERT into supplier (name,"
                      "address_line1,"
                      "address_line2,"
                      "city_id,"
                      "email,"
                      "phone_number) "
                      "VALUES (:name, "
                      ":addressLine1, "
                      ":addressLine2, "
                      ":cityId, "
                      ":email, "
                      ":phoneNumber)")

        query.bindValue(":name", supplier.name)
        query.bindValue(":addressLine1", supplier.addressLine1)
        query.bindValue(":addressLine2", supplier.addressLine2)
        query.bindValue(":cityId", supplier.cityId)
        query.bindValue(":email", supplier.email)
        query.bindValue(":phoneNumber", supplier.phoneNumber)
        query.exec()

    def update(self, supplier):
        query = QSqlQuery()
        query.prepare("UPDATE supplier SET "
                      "name = :name,"
                      "address_line1 = :addressLine1,"
                      "address_line2 = :addressLine2,"
                      "city_id = :cityId,"
                      "email = :email,"
                      "phone_number = :phoneNumber "
                      "WHERE supplier_id = :supplierId")
        query.bindValue(":name", supplier.name)
        query.bindValue(":addressLine1", supplier.addressLine1)
        query.bindValue(":addressLine2", supplier.addressLine2)
        query.bindValue(":cityId", supplier.cityId)
        query.bindValue(":email", supplier.email)
        query.bindValue(":phoneNumber", supplier.phoneNumber)
        query.bindValue(":supplierId", supplier.id)
        query.exec()

    def delete(self, supplier):
        supplierId = 0
        if type(supplier) == Supplier:
            supplierId = supplier.id
        else:
            supplierId = supplier

        query = QSqlQuery()
        query.prepare("DELETE FROM supplier WHERE supplier_id = :supplierId")
        query.bindValue(":supplierId", supplierId)
        success = query.exec()
        self.lastError = query.lastError()
        return success
