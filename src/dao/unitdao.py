# This Python file uses the following encoding: utf-8
from PyQt5.QtSql import QSqlQuery
from src.entity.unit import Unit


class UnitDAO:
    def __init__(self):
        pass

    def select(self, unitId):
        query = QSqlQuery()
        query.prepare("SELECT name, abbreviation "
                      "FROM unit WHERE unit_id = :unitId")
        query.bindValue(":unitId", unitId)
        query.exec()

        if query.next():
            return Unit(unitId,
                        query.value("name"),
                        query.value("abbreviation"))

    def insert(self, unit):
        query = QSqlQuery()
        query.prepare("INSERT INTO unit (name, abbreviation) "
                      "VALUES (:name, :abbreviation)")
        query.bindValue(":name", unit.name)
        query.bindValue(":abbreviation", unit.abbreviation)
        query.exec()

    def update(self, unit):
        query = QSqlQuery()
        query.prepare("UPDATE unit SET name = :name,"
                      "abbreviation = :abbreviation WHERE unit_id = :unit_id")
        query.bindValue(":name", unit.name)
        query.bindValue(":abbreviation", unit.abbreviation)
        query.bindValue(":unit_id", unit.id)
        query.exec()
