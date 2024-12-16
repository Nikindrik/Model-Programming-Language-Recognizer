from enum import Enum

class TokenType(Enum):
    KEYWORD = "KEYWORD"
    ID = "ID"
    NUMBER = "NUMBER"
    STRING = "STRING"
    DELIMITER = "DELIMITER"
    REL_OP = "REL_OP"
    ADD_OP = "ADD_OP"
    MUL_OP = "MUL_OP"
    ASSIGN = "ASSIGN"
    ERROR = "ERROR"

class SyntaxError(Exception):
    pass

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def consume(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type}, but found {self.current_token}")

    def program(self):
        """ program ::= 'program' var <description> begin <statement> end. """
        if self.current_token[0] == TokenType.KEYWORD and self.current_token[1] == "program":
            self.advance()
            if self.current_token[0] == TokenType.KEYWORD and self.current_token[1] == "var":
                self.advance()
                self.description()
                if self.current_token[0] == TokenType.KEYWORD and self.current_token[1] == "begin":
                    self.advance()
                    self.statement()
                    if self.current_token[0] == TokenType.KEYWORD and self.current_token[1] == "end":
                        self.advance()
                        if self.current_token[0] == TokenType.DELIMITER and self.current_token[1] == ".":
                            self.advance()
                        else:
                            raise SyntaxError("Expected '.' at the end of program.")
                    else:
                        raise SyntaxError("Expected 'end' at the end of program.")
                else:
                    raise SyntaxError("Expected 'begin' after var declaration.")
            else:
                raise SyntaxError("Expected 'var' after 'program'.")
        else:
            raise SyntaxError("Expected 'program' at the beginning.")

    def description(self):
        """ description ::= <identifier> {, <identifier>} : <type>; """
        # Для простоты, типы данные % | ! | $
        if self.current_token[0] == TokenType.ID:
            self.advance()
            while self.current_token[0] == TokenType.DELIMITER and self.current_token[1] == ",":
                self.advance()
                if self.current_token[0] == TokenType.ID:
                    self.advance()
                else:
                    raise SyntaxError("Expected identifier after ','")
            self.consume(TokenType.DELIMITER)  # ':'
            self.consume(TokenType.KEYWORD)  # % | ! | $
            self.consume(TokenType.DELIMITER)  # ';'
        else:
            raise SyntaxError("Expected identifier in description.")

    def statement(self):
        """ statement ::= <assignment> | <conditional> | <loop> | <input/output> """
        if self.current_token[0] == TokenType.ID:
            self.assignment()
        elif self.current_token[0] == TokenType.KEYWORD and self.current_token[1] == "if":
            self.conditional()
        elif self.current_token[0] == TokenType.KEYWORD and self.current_token[1] == "while":
            self.loop()
        elif self.current_token[0] == TokenType.KEYWORD and self.current_token[1] in ["readln", "write"]:
            self.input_output()
        else:
            raise SyntaxError("Expected a statement.")

    def assignment(self):
        """ assignment ::= <identifier> as <expression> """
        self.consume(TokenType.ID)
        self.consume(TokenType.ASSIGN)
        self.expression()

    def expression(self):
        """ expression ::= <term> {<add_op> <term>} """
        self.term()
        while self.current_token[0] in [TokenType.ADD_OP]:
            self.advance()
            self.term()

    def term(self):
        """ term ::= <factor> {<mul_op> <factor>} """
        self.factor()
        while self.current_token[0] in [TokenType.MUL_OP]:
            self.advance()
            self.factor()

    def factor(self):
        """ factor ::= <identifier> | <number> | <string> | <parenthesized_expr> """
        if self.current_token[0] == TokenType.ID:
            self.consume(TokenType.ID)
        elif self.current_token[0] == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
        elif self.current_token[0] == TokenType.STRING:
            self.consume(TokenType.STRING)
        elif self.current_token[0] == TokenType.DELIMITER and self.current_token[1] == "(":
            self.advance()
            self.expression()
            self.consume(TokenType.DELIMITER)  # ')'
        else:
            raise SyntaxError("Expected a factor.")

    def conditional(self):
        """ conditional ::= if <expression> then <statement> [else <statement>] end_else """
        self.consume(TokenType.KEYWORD)  # "if"
        self.expression()
        self.consume(TokenType.KEYWORD)  # "then"
        self.statement()
        if self.current_token[0] == TokenType.KEYWORD and self.current_token[1] == "else":
            self.advance()
            self.statement()
        self.consume(TokenType.KEYWORD)  # "end_else"

    def loop(self):
        """ loop ::= while <expression> do <statement> """
        self.consume(TokenType.KEYWORD)  # "while"
        self.expression()
        self.consume(TokenType.KEYWORD)  # "do"
        self.statement()

    def input_output(self):
        """ input_output ::= readln (<identifier>) | write (<expression>) """
        if self.current_token[0] == TokenType.KEYWORD and self.current_token[1] == "readln":
            self.advance()
            self.consume(TokenType.DELIMITER)  # "("
            self.consume(TokenType.ID)  # identifier
            self.consume(TokenType.DELIMITER)  # ")"
        elif self.current_token[0] == TokenType.KEYWORD and self.current_token[1] == "write":
            self.advance()
            self.consume(TokenType.DELIMITER)  # "("
            self.expression()
            self.consume(TokenType.DELIMITER)  # ")"
        else:
            raise SyntaxError("Expected 'readln' or 'write' for input/output.")

# Пример использования:
tokens = [
    (TokenType.KEYWORD, "program"),
    (TokenType.KEYWORD, "var"),
    (TokenType.ID, "x"),
    (TokenType.DELIMITER, ":"),
    (TokenType.KEYWORD, "%"),
    (TokenType.DELIMITER, ";"),
    (TokenType.KEYWORD, "begin"),
    (TokenType.ID, "x"),
    (TokenType.ASSIGN, "as"),
    (TokenType.NUMBER, "5"),
    (TokenType.DELIMITER, ";"),
    (TokenType.KEYWORD, "end"),
    (TokenType.DELIMITER, ".")
]

syntax_analyzer = SyntaxAnalyzer(tokens)
syntax_analyzer.program()
