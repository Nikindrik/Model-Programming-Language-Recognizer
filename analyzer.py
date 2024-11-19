from lexer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer


code = """
program
var a, b, s, i: %;
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
for elem in tokens:
    print(elem)

# Синтаксический анализ
# parser = SyntaxAnalyzer(tokens)
# result = parser.parse()
# print(result)