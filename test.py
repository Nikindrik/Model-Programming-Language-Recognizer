from lex import LexicalAnalyzer
from prettytable import PrettyTable


code = ['''
{
    % x, y, k;
    x as 10;
    y as 5;
    write(x + y);  /* Вывод: 15 */
    write(x - y);  /* Вывод: -5 */
    write(x * y);  /* Вывод: 50 */
    write(y / x);  /* Вывод: 2 */
	k as 10
	while (k != 0) do
	[
		write(k);
		k as k + 1;
	]
}
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