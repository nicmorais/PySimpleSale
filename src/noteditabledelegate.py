# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets


class NotEditableDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super(NotEditableDelegate, self).__init__()

    def createEditor(self, parent, option, index):
        pass
