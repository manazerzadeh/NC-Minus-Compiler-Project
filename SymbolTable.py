from typing import *


class SymbolTableEntry:
    def __init__(self, symbol_name: str, symbol_type: str, scope: int = None, dimension: int = None):
        self.symbolName = symbol_name
        self.symbol_type = symbol_type
        self.scope = scope
        self.dimension = dimension


class SymbolTable:
    def __init__(self):
        self.entries = List[SymbolTableEntry]

    def add_symbol(self, symbol_name, symbol_type):
        symbol = SymbolTable(symbol_name, symbol_type)
        self.entries.append(symbol)

    def find_symbol(self, name):
        for entry in self.entries:
            if(entry.symbolName = name)

