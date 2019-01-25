from SymbolTable import SymbolTable
from typing import *
from Scanner import Scanner

terminals = ['EOF', 'ID', 'NUM', 'int', 'void', '[', ']', ';', '(', ')', ',', 'continue', 'break'
    , 'if', 'else', 'while', 'return', 'switch', '{', '}', 'case', 'NUM', 'default'
    , ':', '<', '==', '+', '-', '*', '=']

keys = ['EOF', 'int', 'void', '[', ']', ';', '(', ')', ',', 'continue', 'break'
    , 'if', 'else', 'while', 'return', 'switch', '{', '}', 'case', 'default', ':', '<'
    , '==', '+', '-', '*', '=']

seperators = ['[', ']', ';', '(', ')', ',', '{', '}', ':', '<', '=', '+', '-', '*', ' ' , '\n']


class Parser:
    def __init__(self, file_name):
        self.symbol_table = SymbolTable()
        self.semantic_stack: List[int] = []
        self.scope_stack: List[int] = []
        self.scanner = Scanner(file_name, self.symbol_table)

