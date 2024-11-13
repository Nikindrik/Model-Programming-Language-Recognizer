class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        self.program()

    def consume(self, expected_type):
        token_type, token_value = self.tokens[self.position]
        if token_type == expected_type:
            self.position += 1
            return token_value
        else:
            raise SyntaxError(f"Expected {expected_type} but found {token_type} ({token_value}) at position {self.position}")

    def program(self):
        self.consume('KEYWORD')  # program
        self.consume('KEYWORD')  # var
        self.var_declaration()
        self.consume('KEYWORD')  # begin
        self.statement_list()
        self.consume('KEYWORD')  # end

    def var_declaration(self):
        while self.peek() == 'IDENTIFIER':
            self.consume('IDENTIFIER')
            if self.peek() == 'SEPARATOR' and self.peek_value() == ',':
                self.consume('SEPARATOR')
            self.consume('SEPARATOR')  # :
            self.consume('TYPE')       # % или другой тип
            self.consume('SEPARATOR')  # ;

    def statement_list(self):
        while self.peek() != 'KEYWORD' or self.peek_value() != 'end':
            self.statement()
            if self.peek() == 'SEPARATOR' and self.peek_value() == ';':
                self.consume('SEPARATOR')

    def statement(self):
        if self.peek() == 'IDENTIFIER':
            self.assignment_statement()
        elif self.peek() == 'KEYWORD' and self.peek_value() == 'writeln':
            self.output_statement()
        elif self.peek() == 'KEYWORD' and self.peek_value() == 'if':
            self.conditional_statement()
        elif self.peek() == 'KEYWORD' and self.peek_value() == 'for':
            self.for_loop()
        elif self.peek() == 'KEYWORD' and self.peek_value() == 'while':
            self.while_loop()
        else:
            raise SyntaxError(f"Unexpected statement start: {self.peek()} ({self.peek_value()})")

    def assignment_statement(self):
        self.consume('IDENTIFIER')  # идентификатор
        self.consume('OPERATOR')    # :=
        self.expression()           # выражение после присваивания

    def output_statement(self):
        self.consume('KEYWORD')  # writeln
        self.expression()

    def conditional_statement(self):
        self.consume('KEYWORD')  # if
        self.consume('SEPARATOR')  # (
        self.expression()
        self.consume('SEPARATOR')  # )
        self.statement()
        if self.peek() == 'KEYWORD' and self.peek_value() == 'else':
            self.consume('KEYWORD')  # else
            self.statement()

    def for_loop(self):
        self.consume('KEYWORD')  # for
        self.assignment_statement()
        self.consume('KEYWORD')  # to
        self.expression()
        if self.peek() == 'KEYWORD' and self.peek_value() == 'step':
            self.consume('KEYWORD')  # step
            self.expression()
        self.statement()
        self.consume('KEYWORD')  # next

    def while_loop(self):
        self.consume('KEYWORD')  # while
        self.consume('SEPARATOR')  # (
        self.expression()
        self.consume('SEPARATOR')  # )
        self.statement()

    def expression(self):
        # Обработка минуса, если он стоит перед числом
        if self.peek() == 'IDENTIFIER':
            self.consume('IDENTIFIER')  # идентификатор
        elif self.peek() == 'INTEGER' or self.peek() == 'REAL' or self.peek() == 'NEGATIVE':
            self.consume(self.peek())  # число или число с минусом
        else:
            raise SyntaxError(f"Unexpected token in expression: {self.peek_value()}")

    def peek(self):
        return self.tokens[self.position][0] if self.position < len(self.tokens) else None

    def peek_value(self):
        return self.tokens[self.position][1] if self.position < len(self.tokens) else None