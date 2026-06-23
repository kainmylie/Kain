import tkinter as tk
from tkinter import messagebox
import random


BG = "#F4DBFF"
CARD = "#FFFFFF"

PRIMARY = "#EC8FFF"
PRIMARY_DARK = "#DF4FFF"
PRIMARY_LIGHT = "#F7D6FF"

TEXT = "#E26FFF"
TEXT_LIGHT = "#D56CFF"


window = tk.Tk()
window.title("KAINY Password Generator 😼")
window.geometry("500x620")
window.configure(bg=BG)
window.resizable(False, False)

title = tk.Label(
    window,
    text="KAINY PASSWORD GENERATOR 🔐",
    font=("Arial", 20, "bold"),
    bg=BG,
    fg=TEXT
)
title.pack(pady=20)

#в этой переменной будет храниться готовый пароль
password_var = tk.StringVar()

password_entry = tk.Entry(
    window,
    textvariable=password_var,
    font=("Arial", 18),
    justify="center",
    bg=CARD,
    fg=TEXT,
    bd=0
)
password_entry.pack(fill="x", padx=25, ipady=12)

length_label = tk.Label(
    window,
    text="Длина пароля: 12",
    font=("Arial", 13, "bold"),
    bg=BG,
    fg=TEXT
)
length_label.pack(pady=15)


def update_length(value):
    #обновляю надпись когда двигается ползун
    length = int(float(value))
    length_label.config(text="Длина пароля: " + str(length))


length_scale = tk.Scale(
    window,
    from_=4,
    to=32,
    orient="horizontal",
    bg=BG,
    fg=TEXT,
    highlightthickness=0,
    command=update_length
)
length_scale.set(12)
length_scale.pack()

#они отвечают за выбранные настройки пароля
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
uppercase_var = tk.BooleanVar(value=True)

tk.Checkbutton(
    window,
    text="Цифры",
    variable=numbers_var,
    bg=BG,
    fg=TEXT,
    font=("Arial", 12)
).pack()

tk.Checkbutton(
    window,
    text="Спецсимволы",
    variable=symbols_var,
    bg=BG,
    fg=TEXT,
    font=("Arial", 12)
).pack()

tk.Checkbutton(
    window,
    text="Большие буквы",
    variable=uppercase_var,
    bg=BG,
    fg=TEXT,
    font=("Arial", 12)
).pack()

strength_label = tk.Label(
    window,
    text="Надежность: -",
    font=("Arial", 14, "bold"),
    bg=BG,
    fg=TEXT
)
strength_label.pack(pady=15)


def generate_password():
    #сначала беру маленькие буквы, а потом добавляю выбранные символы
    chars = "abcdefghijklmnopqrstuvwxyz"

    if uppercase_var.get():
        chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if numbers_var.get():
        chars += "0123456789"

    if symbols_var.get():
        chars += "!@#$%^&*()_+-=[]{}"

    length = length_scale.get()

    #собираю пароль по одному случайному символу
    password = ""

    for i in range(length):
        password += random.choice(chars)

    password_var.set(password)

    #надежность считаю простым способом, длина плюс выбранные настройки
    score = 0

    if length >= 12:
        score += 1

    if uppercase_var.get():
        score += 1

    if numbers_var.get():
        score += 1

    if symbols_var.get():
        score += 1

    if score <= 1:
        strength_label.config(
            text="Надежность: Слабый 🌸",
            fg="#D38BC8"
        )

    elif score <= 3:
        strength_label.config(
            text="Надежность: Средний ✨",
            fg="#C370D8"
        )

    else:
        strength_label.config(
            text="Надежность: Сильный 😼",
            fg=TEXT_LIGHT
        )


def copy_password():
    password = password_var.get()

    if password == "":
        return

    #копирую пароль в буфер обмена, чтобы его можно было сразу вставить
    window.clipboard_clear()
    window.clipboard_append(password)

    messagebox.showinfo(
        "Готово",
        "Пароль скопирован 📋"
    )


generate_button = tk.Button(
    window,
    text="Сгенерировать 🔐",
    command=generate_password,
    bg=PRIMARY,
    fg="white",
    font=("Arial", 14, "bold"),
    bd=0,
    cursor="hand2"
)
generate_button.pack(pady=20, ipadx=20, ipady=10)

copy_button = tk.Button(
    window,
    text="Копировать 📋",
    command=copy_password,
    bg=PRIMARY_LIGHT,
    fg=TEXT,
    font=("Arial", 14, "bold"),
    bd=0,
    cursor="hand2"
)
copy_button.pack(ipadx=20, ipady=10)

footer = tk.Label(
    window,
    text="Made by KAINY 😼",
    font=("Arial", 11),
    bg=BG,
    fg=TEXT_LIGHT
)
footer.pack(side="bottom", pady=20)

window.mainloop()
