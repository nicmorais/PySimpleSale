# This Python file uses the following encoding: utf-8
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QFileDialog


class SettingsWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SettingsWidget, self).__init__()
        uic.loadUi('src/settingswidget.ui', self)
        self.settings = QSettings()
        self.logoPath = self.settings.value("printing/logoPath")

        spinBoxes = []
        spinBoxes.append([self.marginSpinBox, "printing/margin"])
        spinBoxes.append([self.fontSizeSpinBox, "printing/fontSize"])
        spinBoxes.append([self.lineHeightSpinBox, "printing/lineHeight"])
        spinBoxes.append([self.logoPositionSpinBox, "printing/logoPosition"])
        spinBoxes.append([self.logoWidthSpinBox, "printing/logoWidth"])
        spinBoxes.append([self.logoHeightSpinBox, "printing/logoHeight"])

        for spinBox in spinBoxes:
            self.setSpinBoxValue(spinBox[0], spinBox[1])

        self.businessNameLineEdit.setText(self.settings.value("business/name"))
        self.phoneNumberLineEdit.setText(self.settings.value("business/phone"))
        self.addressLine1LineEdit.setText(self.settings.value("business/addressLine1"))
        self.addressLine2LineEdit.setText(self.settings.value("business/addressLine2"))
        self.businessEmailLineEdit.setText(self.settings.value("business/email"))

    def save(self):
        self.settings.setValue("printing/margin", self.marginSpinBox.value())
        self.settings.setValue("printing/fontSize", self.fontSizeSpinBox.value())
        self.settings.setValue("printing/lineHeight", self.lineHeightSpinBox.value())
        self.settings.setValue("printing/logoPosition", self.logoPositionSpinBox.value())
        self.settings.setValue("printing/logoPath", self.logoPath)
        self.settings.setValue("printing/logoWidth", self.logoWidthSpinBox.value())
        self.settings.setValue("printing/logoHeight", self.logoHeightSpinBox.value())

        self.settings.setValue("business/name", self.businessNameLineEdit.text())
        self.settings.setValue("business/phone", self.phoneNumberLineEdit.text())
        self.settings.setValue("business/addressLine1", self.addressLine1LineEdit.text())
        self.settings.setValue("business/addressLine2", self.addressLine2LineEdit.text())
        self.settings.setValue("business/email", self.businessEmailLineEdit.text())

        self.close()

    def setSpinBoxValue(self, spinBox, value):
        valueInt = self.settings.value(value)

        if valueInt is None:
            spinBox.setValue(0)
        else:
            spinBox.setValue(int(valueInt))

    def selectLogo(self):
        fileDialog = QFileDialog()
        self.logoPath = fileDialog.getOpenFileName()[0]
