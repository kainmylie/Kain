import tkinter as tk
from tkinter import messagebox
import random
import pygame


#музыка должна лежать по этому пути
MUSIC_FILE = r"C:\Users\Admin\OneDrive\Рабочий стол\Камила ДЗ\lofi.mp3"


try:
    pygame.mixer.init()
    pygame.mixer.music.load(MUSIC_FILE)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
except Exception as error:
    print("Ошибка музыки:", error)


BG = "#FFF3FB"
PINK = "#FF8FD8"
HOT_PINK = "#FF4FBE"
CYAN = "#9EF8FF"
PURPLE = "#8B6CFF"
DARK = "#8657EA"
WHITE = "#FFFFFF"


FACTS = [
    "Я занимаюсь тренировками дома уже 3 года без отговорок.",
    "Люблю книги ужасов.",
    "У меня есть маленький черный, милый, вислоухий кот.",
    "Музыка помогает мне сосредоточиться🎧.",
    "Учу английский и иногда китайский.",
    "Иногда люблю готовить.",
    "Хочу стать DevOps инженером.",
    "У меня есть маленький черный, милый, вислоухий кот.",
    "Моя любимая еда - ❤️ДОНЕР❤️",
    "Жертвую сном ради свободного времени.",
    "Я люблю дарить подарки.",
    "Я ненавижу смотреть телевизор.",
    "Я ответственный человек.",
    "Мой рост 1.61 м.",
    "Моя любимая еда - ❤️ДОНЕР❤️",
]


root = tk.Tk()
root.title("KAINY PORTFOLIO 😼")
root.geometry("1000x650")
root.resizable(False, False)
root.configure(bg=BG)

canvas = tk.Canvas(
    root,
    width=1000,
    height=650,
    bg=BG,
    highlightthickness=0
)
canvas.pack(fill="both", expand=True)

#тут храню значки фона и кнопки, чтобы потом ими управлять
flowers = []
buttons = []
no_clicks = 0
no_btn = None


def close_program():
    try:
        pygame.mixer.music.stop()
    except:
        pass

    root.destroy()


def draw_background():
    canvas.create_oval(760, -180, 1150, 220, fill=CYAN, outline="")
    canvas.create_oval(-120, 420, 240, 780, fill="#E7DEFF", outline="")
    canvas.create_oval(650, 430, 920, 700, fill="#FFE2F6", outline="")

    #чтоб значки на фоне появлялись в случайных местах
    for i in range(35):
        x = random.randint(20, 980)
        y = random.randint(20, 630)
        symbol = random.choice(["✿", "❀", "✦", "♡", "🌸", "💗", "✨", "🫧", "🌷"])
        size = random.randint(14, 28)
        color = random.choice([PINK, PURPLE, HOT_PINK, "#FFB6E6", "#B8A7FF"])

        item = canvas.create_text(
            x,
            y,
            text=symbol,
            font=("Arial", size),
            fill=color
        )

        speed = random.randint(1, 2)
        side = random.choice([-1, 0, 1])

        flowers.append([item, speed, side])


def animate_flowers():
    #каждый значок чутка двигается вниз
    for flower in flowers:
        item = flower[0]
        speed = flower[1]
        side = flower[2]

        coords = canvas.coords(item)
        x = coords[0]
        y = coords[1]

        canvas.move(item, side, speed)

        if y > 680:
            new_x = random.randint(20, 980)
            canvas.coords(item, new_x, -20)
            flower[2] = random.choice([-1, 0, 1])

        if x < 0 or x > 1000:
            flower[2] = -side

    root.after(30, animate_flowers)


def clear_ui():
    canvas.delete("ui")

    for button in buttons:
        button.destroy()

    buttons.clear()


