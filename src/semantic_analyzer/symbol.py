from abc import ABC


class Symbol(ABC):
    pass


class VariableSymbol(Symbol):
    def __init__(self, var_type, var_id):
        self.type = var_type
        self.id = var_id

    def get_type(self):
        return self.type

    def __repr__(self):
        return f'VariableSymbol:{self.type} {self.id}'


class FunctionSymbol(Symbol):
    def __init__(self, fun_type, fun_id, fun_args_types):
        self.type = fun_type
        self.id = fun_id
        self.arg_types = fun_args_types

    def __repr__(self):
        return f'FunctionDeclaration:{self.type} {self.id} {self.arg_types}'
