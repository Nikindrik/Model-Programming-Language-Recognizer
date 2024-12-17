from enum import Enum


class LexicalAnalyzer:
    class State(Enum):
        H = "H"  # Начальное состояние
        ID = "ID"  # Идентификаторы
        NUM = "NUM"  # Числа
        COM = "COM"  # Комментарии
        STR = "STR"  # Строковые литералы
        DELIM = "DELIM"  # Разделители и операторы
        ERROR = "ERROR"  # Ошибки
        END = "END"  # Конечное состояние

    # Ключевые слова
    TW = [
        "program", "var", "begin", "end", "if", "else", "while", "for", "to", "step", "next",
        "readln", "writeln", "true", "false", "%", "!", "$"
    ]

    # Разделители и операторы
    TD = [
        "{", "}", "(", ")", ",", ";", ".", "+", "-", "*", "/", "&&", "||", ":", ":=", "!=", "==",
        "<", "<=", ">", ">="
    ]

    def __init__(self, input_text):
        self.text = input_text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.tokens = []
        self.state = self.State.H
        self.before_begin = True
        self.level = 0
        self.raw = 0

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def add_token(self, type_, value, number, level, raw):
        self.tokens.append((type_, value, number, level, raw))

    def transition(self):
        while self.current_char:
            if self.state == self.State.H:
                self.state_h()
            elif self.state == self.State.ID:
                self.state_id()
            elif self.state == self.State.NUM:
                self.state_num()
            elif self.state == self.State.STR:
                self.state_str()
            elif self.state == self.State.COM:
                self.state_com()
            elif self.state == self.State.DELIM:
                self.state_delim()
            elif self.state == self.State.END:
                break

    def state_h(self):
        if self.current_char.isspace():
            self.clear_whitespace()
        elif self.current_char.isalpha():
            self.state = self.State.ID
        elif self.current_char.isdigit():
            self.state = self.State.NUM
        elif self.current_char == "'":
            self.state = self.State.STR
            self.advance()
        elif self.current_char == "{":
            self.state = self.State.COM
            self.advance()
        else:
            self.state = self.State.DELIM

    def state_id(self):
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
        self.state = self.State.H

    def state_num(self):
        start = self.pos
        is_real = False
        while self.current_char and (self.current_char.isdigit() or self.current_char in 'ABCDEFabcdef'):
            self.advance()
        if self.current_char == '.':
            is_real = True
            self.advance()
            while self.current_char and self.current_char.isdigit():
                self.advance()
        if self.current_char in 'Ee':
            is_real = True
            self.advance()
            if self.current_char in '+-':
                self.advance()
            while self.current_char and self.current_char.isdigit():
                self.advance()
        if is_real:
            self.add_token('NUMBER', self.text[start:self.pos], len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
            self.state = self.State.H
            return
        if self.current_char in 'Dd':
            self.advance()
            self.add_token('NUMBER', self.text[start:self.pos], len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
            self.state = self.State.H
            return
        elif self.current_char in 'Bb':
            self.advance()
            while self.current_char and self.current_char in '01':
                self.advance()
            self.add_token('NUMBER', self.text[start:self.pos], len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
            self.state = self.State.H
            return
        elif self.current_char in 'Oo':
            self.advance()
            while self.current_char and self.current_char in '01234567':
                self.advance()
            self.add_token('NUMBER', self.text[start:self.pos], len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
            self.state = self.State.H
            return
        elif self.current_char in 'Hh':
            self.advance()
            while self.current_char and (self.current_char.isdigit() or self.current_char in 'ABCDEFabcdef'):
                self.advance()
            self.add_token('NUMBER', self.text[start:self.pos], len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
            self.state = self.State.H
            return
        self.add_token('NUMBER', self.text[start:self.pos], len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        self.state = self.State.H

    def state_str(self):
        start = self.pos
        while self.current_char and self.current_char != "'":
            self.advance()
        text = self.text[start:self.pos]
        self.add_token('STRING', "'" + text + "'", len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        self.advance()
        self.state = self.State.H

    def state_com(self):
        while self.current_char and self.current_char != '}':
            self.advance()
        self.advance()
        self.state = self.State.H

    def state_delim(self):
        start = self.pos
        if self.current_char + self.peek() in [":=", "==", "!=", "<=", ">=", "&&", "||"]:
            self.advance()
            self.advance()
            text = self.text[start:self.pos]
        else:
            text = self.current_char
            self.advance()

        if text in [":", ",", ";", ".", "(", ")", "{", "}"]:
            self.add_token('DELIMITER', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        elif text in [":="]:
            self.add_token('ASSIGN', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        elif text in ["+", "-", "||"]:
            self.add_token('ADD_OP', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        elif text in ["*", "/", "&&"]:
            self.add_token('MUL_OP', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        elif text in ["<", "<=", ">", ">=", "==", "!="]:
            self.add_token('REL_OP', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        elif text in self.TW:
            self.add_token('KEYWORD', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)
        else:
            self.add_token('UNKNOWN', text, len(self.tokens) + 1, self.level, len(self.tokens) + 1 - self.raw)

        self.state = self.State.H


    def peek(self):
        return self.text[self.pos + 1] if self.pos + 1 < len(self.text) else ''

    def clear_whitespace(self):
        while self.current_char and self.current_char in ' \n\r\t':
            if self.current_char == '\n':
                self.level += 1
                self.raw = len(self.tokens)
            self.advance()

    def tokenize(self):
        self.transition()
        return self.tokens