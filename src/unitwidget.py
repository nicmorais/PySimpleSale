# This Python file uses the following encoding: utf-8
from PyQt5 import uic, QtWidgets
from src.entity.unit import Unit
from src.dao.unitdao import UnitDAO
from PyQt5.QtCore import pyqtSignal


class UnitWidget(QtWidgets.QWidget):
    unitUpserted = pyqtSignal()

    def __init__(self):
        super(UnitWidget, self).__init__()
        uic.loadUi('src/unitwidget.ui', self)
        self.mode = "new"

    def edit(self, unit):
        self.mode = "edit"
        self.unitId = unit.id
        self.nameLineEdit.setText(unit.name)
        self.abbreviationLineEdit.setText(unit.abbreviation)

    def save(self):
        dao = UnitDAO()
        if self.mode == "new":
            dao.insert(Unit(None,
                            self.nameLineEdit.text(),
                            self.abbreviationLineEdit.text()))
        else:
            dao.update(Unit(self.unitId,
                            self.nameLineEdit.text(),
                            self.abbreviationLineEdit.text()))
        self.unitUpserted.emit()
        self.close()
