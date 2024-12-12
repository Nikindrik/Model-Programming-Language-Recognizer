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
        self.level = 0
        self.raw = 0

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def add_token(self, type_, value, number, level, raw):
        self.tokens.append((type_, value, number, level, raw))

    def clear_whitespace(self):
        while self.current_char and self.current_char in ' \n\r\t':
            if self.current_char == '\n':
                self.level += 1
                self.raw = len(self.tokens)
            self.advance()

    def parse_identifier_or_keyword(self):
        start = self.pos
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            self.advance()
        text = self.text[start:self.pos]
        if text in self.TW:
            self.add_token('KEYWORD', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
            if text == 'begin':
                self.before_begin = False
        else:
            self.add_token('ID', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)

    def parse_number(self):
        start = self.pos
        base_detected = False

        # Проверка на основание числа
        if self.current_char == '0':
            self.advance()
            if self.current_char in 'Bb':  # Binary
                base_detected = True
                self.advance()
                while self.current_char and self.current_char in '01':
                    self.advance()
            elif self.current_char in 'Oo':  # Octal
                base_detected = True
                self.advance()
                while self.current_char and self.current_char in '01234567':
                    self.advance()
            elif self.current_char in 'Xx':  # Hexadecimal
                base_detected = True
                self.advance()
                while self.current_char and (self.current_char.isdigit() or self.current_char.upper() in 'ABCDEF'):
                    self.advance()

        if not base_detected:  # Decimal or floating point
            while self.current_char and self.current_char.isdigit():
                self.advance()
            if self.current_char == '.':  # Floating-point
                self.advance()
                while self.current_char and self.current_char.isdigit():
                    self.advance()
            if self.current_char and self.current_char.upper() == 'E':  # Exponent
                self.advance()
                if self.current_char in '+-':  # Optional sign
                    self.advance()
                if self.current_char and self.current_char.isdigit():
                    while self.current_char and self.current_char.isdigit():
                        self.advance()
                else:  # Ошибка, если нет числовой части после E
                    self.add_token('ERROR', self.text[start:self.pos], len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
                    return

        # Объединение числа с суффиксом
        if self.current_char in 'bohBOH':
            suffix = self.current_char.lower()
            self.advance()
            self.add_token('NUMBER', self.text[start:self.pos] + suffix, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        else:
            text = self.text[start:self.pos]
            self.add_token('NUMBER', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)

    def parse_string(self):
        self.advance()
        start = self.pos
        while self.current_char and self.current_char != "'":
            self.advance()
        text = self.text[start:self.pos]
        self.add_token('STRING', f"'{text}'", len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
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
            self.add_token('REL_OP', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        elif text in ["+", "-", "||"]:
            self.add_token('ADD_OP', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        elif text in ["*", "/", "&&"]:
            self.add_token('MUL_OP', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        elif text == ":=":
            self.add_token('ASSIGN', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        elif text in self.TD:
            self.add_token('DELIMITER', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        else:
            self.add_token('UNKNOWN', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)

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
                    self.add_token('REL_OP', '!=', len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
                    self.advance()
                    self.advance()
                else:
                    if self.before_begin:
                        self.add_token('KEYWORD', '!', len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
                    else:
                        self.add_token('DELIMITER', '!', len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
                    self.advance()
            elif self.current_char in "%$":
                self.add_token('KEYWORD', self.current_char, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
                self.advance()
            elif self.current_char in self.TD:
                self.parse_delimiter_or_operator()
            else:
                self.add_token('UNKNOWN', self.current_char, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
                self.advance()
        return self.tokens