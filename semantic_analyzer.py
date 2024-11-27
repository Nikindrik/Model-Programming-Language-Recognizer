class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.symbol_table = {}  # имя переменной : тип
        self.current_position = 0

    def current_token(self):
        return self.tokens[self.current_position] if self.current_position < len(self.tokens) else None

    def advance(self):
        self.current_position += 1

    def analyze(self):
        try:
            while self.current_position < len(self.tokens):
                token = self.current_token()
                if token[0] == 'KEYWORD' and token[1] == 'var':
                    self.parse_variable_declaration()
                elif token[0] == 'ID' and self.peek_next()[0] == 'ASSIGN':
                    self.parse_assignment()
                else:
                    self.advance()
            return "Семантический анализ завершён успешно"
        except Exception as e:
            return f"Семантическая ошибка: {e}"

    def peek_next(self):
        next_position = self.current_position + 1
        return self.tokens[next_position] if next_position < len(self.tokens) else None

    def parse_variable_declaration(self):  # Объявления
        self.advance()
        while self.current_token() and self.current_token()[0] == 'ID':
            ids = self.collect_identifiers()
            self.expect('DELIMITER', ':')
            var_type = self.expect('TYPE')
            for var in ids:
                if var in self.symbol_table:
                    raise Exception(f"Переменная '{var}' уже объявлена.")
                self.symbol_table[var] = var_type[1]
            self.expect('DELIMITER', ';')

    def collect_identifiers(self):
        ids = []
        while self.current_token() and self.current_token()[0] == 'ID':
            ids.append(self.current_token()[1])
            self.advance()
            if self.current_token() and self.current_token()[0] == 'DELIMITER' and self.current_token()[1] == ',':
                self.advance()
            else:
                break
        return ids

    def parse_assignment(self):  # Присвоения
        variable = self.expect('ID')
        if variable[1] not in self.symbol_table:
            raise Exception(f"Переменная '{variable[1]}' не была объявлена.")
        var_type = self.symbol_table[variable[1]]
        self.expect('ASSIGN', ':=')
        expr_type = self.parse_expression_to_rpn()
        if expr_type != var_type:
            raise Exception(f"Несоответствие типов: переменная '{variable[1]}' имеет тип {var_type}, но ей присваивается значение типа {expr_type}.")

    def parse_expression_to_rpn(self):  # Операторы и польская запись
        output_queue = []  # Очередь выхода
        operator_stack = []
        types_stack = []

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '&&': 3, '||': 3}
        associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '&&': 'L', '||': 'L'}

        while self.current_token() and self.current_token()[0] not in {'DELIMITER', 'KEYWORD'}:
            token = self.current_token()

            if token[0] in {'NUMBER', 'ID'}:
                if token[0] == 'ID':
                    if token[1] not in self.symbol_table:
                        raise Exception(f"Переменная '{token[1]}' не была объявлена.")
                    types_stack.append(self.symbol_table[token[1]])
                elif token[0] == 'NUMBER':
                    types_stack.append('%')
                output_queue.append(token)
            elif token[0] == 'ADD_OP' or token[0] == 'MUL_OP':
                while operator_stack and operator_stack[-1][1] in precedence and \
                        ((associativity[token[1]] == 'L' and precedence[token[1]] <= precedence[operator_stack[-1][1]]) or
                         (associativity[token[1]] == 'R' and precedence[token[1]] < precedence[operator_stack[-1][1]])):
                    self.apply_operator(output_queue, types_stack, operator_stack.pop())
                operator_stack.append(token)
            elif token[0] == 'DELIMITER' and token[1] == '(':
                operator_stack.append(token)
            elif token[0] == 'DELIMITER' and token[1] == ')':
                while operator_stack and operator_stack[-1][1] != '(':
                    self.apply_operator(output_queue, types_stack, operator_stack.pop())
                operator_stack.pop()  # Убираем '('
            else:
                raise Exception(f"Неподдерживаемый элемент в выражении: {token}")
            self.advance()

        while operator_stack:
            self.apply_operator(output_queue, types_stack, operator_stack.pop())

        if len(types_stack) != 1:
            raise Exception("Некорректное выражение: не совпадает количество операторов и операндов")
        return types_stack[0]

    def apply_operator(self, output_queue, types_stack, operator):  # Применяет оператор, проверяет типы операндов и добавляет результат в стек типов
        if len(types_stack) < 2:
            raise Exception(f"Оператор {operator[1]} не имеет достаточного количества операндов")
        right_type = types_stack.pop()
        left_type = types_stack.pop()

        if operator[1] in {'+', '-', '*', '/'}:
            if left_type != '%' or right_type != '%':
                raise Exception(f"Оператор {operator[1]} применим только к числовым типам")
            types_stack.append('%')  # Результат число
        elif operator[1] in {'&&', '||'}:
            if left_type != '!' or right_type != '!':
                raise Exception(f"Оператор {operator[1]} применим только к логическим типам")
            types_stack.append('!')  # Результат логическое значение
        output_queue.append(operator)

    def expect(self, token_type, value=None):
        token = self.current_token()
        if token and token[0] == token_type and (value is None or token[1] == value):
            self.advance()
            return token
        raise Exception(f"Ожидалось {token_type} '{value}', но найдено {token}")