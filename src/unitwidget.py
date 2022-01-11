# This Python file uses the following encoding: utf-8
from PyQt5 import uic, QtCore, QtWidgets
from src.entity.unit import Unit
from src.dao.unitdao import UnitDAO


class UnitWidget(QtWidgets.QWidget):
    def __init__(self):
        super(UnitWidget, self).__init__()
        uic.loadUi('src/unitwidget.ui', self)
        self.mode = "new"
        self.unitUpserted = QtCore.pyqtSignal()

    def edit(self, unit):
        self.mode = "edit"
        self.unitId = unit.id
        self.nameLineEdit.setText(unit.name)
        self.abbreviationLineEdit.setText(unit.abbreviation)

    def save(self):
        dao = UnitDAO()
        if self.mode == "new":
            dao.insert(Unit(self.nameLineEdit.text(),
                            self.abbreviationLineEdit.text()))
        else:
            dao.update(Unit(self.unitId,
                            self.nameLineEdit.text(),
                            self.abbreviationLineEdit.text()))
        self.unitUpserted.emit()