def draw_start():
    global no_clicks, no_btn

    clear_ui()
    no_clicks = 0

    canvas.create_text(
        500, 110,
        text="KAINY PORTFOLIO",
        font=("Georgia", 44, "bold"),
        fill=DARK,
        tags="ui"
    )

    canvas.create_text(
        500, 165,
        text="be careful😼",
        font=("Arial", 18, "bold"),
        fill=HOT_PINK,
        tags="ui"
    )

    canvas.create_rectangle(
        250, 220, 750, 430,
        fill=WHITE,
        outline="",
        tags="ui"
    )

    canvas.create_text(
        500, 275,
        text="Вы хотите узнать обо мне?",
        font=("Arial", 25, "bold"),
        fill=DARK,
        tags="ui"
    )

    canvas.create_text(
        500, 320,
        text="CAP Education",
        font=("Arial", 15),
        fill="#6F668A",
        tags="ui"
    )

    yes_btn = tk.Button(
        root,
        text="Да 😎",
        command=draw_menu,
        bg=WHITE,
        fg=HOT_PINK,
        activebackground="#FFE2F6",
        activeforeground=DARK,
        font=("Arial", 12, "bold"),
        bd=0,
        cursor="hand2"
    )
    buttons.append(yes_btn)
    canvas.create_window(405, 375, window=yes_btn, width=140, height=45, tags="ui")

    no_btn = tk.Button(
        root,
        text="Нет 🥲",
        command=nothing,
        bg=WHITE,
        fg=HOT_PINK,
        activebackground="#FFE2F6",
        activeforeground=DARK,
        font=("Arial", 12, "bold"),
        bd=0,
        cursor="hand2"
    )
    buttons.append(no_btn)
    canvas.create_window(595, 375, window=no_btn, width=140, height=45, tags="ui")
    no_btn.bind("<Enter>", no_button_hover)


def nothing():
    pass


def no_button_hover(event):
    run_away()


def run_away():
    global no_clicks

    phrases = [
        "Нет 🥲",
        "Точно нет 😭",
        "Не нажимай 😳",
        "Я боюсь 😱",
        "Ну пожалуйста 🥺",
        "Ладно 😔"
    ]

    #чтоб кнопка нет убегала несколько раз, а потом все равно открывалось меню
    if no_clicks < 5:
        no_btn.config(text=phrases[no_clicks])

        x = random.randint(150, 850)
        y = random.randint(230, 570)

        canvas.create_window(x, y, window=no_btn, width=150, height=45, tags="ui")
        no_clicks += 1
    else:
        messagebox.showinfo(
            "Судьбу не обманешь 😼",
            "Ты все равно узнаешь про Kainy!"
        )
        draw_menu()


