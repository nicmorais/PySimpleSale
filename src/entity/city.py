# This Python file uses the following encoding: utf-8
from src.entity.state import State


class City:
    def __init__(self, id, name, state):
        self.id = id
        self.name = name
        if type(state) == State:
            self.stateId = state.id
        else:
            self.stateId = state
