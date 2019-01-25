from Scanner import *

if __name__ == "__main__":
    scanner = Scanner('test.txt', SymbolTable())
    while True:
        token = scanner.get_token()


