# This Python file uses the following encoding: utf-8
from PyQt5.QtSql import QSqlQuery
from src.entity.country import Country


class CountryDAO:
    def __init__(self):
        pass

    def select(self, countryId):
        query = QSqlQuery()
        query.prepare("SELECT name, code FROM country "
                      "WHERE country_id = :countryId")
        query.bindValue(":countryId", countryId)
        query.exec()
        if query.next():
            return Country(countryId,
                           query.value("name"),
                           query.value("code"))

    def count(self):
        count = 0
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM country")
        query.exec()
        query.next()
        count = query.value(0)
        return count

    def insert(self, country):
        query = QSqlQuery()
        query.prepare("INSERT INTO country (name,"
                      "code) VALUES (:name, :code)")
        query.bindValue(":name", country.name)
        query.bindValue(":code", country.code)
        query.exec()
