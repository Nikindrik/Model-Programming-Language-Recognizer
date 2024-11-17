import tkinter as tk
from tkinter import scrolledtext, messagebox
from lex import lexer
from pars import Parser


# Функция для переключения темы
def toggle_theme():
    if theme_var.get() == "light":
        root.tk_setPalette(background="#2e2e2e", foreground="#ffffff")
        text_area.config(bg="#2e2e2e", fg="#ffffff")
        console_area.config(bg="#1e1e1e", fg="#ffffff")
        start_button.config(bg="#444444", fg="#ffffff")
        syntax_button.config(bg="#444444", fg="#ffffff")
        theme_button.config(text="Светлая тема")
        theme_var.set("dark")
    elif theme_var.get() == "dark":
        root.tk_setPalette(background="#ffffff", foreground="#000000")
        text_area.config(bg="#ffffff", fg="#000000")
        console_area.config(bg="#f0f0f0", fg="#000000")
        start_button.config(bg="#e0e0e0", fg="#000000")
        syntax_button.config(bg="#e0e0e0", fg="#000000")
        theme_button.config(text="Темная тема")
        theme_var.set("light")


# Функция для запуска "кода" (пока без реальной логики)
def run_code():
    code = text_area.get("1.0", "end-1c")
    console_area.insert(tk.END, f"Запуск кода:\n{code}\n\n")


# Функция для вывода справки по синтаксису
def show_syntax_info():
    # TODO: Scale window of showinf0 massage
    task_text = '''
    11 вариант 21112

     1. Операции языка
        1.1. Операции группы «отношение»
            2) <операции_группы_отношения>::= != | = = | < | <= | > | >=
        1.2. Операции группы «сложение»
            2) <операции_группы_сложения>::= + | - | ||
        1.3. Операции группы «умножение»
            2) <операции_группы_умножения>::= * | / | &&
        1.4. Унарная операция
            2) <унарная_операция>::= !
    
     2. Правила, определяющие структуру программы
        2.1. Структура программы
            1) <программа>::= program var <описание> begin <оператор> {; <оператор>} end.
    
     3. Правила, определяющие раздел описания переменных
        3.1. Синтаксис команд описания данных
            1) <описание>::= {<идентификатор> {, <идентификатор> } : <тип> ;}
    
     4. Правила, определяющие типы данных
        4.1. Описание типов данных
            1) <тип>::= % | ! | $
    
     5. Правило, определяющее оператор программы
     <оператор>::= <составной> | <присваивания> | <условный> | <фиксированного_цикла> | <условного_цикла> | <ввода> | <вывода>
        5.1. Синтаксис составного оператора
            2) <составной>::= begin <оператор> { ; <оператор> } end
        5.2. Синтаксис оператора присваивания
            2) <присваивания>::= <идентификатор> := <выражение>
        5.3. Синтаксис оператора условного перехода
            2) <условный>::= if «(»<выражение> «)» <оператор> [else <оператор>]
        5.4. Синтаксис оператора цикла с фиксированным числом повторений
            2) <фиксированного_цикла>::= for <присваивания> to <выражение> [step <выражение>] <оператор> next
        5.5. Синтаксис условного оператора цикла
            2) <условного_цикла>::= while «(»<выражение> «)» <оператор>
        5.6. Синтаксис оператора ввода
            2) <ввода>::= readln идентификатор {, <идентификатор> }
        5.7. Синтаксис оператора вывода
            2) <вывода>::= writeln <выражение> {, <выражение> }
    
     6. Многострочные комментарии в программе
        1) { … }
    
    
     Правила языка для всех вариантов:
     Выражения языка задаются правилами:
        1. <выражение>::= <операнд>{<операции_группы_отношения> <операнд>}
        2. <операнд>::= <слагаемое> {<операции_группы_сложения> <слагаемое>}
        3. <слагаемое>::= <множитель> {<операции_группы_умножения> <множитель>}
        4. <множитель>::= <идентификатор> | <число> | <логическая_константа> | <унарная_операция> <множитель> | «(»<выражение>«)»
        5. <число>::= <целое> | <действительное>
        6. <логическая_константа>::= true | false
    
     Правила, определяющие идентификатор, букву и цифру:
        7. <идентификатор>::= <буква> {<буква> | <цифра>}
        8. <буква>::= A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z
        9. <цифра>::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
    
     Правила, определяющие целые числа:
        10. <целое>::= <двоичное> | <восьмеричное> | <десятичное> | <шестнадцатеричное>
        11. <двоичное>::= {/ 0 | 1 /} (B | b)
        12. <восьмеричное>::= {/ 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 /} (O | o)
        13. <десятичное>::= {/ <цифра> /} [D | d]
        14. <шестнадцатеричное>::= <цифра> {<цифра> | A | B | C | D | E | F | a | b | c | d | e | f} (H | h)
    
     Правила, описывающие действительные числа:
        15. <действительное>::= <числовая_строка> <порядок> | [<числовая_строка>] . <числовая_строка> [порядок]
        16. <числовая_строка>::= {/ <цифра> /}
        17. <порядок>::= ( E | e )[+ | -] <числовая_строка>
    '''
    messagebox.showinfo("Синтаксис", task_text)


# Функция для очистки консоли
def clear_console():
    console_area.delete(1.0, tk.END)


root = tk.Tk()
root.title("Распознаватель модельного языка программирования")
root.geometry("1152x864")
theme_var = tk.StringVar(value="dark")

# Панель для кнопок
button_frame = tk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=10)
theme_button = tk.Button(button_frame, text="Темная тема", command=toggle_theme)
theme_button.pack(side=tk.LEFT, padx=10)
start_button = tk.Button(button_frame, text="Запуск", command=run_code)
start_button.pack(side=tk.RIGHT, padx=10)
syntax_button = tk.Button(button_frame, text="Синтаксис", command=show_syntax_info)
syntax_button.pack(side=tk.LEFT, padx=10)
clear_button = tk.Button(button_frame, text="Очистить вывод", command=clear_console)
clear_button.pack(side=tk.LEFT, padx=10)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=140, height=35)
text_area.pack(padx=10, pady=10)
console_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=140, height=20, bg="#f0f0f0", fg="#000000")
console_area.pack(padx=10, pady=10)

toggle_theme()
root.mainloop()