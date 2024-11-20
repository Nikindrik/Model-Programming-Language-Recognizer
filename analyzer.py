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