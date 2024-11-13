import re


# Определение токенов
TOKENS = [
    ('KEYWORD', r'\b(program|var|begin|end|writeln|readln|if|else|for|to|step|next|while|true|false)\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
    ('INTEGER', r'-?\d+'),  # Целые числа с возможным минусом
    ('REAL', r'-?\d+\.\d+([Ee][+-]?\d+)?'),  # Вещественные числа с минусом
    ('NEGATIVE', r'\b-\d+\b|\b-\d+\.\d+([Ee][+-]?\d+)?\b'),  # Минус перед числом
    ('STRING', r"'[^']*'"),  # Строковые литералы
    ('OPERATOR', r'(\:=|<=|>=|!=|==|<|>|\+|-|\|\||\*|/|&&|!)'),
    ('SEPARATOR', r'[;:,()]'),
    ('TYPE', r'[%!$]|integer'),  # Добавлен новый тип 'integer'
    ('COMMENT', r'\{.*?\}'),
    ('WHITESPACE', r'\s+')
]


# Лексический анализатор
def lexer(input_code):
    tokens = []  # Найденные токены
    position = 0
    while position < len(input_code):
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(input_code, position)
            if match:
                lexeme = match.group(0)
                if token_type != 'WHITESPACE':  # Скипаю пробелы
                    tokens.append((token_type, lexeme))
                position = match.end(0)
                break
        if not match:
            raise SyntaxError(f"Unexpected character: {input_code[position]} at position {position}")
    return tokens