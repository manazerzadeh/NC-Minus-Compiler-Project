from typing import *

import SymbolTable
from Parser import keys


class Scanner:
    def __init__(self, file_name: str, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.char_index = 0
        self.code = open(file_name).read()

    def get_char(self):
        if self.char_index == len(self.code):
            return -1
        else:
            char = self.code[self.char_index]
            self.char_index += 1
            return char

    def get_token(self):
        token: str = []


