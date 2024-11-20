from lexer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer


codes = ["""
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
""",
"""
program
var
    a, b, c : %;
    d : !;
    e : $;
begin
    readln(a, b); {ввод двух целых значений}
    c := a + b;  {сложение переменных}
    d := !(a > b); {унарная операция: логическое отрицание сравнения}
    e := c + " суммировано"; {конкатенация строк}

    if (d == true) then
        writeln("a меньше либо равно b")
    else
        writeln("a больше b");

    for i := 0 to 10 step 2 do
        writeln(i * i); {вывод квадратов чисел от 0 до 10 с шагом 2}

    while (a != 0) do
    begin
        writeln("Цикл выполняется");
        a := a - 1;
    end;
    writeln("Программа завершена.", e);
end.

"""]

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