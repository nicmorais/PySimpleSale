# This Python file uses the following encoding: utf-8
from src.entity.unit import Unit


class Product:
    def __init__(self, id, name, description, price, cost, quantity, barcode,
                 unit):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.cost = cost
        self.quantity = quantity
        self.barcode = barcode

        if type(unit) == Unit:
            self.unitId = unit.id
        else:
            self.unitId = unit
