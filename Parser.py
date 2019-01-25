from SymbolTable import SymbolTable
from typing import *
from Scanner import Scanner

terminals = ['EOF', 'ID', 'NUM', 'int', 'void', '[', ']', ';', '(', ')', ',', 'continue', 'break'
    , 'if', 'else', 'while', 'return', 'switch', '{', '}', 'case', 'NUM', 'default'
    , ':', '<', '==', '+', '-', '*', '=']

keys = ['EOF', 'int', 'void', '[', ']', ';', '(', ')', ',', 'continue', 'break'
    , 'if', 'else', 'while', 'return', 'switch', '{', '}', 'case', 'default', ':', '<'
    , '==', '+', '-', '*', '=']

seperators = ['[', ']', ';', '(', ')', ',', '{', '}', ':', '<', '=', '+', '-', '*', ' ', '\n']


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
                raise Exception("expected EOF, instead got " + token[1])
            return

        def handle_declaration_list():
            handle_declaration()
            handle_declaration_list_prime()
            return

        def handle_declaration_list_prime():
            if token[1] in ['continue', 'break', ';', 'ID', '(', 'NUM', 'if', 'return',
                            '{', 'switch', 'while', 'EOF']:
                return
            elif token[1] in ['int', 'void']:
                handle_declaration()
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_declaration():
            handle_type_specifier()
            if not match('ID'):
                raise Exception("Expected ID, instead got " + token[1])
            handle_declaration_prime()
            return

        def handle_declaration_prime():
            if token[1] in [';', '[']:
                handle_var_declaration_prime()
                return
            elif token[1] in ['(']:
                if not match('('):
                    raise Exception("Expected (, instead got " + token[1])
                handle_params()
                if not match(')'):
                    raise Exception("Expected ), instead got " + token[1])
                handle_compound_stmt()
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_var_declaration_prime():
            if token[1] in [';']:
                match(';')
                return
            elif token[1] in ['[']:
                match('[')
                if not match('NUM'):
                    raise Exception("Expected NUM instead got " + token[1])
                if not match(']'):
                    raise Exception("Expected ] instead got " + token[1])
                if not match(';'):
                    raise Exception("Expected ;, instead got " + token[1])
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_type_specifier():
            if token[1] in ['int']:
                match('int')
                return
            if token[1] in ['void']:
                match('void')
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_params_prime():
            if token[1] == 'ID':
                match('ID')
                handle_param_prime()
                handle_param_list_prime()
                return
            if token[1] == ')':
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_params():
            if token[1] == 'void':
                match('void')
                handle_params_prime()
                return
            if token[1] == 'int':
                match('int')
                if not match('ID'):
                    raise Exception("Expected ID, instead got " + token[1])
                handle_param_prime()
                handle_param_list_prime()
                return
            else:
                raise Exception("illegal " + token[1])

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
                raise Exception("illegal " + token[1])

        def handle_param():
            handle_type_specifier()
            match('ID')
            handle_param_prime()

        def handle_param_prime():
            if token[1] == '[':
                match('[')
                if not match(']'):
                    raise Exception("Expected ] instead got " + token[1])
                return
            if token[1] in [',', ')']:
                return
            else:
                raise Exception("illegal ", token[1])

        def handle_compound_stmt():
            if not match('{'):
                raise Exception("Expected {, instead got " + token[1])
            handle_declaration_list()
            handle_statement_list()
            if not match('}'):
                raise Exception("Expected }, instead got " + token[1])

        def handle_statement_list():
            if token[1] in ['continue', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{',
                            'switch', 'while']:
                handle_statement()
                handle_statement_list()
            if token[1] in ['}', 'default']:
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_statement():
            if token[1] in ['continue', 'break', ';', 'ID', '(', 'NUM']:
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
                raise Exception("illegal " + token[1])

        def handle_expression_stmt():
            if token[1] in ['ID', '(', 'NUM']:
                handle_expression()
                if not match(';'):
                    raise Exception('Expected ;, instead got ' + token[1])
                return
            if token[1] == 'continue':
                match('continue')
                if not match(';'):
                    raise Exception('Expected ;, instead got ' + token[1])
                return
            if token[1] == 'break':
                match('break')
                if not match(';'):
                    raise Exception('Expected ;, instead got ' + token[1])
                return
            if token[1] == ';':
                match(';')
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_selection_stmt():
            if not match('if'):
                raise Exception("Expected if, instead got " + token[1])
            if not match('('):
                raise Exception("Expected (, instead got " + token[1])
            handle_expression()
            if not match(')'):
                raise Exception("Expected ), instead got " + token[1])
            handle_statement()
            if not match('else'):
                raise Exception("Expected else, instead got " + token[1])
            handle_statement()
            return

        def handle_iteration_stmt():
            if not match('while'):
                raise Exception("Expected while, instead got " + token[1])
            if not match('('):
                raise Exception("Expected (, instead got " + token[1])
            handle_expression()
            if not match(')'):
                raise Exception("Expected ), instead got " + token[1])
            handle_statement()
            return

        def handle_return_stmt():
            if not match('return'):
                raise Exception("Expected return, instead got " + token[1])
            handle_return_stmt_prime()
            return

        def handle_return_stmt_prime():
            if token == ';':
                match(';')
                return
            if token in ['ID', 'NUM', '(']:
                handle_expression()
                if not match(';'):
                    raise Exception("Expected ;, instead got " + token[1])
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_switch_stmt():
            handle_switch_stmt()
            if not match('('):
                raise Exception("Expected (, instead got " + token[1])
            handle_expression()
            if not match(')'):
                raise Exception("Expected ), instead got " + token[1])
            if not match('{'):
                raise Exception("Expected {, instead got " + token[1])
            handle_case_stmt()
            handle_default_stmt()
            if not match('}'):
                raise Exception("Expected }, instead got " + token[1])
            return

        def handle_case_stmt():
            if not match('case'):
                raise Exception("Expected case, instead got " + token[1])
            if not match('NUM'):
                raise Exception("Expected NUM, instead got " + token[1])
            if not match(':'):
                raise Exception("Expected :, instead got " + token[1])
            handle_statement_list()
            return

        def handle_default_stmt():
            if token[1] == 'default':
                match('default')
                if not match(':'):
                    raise Exception('Expected :, instead got ' + token[1])
                handle_statement_list()
                return
            if token[1] == '}':
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_expression():
            if token[1] == 'NUM':
                match('NUM')
                handle_term_prime()
                handle_additive_expression_prime()
                handle_simple_expression_prime()
                return
            if token[1] == 'ID':
                match('ID')
                handle_expression_prime()
                return
            if token[1] == '(':
                match('(')
                handle_expression()
                if not match(')'):
                    raise Exception("Expected ), instead got " + token[1])
                handle_term_prime()
                handle_additive_expression_prime()
                handle_simple_expression_prime()
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_expression_prime():
            if token[1] in ['[', '=', '*', '+', '-', '==', '<']:
                handle_var_prime()
                handle_expression_zegond()
                return
            if token[1] == '(':
                match('(')
                handle_args()
                if not match(')'):
                    raise Exception("Expected ), instead got " + token[1])
                handle_term_prime()
                handle_additive_expression_prime()
                handle_simple_expression_prime()
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_expression_zegond():
            if token[1] == '=':
                match('=')
                handle_expression()
                return
            if token[1] in ['*', '+', '-', '==', '<']:
                handle_term_prime()
                handle_additive_expression_prime()
                handle_simple_expression_prime()
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_var():
            pass

        def handle_var_prime():
            if token[1] in ['=', '*', '+', '-', '==', '<', ',',
                            ')', ']', ';']:
                return
            if token[1] == '[':
                match('[')
                handle_expression()
                if not match(']'):
                    raise Exception("Expected ], instead got " + token[1])
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_simple_expression():
            pass

        def handle_simple_expression_prime():
            if token[1] in ['==', '<']:
                handle_relop()
                handle_additive_expression()
                return
            if token[1] in [',', ')', ']', ';']:
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_relop():
            if token[1] == '==':
                match('==')
                return
            if token[1] == '<':
                match('<')
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_additive_expression():
            if token in ['(', 'NUM', 'ID']:
                handle_term()
                handle_additive_expression_prime()
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_additive_expression_prime():
            if token[1] in ['==', '<', ',', ')', ']', ';']:
                return
            if token[1] in ['+', '-']:
                handle_addop()
                handle_term()
                handle_additive_expression_prime()
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_addop():
            if token[1] == '+':
                match('+')
                return
            if token[1] == '-':
                match('-')
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_term():
            if token[1] in ['(', 'NUM', 'ID']:
                handle_factor()
                handle_term_prime()
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_term_prime():
            if token[1] == '*':
                match('*')
                handle_factor()
                handle_term_prime()
                return
            if token[1] in ['==', '<', '+', '-', ')', ',', ']', ';']:
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_factor():
            if token[1] == 'NUM':
                match('NUM')
                return
            if token[1] == 'ID':
                match('ID')
                handle_factor_prime()
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_factor_prime():
            if token[1] == '[':
                handle_var_prime()
                return
            if token[1] == '(':
                match('(')
                handle_args()
                if not match(')'):
                    raise Exception("Expected ), instead got " + token[1])
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_call():
            pass

        def handle_args():
            if token[1] in ['ID', '(', 'NUM']:
                handle_arg_list()
                return
            if token[1] == ')':
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_arg_list():
            if token[1] in ['ID', '(', 'NUM']:
                handle_expression()
                handle_arg_list_prime()
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_arg_list_prime():
            if token[1] == ',':
                match(',')
                handle_expression()
                handle_arg_list_prime()
                return
            if token[1] == ')':
                match(')')
                return
            else:
                raise Exception("illegal " + token[1])

        def match(terminal: str):
            nonlocal token
            if token[1] == terminal:
                token = self.scanner.get_token()
                return True
            return False

        token: (str, str)
        token = self.scanner.get_token()
        handle_program()
