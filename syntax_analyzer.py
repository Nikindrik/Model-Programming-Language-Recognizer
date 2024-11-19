class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def expect(self, token_type, value=None):
        token = self.current_token()
        if token and token[0] == token_type and (value is None or token[1] == value):
            self.position += 1
            return token
        raise SyntaxError(f"Expected {token_type} {value}, got {token}")

    def advance(self):
        """Сдвигает позицию на следующий токен."""
        self.position += 1

    def parse_program(self):
        self.expect('KEYWORD', 'program')
        self.expect('KEYWORD', 'var')
        self.parse_variable_declaration()
        self.expect('KEYWORD', 'begin')
        self.parse_statements()
        self.expect('KEYWORD', 'end')
        self.expect('DELIMITER', '.')

    def parse_variable_declaration(self):
        while True:
            self.parse_identifier_list()
            self.expect('DELIMITER', ':')
            self.parse_type()
            self.expect('DELIMITER', ';')
            if self.current_token()[0] != 'ID':
                break

    def parse_identifier_list(self):
        self.expect('ID')
        while self.current_token() and self.current_token()[0] == 'DELIMITER' and self.current_token()[1] == ',':
            self.expect('DELIMITER', ',')
            self.expect('ID')

    def parse_type(self):
        self.expect('TYPE')

    def parse_statements(self):
        while True:
            token = self.current_token()
            if token[0] == 'KEYWORD' and token[1] == 'begin':
                self.parse_compound_statement()  # Обрабатываем вложенные блоки
            elif token[0] == 'ID':
                self.parse_assignment()
            elif token[0] == 'KEYWORD' and token[1] == 'readln':
                self.parse_input_statement()
            elif token[0] == 'KEYWORD' and token[1] == 'writeln':
                self.parse_output_statement()
            elif token[0] == 'KEYWORD' and token[1] == 'for':
                self.parse_for_loop()
            elif token[0] == 'KEYWORD' and token[1] == 'end':
                return
            elif token[0] == 'DELIMITER' and token[1] == ';':
                # Переход к следующему оператору
                self.advance()  # Сдвигаем токены, ожидаем следующий оператор
            else:
                raise SyntaxError(f"Unexpected statement start: {token}")

    def parse_compound_statement(self):
        self.expect('KEYWORD', 'begin')
        self.parse_statements()
        self.expect('KEYWORD', 'end')

    def parse_assignment(self):
        self.expect('ID')
        self.expect('ASSIGN', ':=')
        self.parse_expression()

    def parse_input_statement(self):
        self.expect('KEYWORD', 'readln')
        self.expect('DELIMITER', '(')
        self.expect('ID')
        while self.current_token() and self.current_token()[0] == 'DELIMITER' and self.current_token()[1] == ',':
            self.expect('DELIMITER', ',')
            self.expect('ID')
        self.expect('DELIMITER', ')')

    def parse_output_statement(self):
        self.expect('KEYWORD', 'writeln')
        self.expect('DELIMITER', '(')
        self.parse_expression()
        while self.current_token() and self.current_token()[0] == 'DELIMITER' and self.current_token()[1] == ',':
            self.expect('DELIMITER', ',')
            self.parse_expression()
        self.expect('DELIMITER', ')')

    def parse_for_loop(self):
        self.expect('KEYWORD', 'for')
        self.parse_assignment()  # Обрабатываем присваивание в цикле
        self.expect('KEYWORD', 'to')
        self.parse_expression()  # Обрабатываем условие "до"
        if self.current_token() and self.current_token()[0] == 'KEYWORD' and self.current_token()[1] == 'step':
            self.expect('KEYWORD', 'step')
            self.parse_expression()  # Обрабатываем шаг
        self.expect('ID', 'do')
        self.parse_statements()  # Обрабатываем тело цикла (один или несколько операторов внутри цикла)

    def parse_expression(self):
        self.parse_term()
        while self.current_token() and self.current_token()[0] in {'ADD_OP', 'REL_OP'}:
            self.position += 1
            self.parse_term()

    def parse_term(self):
        self.parse_factor()
        while self.current_token() and self.current_token()[0] == 'MUL_OP':
            self.position += 1
            self.parse_factor()

    def parse_factor(self):
        token = self.current_token()
        if token[0] in {'ID', 'NUMBER', 'STRING'}:
            self.position += 1
        elif token[0] == 'DELIMITER' and token[1] == '(':
            self.expect('DELIMITER', '(')
            self.parse_expression()
            self.expect('DELIMITER', ')')
        elif token[0] == 'ADD_OP' and token[1] in {'+', '-'}:
            self.position += 1
            self.parse_factor()
        else:
            raise SyntaxError(f"Unexpected factor: {token}")