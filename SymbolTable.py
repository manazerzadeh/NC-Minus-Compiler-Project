from typing import *


class SymbolTableEntry:
    def __init__(self, symbol_name: str, symbol_type: str, scope: int = None, dimension: int = None):
        self.symbolName = symbol_name
        self.type = type
        self.scope = scope
        self.Dimension = dimension


class SymbolTable:
    def __init__(self):
        self.entries = []

    def add_symbol(self, symbol_name, symbol_type):
        symbol = SymbolTable(symbol_name, symbol_type)
        self.entries.append(symbol)

    def find_symbol(self, name):
        for entry in self.entries:
            pass
