import tkinter as tk


BG = "#F3FFF6"
PINK = "#8FFF8F"
HOT_PINK = "#4FFF72"
PURPLE = "#6CE7FF"
DARK = "#548E61"
WHITE = "#FFFFFF"


window = tk.Tk()
window.title("KAINY Calculator")
window.geometry("380x610")
window.resizable(False, False)
window.configure(bg=BG)

#здесь будет хранится пример
expression = ""

display = tk.Entry(
    window,
    font=("Arial", 24, "bold"),
    justify="right",
    bd=0,
    bg=WHITE,
    fg=DARK
)
display.pack(
    fill="x",
    padx=20,
    pady=20,
    ipady=15
)


def show_expression():
    display.delete(0, tk.END)
    display.insert(tk.END, expression)


def press(value):
    global expression

    #добавляю цифру или знак в конец примера
    expression += str(value)
    show_expression()


def press_7():
    press("7")


def press_8():
    press("8")


def press_9():
    press("9")


def press_divide():
    press("/")


def press_4():
    press("4")


def press_5():
    press("5")


def press_6():
    press("6")


def press_multiply():
    press("*")


def press_1():
    press("1")


def press_2():
    press("2")


def press_3():
    press("3")


def press_minus():
    press("-")


def press_0():
    press("0")


def press_dot():
    press(".")


def press_plus():
    press("+")


def clear():
    global expression

    #полностью очищаю пример и экран
    expression = ""
    show_expression()


def backspace():
    global expression

    #удаляю последний символ если человек ошибся
    expression = expression[:-1]
    show_expression()


def simple_calculate(text):
    signs = ["+", "-", "*", "/"]

    for sign in signs:
        if sign in text:
            parts = text.split(sign)

            if len(parts) != 2:
                return "Ошибка"

            first_number = float(parts[0])
            second_number = float(parts[1])

            if sign == "+":
                return first_number + second_number

            if sign == "-":
                return first_number - second_number

            if sign == "*":
                return first_number * second_number

            if sign == "/":
                if second_number == 0:
                    return "Ошибка"
                return first_number / second_number

    return "Ошибка"


def calculate():
    global expression

    try:
        result = simple_calculate(expression)

        if result == "Ошибка":
            expression = ""
            display.delete(0, tk.END)
            display.insert(tk.END, "Ошибка")
            return

        #если ответ целый, убираю .0 для красивого вывода
        if result == int(result):
            result = int(result)

        expression = str(result)
        show_expression()

    except:
        display.delete(0, tk.END)
        display.insert(tk.END, "Ошибка")
        expression = ""


#отдельный фрейм нужен, чтобы кнопки калькулятора стояли сеткой
frame = tk.Frame(window, bg=BG)
frame.pack(pady=10)

button_7 = tk.Button(frame, text="7", command=press_7, width=5, height=2, font=("Arial", 18, "bold"), bg=PINK, fg=DARK, bd=0, cursor="hand2")
button_7.grid(row=0, column=0, padx=6, pady=6)

button_8 = tk.Button(frame, text="8", command=press_8, width=5, height=2, font=("Arial", 18, "bold"), bg=PINK, fg=DARK, bd=0, cursor="hand2")
button_8.grid(row=0, column=1, padx=6, pady=6)

button_9 = tk.Button(frame, text="9", command=press_9, width=5, height=2, font=("Arial", 18, "bold"), bg=PINK, fg=DARK, bd=0, cursor="hand2")
button_9.grid(row=0, column=2, padx=6, pady=6)

button_divide = tk.Button(frame, text="/", command=press_divide, width=5, height=2, font=("Arial", 18, "bold"), bg=PURPLE, fg=WHITE, bd=0, cursor="hand2")
button_divide.grid(row=0, column=3, padx=6, pady=6)

button_4 = tk.Button(frame, text="4", command=press_4, width=5, height=2, font=("Arial", 18, "bold"), bg=PINK, fg=DARK, bd=0, cursor="hand2")
button_4.grid(row=1, column=0, padx=6, pady=6)

button_5 = tk.Button(frame, text="5", command=press_5, width=5, height=2, font=("Arial", 18, "bold"), bg=PINK, fg=DARK, bd=0, cursor="hand2")
button_5.grid(row=1, column=1, padx=6, pady=6)

button_6 = tk.Button(frame, text="6", command=press_6, width=5, height=2, font=("Arial", 18, "bold"), bg=PINK, fg=DARK, bd=0, cursor="hand2")
button_6.grid(row=1, column=2, padx=6, pady=6)

button_multiply = tk.Button(frame, text="*", command=press_multiply, width=5, height=2, font=("Arial", 18, "bold"), bg=PURPLE, fg=WHITE, bd=0, cursor="hand2")
button_multiply.grid(row=1, column=3, padx=6, pady=6)

button_1 = tk.Button(frame, text="1", command=press_1, width=5, height=2, font=("Arial", 18, "bold"), bg=PINK, fg=DARK, bd=0, cursor="hand2")
button_1.grid(row=2, column=0, padx=6, pady=6)

button_2 = tk.Button(frame, text="2", command=press_2, width=5, height=2, font=("Arial", 18, "bold"), bg=PINK, fg=DARK, bd=0, cursor="hand2")
button_2.grid(row=2, column=1, padx=6, pady=6)

button_3 = tk.Button(frame, text="3", command=press_3, width=5, height=2, font=("Arial", 18, "bold"), bg=PINK, fg=DARK, bd=0, cursor="hand2")
button_3.grid(row=2, column=2, padx=6, pady=6)

button_minus = tk.Button(frame, text="-", command=press_minus, width=5, height=2, font=("Arial", 18, "bold"), bg=PURPLE, fg=WHITE, bd=0, cursor="hand2")
button_minus.grid(row=2, column=3, padx=6, pady=6)

button_0 = tk.Button(frame, text="0", command=press_0, width=5, height=2, font=("Arial", 18, "bold"), bg=PINK, fg=DARK, bd=0, cursor="hand2")
button_0.grid(row=3, column=0, padx=6, pady=6)

button_dot = tk.Button(frame, text=".", command=press_dot, width=5, height=2, font=("Arial", 18, "bold"), bg=PINK, fg=DARK, bd=0, cursor="hand2")
button_dot.grid(row=3, column=1, padx=6, pady=6)

button_equal = tk.Button(frame, text="=", command=calculate, width=5, height=2, font=("Arial", 18, "bold"), bg=HOT_PINK, fg=WHITE, bd=0, cursor="hand2")
button_equal.grid(row=3, column=2, padx=6, pady=6)

button_plus = tk.Button(frame, text="+", command=press_plus, width=5, height=2, font=("Arial", 18, "bold"), bg=PURPLE, fg=WHITE, bd=0, cursor="hand2")
button_plus.grid(row=3, column=3, padx=6, pady=6)

back_button = tk.Button(
    window,
    text="Назад",
    command=backspace,
    font=("Arial", 14, "bold"),
    bg="#FFF4C9",
    fg=DARK,
    bd=0,
    cursor="hand2"
)

back_button.pack(
    fill="x",
    padx=20,
    pady=5,
    ipady=10
)

clear_button = tk.Button(
    window,
    text="Очистить",
    command=clear,
    font=("Arial", 14, "bold"),
    bg="#9EF8FF",
    fg=DARK,
    bd=0,
    cursor="hand2"
)

clear_button.pack(
    fill="x",
    padx=20,
    pady=10,
    ipady=10
)

window.mainloop()
