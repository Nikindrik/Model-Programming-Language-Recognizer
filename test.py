# from lexer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer
from semantic_analyzer import SemanticAnalyzer
from prettytable import PrettyTable

from lexer import LexicalAnalyzer


code = ['''
program 
var a, o, b, h: %;
	r, re: !;
	flag: $;
begin
!
    a := 0 + 5;  {Это комментарий}
	r := 1.23e+10;
	o := 1234567o;
	b := 101b;
	h := 1ABCh;
	re := 1.234;В 
	flag := true;
end.
''']


for elem in code:
    lexer = LexicalAnalyzer(elem)
    tokens = lexer.tokenize()
    print("Токены:")
    if 'UNKNOWN' in tokens or 'ERROR' in tokens:
        print('Ошибка лексического анализа')
        #continue
    table = PrettyTable()
    table.field_names = ["Тип токена", "Токен", "Номер токена", "Номер строки", "Токен в строке"]
    for jlem in tokens:
        #print(jlem)
        table.add_row(jlem)
    print(table)


    parser = SyntaxAnalyzer(tokens)
    try:
        parser.parse_program()
        print('Синтаксического анализа - OK')
    except SyntaxError as e:
        print(f"Ошибка синтаксического анализа: {e}")
        #continue

    semantic_analyzer = SemanticAnalyzer(tokens)
    semantic_analyzer.analyze()