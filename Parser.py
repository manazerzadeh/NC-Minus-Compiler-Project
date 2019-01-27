from SymbolTable import SymbolTable
from typing import *
from Scanner import Scanner
from Semantic_analyser import SemanticAnalyser
from MemoryManager import MemoryManager
from CodeGenerator import CodeGenerator

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
        self.pc = 0
        self.scope_stack: List[int] = [0]
        self.memory_manager = MemoryManager()
        self.scanner = Scanner(file_name, self.symbol_table)
        self.semantic_analyser = SemanticAnalyser(self.symbol_table, self.scope_stack, self.pc, self.memory_manager)
        self.code_generator = CodeGenerator(self.symbol_table, self.memory_manager, self.pc, self.scope_stack)

    def parse(self):
        def handle_program():
            handle_declaration_list()
            if not match('EOF'):
                raise Exception("expected EOF, instead got " + token[1])
            # todo: self.code_generator.code_gen_token(None, 'main_return_addr')
            return

        def handle_declaration_list():
            if token[1] in ['continue', 'break', ';', 'ID', '(', 'NUM', 'if', 'return',
                            '{', 'switch', 'while', 'EOF', '-']:
                return
            elif token[1] in ['int', 'void']:
                handle_declaration()
                handle_declaration_list()
            else:
                raise Exception("illegal " + token[1])

        def handle_declaration():
            handle_type_specifier()
            self.semantic_analyser.analyse_token(prev_token, 'save_type')
            if not match('ID'):
                raise Exception("Expected ID, instead got " + token[1])
            self.semantic_analyser.analyse_token(prev_token, 'save_token')
            self.semantic_analyser.analyse_token(prev_token, 'check_if_dec_before')
            handle_declaration_prime()
            self.semantic_analyser.analyse_token(None, 'pop_token_and_saved_type')
            return

        def handle_declaration_prime():
            if token[1] in [';', '[']:
                self.semantic_analyser.analyse_token(None, 'check_saved_type')
                handle_var_declaration_prime()
                self.semantic_analyser.analyse_token(prev_token, 'allocate_memory')
                return
            elif token[1] in ['(']:
                self.semantic_analyser.analyse_token(None, 'determine_start_address_return_address')
                self.code_generator.code_gen_token(prev_token, 'p_return')
                if not match('('):
                    raise Exception("Expected (, instead got " + token[1])
                handle_params()
                self.semantic_analyser.analyse_token(None, 'assign_dim')
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
                self.semantic_analyser.analyse_token(None, 'update_dim')
                if not match(']'):
                    raise Exception("Expected ] instead got " + token[1])
                if not match(';'):
                    raise Exception("Expected ;, instead got " + token[1])
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_type_specifier():
            if token[1] in ['int']:
                self.semantic_analyser.analyse_token(None, 'add_dim')
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
                self.semantic_analyser.analyse_token(None, 'illegal_ID_after_void')
                handle_param_prime()
                handle_param_list_prime()
                self.semantic_analyser.analyse_token(None, 'add_dim')
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
                self.semantic_analyser.analyse_token(None, 'add_dim')
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
            self.semantic_analyser.analyse_token(prev_token, 'check_type')
            match('ID')
            self.semantic_analyser.analyse_token(prev_token, 'add_dim')
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
            self.semantic_analyser.analyse_token(None, 'update_scope')
            handle_declaration_list()
            handle_statement_list()
            self.semantic_analyser.analyse_token(None, 'remove_prev_scope')
            if not match('}'):
                raise Exception("Expected }, instead got " + token[1])

        def handle_statement_list():
            if token[1] in ['continue', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{',
                            'switch', 'while', '-']:
                handle_statement()
                handle_statement_list()
                return
            if token[1] in ['}', 'default', 'case']:
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_statement():
            if token[1] in ['continue', 'break', ';', 'ID', '(', 'NUM', '-']:
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
            if token[1] in ['ID', '(', 'NUM', '-']:
                handle_Nsign()
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
            self.code_generator.code_gen_token(None , 'save')
            handle_statement()
            if not match('else'):
                raise Exception("Expected else, instead got " + token[1])
            self.code_generator.code_gen_token(None, 'jpf_save')
            handle_statement()
            self.code_generator.code_gen_token(None, 'jp')
            return

        def handle_iteration_stmt():
            if not match('while'):
                raise Exception("Expected while, instead got " + token[1])
            self.code_generator.code_gen_token(None, 'label')
            if not match('('):
                raise Exception("Expected (, instead got " + token[1])
            handle_expression()
            if not match(')'):
                raise Exception("Expected ), instead got " + token[1])
            self.code_generator.code_gen_token(None, 'save')
            handle_statement()
            self.code_generator.code_gen_token(None, 'while')
            return

        def handle_return_stmt():
            if not match('return'):
                raise Exception("Expected return, instead got " + token[1])
            handle_return_stmt_prime()
            self.code_generator.code_gen_token(None, 'handle_return')
            return

        def handle_return_stmt_prime():
            if token[1] == ';':
                match(';')
                return
            if token[1] in ['ID', 'NUM', '(']:
                handle_expression()
                if not match(';'):
                    raise Exception("Expected ;, instead got " + token[1])
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_switch_stmt():
            if not match('switch'):
                raise Exception("Expected switch, instead got " + token[1])
            if not match('('):
                raise Exception("Expected (, instead got " + token[1])
            handle_expression()
            if not match(')'):
                raise Exception("Expected ), instead got " + token[1])
            if not match('{'):
                raise Exception("Expected {, instead got " + token[1])
            handle_case_stmts()
            handle_default_stmt()
            if not match('}'):
                raise Exception("Expected }, instead got " + token[1])
            return

        def handle_case_stmts():
            if token[1] in ['ID', '(', 'NUM', 'default']:
                return
            if token[1] == 'case':
                handle_case_stmt()
                handle_case_stmts()

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
                self.code_generator.code_gen_token(prev_token, 'pnum')
                handle_term_prime()
                handle_additive_expression_prime()
                handle_simple_expression_prime()
                return
            if token[1] == 'ID':
                match('ID')
                self.semantic_analyser.analyse_token(prev_token, 'check_id_save')
                self.code_generator.code_gen_token(prev_token, 'pid')
                handle_expression_prime()
                self.semantic_analyser.analyse_token(None, 'remove_id')
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
            if token[1] in ['[', '=', '*', '+', '-', '==', '<', ')', ';', ']']:
                handle_var_prime()
                handle_expression_zegond()
                return
            if token[1] == '(':
                self.code_generator.code_gen_token(prev_token, 'p_return')
                match('(')
                handle_args()
                self.semantic_analyser.analyse_token(None, 'check_dim')
                if not match(')'):
                    raise Exception("Expected ), instead got " + token[1])
                self.code_generator.code_gen_token(None, 'call_function')
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
                self.code_generator.code_gen_token(None, 'assign')
                return
            if token[1] in ['*', '+', '-', '==', '<', ')', ';', ']']:
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
                self.code_generator.code_gen_token(None, 'address_update')
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
                self.code_generator.code_gen_token(None, 'handle_relop')
                return
            if token[1] in [',', ')', ']', ';']:
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_relop():
            if token[1] == '==':
                match('==')
                self.code_generator.code_gen_token(prev_token, 'prelop')
                return
            if token[1] == '<':
                match('<')
                self.code_generator.code_gen_token(prev_token, 'prelop')
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_additive_expression():
            if token[1] in ['(', 'NUM', 'ID']:
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
                self.code_generator.code_gen_token(None, 'handle_addop')
                handle_additive_expression_prime()
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_addop():
            if token[1] == '+':
                match('+')
                self.code_generator.code_gen_token(prev_token, 'addop')
                return
            if token[1] == '-':
                match('-')
                self.code_generator.code_gen_token(prev_token, 'addop')
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
                self.code_generator.code_gen_token(None, 'mult')
                handle_term_prime()
                return
            if token[1] in ['==', '<', '+', '-', ')', ',', ']', ';']:
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_factor():
            if token[1] == 'NUM':
                match('NUM')
                self.code_generator.code_gen_token(prev_token, 'pnum')
                return
            if token[1] == 'ID':
                match('ID')
                self.semantic_analyser.analyse_token(prev_token, 'check_id_save')
                self.code_generator.code_gen_token(prev_token, 'pid')
                handle_factor_prime()
                self.semantic_analyser.analyse_token(None, 'remove_id')
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
                self.semantic_analyser.analyse_token(None, 'check_dim')
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
                self.semantic_analyser.analyse_token(None, 'add_dim')
                handle_expression()
                handle_arg_list_prime()
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_arg_list_prime():
            if token[1] == ',':
                self.semantic_analyser.analyse_token(None, 'add_dim')
                match(',')
                handle_expression()
                handle_arg_list_prime()
                return
            if token[1] == ')':
                return
            else:
                raise Exception("illegal " + token[1])

        def handle_Nsign():
            if token[1] == '-':
                match('-')
                self.code_generator.code_gen_token(None, 'handle_sign')

        def match(terminal: str):
            nonlocal token
            nonlocal prev_token
            if token[1] == terminal:
                prev_token = (token[0], token[1])
                token = self.scanner.get_token()
                return True
            return False

        # todo: implement panic mode
        # todo: comment handler

        prev_token: (str, str) = (None, None)
        token: (str, str)
        token = self.scanner.get_token()
        handle_program()
