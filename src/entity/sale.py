# This Python file uses the following encoding: utf-8


class Sale:
    def __init__(self, id, customer, amount, discount, shipping, datetime):
        self.id = id
        self.customerId = customer
        self.amount = amount
        self.discount = discount
        self.shipping = shipping
        self.datetime = datetime
