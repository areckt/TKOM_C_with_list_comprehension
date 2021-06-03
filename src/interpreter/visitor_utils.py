from abc import ABC


class Symbol(ABC):
    pass


class Variable(Symbol):
    def __init__(self, var_id, value):
        self.id = var_id
        self.value = value

    def get_id(self):
        return self.id

    def get_value(self):
        return self.value

    def set_value(self, new_value):
        self.value = new_value

    def __repr__(self):
        return f'Variable: {self.id} = {self.value}'
