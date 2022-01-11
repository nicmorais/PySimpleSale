# This Python file uses the following encoding: utf-8


class Customer:
    def __init__(self, id, name, addressLine1, addressLine2,
                 zipcode, email, phoneNumber, city):
        self.id = id
        self.name = name
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.zipcode = zipcode
        self.email = email
        self.phoneNumber = phoneNumber
        self.cityId = city
