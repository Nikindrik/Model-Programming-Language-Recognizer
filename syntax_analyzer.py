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
        self.expect('KEYWORD')

    def parse_statements(self):
        while True:
            token = self.current_token()
            if not token:
                return
            elif token[0] == 'KEYWORD' and token[1] == 'begin':
                self.parse_compound_statement()
            elif token[0] == 'ID':
                self.parse_assignment()
            elif token[0] == 'KEYWORD' and token[1] == 'readln':
                self.parse_input_statement()
            elif token[0] == 'KEYWORD' and token[1] == 'writeln':
                self.parse_output_statement()
            elif token[0] == 'KEYWORD' and token[1] == 'if':
                self.parse_if_else_statement()
            elif token[0] == 'KEYWORD' and token[1] == 'for':
                self.parse_for_loop()
            elif token[0] == 'KEYWORD' and token[1] == 'while':
                self.parse_while_loop()
            elif token[0] == 'KEYWORD' and token[1] == 'next':
                self.advance()
            elif token[0] == 'KEYWORD' and token[1] == 'end':
                return
            elif token[0] == 'DELIMITER' and token[1] == ';':
                self.advance()
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
        self.expect('ID')
        while self.current_token() and self.current_token()[0] == 'DELIMITER' and self.current_token()[1] == ',':
            self.expect('DELIMITER', ',')
            self.expect('ID')

    def parse_output_statement(self):
        self.expect('KEYWORD', 'writeln')
        self.parse_expression()
        while self.current_token() and self.current_token()[0] == 'DELIMITER' and self.current_token()[1] == ',':
            self.expect('DELIMITER', ',')
            self.parse_expression()

    def parse_for_loop(self):
        self.expect('KEYWORD', 'for')
        self.parse_assignment()
        self.expect('KEYWORD', 'to')
        self.parse_expression()  # Верхняя граница цикла
        if self.current_token() and self.current_token()[0] == 'KEYWORD' and self.current_token()[1] == 'step':
            self.expect('KEYWORD', 'step')
            self.parse_expression()
        self.expect('KEYWORD', 'begin')  # Внутрянка цикла

        while True:
            token = self.current_token()
            if token[0] == 'KEYWORD' and token[1] == 'next':
                self.advance()
            elif token[0] == 'KEYWORD' and token[1] == 'end':
                break
            else:
                self.parse_statements()

        self.expect('KEYWORD', 'end')

    def parse_while_loop(self):
        self.expect('KEYWORD', 'while')
        self.expect('DELIMITER', '(')
        self.parse_expression()
        self.expect('DELIMITER', ')')
        self.expect('KEYWORD', 'begin')
        self.parse_statements()
        self.expect('KEYWORD', 'end')

    def parse_expression(self):
        self.parse_term()
        while self.current_token() and self.current_token()[0] in {'ADD_OP', 'REL_OP'}:
            self.advance()
            self.parse_term()

    def parse_term(self):
        self.parse_factor()
        while self.current_token() and self.current_token()[0] == 'MUL_OP':
            self.advance()
            self.parse_factor()

    def parse_factor(self):
        token = self.current_token()
        if token[0] in {'ID', 'STRING'}:
            self.advance()
        elif token[0] == 'NUMBER':
            self.parse_number()
        elif token[0] == 'DELIMITER' and token[1] == '(':
            self.expect('DELIMITER', '(')
            self.parse_expression()
            self.expect('DELIMITER', ')')
        elif token[0] == 'KEYWORD' and token[1] in {'true', 'false'}:
            self.parse_boolean_literal()
        elif token[0] == 'ADD_OP' and token[1] in {'+', '-'}:
            self.advance()
            self.parse_factor()
        else:
            raise SyntaxError(f"Unexpected factor: {token}")

    def parse_if_else_statement(self):
        self.expect('KEYWORD', 'if')
        self.expect('DELIMITER', '(')
        self.parse_expression()
        self.expect('DELIMITER', ')')
        self.expect('KEYWORD', 'begin')
        self.parse_statements()
        self.expect('KEYWORD', 'end')
        if self.current_token() and self.current_token()[0] == 'KEYWORD' and self.current_token()[1] == 'else':
            self.advance()
            self.expect('KEYWORD', 'begin')
            self.parse_statements()
            self.expect('KEYWORD', 'end')

    def parse_number(self):
        token = self.current_token()
        if self.is_binary(token):
            self.advance()
        elif self.is_octal(token):
            self.advance()
        elif self.is_decimal(token):
            self.advance()
        elif self.is_hexadecimal(token):
            self.advance()
        elif self.is_real(token):
            self.advance()
        else:
            raise SyntaxError(f"Unexpected number format: {token}")

    def parse_boolean_literal(self):
        token = self.current_token()
        if token[0] == 'KEYWORD' and token[1] in {'true', 'false'}:
            self.advance()
        else:
            raise SyntaxError(f"Unexpected boolean literal: {token}")

    def is_binary(self, token):
        if token[0] != 'NUMBER':
            return False
        value = token[1]
        if value.endswith(('b', 'B')):
            return all(c in '01' for c in value[:1])
        return False

    def is_octal(self, token):
        if token[0] != 'NUMBER':
            return False
        value = token[1]
        if value.endswith(('o', 'O')):
            return all(c in '01234567' for c in value[:1])
        return False

    def is_decimal(self, token):
        if token[0] != 'NUMBER':
            return False
        value = token[1]
        if value.isdigit():
            return True
        if value.endswith(('d', 'D')):
            return value[:-1].isdigit()
        return False

    def is_hexadecimal(self, token):
        if token[0] != 'NUMBER':
            return False
        value = token[1]
        if value.endswith(('h', 'H')):
            valid_chars = set('0123456789ABCDEFabcdef')
            return all(c in valid_chars for c in value[:1])
        return False

    def is_real(self, token):
        if token[0] != 'NUMBER':
            return False
        value = token[1]
        try:
            float(value)
            return True
        except ValueError:
            return False