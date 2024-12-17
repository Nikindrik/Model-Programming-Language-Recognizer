class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.symbol_table = {'%': '%', '!': '!', '$': '$'}  # имя переменной : тип
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

    def parse_variable_declaration(self):
        self.advance()
        while self.current_token() and self.current_token()[0] == 'ID':
            ids = self.collect_identifiers()
            self.expect('DELIMITER', ':')
            var_type = self.expect('KEYWORD')
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

    def parse_assignment(self):
        variable = self.expect('ID')
        if variable[1] not in self.symbol_table:
            raise Exception(f"Переменная '{variable[1]}' не была объявлена")
        var_type = self.symbol_table[variable[1]]
        self.expect('ASSIGN', ':=')
        expr_type = self.parse_expression_to_rpn(variable[1])

        if var_type != expr_type:
            raise Exception(f"Несоответствие типов: переменная '{variable[1]}' имеет тип {var_type}, но ей присваивается значение типа {expr_type}")

        self.symbol_table[variable[1]] = expr_type

    def parse_expression_to_rpn(self, variable_name=None):
        output_queue = []
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
                    number_type = self.detect_number_type(token[1])
                    types_stack.append(number_type)
                output_queue.append(token)
            elif token[0] == 'ADD_OP' or token[0] == 'MUL_OP':
                while operator_stack and operator_stack[-1][1] in precedence and (
                        (associativity[token[1]] == 'L' and precedence[token[1]] <= precedence[operator_stack[-1][1]]) or
                        (associativity[token[1]] == 'R' and precedence[token[1]] < precedence[operator_stack[-1][1]])):
                    self.apply_operator(output_queue, types_stack, operator_stack.pop())
                operator_stack.append(token)
            elif token[0] == 'DELIMITER' and token[1] == '(':
                operator_stack.append(token)
            elif token[0] == 'DELIMITER' and token[1] == ')':
                while operator_stack and operator_stack[-1][1] != '(':
                    self.apply_operator(output_queue, types_stack, operator_stack.pop())
                operator_stack.pop()
            else:
                raise Exception(f"Неподдерживаемый элемент в выражении: {token}")
            self.advance()

        while operator_stack:
            self.apply_operator(output_queue, types_stack, operator_stack.pop())

        if len(types_stack) != 1:
            raise Exception("Некорректное выражение: не совпадает количество операторов и операндов")

        if variable_name:
            print(f"Для переменной '{variable_name}' выражение в ОПН: ", end="")
        for item in output_queue:
            print(item[1], end=" ")
        print()
        return types_stack[0]

    def apply_operator(self, output_queue, types_stack, operator):
        if len(types_stack) < 2:
            raise Exception(f"Оператор {operator[1]} не имеет достаточного количества операндов")
        right_type = types_stack.pop()
        left_type = types_stack.pop()

        if operator[1] in {'+', '-', '*', '/'}:
            if left_type not in {'%', '!'} or right_type not in {'%', '!'}:
                raise Exception(f"Оператор {operator[1]} применим только к числовым типам (целым или действительным)")
            # Результатом арифметических операций будет float, если один из операндов float
            types_stack.append('!' if '!' in (left_type, right_type) else '%')

        elif operator[1] in {'&&', '||'}:
            if left_type != '!' or right_type != '!':
                raise Exception(f"Оператор {operator[1]} применим только к логическим типам")
            types_stack.append('!')

        output_queue.append(operator)

    def expect(self, token_type, value=None):
        token = self.current_token()
        if token and token[0] == token_type and (value is None or token[1] == value):
            self.advance()
            return token
        raise Exception(f"Ожидалось {token_type} '{value}', но найдено {token}")

    def detect_number_type(self, value):
        """
        Определяет тип числа: двоичное, восьмеричное, десятичное, шестнадцатеричное или действительное.
        """
        if value.endswith(('B', 'b')):  # Двоичное число
            core = value[:-1]
            if all(c in '01' for c in core):
                return '%'
            else:
                raise Exception(f"Некорректный формат двоичного числа: {value}")
        elif value.endswith(('O', 'o')):  # Восьмеричное число
            core = value[:-1]
            if all(c in '01234567' for c in core):
                return '%'
            else:
                raise Exception(f"Некорректный формат восьмеричного числа: {value}")
        elif value.endswith(('H', 'h')):  # Шестнадцатеричное число
            core = value[:-1]
            if all(c.isdigit() or c.upper() in 'ABCDEF' for c in core):
                return '%'
            else:
                raise Exception(f"Некорректный формат шестнадцатеричного числа: {value}")
        elif value.endswith(('D', 'd')):  # Десятичное число
            core = value[:-1]
            if core.isdigit():
                return '%'
            else:
                raise Exception(f"Некорректный формат десятичного числа: {value}")
        elif 'E' in value.upper() or '.' in value:  # Действительное число
            try:
                float(value)  # Проверка на корректность числа с плавающей точкой
                return '!'
            except ValueError:
                raise Exception(f"Некорректный формат действительного числа: {value}")
        elif value.isdigit():  # Десятичное число без суффикса
            return '%'
        else:
            raise Exception(f"Неизвестный числовой формат: {value}")