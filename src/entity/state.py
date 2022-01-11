# This Python file uses the following encoding: utf-8
from src.entity.country import Country


class State:
    def __init__(self, id, name, code, country):
        self.id = id
        self.name = name
        self.code = code
        if type(country) == Country:
            self.countryId = country.id
        else:
            self.countryId = country
