from SymbolTable import SymbolTable
from typing import *
from MemoryManager import MemoryManager


class SemanticAnalyser:
    def __init__(self, symbol_table: SymbolTable, scope_stack: List[int], pc: int, memory_manager: MemoryManager):
        self.symbol_table = symbol_table
        self.scope_stack = scope_stack
        self.pc = pc
        self.ss = []
        self.memory_manager = memory_manager
        self.dim = 0

    def analyse_token(self, token: (str, str), action: str):
        # todo: handle_sign... update: Codegen is doing that!

        if action == 'save_type':
            self.ss.append(token[1])
            return
        if action == 'save_token':
            self.ss.append(token)
            return
        if action == 'check_if_dec_before':
            if self.symbol_table.find_symbol_in_scope(token[0], self.scope_stack[-1]) is not None:
                raise Exception('Same Declaration in this scope')
            return
        if action == 'pop_token_and_saved_type':
            self.ss.pop()
            self.ss.pop()
            return
        if action == 'check_saved_type':
            if self.ss[-2] == 'void':
                raise Exception('Variable type cannot be Void')
            return
        if action == 'allocate_memory':
            entry = self.symbol_table.find_symbol(self.ss[-1][0])
            entry.scope = self.scope_stack[-1]
            entry.address = self.memory_manager.get_dynamic(self.dim)
            entry.dimension = self.dim
            self.dim = 0
            return
        if action == 'determine_start_address_return_address':
            # todo: check this again later. Reason is that if we defined an int function dim would be added here we
            #  decrease it
            self.dim = 0
            entry = self.symbol_table.find_symbol(self.ss[-1][0])
            entry.scope = self.scope_stack[-1]
            entry.address = self.pc
            entry.return_address = self.memory_manager.get_dynamic()
            return
        if action == 'assign_dim':
            entry = self.symbol_table.find_symbol_in_scope(self.ss[-1][0], self.scope_stack[-1])
            entry.dimension = self.dim
            self.dim = 0
            return
        if action == 'update_dim':
            self.dim = (1, int(token[0]))
            return
        if action == 'add_dim':
            self.dim += 1
            return
        if action == 'illegal_ID_after_void':
            raise Exception('illegal ID after void')
        if action == 'check_type':
            if token[0] == 'void':
                raise Exception('illegal ID after void')
            return
        if action == 'update_scope':
            self.scope_stack.append(self.scope_stack[-1] + 1)
            return
        if action == 'remove_prev_scope':
            for entry in self.symbol_table.entries:
                if entry.scope == self.scope_stack[-1]:
                    self.symbol_table.entries.remove(entry)
            self.scope_stack.pop()
            return
        if action == 'check_id_save':
            if self.symbol_table.find_symbol(token[0]) is None:
                raise Exception("Undefined variable")
            self.ss.append(token)
            return
        if action == 'remove_id':
            self.ss.pop()
            return
        if action == 'check_dim':
            entry = self.symbol_table.find_symbol(self.ss[-1][0])
            if self.dim != entry.dimension:
                raise Exception("Dimension isn't correct")
            self.dim = 0
            return
