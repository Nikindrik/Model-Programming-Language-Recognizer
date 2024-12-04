from enum import Enum


class LexicalAnalyzer:
    class State(Enum):
        H = "H"  # Начальное состояние
        ID = "ID"  # Идентификаторы
        NUM = "NUM"  # Числа
        COM = "COM"  # Комментарии
        ALE = "ALE"  # Операции отношения
        NEQ = "NEQ"  # Неравенство (!=)
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
        self.before_begin = True  # Флаг до появления 'begin'

    def advance(self):
        """Перемещает указатель на следующий символ."""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def add_token(self, type_, value):
        self.tokens.append((type_, value))

    def clear_whitespace(self):
        """Пропуск пробелов и переносов строк."""
        while self.current_char and self.current_char in ' \n\r\t':
            self.advance()

    def parse_identifier_or_keyword(self):
        """Идентификаторы или ключевые слова."""
        start = self.pos
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            self.advance()
        text = self.text[start:self.pos]
        if text in self.TW:
            self.add_token('KEYWORD', text)
            if text == 'begin':
                self.before_begin = False  # Обновляем флаг после 'begin'
        else:
            self.add_token('ID', text)

    def parse_number(self):
        """Числа (целые и действительные)."""
        start = self.pos
        while self.current_char and self.current_char.isdigit():
            self.advance()
        if self.current_char == '.':
            self.advance()
            while self.current_char and self.current_char.isdigit():
                self.advance()
        text = self.text[start:self.pos]
        self.add_token('NUMBER', text)

    def parse_string(self):
        """Строковые литералы."""
        self.advance()  # Пропустить начальный апостроф
        start = self.pos
        while self.current_char and self.current_char != "'":
            self.advance()
        text = self.text[start:self.pos]
        self.add_token('STRING', f"'{text}'")  # Включить кавычки
        self.advance()  # Пропустить конечный апостроф

    def parse_comment(self):
        """Многострочные комментарии."""
        self.advance()  # Пропустить '{'
        while self.current_char and self.current_char != '}':
            self.advance()
        self.advance()  # Пропустить '}'

    def parse_delimiter_or_operator(self):
        """Разделители и операторы."""
        start = self.pos
        self.advance()
        # Попытка прочитать двухсимвольный оператор
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
        """Основной цикл обработки текста."""
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
                # Проверка на оператор !=
                if self.text[self.pos:self.pos + 2] == "!=":
                    self.add_token('REL_OP', '!=')
                    self.advance()
                    self.advance()
                else:
                    # Обработка одиночного !
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