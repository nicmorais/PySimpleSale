# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class SqlConnection(QtCore.QObject):
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("database.db")
        self.startDB()

    def startDB(self):
        self.db.open()
        query = QSqlQuery()
        query.exec("SELECT name FROM sqlite_schema "
                   "WHERE type ='table' AND name NOT LIKE 'sqlite_%'")
        if(not query.next()):
            self.createDB()

    def createDB(self):
        createQuery = QSqlQuery()
        sqlFile = open('sql/db.sql', 'r')
        lines = sqlFile.readlines()
        for line in lines:
            createQuery.exec(line)
