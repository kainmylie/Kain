import tkinter as tk
from tkinter import filedialog, messagebox


BG = "#FFFDF5"
CARD = "#FFFFFF"
PRIMARY = "#FFE89A"
PRIMARY_LIGHT = "#FFF4C9"
TEXT = "#8A6D3B"
TEXT_LIGHT = "#B59A5A"

current_text = ""
analysis_result = ""


def open_file():
    global current_text

    file_path = filedialog.askopenfilename(
        title="Выбери текстовый файл",
        filetypes=[("Текстовые файлы", "*.txt")]
    )

    if file_path == "":
        return

    try:
        file = open(file_path, "r", encoding="utf-8")
        current_text = file.read()
        file.close()
    except:
        messagebox.showerror("Ошибка", "Не получилось открыть файл")
        return

    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, current_text)

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, "Файл открыт. Теперь можно нажать Анализировать")


def make_word_normal(word):
    #убираю лишние знаки
    symbols = ".,!?;:()[]{}\"'«»—-"
    word = word.strip(symbols)
    word = word.lower()
    return word


def count_words(words):
    word_count = {}

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count


def get_top_words(word_count):
    #делаю список чтобы потом отсортировать
    top_words = []

    for word in word_count:
        top_words.append([word, word_count[word]])

    top_words.sort(key=lambda item: item[1], reverse=True)
    return top_words[:5]


def analyze_text():
    global current_text, analysis_result

    #беру текст из поля
    current_text = text_box.get("1.0", tk.END).strip()

    if current_text == "":
        messagebox.showwarning("Пусто", "Сначала открой файл или введи текст")
        return

    lines = current_text.splitlines()
    all_words = current_text.split()
    clean_words = []

    for word in all_words:
        normal_word = make_word_normal(word)

        if normal_word != "":
            clean_words.append(normal_word)

    longest_word = "-"

    for word in clean_words:
        if longest_word == "-" or len(word) > len(longest_word):
            longest_word = word

    word_count = count_words(clean_words)
    top_words = get_top_words(word_count)

    top_words_text = ""

    #собираю топ слов для вывода
    for word, count in top_words:
        top_words_text += word + ": " + str(count) + " раз(а)\n"

    analysis_result = (
        "АНАЛИЗ ФАЙЛА\n\n"
        "Количество строк: " + str(len(lines)) + "\n"
        "Количество слов: " + str(len(clean_words)) + "\n"
        "Количество символов: " + str(len(current_text)) + "\n"
        "Самое длинное слово: " + longest_word + "\n\n"
        "Топ-5 частых слов:\n"
        + top_words_text
    )

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, analysis_result)


def save_result():
    if analysis_result == "":
        messagebox.showwarning("Нет анализа", "Сначала нажми Анализировать")
        return

    file_path = filedialog.asksaveasfilename(
        title="Сохранить результат анализа",
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt")]
    )

    if file_path == "":
        return

    try:
        file = open(file_path, "w", encoding="utf-8")
        file.write(analysis_result)
        file.close()
    except:
        messagebox.showerror("Ошибка", "Не получилось сохранить файл")
        return

    messagebox.showinfo("Готово", "Результат анализа сохранен")


def clear_all():
    global current_text, analysis_result

    #очищаю текст и результат
    current_text = ""
    analysis_result = ""

    text_box.delete("1.0", tk.END)
    result_box.delete("1.0", tk.END)


window = tk.Tk()
window.title("KAINY File Analyzer")
window.geometry("760x650")
window.configure(bg=BG)
window.resizable(False, False)


title = tk.Label(
    window,
    text="KAINY FILE ANALYZER",
    font=("Arial", 22, "bold"),
    bg=BG,
    fg=TEXT
)
title.pack(pady=15)

subtitle = tk.Label(
    window,
    text="Чтение, запись и обработка данных в файлах",
    font=("Arial", 12),
    bg=BG,
    fg=TEXT_LIGHT
)
subtitle.pack()

text_box = tk.Text(
    window,
    font=("Arial", 12),
    bg=CARD,
    fg=TEXT,
    bd=0,
    wrap="word",
    height=13
)
text_box.pack(padx=25, pady=15, fill="x")

result_box = tk.Text(
    window,
    font=("Arial", 12, "bold"),
    bg=PRIMARY_LIGHT,
    fg=TEXT,
    bd=0,
    wrap="word",
    height=9
)
result_box.pack(padx=25, pady=10, fill="x")

button_frame = tk.Frame(window, bg=BG)
button_frame.pack(pady=10)


open_button = tk.Button(
    button_frame,
    text="Открыть файл",
    command=open_file,
    bg=PRIMARY,
    fg=TEXT,
    font=("Arial", 11, "bold"),
    bd=0,
    width=16,
    height=2,
    cursor="hand2"
)
open_button.grid(row=0, column=0, padx=5)

analyze_button = tk.Button(
    button_frame,
    text="Анализировать",
    command=analyze_text,
    bg=PRIMARY_LIGHT,
    fg=TEXT,
    font=("Arial", 11, "bold"),
    bd=0,
    width=16,
    height=2,
    cursor="hand2"
)
analyze_button.grid(row=0, column=1, padx=5)

save_button = tk.Button(
    button_frame,
    text="Сохранить",
    command=save_result,
    bg=PRIMARY_LIGHT,
    fg=TEXT,
    font=("Arial", 11, "bold"),
    bd=0,
    width=16,
    height=2,
    cursor="hand2"
)
save_button.grid(row=0, column=2, padx=5)

clear_button = tk.Button(
    button_frame,
    text="Очистить",
    command=clear_all,
    bg=PRIMARY_LIGHT,
    fg=TEXT,
    font=("Arial", 11, "bold"),
    bd=0,
    width=16,
    height=2,
    cursor="hand2"
)
clear_button.grid(row=0, column=3, padx=5)

footer = tk.Label(
    window,
    text="Made by KAINY",
    font=("Arial", 11),
    bg=BG,
    fg=TEXT_LIGHT
)
footer.pack(pady=10)


window.mainloop()
