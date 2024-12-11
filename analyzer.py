from lexer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer
from semantic_analyzer import SemanticAnalyzer
from prettytable import PrettyTable


code = ['''
program 
var a, i, sum, k, bi: %;
	r: !;
	flag: $;
begin
	a := 0 + 5;  {Это комментарий}
	if (a > 5)
	begin
		writeln 'a больше 5';
	end
	else
	begin
        writeln 'a меньше или равно 5';
	end
	sum := 0;
	for i := 0 to a step 1
	begin
		writeln 'i = ', i;
		sum := sum + i;
		next;
	end
	writeln 'sum = ', sum;
	if (sum >= 10)
	begin
		writeln 'sum больше или равно 10';
	end
	k := 10
	while (k != 0)
	begin
		writeln 'k = ', k;
		k := k + 1;
	end
	writeln 'Введите true либо false';
	readln flag;
	if (flag)
	begin
		writeln 'flag имеет значение true'
	end
	else
	begin
		writeln 'flag имеет значение false'
	end
	bi := 123o
	writeln 'bi = ', bi;
end.
''']


for elem in code:
    lexer = LexicalAnalyzer(elem)
    tokens = lexer.tokenize()
    print("Токены:")
    # print(tokens)
    table = PrettyTable()
    table.field_names = ["Тип токена", "Токен"]
    for jlem in tokens:
        table.add_row(jlem)
    print(table)

    parser = SyntaxAnalyzer(tokens)
    try:
        parser.parse_program()
        print('Синтаксического анализа - OK')
    except SyntaxError as e:
        print(f"Ошибка синтаксического анализа: {e}")

    analyzer = SemanticAnalyzer(tokens)
    result = analyzer.analyze()
    print(result)