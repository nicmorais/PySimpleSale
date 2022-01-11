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
