# This Python file uses the following encoding: utf-8
from PyQt5.QtSql import QSqlQuery, QSqlError
from src.entity.purchase import Purchase
from src.dao.dao import DAO


class PurchaseDAO(DAO):
    def __init__(self):
        pass
