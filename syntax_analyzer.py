class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        """Начинает синтаксический анализ."""
        return self.parse_program()

    def parse_program(self):
        """Обрабатывает программу."""
        self.expect('KEYWORD', 'program')
        self.expect('KEYWORD', 'var')
        self.parse_variable_declaration()
        self.expect('KEYWORD', 'begin')
        self.parse_statements()
        self.expect('KEYWORD', 'end')
        self.expect('DELIMITER', '.')  # Завершение программы

    def parse_variable_declaration(self):
        """Обрабатывает блок объявления переменных."""
        while self.peek()[0] == 'ID':
            self.consume('ID')  # Идентификатор
            if self.peek()[1] == ',':
                self.consume('DELIMITER', ',')
            else:
                self.expect('DELIMITER', ':')
                self.expect('TYPE')
                self.expect('DELIMITER', ';')
                break

    def parse_statements(self):
        """Обрабатывает список операторов."""
        while self.peek()[0] != 'KEYWORD' or self.peek()[1] != 'end':
            self.parse_statement()
            if self.peek()[1] == ';':
                self.consume('DELIMITER', ';')

    def parse_statement(self):
        """Обрабатывает один оператор."""
        if self.peek()[0] == 'KEYWORD':
            if self.peek()[1] == 'for':
                self.parse_for_loop()
            elif self.peek()[1] == 'if':
                self.parse_if_statement()
            elif self.peek()[1] == 'readln':
                self.parse_readln()
            elif self.peek()[1] == 'writeln':
                self.parse_writeln()
        else:
            self.parse_assignment()

    def parse_for_loop(self):
        """Обрабатывает цикл for."""
        self.expect('KEYWORD', 'for')
        self.parse_assignment()
        self.expect('KEYWORD', 'to')
        self.parse_expression()
        if self.peek()[1] == 'step':
            self.consume('KEYWORD', 'step')
            self.parse_expression()
        self.expect('KEYWORD', 'do')
        self.expect('KEYWORD', 'begin')
        self.parse_statements()
        self.expect('KEYWORD', 'end')  # Завершение вложенного блока

    def parse_if_statement(self):
        """Обрабатывает условный оператор."""
        self.expect('KEYWORD', 'if')
        self.expect('DELIMITER', '(')
        self.parse_expression()
        self.expect('DELIMITER', ')')
        self.parse_statement()
        if self.peek()[1] == 'else':
            self.consume('KEYWORD', 'else')
            self.parse_statement()

    def parse_readln(self):
        """Обрабатывает readln."""
        self.expect('KEYWORD', 'readln')
        self.expect('ID')
        while self.peek()[1] == ',':
            self.consume('DELIMITER', ',')
            self.expect('ID')

    def parse_writeln(self):
        """Обрабатывает writeln."""
        self.expect('KEYWORD', 'writeln')
        self.parse_expression()
        while self.peek()[1] == ',':
            self.consume('DELIMITER', ',')
            self.parse_expression()

    def parse_assignment(self):
        """Обрабатывает присваивание."""
        self.expect('ID')
        self.expect('ASSIGN')
        self.parse_expression()

    def parse_expression(self):
        """Обрабатывает выражение."""
        self.expect('ID')  # Упрощенное выражение

    def consume(self, token_type, value=None):
        """Потребляет токен, если он соответствует."""
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == token_type and (value is None or self.tokens[self.pos][1] == value):
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {token_type} {value}, got {self.peek()}")

    def expect(self, token_type, value=None):
        """Ожидает токен, иначе вызывает ошибку."""
        self.consume(token_type, value)

    def peek(self):
        """Возвращает текущий токен."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None