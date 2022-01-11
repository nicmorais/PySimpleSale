# This Python file uses the following encoding: utf-8
from PyQt5.QtSql import QSqlQuery
from src.entity.state import State


class StateDAO:
    def __init__(self):
        pass

    def select(self, stateId):
        query = QSqlQuery()
        query.prepare("SELECT name, code, country_id "
                      "FROM state "
                      "WHERE state_id = :stateId")
        query.bindValue(":stateId", stateId)
        query.exec()
        if query.next():
            return State(stateId,
                         query.value("name"),
                         query.value("code"),
                         query.value("country_id"))
