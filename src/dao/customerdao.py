# This Python file uses the following encoding: utf-8
from PyQt5.QtSql import QSqlQuery
from src.entity.customer import Customer


class CustomerDAO:
    def __init__(self):
        pass

    def select(self, customerId):
        query = QSqlQuery()
        query.prepare("SELECT name,"
                      "address_line1,"
                      "address_line2,"
                      "zipcode,"
                      "email,"
                      "phone_number, "
                      "city_id "
                      "FROM customer "
                      "WHERE customer_id = :customerId")
        query.bindValue(":customerId", customerId)
        query.exec()
        if query.next():
            return Customer(customerId,
                            query.value("name"),
                            query.value("address_line1"),
                            query.value("address_line2"),
                            query.value("zipcode"),
                            query.value("email"),
                            query.value("phone_number"),
                            query.value("city_id"))

    def insert(self, customer):
        pass

    def update(self, customer):
        query = QSqlQuery()
        query.prepare("UPDATE customer SET name = :name,"
                      "address_line1 = :addressLine1,"
                      "address_line2 = :addressLine2,"
                      "zipcode = :zipcode,"
                      "email = :email,"
                      "phone_number = :phoneNumber,"
                      "city_id = :cityId "
                      "WHERE customer_id = :customerId")
        query.bindValue(":name", customer.name)
        query.bindValue(":addressLine1", customer.addressLine1)
        query.bindValue(":addressLine2", customer.addressLine2)
        query.bindValue(":zipcode", customer.zipcode)
        query.bindValue(":email", customer.email)
        query.bindValue(":phoneNumber", customer.phoneNumber)
        query.bindValue(":cityId", customer.cityId)
        query.bindValue(":customerId", customer.id)
        return query.exec()