def draw_menu():
    clear_ui()

    canvas.create_text(
        500, 50,
        text="Добро пожаловать во вселенную Kainy✨",
        font=("Georgia", 28, "bold"),
        fill=DARK,
        tags="ui"
    )
    
    canvas.create_rectangle(105, 90, 335, 180, fill=WHITE, outline="", tags="ui")
    btn_about = tk.Button(root, text="👤 О себе", command=about, bg=WHITE, fg=HOT_PINK, activebackground="#FFE2F6", activeforeground=DARK, font=("Arial", 12, "bold"), bd=0, cursor="hand2")
    buttons.append(btn_about)
    canvas.create_window(220, 135, window=btn_about, width=215, height=65, tags="ui")

    canvas.create_rectangle(385, 90, 615, 180, fill=WHITE, outline="", tags="ui")
    btn_goal = tk.Button(root, text="🎯 Моя цель", command=goal, bg=WHITE, fg=HOT_PINK, activebackground="#FFE2F6", activeforeground=DARK, font=("Arial", 12, "bold"), bd=0, cursor="hand2")
    buttons.append(btn_goal)
    canvas.create_window(500, 135, window=btn_goal, width=215, height=65, tags="ui")

    canvas.create_rectangle(665, 90, 895, 180, fill=WHITE, outline="", tags="ui")
    btn_cap = tk.Button(root, text="🚪 Как я пришла в CAP Education", command=cap_story, bg=WHITE, fg=HOT_PINK, activebackground="#FFE2F6", activeforeground=DARK, font=("Arial", 12, "bold"), bd=0, cursor="hand2")
    buttons.append(btn_cap)
    canvas.create_window(780, 135, window=btn_cap, width=215, height=65, tags="ui")

    canvas.create_rectangle(105, 210, 335, 300, fill=WHITE, outline="", tags="ui")
    btn_mentor = tk.Button(root, text="🧑‍🏫 Мой ментор", command=mentor, bg=WHITE, fg=HOT_PINK, activebackground="#FFE2F6", activeforeground=DARK, font=("Arial", 12, "bold"), bd=0, cursor="hand2")
    buttons.append(btn_mentor)
    canvas.create_window(220, 255, window=btn_mentor, width=215, height=65, tags="ui")

    canvas.create_rectangle(385, 210, 615, 300, fill=WHITE, outline="", tags="ui")
    btn_progress = tk.Button(root, text="📈 Точка А → Б", command=progress, bg=WHITE, fg=HOT_PINK, activebackground="#FFE2F6", activeforeground=DARK, font=("Arial", 12, "bold"), bd=0, cursor="hand2")
    buttons.append(btn_progress)
    canvas.create_window(500, 255, window=btn_progress, width=215, height=65, tags="ui")

    canvas.create_rectangle(665, 210, 895, 300, fill=WHITE, outline="", tags="ui")
    btn_hobbies = tk.Button(root, text="🎵 Хобби", command=hobbies, bg=WHITE, fg=HOT_PINK, activebackground="#FFE2F6", activeforeground=DARK, font=("Arial", 12, "bold"), bd=0, cursor="hand2")
    buttons.append(btn_hobbies)
    canvas.create_window(780, 255, window=btn_hobbies, width=215, height=65, tags="ui")

    canvas.create_rectangle(105, 330, 335, 420, fill=WHITE, outline="", tags="ui")
    btn_projects = tk.Button(root, text="⭐ Лучшие работы", command=projects, bg=WHITE, fg=HOT_PINK, activebackground="#FFE2F6", activeforeground=DARK, font=("Arial", 12, "bold"), bd=0, cursor="hand2")
    buttons.append(btn_projects)
    canvas.create_window(220, 375, window=btn_projects, width=215, height=65, tags="ui")

    canvas.create_rectangle(385, 330, 615, 420, fill=WHITE, outline="", tags="ui")
    btn_github = tk.Button(root, text="🐙 GitHub", command=github, bg=WHITE, fg=HOT_PINK, activebackground="#FFE2F6", activeforeground=DARK, font=("Arial", 12, "bold"), bd=0, cursor="hand2")
    buttons.append(btn_github)
    canvas.create_window(500, 375, window=btn_github, width=215, height=65, tags="ui")

    canvas.create_rectangle(665, 330, 895, 420, fill=WHITE, outline="", tags="ui")
    btn_principles = tk.Button(root, text="🏆 Принципы", command=principles, bg=WHITE, fg=HOT_PINK, activebackground="#FFE2F6", activeforeground=DARK, font=("Arial", 12, "bold"), bd=0, cursor="hand2")
    buttons.append(btn_principles)
    canvas.create_window(780, 375, window=btn_principles, width=215, height=65, tags="ui")

    canvas.create_rectangle(105, 450, 335, 540, fill=WHITE, outline="", tags="ui")
    btn_fact = tk.Button(root, text="🎲 Случайный факт", command=random_fact, bg=WHITE, fg=HOT_PINK, activebackground="#FFE2F6", activeforeground=DARK, font=("Arial", 12, "bold"), bd=0, cursor="hand2")
    buttons.append(btn_fact)
    canvas.create_window(220, 495, window=btn_fact, width=215, height=65, tags="ui")

    secret_cat = canvas.create_text(
        960,
        610,
        text="😼",
        font=("Arial", 16),
        fill="#FFD6F3",
        tags="ui"
    )

    canvas.tag_bind(secret_cat, "<Button-1>", secret_cat_click)


def secret_cat_click(event):
    easter_egg()


def popup(title, text):
    messagebox.showinfo(title, text)


def about():
    popup(
        "О себе",
        "Меня зовут Камила Нуртазина Данияровна.\n"
        "Можно просто Kainy хехе😼\n\n"
        "Мне 16 лет. Я амбициозная, упрямая и дисциплинированная.\n"
        "Раньше я думала, что IT это слишком сложно и только для вундеркиндов.\n"
        "А теперь я пишу код и строю свой путь в IT."
    )


