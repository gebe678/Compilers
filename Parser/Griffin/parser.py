# A recursive descent parser
from lexilyzer import main as lex
from lexilyzer import symbolTable

tokens = {                                                      #   token table (from specification document)
    "program":2,    "while":18,     "EOF":35,
    "begin":3,      "loop":19,      "var":36,
    "end":4,        "end_loop":20,  "const":37,
    ';':5,          "input":21,     "call":38,
    "declare":6,    "output":22,    "procedure":39,
    ',':7,          '+':23,         "<>":40,
    ":=":8,         '-':24,         '<':41,
    '.':9,          '*':25,         '>':42,
    "if":10,        '/':26,         ">=":43,
    "then":11,      '(':27,         "<=":44,
    "else":12,      ')':28,         "do":29,                    #   NOTE:  added "do":29 (not in documentation)
    "end_if":13,    "Real":30,
    "odd":14,       "Integer":31,
    ':':15,         "Boolean":32,
    '{':16,         '=':33,
    '}':17,         "EOL":34
}

token_identity = {
    "0": "ident",
    "1": "number",
    "2": "program",   "18": "while",    "34":"EOL",
    "3": "begin",     "19": "loop",     "35":"EOF",
    "4": "end",       "20": "end_loop", "36":"var",
    "5": ";",         "21": "input",    "37":"const",
    "6": "declare",   "22": "output",   "38":"call",
    "7": ",",         "23":"+",         "39":"procedure",
    "8": ":=",        "24":"-",         "40":"<>",
    "9": ".",         "25": "*",        "41":"<",
    "10":"if",        "26": "/",        "42":">",
    "11": "then",     "27": "(",        "43":">=",
    "12": "else",     "28": ")",        "44":"<=",
    "13": "end_if",   "29":"do",
    "14": "odd",      "30":"Real",
    "15": ":",        "31":"Integer",
    "16": "{",        "32":"Boolean",
    "17": "}",        "33":"=",
}

def get_tokens(index):
    token_list = lex()

    token_list = token_list.split("*")
    for i in range(len(token_list)):
        token_list[i] = token_list[i].strip()

        if token_list[i][0] == "0":
            token_list[i] = "0"

        elif token_list[i][0] == "1":
            token_list[i] = "1"

    return token_list[index]

def decode_token(current_token):
    encoded_token = get_tokens(current_token)
    token = token_identity[encoded_token]

    return token

def program(current_token = 0, end = False):
    encoded_token = get_tokens(current_token)
    token = token_identity[encoded_token]

    if token == "EOF":
        print("Program parsed successfully")
        return

    elif token == ".":
        program(current_token + 1)

    elif token == "const" or token == "var" or token == "procedure":
        block(current_token)

    elif token == "ident" or token == "begin" or token == "if" or token == "while" or "call":
        statement(current_token)

    else:
        print("ERROR: expected block statement")

def block(current_token):
    encoded_token = get_tokens(current_token)
    token = token_identity[encoded_token]

    def const(current_token):
        token = decode_token(current_token)

        if token != "ident":
            print("Error: recieved ", token, " expected identifier ", " on token ", current_token)
            exit()
        else:
            print("token ", token, " number ", current_token, " parsed successfully in func const")
            current_token += 1
            token = decode_token(current_token)
            
        if token != "=":
            print("Error: recieved ", token, " expected = ", " on token ", current_token)
            exit()
        else:
            print("token ", token, " number ", current_token, " parsed successfully in func const")
            current_token += 1
            token = decode_token(current_token)

        if token != "number":
            print("Error: recieved ", token, " expected number ", " on token ", current_token)
            exit()
        else:
            print("token ", token, " number ", current_token, " parsed successfully in func const")
            current_token += 1
            token = decode_token(current_token)

        if token != "," and token != ";":
            print("Error: recieved ", token, " expected ; ", " on token ", current_token)
            exit()
        else:
            if token == ",":
                print("token ", token, " number ", current_token, " parsed successfully in func const")
                current_token = const(current_token + 1)
            elif token == ";":
                print("token ", token, " number ", current_token, " parsed successfully in func const")
                current_token += 1
        return current_token

    def var(current_token):
        token = decode_token(current_token)
        if token != "ident":
            print("Error: recieved ", token, " expected identifier ", " on token ", current_token)
            exit()
        else:
            print("token ", token, " number ", current_token, " parsed successfully in func var")
            current_token += 1
            token = decode_token(current_token)

        if token != "," and token != ";":
            print("Error: recieved ", token, " expected ; ", " on token ", current_token)
            exit()
        else:
            if token == ",":
                print("token ", token, " number ", current_token, " parsed successfully in func var")
                current_token = var(current_token + 1)
            elif token == ";":
                print("token ", token, " number ", current_token, " parsed successfully in func var")
                current_token += 1
        return current_token

    def procedure(current_token):
        token = decode_token(current_token)

        if token != "ident":
            print("Error: recieved ", token, " expected identifier ", " on token ", current_token)
            exit()
        else:
            print("token ", token, " number ", current_token, " parsed successfully in func procedure")
            current_token += 1
            token = decode_token(current_token)

        if token != ";":
            print("Error: recieved ", token, " expected ; ", " on token ", current_token)
            exit()
        else:
            print("token ", token, " number ", current_token, " parsed successfully in func procedure")
            current_token += 1
            token = decode_token(current_token)

        current_token = block(current_token)
        return current_token
    
    if token == "const":
        print("token ", token, " number ", current_token, " parsed successfully in func block")
        current_token += 1
        current_token = const(current_token)
        token = decode_token(current_token)
    
    if token == "var":
        print("token ", token, " number ", current_token, " parsed successfully in func block")
        current_token += 1
        current_token = var(current_token)
        token = decode_token(current_token)

    if token == "procedure":
        print("token ", token, " number ", current_token, " parsed successfully in func block")
        current_token += 1
        current_token = procedure(current_token)
        token = decode_token(current_token)

    if token == "EOL":
        print("token ", token, " number ", current_token, " parsed successfully in func block")
        current_token += 1
        program(current_token)

    return current_token

