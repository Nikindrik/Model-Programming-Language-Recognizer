from lexer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer


code = """
program
var a, b, s, i: %;
    r, t, q, g: !;
begin
    readln(a, b);
    s := 0;
    for i := a to b step 1 do
    begin
        s := s + i;
    end;
    writeln('Сумма чисел от ', a, ' до ', b, ' равна ', s);
end.
"""
# Лексический анализ
lexer = LexicalAnalyzer()
tokens = lexer.tokenize(code)
print("Tokens:")
print(tokens)
# for elem in tokens:
    # print(elem)

# Синтаксический анализ
parser = SyntaxAnalyzer(tokens)
try:
    parser.parse_program()
    print("OK")
except SyntaxError as e:
    print(f"Ошибка синтаксического анализа: {e}")