def goal():
    popup(
        "Моя цель",
        "Моя цель это стать DevOps инженером 💻\n\n"
        "Я хочу понимать серверы, Linux, деплой,\n"
        "автоматизацию и настоящие IT системы.\n\n"
        "Я хочу не просто учиться, а построить сильную карьеру."
    )


def cap_story():
    popup(
        "Как я пришла в CAP Education",
        "О CAP Education мне рассказала мама.\n\n"
        "До CAP Education я уже начала интересоваться IT:\n"
        "Linux, серверами, программированием через телефон,\n"
        "как вообще работает IT мир.\n\n"
        "Когда мама предложила попробовать обучение,\n"
        "мне показалось, что это зов судьбы, и я решила не упускать шанс.\n\n"
        "Сейчас я понимаю, что это было правильное решение:\n"
        "CAP Education помог мне перейти от интереса к реальным мини проектам."
    )


def mentor():
    popup(
        "Мой ментор",
        "Мой ментор - Диана Есендос ✨\n\n"
        "Она золотой преподаватель, очень харизматичная и энергичная.\n"
        "Она вдохновляет меня не только как ментор, поддерживает и помогает двигаться вперед.\n\n"
        "Благодаря ей обучение стало интереснее и живее, это доказало, что преподаватель играет большую роль в обучении.\n\n"
        "Иногда я вижу в ней будущую себя."
    )


def progress():
    popup(
        "Точка А → Точка Б",
        "Точка А:\n"
        "Я до конца школы умела только включать компьютер.\n"
        "Я не любила информатику, потому что для меня она была слишком трудным предметом.\n"
        "У меня никогда не было своего личного ноутбука.\n"
        "Что побудило интерес? Нуу... деньги👉👈 и игра про айти.\n\n"
        "Точка Б:\n"
        "Сейчас я пишу маленькие программы на Python,\n"
        "делаю проекты, изучаю IT глубже\n"
        "и уже вижу себя в DevOps."
    )


def hobbies():
    popup(
        "Хобби",
        "🏋️ Тренируюсь дома\n"
        "💻 Изучаю IT\n"
        "📚 Читаю книги\n"
        "🎵 Слушаю музыку\n"
        "🌍 Учу английский и китайский\n"
        "🍳 Готовлю еду\n"
    )


def projects():
    popup(
        "Лучшие работы",
        "❤️ Калькулятор\n"
        "Программа для быстрых вычислений.\n\n"
        "❤️ Генератор паролей\n"
        "Создает безопасные пароли.\n\n"
        "❤️ Работа с файлами\n"
        "Проект про чтение, запись и обработку данных.\n\n"
        "❤️ KAINY PORTFOLIO\n"
        "Интерактивное портфолио с анимацией и пасхалками.\n\n"
        "❤️ Спамер окнами\n"
        "Спам с маленькими окнами."
    )


def github():
    popup(
        "GitHub",
        "Здесь будет ссылка на GitHub-репозиторий 🐙\n\n"
        "В README будут:\n"
        "- описание проекта\n"
        "- скриншоты\n"
        "- ссылка на сайт / Figma\n"
        "- инструкция запуска"
    )


def principles():
    popup(
        "Мои принципы",
        "1. Никогда не сдаваться.\n"
        "2. Дисциплина важнее настроения.\n"
        "3. Не бояться рисковать и пробовать новое.\n"
        "4. Быть щедрой.\n"
        "5. Уметь ладить с людьми.\n"
        "6. Не лениться."
    )


def random_fact():
    popup("Случайный факт", random.choice(FACTS))


def easter_egg():
    popup(
        "Секретная пасхалка",
        "😼 Ты нашла секретного котика!\n\n"
        "while True:\n"
        "    keep_learning()\n"
        "    become_stronger()\n"
        "    never_give_up()\n\n"
        "Kainy mode activated 🌸"
    )


root.protocol("WM_DELETE_WINDOW", close_program)

draw_background()
draw_start()
animate_flowers()

root.mainloop()