from typing import *


class SymbolTableEntry:
    def __init__(self, symbol_name: str, symbol_type: str, scope: int = None, dimension: int = None,
                 address: int = None):
        self.symbolName = symbol_name
        self.symbol_type = symbol_type
        self.scope = scope
        self.dimension = dimension
        self.address = address


class SymbolTable:
    def __init__(self):
        self.entries: List[SymbolTableEntry] = []

    def add_symbol(self, symbol_name: str, symbol_type: str):  # will be used in scanner
        symbol = SymbolTableEntry(symbol_name, symbol_type)
        self.entries.append(symbol)

    def find_symbol(self, symbol_name: str):  # will be used in semantic analysis
        for entry in self.entries:
            if entry.symbolName == symbol_name:
                return entry
        return None

    def find_symbol_in_scope(self, symbol_name, scope: int = None):
        for entry in self.entries:
            if entry.symbolName == symbol_name and entry.scope is scope:
                return entry
        return None

    def is_in_table(self, symbol_name: str):
        entry = self.find_symbol(symbol_name)
        if entry is None:
            return False
        else:
            return True
