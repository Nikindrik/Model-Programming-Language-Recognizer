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

    # Ключевые слова
    TW = [
        "program", "var", "begin", "end", "if", "else", "while", "for", "to", "step", "next",
        "readln", "writeln", "true", "false", "%", "!", "$"
    ]

    # Разделители и операторы
    TD = [
        "{", "}", "(", ")", ",", ":", ";", ":=", ".", "+", "-", "*", "/", "&&", "||", "!",
        "!=", "==", "<", "<=", ">", ">="
    ]

    def __init__(self, input_text):
        self.text = input_text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.tokens = []
        self.before_begin = True

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
            if text == 'begin':
                self.before_begin = False
        else:
            self.add_token('ID', text)

    def parse_number(self):
        start = self.pos

        # Основной цикл для чисел
        while self.current_char and (self.current_char.isdigit() or self.current_char.isalpha()):
            self.advance()

        text = self.text[start:self.pos]

        if text[-1] in 'Bb' and all(c in '01' for c in text[:-1]):
            self.add_token('NUMBER', text)
        elif text[-1] in 'Oo' and all(c in '01234567' for c in text[:-1]):
            self.add_token('NUMBER', text)
        elif text[-1] in 'Hh' and all(c.isdigit() or c.upper() in 'ABCDEF' for c in text[:-1]):
            self.add_token('NUMBER', text)
        else:  # Десятичное или действительное число
            if '.' in text or 'E' in text or 'e' in text:
                parts = text.split('E') if 'E' in text else text.split('e')
                if len(parts) == 2 and (parts[1].isdigit() or (parts[1][0] in '+-' and parts[1][1:].isdigit())):
                    self.add_token('NUMBER', text)
                else:
                    self.add_token('UNKNOWN', text)
            elif text.isdigit():
                self.add_token('NUMBER', text)
            else:
                self.add_token('UNKNOWN', text)

    def parse_string(self):
        self.advance()
        start = self.pos
        while self.current_char and self.current_char != "'":
            self.advance()
        text = self.text[start:self.pos]
        self.add_token('STRING', f"'{text}'")
        self.advance()

    def parse_comment(self):
        self.advance()  # Спускаем {
        while self.current_char and self.current_char != '}':
            self.advance()
        self.advance()  # И снова

    def parse_delimiter_or_operator(self):
        start = self.pos
        self.advance()
        if self.current_char and (self.text[start:self.pos + 1] in self.TD):
            self.advance()
        text = self.text[start:self.pos]
        if text in ["==", "!=", "<", "<=", ">", ">="]:
            self.add_token('REL_OP', text)
        elif text in ["+", "-", "||"]:
            self.add_token('ADD_OP', text)
        elif text in ["*", "/", "&&"]:
            self.add_token('MUL_OP', text)
        elif text == ":=":
            self.add_token('ASSIGN', text)
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
            elif self.current_char == "'":
                self.parse_string()
            elif self.current_char == '{':
                self.parse_comment()
            elif self.current_char == '!':
                if self.text[self.pos:self.pos + 2] == "!=":
                    self.add_token('REL_OP', '!=')
                    self.advance()
                    self.advance()
                else:
                    if self.before_begin:
                        self.add_token('KEYWORD', '!')
                    else:
                        self.add_token('DELIMITER', '!')
                    self.advance()
            elif self.current_char in "%$":
                self.add_token('KEYWORD', self.current_char)
                self.advance()
            elif self.current_char in self.TD:
                self.parse_delimiter_or_operator()
            else:
                self.add_token('UNKNOWN', self.current_char)
                self.advance()
        return self.tokens