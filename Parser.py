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




    def parse(self):
        def handle_program():
            handle_declaration_list()
            if not match('EOF'):
                raise Exception("expected EOF, instead got ", token[1])
            return
        def handle_declaration_list():
            handle_declaration()
            handle_declaration_list_prime()
            return

        def handle_declaration_list_prime():
            if token[1] in ['continue' , 'break' , ';' , 'ID' , '(', 'NUM' , 'if' , 'return',
                             '{' , 'switch' , 'while', 'EOF']:
                return
            elif token[1] in ['int' , 'void']:
                handle_declaration()
                return
            else: raise Exception("illegal ", token[1])

        def handle_declaration():
            handle_type_specifier()
            if  not match('ID'):
                raise Exception("Expected ID, instead got ", token[1])
            handle_declaration_prime()
            return
        def handle_declaration_prime():
            if token[1] in [';' , '[']:
                handle_var_declaration_prime()
                return
            elif token[1] in ['(']:
                if not match('('):
                    raise Exception("Expected (, instead got ", token[1])
                handle_params()
                if not match(')'):
                    raise Exception("Expected ), instead got ", token[1])
                handle_compound_stmt()
                return
            else: raise Exception("illegal ", token[1])

        def handle_var_declaration_prime():
            if token[1] in [';']:
                match(';')
                return
            elif token[1] in ['[']:
                match('[')
                if not match('NUM'):
                    raise Exception("Expected NUM instead got ", token[1])
                if not match(']'):
                    raise Exception("Expected ] instead got ", token[1])
                if not match(';'):
                    raise Exception("Expected ;, instead got ", token[1])
                return
            else: raise Exception("illegal ", token[1])
        def handle_type_specifier():
            if token[1] in ['int']:
                match('int')
                return
            if token[1] in ['void']:
                match('void')
                return
            else:
                raise Exception("illegal ", token[1])
        def handle_params_prime():
            if token[1] == 'ID':
                match('ID')
                handle_param_prime()
                handle_param_list_prime()
                return
            if token[1] == ')':
                return
            else:
                raise Exception("illegal ", token[1])
        def handle_params():
            if token[1] == 'void':
                match('void')
                handle_params_prime()
                return
            if token[1] == 'int':
                match('int')
                if not match('ID'):
                    raise Exception("Expected ID, instead got " , token[1])
                handle_param_prime()
                handle_param_list_prime()
                return
            else:
                raise Exception("illegal ", token[1])
        def handle_param_list():
            handle_param()
            handle_param_list_prime()
        def handle_param_list_prime():
            if token[1] == ')':
                return
            if token[1] == ',':
                match(',')
                handle_param()
                return
            else:
                raise Exception("illegal ", token[1])
        def handle_param():
            handle_type_specifier()
            match('ID')
            handle_param_prime()
        def handle_param_prime():
            if token[1] == '[':
                match('[')
                if not match(']'):
                    raise Exception("Expected ] instead got ", token[1])
                return
            if token[1] in [',' , ')']:
                return
            else:
                raise Exception("illegal ", token[1])
        def handle_compound_stmt():
            if not match('{'):
                raise Exception("Expected {, instead got ", token[1])
        def handle_statement_list():
            if token[1] in ['continue' , 'break' , ';', 'ID', '(', 'NUM', 'if', 'return' , '{',
                            'switch', 'while']:
                handle_statement()
                handle_statement_list()
            if token[1] in ['}' , 'default']:
                return
            else:
                raise Exception("illegal ", token[1])
        def handle_statement():
            if token[1] in ['continue' , 'break' , ';' , 'ID' , '(' , 'NUM']:
                handle_expression_stmt()
                return
            if token[1] == '{':
                handle_compound_stmt()
                return
            if token[1] == 'if':
                handle_selection_stmt()
                return
            if token[1] == 'while':
                handle_iteration_stmt()
                return
            if token[1] == 'return':
                handle_return_stmt()
                return
            if token[1] == 'switch':
                handle_switch_stmt()
                return
            else:
                raise Exception("illegal ", token[1])
        def handle_expression_stmt():
            if token[1] in ['ID', '(' , 'NUM']:
                handle_expression()
                if not match(';'):
                    raise Exception('Expected ;, instead got ', token[1])
                return
            if token[1] == 'continue':
                match('continue')
                if not match(';'):
                    raise Exception('Expected ;, instead got ', token[1])
                return
            if token[1] == 'break':
                match('break')
                if not match(';'):
                    raise Exception('Expected ;, instead got ', token[1])
                return
            if token[1] == ';':
                match(';')
                return
            else:
                raise Exception("illegal ", token[1])
        def handle_selection_stmt():
            if not match('if'):
                raise Exception("Expected if, instead got ", token[1])
            if not match('('):
                raise Exception("Expected (, instead got ", token[1])
            handle_expression()
            if not match(')'):
                raise Exception("Expected ), instead got ", token[1])
            handle_statement()
            if not match('else'):
                raise Exception("Expected else, instead got ", token[1])
            handle_statement()
            return
        def handle_iteration_stmt():
            if not match('while'):
                raise Exception("Expected while, instead got ", token[1])
            if not match('('):
                raise Exception("Expected (, instead got ", token[1])
            handle_expression()
            if not match(')'):
                raise Exception("Expected ), instead got ", token[1])
            handle_statement()
            return
        def handle_return_stmt():

        def handle_return_stmt_prime():
        def handle_switch_stmt():
        def handle_case_stmt():
        def handle_default_stmt():
        def handle_expression():
        def handle_expression_prime():
        def handle_expression_zegond():
        def handle_var():
        def handle_var_prime():
        def handle_simple_expression():
        def handle_simple_expression_prime():
        def handle_addop():
        def handle_term():
        def handle_term_prime():
        def handle_factor():
        def handle_factor_prime():
        def handle_call():
        def handle_args():
        def handle_arg_list():
        def handle_arg_list_prime():
        def match(terminal: str):
            nonlocal token
            if token[1] == terminal:
                token = self.scanner.get_token()
                return True
            return False


        token: (str, str)
        token = self.scanner.get_token()
        handle_program()