from enum import Enum

class LexicalAnalyzer:
    class State(Enum):
        H = "H"  # Начальное состояние
        ID = "ID"  # Идентификаторы
        NUM = "NUM"  # Числа
        COM = "COM"  # Комментарии
        ALE = "ALE"  # Операции отношения
        NEQ = "NEQ"  # Неравенство
        DELIM = "DELIM"  # Разделители
        STR = "STR"  # Строковые литералы

    # Ключевые слова и типы данных
    TW = [
        "if", "then", "else", "while", "do", "for", "to", "read", "write",
        "true", "false", "as", "not", "or", "and", "%", "!", "$"
    ]

    # Разделители и операторы
    TD = [
        "{", "}", "[", "]", "(", ")", ",", ";", ":", "<>", "=", "<", "<=", ">", ">=", "+", "-", "*", "/", "or", "and"
    ]

    def __init__(self, input_text):
        self.text = input_text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.tokens = []

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def add_token(self, type_, value):
        self.tokens.append((type_, value))

    def clear_whitespace(self):
        while self.current_char and self.current_char in ' \n\r\t':
            self.advance()

    def parse_identifier_or_keyword(self):
        start = self.pos
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            self.advance()
        text = self.text[start:self.pos]
        if text in self.TW:
            self.add_token('KEYWORD', text)
        else:
            self.add_token('ID', text)

    def parse_number(self):
        start = self.pos
        while self.current_char and self.current_char.isdigit():
            self.advance()
        if self.current_char == '.' or self.current_char in 'eE':
            self.advance()
            while self.current_char and (self.current_char.isdigit() or self.current_char in '+-'):
                self.advance()
        text = self.text[start:self.pos]
        self.add_token('NUMBER', text)

    def parse_comment(self):
        self.advance()  # Спускаемся с /*
        while self.current_char and not (self.current_char == '*' and self.text[self.pos + 1:self.pos + 2] == '/'):
            self.advance()
        self.advance()  # Спускаемся на *
        self.advance()  # И на /

    def parse_delimiter_or_operator(self):
        start = self.pos
        self.advance()
        while self.current_char and (self.text[start:self.pos + 1] in self.TD):
            self.advance()
        text = self.text[start:self.pos]
        if text in ["<>", "=", "<", "<=", ">", ">="]:
            self.add_token('REL_OP', text)
        elif text in ["+", "-", "or"]:
            self.add_token('ADD_OP', text)
        elif text in ["*", "/", "and"]:
            self.add_token('MUL_OP', text)
        elif text in self.TD:
            self.add_token('DELIMITER', text)
        else:
            self.add_token('UNKNOWN', text)

    def tokenize(self):
        while self.current_char:
            self.clear_whitespace()
            if not self.current_char:
                break
            if self.current_char.isalpha():
                self.parse_identifier_or_keyword()
            elif self.current_char.isdigit():
                self.parse_number()
            elif self.current_char == '/' and self.text[self.pos + 1:self.pos + 2] == '*':
                self.parse_comment()
            elif self.current_char in self.TD:
                self.parse_delimiter_or_operator()
            else:
                self.add_token('UNKNOWN', self.current_char)
                self.advance()
        return self.tokens