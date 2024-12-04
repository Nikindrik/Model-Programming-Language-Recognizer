# Model-Programming-Language-Recognizer
Course project on the discipline of TFY


```
python -m venv venv    
.\venv\Scripts\activate
pip install tk 
pip install Pillow 
pip install prettytable
python main.py
```

Лексический анализатор в lexer.py

Синтаксический анализатор syntax_analyzer.py

Семантический анализатор semantic_analyzer.py

analyzer.py для запуска анализа

main.py GUI, пока без функционала

Граф состояний лексического анализтора

```
digraph LexicalAnalyzer {
    rankdir=LR;

    // Начальное состояние
    H [shape=ellipse, label="H (Начальное)"];

    // Основные состояния
    ID [shape=ellipse, label="ID (Идентификаторы)"];
    NUM [shape=ellipse, label="NUM (Числа)"];
    COM [shape=ellipse, label="COM (Комментарии)"];
    ALE [shape=ellipse, label="ALE (Операторы отношений)"];
    NEQ [shape=ellipse, label="NEQ (Неравенство)"];
    DELIM [shape=ellipse, label="DELIM (Разделители)"];
    STR [shape=ellipse, label="STR (Строки)"];
    ERR [shape=ellipse, label="ERR (Ошибка)"];

    // Переходы из начального состояния
    H -> H [label="Пробел, \\n, \\r, \\t"];
    H -> ID [label="Буква"];
    H -> NUM [label="Цифра"];
    H -> COM [label="'{'"];
    H -> ALE [label="'<', '>'"];
    H -> NEQ [label="'!'"];
    H -> DELIM [label="Разделители или операторы"];
    H -> STR [label="' (Строка)"];

    // Переходы для идентификаторов
    ID -> ID [label="Буква, цифра"];
    ID -> H [label="Иной символ (Токен завершён)"];

    // Переходы для чисел
    NUM -> NUM [label="Цифра"];
    NUM -> NUM [label="'.' (Дробная часть)"];
    NUM -> H [label="Иной символ (Токен завершён)"];

    // Переходы для комментариев
    COM -> COM [label="Любой символ, кроме '}'"];
    COM -> H [label="'}'"];

    // Переходы для операторов отношений
    ALE -> H [label="Одиночный символ (Например, '<')"];
    ALE -> H [label="'=' (Двухсимвольный оператор, например '<=')"];

    // Переходы для неравенства (!=)
    NEQ -> H [label="'=' (Завершение !=)"];
    NEQ -> ERR [label="Другой символ"];

    // Переходы для разделителей и операторов
    DELIM -> H [label="Токен завершён"];

    // Переходы для строк
    STR -> STR [label="Любой символ, кроме '"];
    STR -> H [label="' (Завершение строки)"];

    // Ошибки
    NEQ -> ERR [label="Неизвестный символ"];
}

```
