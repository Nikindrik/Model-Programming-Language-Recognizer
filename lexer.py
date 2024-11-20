import re

class LexicalAnalyzer:
    def __init__(self):
        self.tokens = []
        self.token_specs = [
            ('COMMENT', r'\{.*?\}'),  # Многострочные комментарии
            ('STRING', r"'[^']*'"),  # Строковые литералы
            ('KEYWORD', r'program|var|begin|end|if|else|for|to|step|next|while|readln|writeln'),  # Ключевые слова
            ('NUMBER', r'\d+(\.\d+)?([eE][+-]?\d+)?'),  # Числа
            ('REL_OP', r'!=|==|<=|>=|<|>'),  # Операции отношения
            ('ADD_OP', r'\+|-|\|\|'),  # Операции сложения
            ('MUL_OP', r'\*|/|&&'),  # Операции умножения
            ('UNARY_OP', r'!'),  # Унарная операция
            ('ID', r'[a-zA-Z_][a-zA-Z_0-9]*'),  # Идентификаторы
            ('TYPE', r'%|!|\$'),  # Типы данных
            ('ASSIGN', r':='),  # Присваивание
            ('DELIMITER', r';|,|:|\(|\)|\.|end\.'),  # Ограничители
            ('WHITESPACE', r'\s+'),  # Пробелы
            ('UNKNOWN', r'.'),  # Неизвестные символы
        ]
        self.token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.token_specs)

    def tokenize(self, text):
        """Разделяет текст на токены с учетом контекста."""
        self.tokens = []
        in_code_block = False
        for match in re.finditer(self.token_regex, text):
            kind = match.lastgroup
            value = match.group(kind)
            if kind == 'WHITESPACE' or kind == 'COMMENT':
                continue  # Игнорируем пробелы и комментарии
            elif kind == 'KEYWORD' and value == 'begin':
                in_code_block = True
            elif value == '!' and in_code_block:
                kind = 'UNARY_OP'  # После `begin` `!` интерпретируется как `UNARY_OP`
            elif value == '!' and not in_code_block:
                kind = 'TYPE'  # До `begin` `!` интерпретируется как `TYPE`
            elif kind == 'UNKNOWN':
                raise SyntaxError(f"Unknown token: {value}")
            self.tokens.append((kind, value))
        return self.tokens