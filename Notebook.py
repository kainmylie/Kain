import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime


window = tk.Tk()
window.title("KAINY Notes")
window.geometry("820x620")
window.configure(bg="#eeeeee")
window.resizable(False, False)


title = tk.Label(window, text="KAINY NOTES", font=("Arial", 24, "bold"), bg="#eeeeee", fg="#333333")
title.pack(pady=15)

subtitle = tk.Label(window, text="Блокнот для заметок и списков", font=("Arial", 11), bg="#eeeeee", fg="#666666")
subtitle.pack()

button_frame = tk.Frame(window, bg="#eeeeee")
button_frame.pack(pady=12)

text_box = tk.Text(
    window,
    font=("Arial", 13),
    bg="white",
    fg="#222222",
    width=80,
    height=20,
    wrap="word",
    bd=2,
    relief="sunken"
)
text_box.pack(padx=20, pady=10)

counter_label = tk.Label(window, text="Символы 0 | Слова 0", font=("Arial", 10), bg="#eeeeee", fg="#555555")
counter_label.pack(pady=5)


def update_counter():
    text = text_box.get("1.0", tk.END).strip()
    words = text.split()

    counter_label.config(text="Символы " + str(len(text)) + " | Слова " + str(len(words)))


def text_changed(event):
    update_counter()


def save_note():
    #сохраняю заметку в txt файл
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt")]
    )

    if file_path == "":
        return

    try:
        file = open(file_path, "w", encoding="utf-8")
        file.write(text_box.get("1.0", tk.END).strip())
        file.close()

        messagebox.showinfo("Готово", "Заметка сохранена")
    except:
        messagebox.showerror("Ошибка", "Не получилось сохранить заметку")


def new_note():
    answer = messagebox.askyesno("Новая заметка", "Очистить текущую заметку?")

    if answer:
        text_box.delete("1.0", tk.END)
        update_counter()


def add_check():
    #добавляю кружок для списка дел
    text_box.insert(tk.INSERT, "○ ")
    update_counter()


def make_done():
    #меняю кружок в строке где стоит курсор
    cursor_place = text_box.index(tk.INSERT)
    line_number = cursor_place.split(".")[0]

    start = line_number + ".0"
    end = line_number + ".end"

    line = text_box.get(start, end)

    if line.startswith("○"):
        new_line = "●" + line[1:]
    elif line.startswith("●"):
        new_line = "○" + line[1:]
    else:
        new_line = "○ " + line

    text_box.delete(start, end)
    text_box.insert(start, new_line)

    update_counter()


def add_date():
    today = datetime.now().strftime("%d.%m.%Y")
    text_box.insert(tk.INSERT, "Дата " + today + "\n")
    update_counter()


def add_title():
    text_box.insert(tk.INSERT, "\nНовый раздел\n")
    update_counter()


def clear_text():
    #быстрая очистка без вопроса
    text_box.delete("1.0", tk.END)
    update_counter()


text_box.bind("<KeyRelease>", text_changed)


save_btn = tk.Button(button_frame, text="Сохранить", command=save_note, width=12, bg="#dcdcdc", font=("Arial", 10))
save_btn.grid(row=0, column=0, padx=4, pady=4)

new_btn = tk.Button(button_frame, text="Новая", command=new_note, width=12, bg="#dcdcdc", font=("Arial", 10))
new_btn.grid(row=0, column=1, padx=4, pady=4)

check_btn = tk.Button(button_frame, text="Кружок", command=add_check, width=12, bg="#dcdcdc", font=("Arial", 10))
check_btn.grid(row=0, column=2, padx=4, pady=4)

done_btn = tk.Button(button_frame, text="Готово", command=make_done, width=12, bg="#dcdcdc", font=("Arial", 10))
done_btn.grid(row=0, column=3, padx=4, pady=4)

date_btn = tk.Button(button_frame, text="Дата", command=add_date, width=12, bg="#cfcfcf", font=("Arial", 10))
date_btn.grid(row=1, column=0, padx=4, pady=4)

title_btn = tk.Button(button_frame, text="Раздел", command=add_title, width=12, bg="#cfcfcf", font=("Arial", 10))
title_btn.grid(row=1, column=1, padx=4, pady=4)

clear_btn = tk.Button(button_frame, text="Очистить", command=clear_text, width=12, bg="#cfcfcf", font=("Arial", 10))
clear_btn.grid(row=1, column=2, padx=4, pady=4)


footer = tk.Label(window, text="Пиши и сохраняй мысли", font=("Arial", 10), bg="#eeeeee", fg="#555555")
footer.pack(pady=8)


window.mainloop()