def statement(current_token):
    encoded_token = get_tokens(current_token)
    token = token_identity[encoded_token]

    def ident(current_token):
        token = decode_token(current_token)

        if token != ":=":
            print("Error: recieved ", token, " expected := ", " on token ", current_token)
            exit()
        else:
            print("token ", token, " number ", current_token, " parsed successfully in ident procedure (statement)")
            current_token += 1
            token = decode_token(current_token)

        if token != "+" or token != "-":
            print("Error: recieved ", token, " expected + or - ", " on token ", current_token)
            exit()
        else:
            print("token ", token, " number ", current_token, " parsed successfully in ident procedure (statement)")
            current_token = expression(current_token)
            token = decode_token(current_token)

        return current_token
    
    def call(current_token):
        token = decode_token(current_token)

        if token != "ident":
            print("Error: recieved ", token, " expected identifier ", " on token ", current_token)
            exit()
        else:
            print("token ", token, " number ", current_token, " parsed successfully in call procedure (statement)")
            current_token += 1
            token = decode_token(current_token)

        ### TODO find if this line is necessary not in DFA for the call line ###
        if token != ";":
            print("Error: recieved ", token, " expected ; ", " on token ", current_token)
            exit()
        else:
            print("token ", token, " number ", current_token, " parsed successfully in call procedure (statement)")
            current_token += 1
            token = decode_token(current_token)

        return current_token

    def begin(current_token):
        token = decode_token(current_token)

        if token == "ident" or token == "call" or token == "if" or token == "while" or token == "begin":
            print("token ", token, " number ", current_token, " parsed successfully in begin procedure (statement)")
            current_token = statement(current_token)
            token = decode_token(current_token)
        else:
            print("Error: recieved ", token, " expected ident, call, if, while, or begin ", " on token ", current_token)
            exit()

        if token == ";" or token == "end":
            if token == "end":
                print("token ", token, " number ", current_token, " parsed successfully in begin procedure (statement)")
                current_token += 1
                token = decode_token(current_token)

            elif token == ";":
                print("token ", token, " number ", current_token, " parsed successfully in begin procedure (statement)")
                current_token += 1
                token = decode_token(current_token)

                if token == "ident" or token == "call" or token == "if" or token == "while" or token == "begin":
                    print("token ", token, " number ", current_token, " parsed successfully in begin procedure (statement)")
                    current_token = statement(current_token)
                    token = decode_token(current_token)
                else:
                    print("Error: recieved ", token, " expected ident, call, if, while, or begin ", " on token ", current_token)
                    exit()
        else:
            print("Error: recieved ", token, " expected ; or end ", " on token ", current_token)
            exit()
            

        return current_token

    def if_(current_token):
        token = decode_token(current_token)
        return current_token

    def while_(current_token):
        return current_token

    if token == "ident":
        print("token ", token, " number ", current_token, " parsed successfully in statement block")
        current_token += 1
        current_token = ident(current_token)
        token = decode_token(current_token)

    if token == "call":
        pass

    if token == "if":
        pass

    if token == "while":
        pass

    if token == "begin":
        print("token ", token, " number ", current_token, " parsed successfully in statement block")
        current_token += 1
        current_token = begin(current_token)
        token = decode_token(current_token)

    if token == "EOL":
        print("token ", token, " number ", current_token, " parsed successfully in statement block")
        current_token += 1
        program(current_token)

    return current_token

def condition(current_token):
    return current_token

def expression(current_token):
    return current_token

def term(current_token):
    return current_token

def factor(current_token):
    return current_token

def main():
    program()

if __name__ == "__main__":
    main()
