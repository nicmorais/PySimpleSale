# This Python file uses the following encoding: utf-8


class Purchase:
    def __init__(self, id, supplier, amount, discount, shipping, datetime):
        self.id = id
        self.supplierId = supplier
        self.amount = amount
        self.discount = discount
        self.shipping = shipping
        self.datetime = datetime
