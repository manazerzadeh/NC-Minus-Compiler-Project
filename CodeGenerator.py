from SymbolTable import SymbolTable
from MemoryManager import MemoryManager
from typing import *


class CodeGenerator:
    def __init__(self, symbol_table: SymbolTable, memory_manager: MemoryManager, pc: int, scope_stack: List[int]):
        self.symbol_table = symbol_table
        self.semantic_stack = []
        self.memory_manager = memory_manager
        self.pc = pc
        self.sign_flag = False
        self.PB = []
        self.scope_stack = scope_stack

    def find_address(self, token: (str, str)):
        entry = self.symbol_table.find_symbol(token[0])
        return entry.address

    def find_return_address(self, token: (str, str)):
        entry = self.symbol_table.find_symbol(token[0])
        return entry.return_address

    def code_gen_token(self, token: (str, str), action: str):
        if action == 'handle_sing':
            self.sign_flag = True
            return
        if action == 'save':
            self.semantic_stack.append(self.pc)
            self.pc += 1
            return
        if action == 'jpf_save':
            self.PB[int(self.semantic_stack[-1])] = ('JPF', self.semantic_stack[-2], self.pc + 1,)
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.semantic_stack.append(self.pc)
            self.pc += 1
            return
        if action == 'jp':
            self.PB[int(self.semantic_stack[-1])] = ('JP', self.pc,)
            self.semantic_stack.pop()
            return
        if action == 'label':
            self.semantic_stack.append(self.pc)
            return
        if action == 'save':
            self.semantic_stack.append(self.pc)
            self.pc += 1
            return
        if action == 'while':
            self.PB[int(self.semantic_stack[-1])] = ('JPF', self.semantic_stack[-2], self.pc + 1,)
            self.PB[self.pc] = ('JP', self.semantic_stack[-2],)
            self.pc += 1
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            return
        if action == 'handle_return':
            self.PB[self.pc] = ('JP', '@' + str(self.semantic_stack[-1]),)
            self.semantic_stack.pop()
            self.pc += 1
        if action == 'call_function':
            return_addr = int(self.semantic_stack[-1])
            self.PB[self.pc] = ('ASSIGN', self.pc + 2, return_addr,)
            self.pc += 1
            self.PB[self.pc] = ('JP', self.semantic_stack[-2],)
            self.pc += 1
            return
        if action == 'pid':
            addr = self.find_address(token)
            self.semantic_stack.append(addr)
            return
        if action == 'p_return':
            return_addr = self.find_return_address(token)
            self.semantic_stack.append(return_addr)
            return
        if action == 'pnum':
            self.semantic_stack.append('#' + token[0])
            return
        if action == 'assign':
            self.PB[self.pc] = ('ASSIGN', self.semantic_stack[-1], self.semantic_stack[-2])
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.pc += 1
            return
        if action == 'address_update':
            temp_addr = self.memory_manager.get_temp()
            self.PB[self.pc] = ('MULT', self.semantic_stack[-1], '#4', temp_addr)
            self.pc += 1
            temp2_addr = self.memory_manager.get_temp()
            self.PB[self.pc] = ('ADD', temp_addr, self.semantic_stack[-2], temp2_addr)
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.semantic_stack.append(temp2_addr)
            self.pc += 1
            return
        if action == 'handle_relop':
            temp_addr = self.memory_manager.get_temp()
            if self.semantic_stack[-2] == '==':
                self.PB[self.pc] = ('EQ', self.semantic_stack[-1], self.semantic_stack[-3], temp_addr)
            elif self.semantic_stack[-2] == '<':
                self.PB[self.pc] = ('LT', self.semantic_stack[-3], self.semantic_stack[-1], temp_addr)
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.pc += 1
            self.semantic_stack.append(temp_addr)
            return
        if action == 'handle_addop':
            temp_addr = self.memory_manager.get_temp()
            if self.semantic_stack[-2] == '+':
                self.PB[self.pc] = ('EQ', self.semantic_stack[-3], self.semantic_stack[-1], temp_addr)
            elif self.semantic_stack[-2] == '-':
                self.PB[self.pc] = ('LT', self.semantic_stack[-3], self.semantic_stack[-1], temp_addr)
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.pc += 1
            self.semantic_stack.append(temp_addr)
            return
        if action == 'mult':
            temp_addr = self.memory_manager.get_temp()
            self.PB[self.pc] = ('MULT', self.semantic_stack[-2], self.semantic_stack[-1], temp_addr)
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.pc += 1
            self.semantic_stack.append(temp_addr)
            return
        if action == 'prelop':
            self.semantic_stack.append(token[0])
            return
        if action == 'addop':
            self.semantic_stack.append(token[0])
            return
        if action == 'handle_sign':
            temp_addr = self.memory_manager.get_temp()
            self.PB[self.pc] = ('NOT', self.semantic_stack[-1], temp_addr)
            self.semantic_stack.pop()
            self.semantic_stack.append(temp_addr)
            self.pc += 1

