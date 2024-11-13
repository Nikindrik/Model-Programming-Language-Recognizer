from lex import lexer
from pars import Parser


def analyze_code(code):
    try:
        tokens = lexer(code)
        print("Tokens:", tokens)
        parser = Parser(tokens)
        parser.parse()
        print("Parsing successful.")
    except SyntaxError as e:
        print("Parsing error:", e)
        '''for i in range(len(code)):
            if i == 17:
                print(code[i - 2])
                print(code[i - 1])
                print(code[i])
                print(code[i + 1], end='')'''


code = '''
program var a: %; 
begin 
  a := 0;
  writeln a;
end
'''

analyze_code(code)