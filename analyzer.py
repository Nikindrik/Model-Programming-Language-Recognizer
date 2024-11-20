from lexer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer


all_codes = [
    '''
program 
var a, i, sum: %;
	r: !;
	flag: $;
begin 
	a := 5 + 5;  {Это комментарий}
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
end.
    '''
]

code = '''
program 
var a, i, sum, k: %;
	r: !;
	flag: $;
begin 
	a := 5 + 5;  {Это комментарий}
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
		while 'flag имеет значение true'
	end
	else
	begin
		while 'flag имеет значение false'
	end
end.
'''

for elem in all_codes:
    # Лексический анализ
    lexer = LexicalAnalyzer()
    tokens = lexer.tokenize(elem)
    print("Tokens:")
    print(tokens)
    # for jlem in tokens:
        # print(jlem)

    # Синтаксический анализ
    parser = SyntaxAnalyzer(tokens)
    try:
        parser.parse_program()
        print("OK")
    except SyntaxError as e:
        print(f"Ошибка синтаксического анализа: {e}")