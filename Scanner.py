from typing import *

import SymbolTable
from Parser import keys
from Parser import seperators


def check_num_id(token: str) -> str:
    if token[0].isidentifier():
        return 'ID'
    elif token.isnumeric():
        return 'NUM'
    elif token[0] == '+' or token[0] == '-':
        if token[1:].isnumeric():
            return 'NUM'
    else:
        raise Exception('invalid string')


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

        while True:

            char = self.get_char()
            if char == -1:
                return
            else:
                if char in seperators:
                    self.char_index -= 1
                    if token in keys:

                        return token, token
                    else:
                        symbol_type = check_num_id(token)
                        return token, symbol_type
