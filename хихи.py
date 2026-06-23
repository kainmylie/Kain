import tkinter as tk
import random


root = tk.Tk()
root.title("WARNING")
root.geometry("400x250")
root.configure(bg="#0A0A0A")
root.resizable(False, False)

#тут сохраняю все открытые маленькие окна, чтобы потом закрыть их одной кнопкой
windows = []


title = tk.Label(
    root,
    text="DO NOT PRESS",
    font=("Consolas", 24, "bold"),
    fg="#FF3333",
    bg="#0A0A0A"
)
title.pack(pady=30)


def create_window():
    #выбираю случайное место, чтобы окна появлялись в разных частях экрана
    x = random.randint(50, 1200)
    y = random.randint(50, 700)

    popup = tk.Toplevel(root)
    popup.title("WARNING")
    popup.geometry("300x140+" + str(x) + "+" + str(y))
    popup.configure(bg="#111111")

    #делаю окно поверх других, чтобы эффект был заметнее
    popup.attributes("-topmost", True)

    label = tk.Label(
        popup,
        text="ТЫ СЛОНЯРА 🐘",
        font=("Consolas", 18, "bold"),
        fg="#FF3333",
        bg="#111111"
    )
    label.pack(expand=True)

    windows.append(popup)


def summon_windows():
    #окна появляются не сразу, а по очереди с небольшой задержкой
    for i in range(10):
        root.after(
            i * 150,
            create_window
        )


def clear_windows():
    #закрываю все окна из списка даже если часть уже была закрыта вручную
    for window in windows[:]:
        try:
            window.destroy()
        except:
            pass

    windows.clear()

    #после очистки показываю отдельное окно с результатом
    result = tk.Toplevel(root)
    result.title("SUCCESS")
    result.geometry("350x150")
    result.configure(bg="#111111")
    result.attributes("-topmost", True)

    tk.Label(
        result,
        text="СЛОНЯРА ОБЕЗВРЕЖЕН 🐘",
        font=("Consolas", 16, "bold"),
        fg="#00FF66",
        bg="#111111"
    ).pack(expand=True)


#основная кнопка запускает появление окон
activate_button = tk.Button(
    root,
    text="ACTIVATE",
    command=summon_windows,
    font=("Consolas", 16, "bold"),
    bg="#990000",
    fg="white",
    activebackground="#CC0000",
    bd=0,
    padx=25,
    pady=10,
    cursor="hand2"
)
activate_button.pack(pady=10)


#эта кнопка убирает все созданные окна
clear_button = tk.Button(
    root,
    text="CLEAR",
    command=clear_windows,
    font=("Consolas", 16, "bold"),
    bg="#333333",
    fg="white",
    activebackground="#555555",
    bd=0,
    padx=25,
    pady=10,
    cursor="hand2"
)
clear_button.pack(pady=10)


footer = tk.Label(
    root,
    text="Fake Chaos Simulator",
    font=("Consolas", 10),
    fg="#666666",
    bg="#0A0A0A"
)
footer.pack(side="bottom", pady=15)


root.mainloop()