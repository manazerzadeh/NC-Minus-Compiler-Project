from SymbolTable import SymbolTable

terminals = ['EOF', 'ID', 'NUM', 'int', 'void', '[', ']', ';', '(', ')', ',', 'continue', 'break'
    , 'if', 'else', 'while', 'return', 'switch', '{', '}', 'case', 'NUM', 'default'
    , ':', '<', '==', '+', '-', '*', '=']

keys = ['EOF', 'int', 'void', '[', ']', ';', '(', ')', ',', 'continue', 'break'
    , 'if', 'else', 'while', 'return', 'switch', '{', '}', 'case', 'default', ':', '<'
    , '==', '+', '-', '*', '=']

seperators = ['[', ']', ';', '(', ')', ',', '{', '}', ':', '<', '=', '+', '-', '*', ' ', '\n', 'EOF', '\t']


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
        token = str()
        while True:

            char = self.get_char()
            if char == -1:
                if len(token) == 0:
                    return 'EOF', 'EOF'
                elif token not in keys:
                    symbol_type = check_num_id(token)
                    if not self.symbol_table.is_in_table(token):
                        self.symbol_table.add_symbol(token, symbol_type)
                    return token, symbol_type
                elif token in keys:
                    if not self.symbol_table.is_in_table(token):
                        self.symbol_table.add_symbol(token, token)
                    return token, token
                else:
                    raise Exception('Incorrect lexeme')

            else:
                if len(token) >= 1:
                    if char in seperators:
                        self.char_index -= 1
                        if token in keys:
                            if not self.symbol_table.is_in_table(token):
                                self.symbol_table.add_symbol(token, token)
                            return token, token
                        else:
                            symbol_type = check_num_id(token)
                            if not self.symbol_table.is_in_table(token):
                                self.symbol_table.add_symbol(token, symbol_type)
                            return token, symbol_type
                    else:
                        token += char
                else:
                    if char in seperators:
                        if char == ' ' or char == '\n' or char == '\t':
                            continue
                        if char == '=':
                            token += char
                            if self.get_char() == '=':
                                token += char
                                if not self.symbol_table.is_in_table(token):
                                    self.symbol_table.add_symbol(token, token)
                                return token, token
                            else:
                                self.char_index -= 1
                                if not self.symbol_table.is_in_table(token):
                                    self.symbol_table.add_symbol(token, token)
                                return token, token
                        else:
                            token += char
                            if not self.symbol_table.is_in_table(token):
                                self.symbol_table.add_symbol(token, token)
                            return token, token
                    else:
                        token += char
